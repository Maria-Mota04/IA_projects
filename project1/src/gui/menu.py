import pygame
from src.game.solver import Solver
import random
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState

class Menu:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        game_running = True
        font = pygame.font.SysFont('arial', 40)
        WHITE = (255,255,255)
        LIGHT = (170,170,170)
        DARK = (100,100,100)
        BG = (60,25,60)

        l = list(range(1,20))
        random.shuffle(l)
        board = Board(l)
        state = GameState(board)
        game = Game(state,10)

        solver = Solver()

        while game_running:
            self.screen.fill(BG)
            mouse = pygame.mouse.get_pos()

            play_button = pygame.Rect(300, 300, 140, 50)
            quit_button = pygame.Rect(300, 380, 140, 50)

            pygame.draw.rect(self.screen, LIGHT if play_button.collidepoint(mouse) else DARK, play_button)
            pygame.draw.rect(self.screen, LIGHT if quit_button.collidepoint(mouse) else DARK, quit_button)

            play_text = font.render("Play", True, WHITE)
            quit_text = font.render("Quit", True, WHITE)

            self.screen.blit(play_text, (335, 305))
            self.screen.blit(quit_text, (335, 385))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.MOUSEBUTTONUP:

                    if play_button.collidepoint(mouse):
                        solver.solve(game= game, screen= self.screen, mode=2)

                    if quit_button.collidepoint(mouse):
                        game_running = False

            pygame.display.update()