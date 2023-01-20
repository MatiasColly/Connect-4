import time
from boardClass import Board
from boardClass import simulate_piece_drop
from scoreSystem import calculate_score

MAX_COLUMN = 7
CURRENT_DEPTH = 4
BestColumn = 0


def minimax(board: Board, depth, currentPlayer):

    min_score = 9999
    max_score = -9999
    global BestColumn

    if depth == 0:
        return calculate_score(board.board)

    else:
        # print("Iter in depth:", depth)
        for column in range(0, MAX_COLUMN):
            # Checks if current column is not full
            if board.check_availability_in_column(column) == "VALID":
                new_board = simulate_piece_drop(board, column, currentPlayer)
                score = minimax(new_board, depth - 1, 3 - currentPlayer)
                if depth == CURRENT_DEPTH:
                    print(column, ":", score)
                if currentPlayer == 1 and score > max_score:
                    if depth == CURRENT_DEPTH:
                        BestColumn = column
                    max_score = score
                if currentPlayer == 2 and score < min_score:
                    if depth == CURRENT_DEPTH:
                        BestColumn = column
                    min_score = score

            # else:
            #     print("Full column: ", column)

        if depth == CURRENT_DEPTH:
            print("Best column:", BestColumn)

        if currentPlayer == 1:
            return max_score
        else:
            return min_score


def analyze_best_move(board, currentPlayer):
    t0 = time.monotonic()
    global BestColumn
    minimax(board, CURRENT_DEPTH, currentPlayer)
    t1 = time.monotonic()
    print(f'Time took: {t1-t0:.4f}')
    return BestColumn

