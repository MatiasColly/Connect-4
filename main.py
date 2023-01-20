import numpy as np
import pygame
import sys
from boardClass import Board
from minimax import analyze_best_move

# Game Parameter
currentPlayer = 1

# AI Parameters
AUTO_PLAY_AI = False
AI_PLAY_FIRST = False

# Pygame parameters
MAX_ROW = 6
MAX_COLUMN = 7

BLUE_COLOUR = (0, 0, 255)
BLACK_COLOUR = (0, 0, 0)
RED_COLOUR = (255, 0, 0)
YELLOW_COLOUR = (255, 255, 0)
WHITE_COLOUR = (255, 255, 255)

SQUARE_SIZE = 100
GRAPH_WIDTH = MAX_COLUMN * SQUARE_SIZE
GRAPH_HEIGHT = MAX_ROW * SQUARE_SIZE
MENU_WIDTH = 200
GRAPH_SIZE = (GRAPH_WIDTH + MENU_WIDTH, GRAPH_HEIGHT)
CURRENT_TURN_DIS_POS = (GRAPH_WIDTH + 100, 90)
def main():
    # Pygame and board class init
    pygame.init()

    screen = pygame.display.set_mode(GRAPH_SIZE)
    draw_board(screen)
    draw_menu_text(screen)
    # Board object
    board = Board()

    returnValue = "NO WIN"
    global currentPlayer
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
                    draw_menu_text(screen)
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

def draw_menu_text(screen):

    # Cleans previous menu
    pygame.draw.rect(screen, BLACK_COLOUR, (GRAPH_WIDTH, 0, MENU_WIDTH, GRAPH_HEIGHT))

    # Current turn box
    textfont = pygame.font.SysFont("monospace", 20)
    textTBD = textfont.render("Current Turn:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 30))
    if currentPlayer == 1:
        pygame.draw.circle(screen, RED_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
    else:
        pygame.draw.circle(screen, YELLOW_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)

    # AI autoplay box
    textTBD = textfont.render(" AI autoplay:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 130))
    if AUTO_PLAY_AI:
        textTBD = textfont.render("ON", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 85, 160))
    else:
        textTBD = textfont.render("OFF", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 80, 160))

    # Hotkeys box
    textTBD = textfont.render("Hotkeys:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 450))
    textTBD = textfont.render("a: AI ON/OFF", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 480))
    textTBD = textfont.render("s: play best", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 510))
    textTBD = textfont.render("   move", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 530))

    pygame.display.update()

def add_piece(row, column, player, screen):
    if player == 1:
        pygame.draw.circle(screen, RED_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
        pygame.draw.circle(screen, YELLOW_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
    else:
        pygame.draw.circle(screen, YELLOW_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                        (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2 / 5)
        pygame.draw.circle(screen, RED_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
    pygame.display.update()


if __name__ == '__main__':
    main()
