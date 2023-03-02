import numpy as np
import pygame
import sys
from boardClass import Board
from minimax import analyze_best_move

# Game Parameters
currentPlayer = 1
MAX_ROW = 6
MAX_COLUMN = 7

# AI Parameters
AUTO_PLAY_AI = False
AI_PLAY_FIRST = False

# RGB Colours
BLUE_COLOUR = (0, 0, 255)
BLACK_COLOUR = (0, 0, 0)
RED_COLOUR = (255, 0, 0)
YELLOW_COLOUR = (255, 255, 0)
WHITE_COLOUR = (255, 255, 255)

# Pygame board parameters
SQUARE_SIZE = 100
GRAPH_WIDTH = MAX_COLUMN * SQUARE_SIZE
GRAPH_HEIGHT = MAX_ROW * SQUARE_SIZE
MENU_WIDTH = 200
GRAPH_SIZE = (GRAPH_WIDTH + MENU_WIDTH, GRAPH_HEIGHT)
CURRENT_TURN_DIS_POS = (GRAPH_WIDTH + 100, 90)


def main():

    # Board object. All game mechanics are coded in Board class
    board = Board()

    # Pygame and board class init
    pygame.init()

    screen = pygame.display.set_mode(GRAPH_SIZE)
    draw_board(screen)
    draw_menu_text(screen, board)

    returnValue = "NO WIN"
    global currentPlayer
    global AUTO_PLAY_AI
    ai_to_play = AI_PLAY_FIRST
    best_move = analyze_best_move(board, currentPlayer)

    # Main pygame loop
    while returnValue != "WIN" and returnValue != "DRAW":
        for event in pygame.event.get():

            # Top right corner 'X' for game quitting
            if event.type == pygame.QUIT:
                sys.exit()

            # Mouse button press defines where the piece is being played
            if event.type == pygame.MOUSEBUTTONDOWN or ai_to_play:
                if ai_to_play:
                    inputValue = best_move
                else:
                    inputValue = int(event.pos[0] / 100)

                # Update object with the new piece placement
                returnValue = board.drop_piece(inputValue, currentPlayer)

                # Return "INVALID" if column is full or mouse button press is out of game's boundaries
                if returnValue == "INVALID":
                    print("Invalid input, insert again")

                else:
                    # Log debbuging print
                    board.print_board()

                    # Pygame's piece add to game screen
                    add_piece(MAX_ROW - board.column_height(inputValue), inputValue, currentPlayer, screen)

                    if returnValue == "WIN" or returnValue == "DRAW":
                        draw_game_end(screen, returnValue)

                    else:
                        # Switch turn to other player and analyze it's best move
                        currentPlayer = 3 - currentPlayer
                        best_move = analyze_best_move(board, currentPlayer)

                        # Toggle AI's flag to play next turn if autoplay is enabled
                        if AUTO_PLAY_AI:
                            ai_to_play = not ai_to_play
                        else:
                            ai_to_play = False

                        draw_menu_text(screen, board)



            # Hotkeys menu
            if event.type == pygame.KEYDOWN:

                # a: toggles AI's autoplay
                if event.key == pygame.K_a:
                    AUTO_PLAY_AI = not AUTO_PLAY_AI
                    draw_menu_text(screen, board)
                    print("Auto play AI:", AUTO_PLAY_AI)

                # s: play's best move according to AI
                if event.key == pygame.K_s:
                    print("Playing best move")
                    ai_to_play = True

    # After game is finished, mouse button press is needed to avoid pygame quitting without letting the player see
    # the final board
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.QUIT:
                sys.exit()


# Draw Connect 4 grid
def draw_board(screen):
    pygame.draw.rect(screen, BLUE_COLOUR, (0, 0, GRAPH_WIDTH, GRAPH_HEIGHT))
    for row in range(MAX_ROW):
        for column in range(MAX_COLUMN):
            pygame.draw.circle(screen, BLACK_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                (row * SQUARE_SIZE) + SQUARE_SIZE / 2), radius=SQUARE_SIZE * 2/5)
    pygame.display.update()


# Draw right side menu
def draw_menu_text(screen, board):

    # Cleans previous menu
    pygame.draw.rect(screen, BLACK_COLOUR, (GRAPH_WIDTH, 0, MENU_WIDTH, GRAPH_HEIGHT))

    # Player to play box
    textfont = pygame.font.SysFont("monospace", 20)
    textTBD = textfont.render("  Play next:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 30))
    if currentPlayer == 1:
        pygame.draw.circle(screen, RED_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
    else:
        pygame.draw.circle(screen, YELLOW_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)

    # AI autoplay box
    textTBD = textfont.render(" AI autoplay:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 15, 130))
    if AUTO_PLAY_AI:
        textTBD = textfont.render("ON", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 85, 155))
    else:
        textTBD = textfont.render("OFF", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 80, 155))

    # Turn number box
    textTBD = textfont.render("Current Turn:", 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 20, 200))
    textTBD = textfont.render(str(board.piece_count() + 1), 1, WHITE_COLOUR)
    screen.blit(textTBD, (GRAPH_WIDTH + 90, 225))

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


# Screen print when game ends
def draw_game_end(screen, returnValue):

    textfont = pygame.font.SysFont("monospace", 20)

    if returnValue == "WIN":
        if currentPlayer == 1:
            textTBD = textfont.render("  Red Player", 1, RED_COLOUR)
            screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
            textTBD = textfont.render("     WON!", 1, RED_COLOUR)
            screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))
        else:
            textTBD = textfont.render(" Yellow Player", 1, YELLOW_COLOUR)
            screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
            textTBD = textfont.render("     WON!", 1, YELLOW_COLOUR)
            screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))

    if returnValue == "DRAW":
        textTBD = textfont.render("Game ended in", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
        textTBD = textfont.render("     DRAW", 1, WHITE_COLOUR)
        screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))

    pygame.display.update()


# Adds recent played piece in to the grid
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
