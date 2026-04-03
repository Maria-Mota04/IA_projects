import pygame
import random
from src.gui.game_graphics import *
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState

class PlayerControl:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        game_running = True

        l = list(range(1,20))
        random.shuffle(l)
        board = Board(l)
        state = GameState(board)

        game = Game(state,10)

        gg = GameGraphics(game)

        while game_running:
            for event in pygame.event.get():

                # event closing the window
                if event.type == pygame.QUIT:
                    game_running = False

                # event a key is pushed
                if event.type == pygame.KEYDOWN:
                    # right key
                    if event.key == pygame.K_RIGHT:
                        game.make_rotate(1)
                        gg.update(game)

                    # left key
                    if event.key == pygame.K_LEFT:
                        game.make_rotate(-1)
                        gg.update(game)

                # event is a mouse click
                if event.type == pygame.MOUSEBUTTONUP:
                    game.make_move(1)
                    gg.update(game)

            gg.display(self.screen)

            pygame.display.flip()