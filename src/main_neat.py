import sys
import board_ui
from boardClass import Board
import random
import time
# Game Parameters
MAX_ROW = 6
MAX_COLUMN = 7


def test_ai():

    board = Board()
    current_player = 1
    ui = board_ui.BoardUI(current_player, False, board)

    while True:

        inputValue = random.randint(0, 6)
        return_value = board.drop_piece(inputValue, current_player)

        if return_value == "INVALID":
            print("Invalid input, insert again")

        else:
            #board.print_board()
            print(board.return_board_for_nn(current_player))
            ui.add_piece(MAX_ROW - board.column_height(inputValue), inputValue, current_player)

            if return_value == "WIN" or return_value == "DRAW":
                ui.draw_game_end(return_value)
                return return_value, current_player

            else:
                # Switch turn to other player and analyze it's best move
                current_player = 3 - current_player
                ui.draw_menu_text(board)
                time.sleep(0.3)


def main():
    test_ai()
    time.sleep(3)
    sys.exit()


if __name__ == '__main__':
    main()
