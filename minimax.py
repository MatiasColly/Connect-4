from boardClass import Board
from boardClass import simulate_piece_drop
from scoreSystem import calculate_score

MAX_COLUMN = 7


def minimax(board: Board, depth, currentPlayer):

    min_score = 9999
    max_score = -9999

    if depth == 0:
        return calculate_score(board.board)

    else:
        # print("Iter in depth:", depth)
        for column in range(0, MAX_COLUMN):
            # Checks if current column is not full
            if board.check_availability_in_column(column) == "VALID":
                new_board = simulate_piece_drop(board, column, currentPlayer)
                score = minimax(new_board, depth - 1, 3 - currentPlayer)
                if depth == 4:
                    print(score)
                if currentPlayer == 1 and score > max_score:
                    best_column = column
                    max_score = score
                if currentPlayer == 2 and score < min_score:
                    best_column = column
                    min_score = score

            # else:
            #     print("Full column: ", column)

        if depth == 4:
            print("Best column:", best_column)

        if currentPlayer == 1:
            return max_score
        else:
            return min_score
