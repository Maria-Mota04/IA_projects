import pygame
from src.game.solver import Solver
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState
import time

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

        board = Board([1,2,3,7,6,5,4,8,9,10,11,12,13,14,15,16,17,18,19,20])
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
                        ret = solver.solve(game= game, screen= self.screen, mode=2)

                        if(ret == 0):
                            WinMenu.display(self.screen)
                        else:
                            LossMenu.display(self.screen)

                    if quit_button.collidepoint(mouse):
                        game_running = False

            pygame.display.update()


class WinMenu:
    def display(screen):
        screen.fill((60,25,60))
        font = pygame.font.SysFont('arial', 40)
        win_text = font.render("WIN", True, (255,255,255))
        screen.blit(win_text, (335, 305))

        pygame.display.flip()
        time.sleep(2)

class LossMenu:
    def display(screen):
        screen.fill((60,25,60))
        font = pygame.font.SysFont('arial', 40)
        win_text = font.render("LOSS", True, (255,255,255))
        screen.blit(win_text, (335, 305))

        pygame.display.flip()
        time.sleep(2)