# Converts number of aligned pieces to score points

MAX_ROW = 6
MAX_COLUMN = 7

pieces_to_points = {
    0 : 1,
    1 : 2,
    2 : 4,
    3 : 8,
    4 : 999
}


def calculate_score(board):
    score = [0, 0]
    pieceCount = 0
    for player in range(1, 3):
        for row in range(MAX_ROW):
            for column in range(MAX_COLUMN):
                if board[row, column] == player or board[row, column] == 0:
                    # Weighted score system:
                    # 4 blank: 1 point
                    # 1 piece: 2 point
                    # 2 pieces: 4 points
                    # 3 pieces: 8 points

                    if column < MAX_COLUMN - 3:
                        # Horizontal win possibility
                        if ((board[row, column + 1] == player or board[row, column + 1] == 0) and
                                (board[row, column + 2] == player or board[row, column + 2] == 0) and
                                (board[row, column + 3] == player or board[row, column + 3] == 0)):
                            pieceCount = pieceCount + 1 if board[row, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row, column + 1] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row, column + 2] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row, column + 3] == player else pieceCount
                            score[player - 1] += pieces_to_points[pieceCount]
                            pieceCount = 0

                    if row < MAX_ROW - 3:
                        # Vertical win
                        if ((board[row + 1, column] == player or board[row + 1, column] == 0) and
                                (board[row + 2, column] == player or board[row + 2, column] == 0) and
                                (board[row + 3, column] == player or board[row + 3, column] == 0)):
                            pieceCount = pieceCount + 1 if board[row, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 1, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 2, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 3, column] == player else pieceCount
                            score[player - 1] += pieces_to_points[pieceCount]
                            pieceCount = 0

                    if column < MAX_COLUMN - 3 and row < MAX_ROW - 3:
                        # Right downward win
                        if ((board[row + 1, column + 1] == player or board[row + 1, column + 1] == 0) and
                                (board[row + 2, column + 2] == player or board[row + 2, column + 2] == 0) and
                                (board[row + 3, column + 3] == player or board[row + 3, column + 3] == 0)):
                            pieceCount = pieceCount + 1 if board[row, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 1, column + 1] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 2, column + 2] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 3, column + 3] == player else pieceCount
                            score[player - 1] += pieces_to_points[pieceCount]
                            pieceCount = 0

                    # Protection to avoid exceeding array limits
                    if row < MAX_ROW - 3 and column >= 3:
                        # Left downward win
                        if ((board[row + 1, column - 1] == player or board[row + 1, column - 1] == 0) and
                                (board[row + 2, column - 2] == player or board[row + 2, column - 2] == 0) and
                                (board[row + 3, column - 3] == player or board[row + 3, column - 3] == 0)):
                            pieceCount = pieceCount + 1 if board[row, column] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 1, column - 1] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 2, column - 2] == player else pieceCount
                            pieceCount = pieceCount + 1 if board[row + 3, column - 3] == player else pieceCount
                            score[player - 1] += pieces_to_points[pieceCount]
                            pieceCount = 0

    # print("Score 1:", score[0], "- Score 2:", score[1])
    # print("Final Score:", score[0] - score[1])
    return score[0] - score[1]