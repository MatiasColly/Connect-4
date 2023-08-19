import pygame
import numpy as np

# Connect 4 board
MAX_ROW = 6
MAX_COLUMN = 7

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


class BoardUI:

    def __init__(self, current_player, auto_ai, board):
        pygame.init()
        self.current_player = current_player
        self.auto_ai = auto_ai
        self.screen = pygame.display.set_mode(GRAPH_SIZE)
        self.draw_board()
        self.draw_menu_text(board)

    # Draw Connect 4 grid
    def draw_board(self):
        pygame.draw.rect(self.screen, BLUE_COLOUR, (0, 0, GRAPH_WIDTH, GRAPH_HEIGHT))
        for row in range(MAX_ROW):
            for column in range(MAX_COLUMN):
                pygame.draw.circle(self.screen, BLACK_COLOUR,
                                   center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                           (row * SQUARE_SIZE) + SQUARE_SIZE / 2),
                                   radius=SQUARE_SIZE * 2 / 5)
        pygame.display.update()

    # Draw right side menu
    def draw_menu_text(self, board):

        # Cleans previous menu
        pygame.draw.rect(self.screen, BLACK_COLOUR, (GRAPH_WIDTH, 0, MENU_WIDTH, GRAPH_HEIGHT))

        # Player to play box
        textfont = pygame.font.SysFont("monospace", 20)
        textTBD = textfont.render("  Play next:", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 30))
        if self.current_player == 1:
            pygame.draw.circle(self.screen, RED_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
        else:
            pygame.draw.circle(self.screen, YELLOW_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)

        # AI autoplay box
        textTBD = textfont.render(" AI autoplay:", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 15, 130))
        if self.auto_ai:
            textTBD = textfont.render("ON", 1, WHITE_COLOUR)
            self.screen.blit(textTBD, (GRAPH_WIDTH + 85, 155))
        else:
            textTBD = textfont.render("OFF", 1, WHITE_COLOUR)
            self.screen.blit(textTBD, (GRAPH_WIDTH + 80, 155))

        # Turn number box
        textTBD = textfont.render("Current Turn:", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 200))
        textTBD = textfont.render(str(board.piece_count() + 1), 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 90, 225))

        # Hotkeys box
        textTBD = textfont.render("Hotkeys:", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 450))
        textTBD = textfont.render("a: AI ON/OFF", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 480))
        textTBD = textfont.render("s: play best", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 510))
        textTBD = textfont.render("   move", 1, WHITE_COLOUR)
        self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 530))

        pygame.display.update()

    # Screen print when game ends
    def draw_game_end(self, returnValue):

        textfont = pygame.font.SysFont("monospace", 20)

        if returnValue == "WIN":
            if self.current_player == 1:
                textTBD = textfont.render("  Red Player", 1, RED_COLOUR)
                self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
                textTBD = textfont.render("     WON!", 1, RED_COLOUR)
                self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))
            else:
                textTBD = textfont.render(" Yellow Player", 1, YELLOW_COLOUR)
                self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
                textTBD = textfont.render("     WON!", 1, YELLOW_COLOUR)
                self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))

        if returnValue == "DRAW":
            textTBD = textfont.render("Game ended in", 1, WHITE_COLOUR)
            self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 300))
            textTBD = textfont.render("     DRAW", 1, WHITE_COLOUR)
            self.screen.blit(textTBD, (GRAPH_WIDTH + 20, 320))

        pygame.display.update()

    # Adds recent played piece in to the grid
    def add_piece(self, row, column, player):
        if player == 1:
            pygame.draw.circle(self.screen, RED_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                                           (row * SQUARE_SIZE) + SQUARE_SIZE / 2),
                               radius=SQUARE_SIZE * 2 / 5)
            pygame.draw.circle(self.screen, YELLOW_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
        else:
            pygame.draw.circle(self.screen, YELLOW_COLOUR, center=((column * SQUARE_SIZE) + SQUARE_SIZE / 2,
                                                              (row * SQUARE_SIZE) + SQUARE_SIZE / 2),
                               radius=SQUARE_SIZE * 2 / 5)
            pygame.draw.circle(self.screen, RED_COLOUR, center=CURRENT_TURN_DIS_POS, radius=SQUARE_SIZE * 1 / 5)
        pygame.display.update()

