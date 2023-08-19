import pygame
import sys
import board_ui
from boardClass import Board
from minimax import analyze_best_move

# Game Parameters
current_player = 1
MAX_ROW = 6
MAX_COLUMN = 7

# AI Parameters
AUTO_PLAY_AI = False
AI_PLAY_FIRST = False


def main():

    global current_player
    global AUTO_PLAY_AI

    # Board object. All game mechanics are coded in Board class
    board = Board()
    ui = board_ui.BoardUI(current_player, AUTO_PLAY_AI, board)

    return_value = "NO WIN"
    ai_to_play = AI_PLAY_FIRST
    best_move = analyze_best_move(board, current_player)

    # Main pygame loop
    while return_value != "WIN" and return_value != "DRAW":
        for event in pygame.event.get():

            # Top right corner 'X' for game quitting
            if event.type == pygame.QUIT:
                sys.exit()

            # Mouse button press defines where the piece is being played
            if event.type == pygame.MOUSEBUTTONDOWN or ai_to_play:
                if ai_to_play:
                    inputValue = best_move
                else:
                    inputValue = int(event.pos[0] / 100)

                # Update object with the new piece placement
                return_value = board.drop_piece(inputValue, current_player)

                # Return "INVALID" if column is full or mouse button press is out of game's boundaries
                if return_value == "INVALID":
                    print("Invalid input, insert again")

                else:
                    # Log debuging print
                    board.print_board()

                    # Pygame's piece add to game screen
                    ui.add_piece(MAX_ROW - board.column_height(inputValue), inputValue, current_player)

                    if return_value == "WIN" or return_value == "DRAW":
                        ui.draw_game_end(return_value)

                    else:
                        # Switch turn to other player and analyze it's best move
                        current_player = 3 - current_player
                        ui.current_player = current_player
                        best_move = analyze_best_move(board, current_player)

                        # Toggle AI's flag to play next turn if autoplay is enabled
                        if AUTO_PLAY_AI:
                            ai_to_play = not ai_to_play
                        else:
                            ai_to_play = False

                        ui.draw_menu_text(board)

            # Hotkeys menu
            if event.type == pygame.KEYDOWN:

                # a: toggles AI's autoplay
                if event.key == pygame.K_a:
                    AUTO_PLAY_AI = not AUTO_PLAY_AI
                    ui.draw_menu_text(board)
                    print("Auto play AI:", AUTO_PLAY_AI)

                # s: play's best move according to AI
                if event.key == pygame.K_s:
                    print("Playing best move")
                    ai_to_play = True

    # After game is finished, mouse button press is needed to avoid pygame quitting without letting the player see
    # the final board
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                sys.exit()


if __name__ == '__main__':
    main()
