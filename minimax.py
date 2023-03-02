import time
import math
from boardClass import Board
from boardClass import simulate_piece_drop
from scoreSystem import calculate_score

MAX_COLUMN = 7
CURRENT_DEPTH = 6
ENABLE_AB_PRUNE = 1

BestColumn = 0
AnalyzedPositions = 0
PrunedPositions = 0

def minimax(board: Board, depth, alpha, beta, currentPlayer):

    min_score = 9999999999999
    max_score = -9999999999999
    global BestColumn, AnalyzedPositions, PrunedPositions

    if depth == 0:
        AnalyzedPositions = AnalyzedPositions + 1
        return calculate_score(board.board)

    else:
        # print("Iter in depth:", depth)
        for column in range(0, MAX_COLUMN):
            # Checks if current column is not full
            if board.check_availability_in_column(column) == "VALID":

                new_board = simulate_piece_drop(board, column, currentPlayer)
                score = calculate_score(new_board.board)
                AnalyzedPositions = AnalyzedPositions + 1

                if (score > 500 and currentPlayer == 1) or (score < -500 and currentPlayer == 2):
                    if depth == CURRENT_DEPTH:
                        print(column, ":", score)
                        BestColumn = column
                    return score * math.pow(10, depth)

                # If next iteration in minimax is the last one, there is no need to calculate score because it will be
                # the same as the one calculated to check if there is a win
                if depth > 1:
                    score = minimax(new_board, depth - 1, alpha, beta, 3 - currentPlayer)

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

                if ENABLE_AB_PRUNE:
                    if currentPlayer == 1:
                        alpha = maxNum(alpha, score)

                    if currentPlayer == 2:
                        beta = minNum(beta, score)

                    if beta <= alpha:
                        PrunedPositions = PrunedPositions + pow(7, depth - 1) * (6 - column)
                        break

            # else:
            #     print("Full column: ", column)

        if currentPlayer == 1:
            return max_score
        else:
            return min_score


def analyze_best_move(board, currentPlayer):

    global BestColumn, AnalyzedPositions, PrunedPositions, CURRENT_DEPTH

    print("Player", currentPlayer, "to play")
    t0 = time.monotonic()
    minimax(board, CURRENT_DEPTH, -9999999999999, 9999999999999, currentPlayer)
    t1 = time.monotonic()

    print("Best column:", BestColumn)
    print(f'Time took: {t1-t0:.4f}')
    print("Analyzed positions:", AnalyzedPositions)
    print("Pruned positions:", PrunedPositions)
    AnalyzedPositions = 0
    PrunedPositions = 0
    return BestColumn


def maxNum(num1, num2):
    if num1 > num2:
        return num1
    else:
        return num2

def minNum(num1, num2):
    if num1 < num2:
        return num1
    else:
        return num2