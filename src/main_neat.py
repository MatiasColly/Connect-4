import sys
import board_ui
from boardClass import Board
import random
import time
import os
import neat
import pickle

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
            ui.add_piece(MAX_ROW - board.column_height(inputValue), inputValue, current_player)

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
    Run each genome against eachother one time to determine the fitness.
    """
    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
    for i, (genome_id1, genome1) in enumerate(genomes):

        print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0 if genome1.fitness is None else genome1.fitness

        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness is None else genome2.fitness
            result, player = train_ai(genome1, genome2, config)
            if result == "WIN":
                if player == 1:
                    genome1.fitness += 1
                else:
                    genome2.fitness += 1


def run_neat(config):
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-85')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 50)
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
