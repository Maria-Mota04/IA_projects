import pygame
from src.gui.game_graphics import *
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState


def main():
    pygame.init()

    game_running = True

    screen = pygame.display.set_mode((800, 600))

    board = Board([1, 2, 3, 4, 5, 7, 6, 8, 9, 10])
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

        screen.fill([255,255,255])
        gg.display(screen)

        pygame.display.flip()
    
    pygame.quit()