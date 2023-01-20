import numpy as np
import pygame
import sys
from boardClass import Board
from minimax import analyze_best_move

# AI Parameters
AUTO_PLAY_AI = True
AI_PLAY_FIRST = False

# Pygame parameters
MAX_ROW = 6
MAX_COLUMN = 7

BLUE_COLOUR = (0, 0, 255)
BLACK_COLOUR = (0, 0, 0)
RED_COLOUR = (255, 0, 0)
YELLOW_COLOUR = (255, 255, 0)

SQUARE_SIZE = 100
GRAPH_WIDTH = MAX_COLUMN * SQUARE_SIZE
GRAPH_HEIGHT = MAX_ROW * SQUARE_SIZE
GRAPH_SIZE = (GRAPH_WIDTH, GRAPH_HEIGHT)

def main():
    # Pygame and board class init
    pygame.init()

    screen = pygame.display.set_mode(GRAPH_SIZE)
    draw_board(screen)

    # Board object
    board = Board()

    returnValue = "NO WIN"
    currentPlayer = 1
    inputValue = 0
    global AUTO_PLAY_AI

    if AI_PLAY_FIRST:
        ai_to_play = True
        best_move = analyze_best_move(board, currentPlayer)
    else:
        ai_to_play = False

    while returnValue != "WIN" and returnValue != "DRAW":
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN or ai_to_play:
                if ai_to_play:
                    inputValue = best_move
                else:
                    inputValue = int(event.pos[0] / 100)

                returnValue = board.drop_piece(inputValue, currentPlayer)

                if returnValue == "INVALID":
                    print("Invalid input, insert again")
                else:
                    board.print_board()
                    add_piece(MAX_ROW - board.column_height(inputValue), inputValue, currentPlayer, screen)
                    if returnValue == "WIN":
                        print("Player", currentPlayer, "WON!")
                    if returnValue == "DRAW":
                        print("Game is a DRAW")
                    currentPlayer = 3 - currentPlayer
                    best_move = analyze_best_move(board, currentPlayer)
                    if AUTO_PLAY_AI:
                        ai_to_play = not ai_to_play
                    else:
                        ai_to_play = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    AUTO_PLAY_AI = not AUTO_PLAY_AI
                    print("Auto play AI:", AUTO_PLAY_AI)
                if event.key == pygame.K_s:
                    print("Playing best move")
                    ai_to_play = True



    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                sys.exit()


def draw_board(screen):
    pygame.draw.rect(screen, BLUE_COLOUR, (0, 0, GRAPH_WIDTH, GRAPH_HEIGHT))
    for row in range(MAX_ROW):
        for column in range(MAX_COLUMN):
            pygame.draw.circle(screen, BLACK_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2/5)
    pygame.display.update()


def add_piece(row, column, player, screen):
    if player == 1:
        pygame.draw.circle(screen, RED_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
    else:
        pygame.draw.circle(screen, YELLOW_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
    pygame.display.update()


if __name__ == '__main__':
    main()
