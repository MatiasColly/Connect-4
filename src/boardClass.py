import numpy as np
from scoreSystem import calculate_score
import copy

MAX_ROW = 6
MAX_COLUMN = 7


class Board:
    def __init__(self):
        self.board = np.zeros((MAX_ROW, MAX_COLUMN), dtype=np.uint8)
        self.columnHeight = np.zeros(MAX_COLUMN, dtype=np.uint8)
        self.score = 0

    def print_board(self):
        print(self.board)
        print()

    def return_board(self):
        return self.board

    def return_board_for_nn(self, player):
        board = np.zeros((MAX_ROW, MAX_COLUMN), dtype=np.float)
        for row in range(MAX_ROW):
            for column in range(MAX_COLUMN):
                if self.board[row, column] == player:
                    board[row, column] = 1
                elif self.board[row, column] == 0:
                    board[row, column] = 0.5
                else:
                    board[row, column] = 0
        return board

    def add_piece(self, row, column, player):
        self.board[row, column] = player

    def column_height(self, column):
        return self.columnHeight[column]

    def piece_count(self):
        count = np.count_nonzero(self.board == 1)
        count = count + np.count_nonzero(self.board == 2)
        return count

    def check_availability_in_column(self, column):
        if column < MAX_COLUMN and self.columnHeight[column] != MAX_ROW:
            return "VALID"
        else:
            return "INVALID"

    def drop_piece(self, column, player):
        if column < MAX_COLUMN and self.columnHeight[column] != MAX_ROW:
            self.add_piece(MAX_ROW - 1 - self.columnHeight[column], column, player)
            self.columnHeight[column] += 1
            # self.update_score()
            return self.check_win(player)
        else:
            return "INVALID"

    def check_win(self, player):
        for row in range(MAX_ROW):
            for column in range(MAX_COLUMN):
                if self.board[row, column] == player:

                    # Protection to avoid exceeding array limits
                    if column < MAX_COLUMN - 3:
                        # Horizontal win
                        if (self.board[row, column + 1] == player and self.board[row, column + 2] == player and
                                self.board[row, column + 3] == player):
                            return "WIN"

                    # Protection to avoid exceeding array limits
                    if row < MAX_ROW - 3:
                        # Vertical win
                        if (self.board[row + 1, column] == player and self.board[row + 2, column] == player and
                                self.board[row + 3, column] == player):
                            return "WIN"

                    # Protection to avoid exceeding array limits
                    if column < MAX_COLUMN - 3 and row < MAX_ROW - 3:
                        # Right downward win
                        if (self.board[row + 1, column + 1] == player and self.board[row + 2, column + 2] == player and
                                self.board[row + 3, column + 3] == player):
                            return "WIN"

                    # Protection to avoid exceeding array limits
                    if row < MAX_ROW - 3 and column >= 3:
                        # Left downward win
                        if (self.board[row + 1, column - 1] == player and self.board[row + 2, column - 2] == player and
                                self.board[row + 3, column - 3] == player):
                            return "WIN"

        if self.check_full_board() == "FULL":
            return "DRAW"
        else:
            return "NO WIN"

    def check_full_board(self):
        for height in self.columnHeight:
            if height < 6:
                return "NOT FULL"
        return "FULL"

    # Score for any player is the sum of all possible 'connect 4 wins' available for this player in the current
    # board. Final board score is the difference between those values (a negative score mean, it favours player 2)
    def update_score(self):
        # Same behaviour as detect win, but 0 are counted towards the current player's count. Any possible win is added
        # to player score
        self.score = calculate_score(self.board)


def simulate_piece_drop(board: Board, column, player):
    new_board = copy.deepcopy(board)
    if new_board.check_availability_in_column(column):
        new_board.drop_piece(column, player)
    return new_board
