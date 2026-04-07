import pygame
from src.game.solver import Solver
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState
import time

class Menu:
    def __init__(self, screen):
        self.screen = screen

        self.WHITE = (255,255,255)
        self.LIGHT = (170,170,170)
        self.DARK = (100,100,100)
        self.BG = (60,25,60)

    def run(self):
        game_running = True
        font = pygame.font.SysFont('arial', 40)

        board = Board([1,2,3,7,6,5,4,8,9,10,11,12,13,14,15,16,17,18,19,20])
        state = GameState(board)
        game = Game(state)

        solver = Solver()
        try_again = False

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            play_button = pygame.Rect(300, 300, 140, 50)
            quit_button = pygame.Rect(300, 380, 140, 50)

            pygame.draw.rect(self.screen, self.LIGHT if play_button.collidepoint(mouse) else self.DARK, play_button)
            pygame.draw.rect(self.screen, self.LIGHT if quit_button.collidepoint(mouse) else self.DARK, quit_button)

            play_text = font.render("Play", True, self.WHITE)
            quit_text = font.render("Quit", True, self.WHITE)

            self.screen.blit(play_text, (335, 305))
            self.screen.blit(quit_text, (335, 385))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    game_running = False

                if event.type == pygame.MOUSEBUTTONUP or try_again:

                    if play_button.collidepoint(mouse) or try_again:
                        try_again = False
                        ret = solver.solve(game= game, screen= self.screen, mode=2)

                        if(ret == 0):
                            self.display_win()
                        elif(ret == -1):
                            game_running = False
                        else:
                            ret1 = self.display_lose()

                            # they want to retry the level
                            if(ret1==0):
                                board.reset_board()
                                print("board was reset")
                                try_again = True
                                pygame.event.post(pygame.event.Event(1))
                                continue

                            if(ret1==-1):
                                game_running = False

                        # make a new board, for next try
                        board = Board([1,2,3,7,6,5,4,8,9,10,11,12,13,14,15,16,17,18,19,20])
                        state = GameState(board)
                        game = Game(state)

                    if quit_button.collidepoint(mouse):
                        game_running = False

            pygame.display.update()

    def display_win(self):
        self.screen.fill((60,25,60))
        font = pygame.font.SysFont('arial', 40)
        win_text = font.render("WIN", True, (255,255,255))
        self.screen.blit(win_text, (335, 305))

        pygame.display.flip()
        time.sleep(2)


    def display_lose(self):
        game_running = True

        while game_running:
            self.screen.fill(self.BG)
            mouse = pygame.mouse.get_pos()

            font = pygame.font.SysFont('arial', 40)
            win_text = font.render("LOSS", True, self.WHITE)
            self.screen.blit(win_text, (335, 200))

            retry_button = pygame.Rect(300, 300, 140, 50)
            menu_button = pygame.Rect(300, 380, 140, 50)

            pygame.draw.rect(self.screen, self.LIGHT if retry_button.collidepoint(mouse) else self.DARK, retry_button)
            pygame.draw.rect(self.screen, self.LIGHT if menu_button.collidepoint(mouse) else self.DARK, menu_button)
            retry_text = font.render("Retry", True, self.WHITE)
            menu_text = font.render("Back to menu", True, self.WHITE)

            self.screen.blit(retry_text, (335, 305))
            self.screen.blit(menu_text, (335, 385))

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:

                    if retry_button.collidepoint(mouse):
                        return 0

                    if menu_button.collidepoint(mouse):
                        return 1

            pygame.display.update()
