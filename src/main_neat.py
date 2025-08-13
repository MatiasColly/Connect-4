import sys
import board_ui
from boardClass import Board
import random
import time
import os
import neat
import pickle
import numpy as np

# Game Parameters
MAX_ROW = 6
MAX_COLUMN = 7


def train_ai(genome1, genome2, config):

    board = Board()
    current_player = 1
    ui = board_ui.BoardUI(current_player, False, board)

    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)
    randomize_decision = False

    while True:
        net = net1 if current_player == 1 else net2
        board_nn_format = board.return_board_for_nn(current_player).flatten()
        output = net.activate(board_nn_format)
        decision = output.index(max(output))

        if not randomize_decision:
            inputValue = decision
        else:
            inputValue = random.randint(0, 6)
            randomize_decision = False

        return_value = board.drop_piece(inputValue, current_player)

        if return_value == "INVALID":
            #print("Invalid input, insert again")
            randomize_decision = True
        else:
            #board.print_board()
            #print(board.return_board_for_nn(current_player))
            ui.add_piece(int(MAX_ROW - board.column_height(inputValue)), inputValue, current_player)

            if return_value == "WIN" or return_value == "DRAW":
                #board.print_board()
                ui.draw_game_end(return_value)
                return return_value, current_player

            else:
                # Switch turn to other player and analyze it's best move
                current_player = 3 - current_player
                ui.draw_menu_text(board)
                #time.sleep(0.001)


def eval_genomes(genomes, config):
    """
    Round-robin: each genome plays several matches against every other genome.
    Each pair plays 'n_games_per_pair' games and swaps starting player to remove bias.
    Prints per-generation statistics:
      - Average final pieces per match
      - Total invalid-losses (and breakdown by player)
    """
    # convert to list for stable indexing
    genome_list = list(genomes)
    n = len(genome_list)

    # reset fitness every generation (avoid accumulation across generations)
    for gid, g in genome_list:
        g.fitness = 0.0

    # Stats accumulators
    total_games = 0
    sum_final_pieces = 0
    invalid_losses_total = 0
    invalid_losses_p1 = 0
    invalid_losses_p2 = 0

    n_games_per_pair = 1

    for i in range(n):
        gid1, genome1 = genome_list[i]
        for j in range(i + 1, n):
            gid2, genome2 = genome_list[j]

            # play several games to reduce noise
            for game_idx in range(n_games_per_pair):
                # alternate who starts
                starting_player = 1 if (game_idx % 2 == 0) else 2

                # if starting_player == 2, swap genomes when calling train_ai so the second genome goes first
                if starting_player == 1:
                    result, winning_player, invalid_by, final_pieces = train_ai_with_record(genome1, genome2, config)
                    # winning_player: 1 or 2 relative to the order passed to train_ai_with_record
                else:
                    result, winning_player, invalid_by, final_pieces = train_ai_with_record(genome2, genome1, config)
                    # invert the winner to map relative -> absolute player
                    if winning_player is not None:
                        winning_player = 3 - winning_player

                # Update stats
                total_games += 1
                sum_final_pieces += final_pieces
                if invalid_by == 1:
                    invalid_losses_total += 1
                    invalid_losses_p1 += 1
                elif invalid_by == 2:
                    invalid_losses_total += 1
                    invalid_losses_p2 += 1

                # scoring
                if result == "WIN":
                    if winning_player == 1:
                        genome1.fitness += 1.0
                    elif winning_player == 2:
                        genome2.fitness += 1.0
                elif result == "DRAW":
                    genome1.fitness += 0.5
                    genome2.fitness += 0.5

                # penalty for invalid move (if detected)
                if invalid_by == 1:
                    genome1.fitness -= 0.5
                elif invalid_by == 2:
                    genome2.fitness -= 0.5

    # Print per-generation stats
    avg_pieces = (sum_final_pieces / total_games) if total_games > 0 else 0.0
    print(f"Gen match stats: games={total_games}, avg_final_pieces={avg_pieces:.2f}, "
          f"invalid_losses_total={invalid_losses_total} (P1={invalid_losses_p1}, P2={invalid_losses_p2})")


def train_ai_with_record(genome1, genome2, config, draw_ui=False):
    """
    Plays a game between two genomes and returns:
    - result_str: "WIN", "LOSE", or "DRAW" relative to genome1
    - winning_player: 1, 2, or None (relative to genome1/genome2 order)
    - invalid_by: 1 or 2 if a player lost by invalid placement, else None
    - final_pieces: total number of pieces on the board when the game ended
    """
    board = Board()
    current_player = 1
    ui = None
    if draw_ui:
        ui = board_ui.BoardUI(current_player, False, board)

    net1 = neat.nn.FeedForwardNetwork.create(genome1, config)
    net2 = neat.nn.FeedForwardNetwork.create(genome2, config)

    invalid_by = None
    game_over = False
    winner = None

    while not game_over:
        player_net = net1 if current_player == 1 else net2
        board_matrix = board.return_board_for_nn(current_player)
        output = player_net.activate(board_matrix.flatten())
        move = int(np.argmax(output))

        # Check move validity using check_availability_in_column
        if board.check_availability_in_column(move) == "INVALID":
            invalid_by = current_player
            winner = 2 if current_player == 1 else 1
            game_over = True
            break

        # Drop piece (update board)
        result = board.drop_piece(move, current_player)
        if draw_ui and ui is not None:
            ui.add_piece(int(MAX_ROW - board.column_height(move)), move, current_player)
            ui.draw_menu_text(board)

        if result == "WIN":
            winner = current_player
            game_over = True
        elif result == "DRAW":
            winner = None
            game_over = True
        else:
            current_player = 1 if current_player == 2 else 2

    # Decide result string relative to genome1
    if winner == 1:
        result_str = "WIN"
        winning_player = 1
    elif winner == 2:
        result_str = "LOSE"
        winning_player = 2
    else:
        result_str = "DRAW"
        winning_player = None

    # Total pieces on the board at the end
    final_pieces = board.piece_count()

    return result_str, winning_player, invalid_by, final_pieces


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-35a')
    # p.config.fitness_threshold = 200000
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 5000)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)


def main():

    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    run_neat(config)
    #test_best_network(config)

    print(f"ENDED!!")
    time.sleep(3)
    sys.exit()


if __name__ == '__main__':
    main()