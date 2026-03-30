import pygame
from pygame.locals import *
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState

class Piece:
    def __init__(self, position, num, radius):
        self.position = position
        self.radius = radius
        self.num = num

    def move_right(self):
        self.position[0] += self.radius

    def move_left(self):
        self.position[0] -= self.radius

    def move_up(self):
        self.position[1] += 20

    def display(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius)

        size = 40

        font = pygame.font.SysFont('arial', size)
        text = font.render(str(self.num), True, (0, 0, 0))

        screen.blit(text, [self.position[0] - 10, self.position[1] - (self.radius * 2 - size) - 2])

class GameGraphics:
    def __init__(self, game : Game):
        self.update(game)

    def update(self, game : Game):
        self.pieces = []
        radius = 30

        num = game.get_board_state().get_board().get_tiles()

        for i in range(len(num)):
            self.pieces.append(Piece([100 + (radius* 2 + 5)*i, 100], num[i], radius))


    def display(self,screen):
        for piece in self.pieces:
            piece.display(screen)