import pygame
import math
from pygame.locals import *
from src.game.game import *
from src.states.board import Board
from src.states.game_state import GameState

class Piece:
    def __init__(self, position, num, radius):
        self.position = position
        self.radius = radius
        self.num = num

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.position

    def display(self, screen):
        pygame.draw.circle(screen, (220, 184, 4), self.position, self.radius)

        size = 40

        font = pygame.font.SysFont('arial', size)
        text = font.render(str(self.num), True, (0, 0, 0))

        screen.blit(text, [self.position[0] - 10, self.position[1] - (self.radius * 2 - size) - 2])

class GameGraphics:
    def __init__(self, game : Game):
        self.update(game)
        self.turn_size = game.get_segment_size()
        self.initial = [0,0]
        self.diameter = 0

    def get_center_circle(self):
        return [self.initial[0] + self.diameter/2 - (self.pieces)[1].get_radius() - self.spacing/4 + 5, self.initial[1]]
    
    def get_radius_circle(self):
        return self.diameter/2-5

    def get_position_on_track(self, d, cx, cy, width, r):

        top_len = width
        curve_len = math.pi * r
        bottom_len = width

        # top row
        if d < top_len:
            t = d / top_len
            x = cx - width/2 + t * width
            y = cy - r
            return x, y

        d -= top_len

        if d < curve_len:
            t = d / curve_len
            angle = -math.pi/2 + t * math.pi
            x = cx + width/2 + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            return x, y

        d -= curve_len

        if d < bottom_len:
            t = d / bottom_len
            x = cx + width/2 - t * width
            y = cy + r
            return x, y

        d -= bottom_len

        t = d / curve_len
        angle = math.pi/2 + t * math.pi
        x = cx - width/2 + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        return x, y

    def update(self, game: Game):
        self.pieces = []
        radius = 30

        num = game.get_board_state().get_board().get_tiles()
        total = len(num)

        cx, cy = 400, 300
        width = 350
        height = 250
        r = height / 2

        total_len = width + width + 2 * math.pi * r

        self.spacing = total_len / total

        for i in range(total):
            d = i * self.spacing
            x, y = self.get_position_on_track(d, cx, cy, width, r)
            self.pieces.append(Piece([int(x), int(y)], num[i], radius))

    def display(self,screen):
        # grey background
        pygame.draw.rect(screen, (166, 171, 175), pygame.Rect(400 - 350/2 - 20, 300 - 250 / 2 - 40, 350 + 40, 250 + 80))
        pygame.draw.circle(screen, (166, 171, 175), [400 + 350/2, 300], 250/2 + 40)
        pygame.draw.circle(screen, (166, 171, 175), [400 - 350/2, 300], 250/2 + 40)

        # purple circle
        self.diameter = (self.pieces)[1].get_radius() * (self.turn_size-1) + self.spacing * (self.turn_size -1)
        self.initial = (self.pieces)[1].get_position()

        pygame.draw.circle(screen, (69, 92, 168), [self.initial[0] + self.diameter/2 - (self.pieces)[1].get_radius() - self.spacing/4 + 5, self.initial[1]], self.diameter/2-5)


        for piece in self.pieces:
            piece.display(screen)