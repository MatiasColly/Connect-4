import time
import math
from boardClass import Board
from boardClass import simulate_piece_drop
from scoreSystem import calculate_score

INF = 9e26

MAX_COLUMN = 7
CURRENT_DEPTH = 6
ENABLE_AB_PRUNE = 1
DYNAMIC_DEPTH = 1
TIME_THR_FOR_DYNAMIC_DEPTH = 0.3

BestColumn = 0
AnalyzedPositions = 0
PrunedPositions = 0
ORDER_FOR_AB_PRUNING = [3, 2, 4, 1, 5, 0, 6]


def minimax(board: Board, depth, alpha, beta, current_player):

    min_score = INF
    max_score = -INF
    global BestColumn, AnalyzedPositions, PrunedPositions

    if depth == 0:
        AnalyzedPositions = AnalyzedPositions + 1
        return calculate_score(board.board)

    else:
        # print("Iter in depth:", depth)
        for column in ORDER_FOR_AB_PRUNING:
            # Checks if current column is not full
            if board.check_availability_in_column(column) == "VALID":

                new_board = simulate_piece_drop(board, column, current_player)
                score = calculate_score(new_board.board)
                AnalyzedPositions = AnalyzedPositions + 1

                if (score > 500 and current_player == 1) or (score < -500 and current_player == 2):
                    if depth == CURRENT_DEPTH:
                        print(column, ":", score)
                        BestColumn = column
                    return score * math.pow(10, depth)

                # If next iteration in minimax is the last one, there is no need to calculate score because it will be
                # the same as the one calculated to check if there is a win
                if depth > 1:
                    score = minimax(new_board, depth - 1, alpha, beta, 3 - current_player)

                if depth == CURRENT_DEPTH:
                    print(column, ":", score)

                if current_player == 1 and score > max_score:
                    if depth == CURRENT_DEPTH:
                        BestColumn = column
                    max_score = score

                if current_player == 2 and score < min_score:
                    if depth == CURRENT_DEPTH:
                        BestColumn = column
                    min_score = score

                if ENABLE_AB_PRUNE:
                    if current_player == 1:
                        alpha = max_num(alpha, score)

                    if current_player == 2:
                        beta = min_num(beta, score)

                    if beta <= alpha:
                        PrunedPositions = PrunedPositions + pow(7, depth - 1) * (6 - column)
                        break

            # else:
            #     print("Full column: ", column)

        if current_player == 1:
            return max_score
        else:
            return min_score


def analyze_best_move(board, current_player):

    global BestColumn, AnalyzedPositions, PrunedPositions, CURRENT_DEPTH, DYNAMIC_DEPTH

    print("Player", current_player, "to play")

    emptySpaces = 42 - board.piece_count()
    if emptySpaces <= CURRENT_DEPTH:
        CURRENT_DEPTH = emptySpaces

    t0 = time.monotonic()
    minimax(board, CURRENT_DEPTH, -INF, INF, current_player)
    t1 = time.monotonic()

    takenTime = t1 - t0
    print("Best column:", BestColumn)
    print(f'Taken time: {takenTime:.4f}')
    print("Analyzed positions:", AnalyzedPositions)
    print("Pruned positions:", PrunedPositions)
    AnalyzedPositions = 0
    PrunedPositions = 0

    # When dynamic depth is enabled, if last computation was fast, an extra depth is added to analysis to get better
    # results
    if DYNAMIC_DEPTH and takenTime < TIME_THR_FOR_DYNAMIC_DEPTH and CURRENT_DEPTH < 22:
        CURRENT_DEPTH = CURRENT_DEPTH + 1
        print("Depth increased:", CURRENT_DEPTH)

    return BestColumn


def max_num(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2


def min_num(num1, num2):
    if num1 < num2:
        return num1
    else:
        return num2
