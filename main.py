import numpy as np
import pygame
import sys

MAX_ROW = 6
MAX_COLUMN = 7

class Board:
    def __init__(self):
        self.board = np.zeros((MAX_ROW, MAX_COLUMN))
        self.columnHeight = np.zeros(MAX_COLUMN, dtype=np.uint8)
        self.score = 0

    def print_board(self):
        print(self.board)
        print()

    def return_board(self):
        return self.board

    def add_piece(self, row, column, player):
        self.board[row, column] = player

    def column_height(self, column):
        return self.columnHeight[column]

    def drop_piece(self, column, player):
        if column < MAX_COLUMN and self.columnHeight[column] != MAX_ROW:
            self.add_piece(MAX_ROW - 1 - self.columnHeight[column], column, player)
            self.columnHeight[column] += 1
            self.update_score()
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
        score = [0, 0]
        pieceCount = 0
        for player in range(1, 3):
            for row in range(MAX_ROW):
                for column in range(MAX_COLUMN):
                    if self.board[row, column] == player or self.board[row, column] == 0:
                        # Weighted score system:
                        # 4 blank: 1 point
                        # 1 piece: 2 point
                        # 2 pieces: 4 points
                        # 3 pieces: 8 points

                        if column < MAX_COLUMN - 3:
                            # Horizontal win posibility
                            if ((self.board[row, column + 1] == player or self.board[row, column + 1] == 0) and
                                    (self.board[row, column + 2] == player or self.board[row, column + 2] == 0) and
                                    (self.board[row, column + 3] == player or self.board[row, column + 3] == 0)):
                                pieceCount = pieceCount + 1 if self.board[row, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row, column + 1] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row, column + 2] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row, column + 3] == player else pieceCount
                                score[player - 1] += pieces_to_points[pieceCount]
                                pieceCount = 0

                        if row < MAX_ROW - 3:
                            # Vertical win
                            if ((self.board[row + 1, column] == player or self.board[row + 1, column] == 0) and
                                    (self.board[row + 2, column] == player or self.board[row + 2, column] == 0) and
                                    (self.board[row + 3, column] == player or self.board[row + 3, column] == 0)):
                                pieceCount = pieceCount + 1 if self.board[row, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 1, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 2, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 3, column] == player else pieceCount
                                score[player - 1] += pieces_to_points[pieceCount]
                                pieceCount = 0

                        if column < MAX_COLUMN - 3 and row < MAX_ROW - 3:
                            # Right downward win
                            if ((self.board[row + 1, column + 1] == player or self.board[row + 1, column + 1] == 0) and
                                    (self.board[row + 2, column + 2] == player or self.board[row + 2, column + 2] == 0) and
                                    (self.board[row + 3, column + 3] == player or self.board[row + 3, column + 3] == 0)):
                                pieceCount = pieceCount + 1 if self.board[row, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 1, column + 1] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 2, column + 2] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 3, column + 3] == player else pieceCount
                                score[player - 1] += pieces_to_points[pieceCount]
                                pieceCount = 0

                        # Protection to avoid exceeding array limits
                        if row < MAX_ROW - 3 and column >= 3:
                            # Left downward win
                            if ((self.board[row + 1, column - 1] == player or self.board[row + 1, column - 1] == 0) and
                                    (self.board[row + 2, column - 2] == player or self.board[row + 2, column - 2] == 0) and
                                    (self.board[row + 3, column - 3] == player or self.board[row + 3, column - 3] == 0)):
                                pieceCount = pieceCount + 1 if self.board[row, column] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 1, column - 1] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 2, column - 2] == player else pieceCount
                                pieceCount = pieceCount + 1 if self.board[row + 3, column - 3] == player else pieceCount
                                score[player - 1] += pieces_to_points[pieceCount]
                                pieceCount = 0

        print("Score 1:", score[0], "- Score 2:", score[1])
        print("Final Score:", score[0] - score[1])
        return score[0] - score[1]

pieces_to_points = {
    0 : 1,
    1 : 2,
    2 : 4,
    3 : 8,
    4 : 999
}

BLUE_COLOUR = (0, 0, 255)
BLACK_COLOUR = (0, 0, 0)
RED_COLOUR = (255, 0, 0)
YELLOW_COLOUR = (255, 255, 0)


def draw_board():
    pygame.draw.rect(screen, BLUE_COLOUR, (0, 0, GRAPH_WIDTH, GRAPH_HEIGHT))
    for row in range(MAX_ROW):
        for column in range(MAX_COLUMN):
            pygame.draw.circle(screen, BLACK_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2/5)
    pygame.display.update()


def add_piece(row, column, player):
    if player == 1:
        pygame.draw.circle(screen, RED_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
    else:
        pygame.draw.circle(screen, YELLOW_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
    pygame.display.update()


# Pygame parameters and board init
pygame.init()
SQUARE_SIZE = 100
GRAPH_WIDTH = MAX_COLUMN * SQUARE_SIZE
GRAPH_HEIGHT = MAX_ROW * SQUARE_SIZE
GRAPH_SIZE = (GRAPH_WIDTH, GRAPH_HEIGHT)
screen = pygame.display.set_mode(GRAPH_SIZE)
draw_board()

# Board object
board = Board()

returnValue = "NO WIN"
currentPlayer = 1
inputValue = 0

while returnValue != "WIN" and returnValue != "DRAW":
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            inputValue = int(event.pos[0] / 100)
            returnValue = board.drop_piece(inputValue, currentPlayer)
            if returnValue == "INVALID":
                print("Invalid input, insert again")
            else:
                board.print_board()
                add_piece(MAX_ROW - board.column_height(inputValue), inputValue, currentPlayer)
                if returnValue == "WIN":
                    print("Player", currentPlayer, "WON!")
                if returnValue == "DRAW":
                    print("Game is a DRAW")
                currentPlayer = 3 - currentPlayer

while 1:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            sys.exit()
