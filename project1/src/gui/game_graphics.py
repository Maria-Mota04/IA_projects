import pygame
import math
import time
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

    def display(self, screen, highlight=False):
        color = (230, 80, 80) if highlight else (220, 184, 4)
        pygame.draw.circle(screen, color, self.position, self.radius)
        if highlight:
            pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 3)

        size = 40

        font = pygame.font.SysFont("arial", size)
        text = font.render(str(self.num), True, (0, 0, 0))

        screen.blit(
            text,
            [self.position[0] - 10, self.position[1] - (self.radius * 2 - size) - 2],
        )


class GameGraphics:
    def __init__(self, game: Game):
        self.update(game)
        print(self.pieces)
        self.turn_size = game.get_segment_size()
        self.initial = [0,0]
        self.diameter = (self.pieces)[1].get_radius() * (self.turn_size-1) + self.spacing * (self.turn_size -1)
        self.center_circle = [self.pieces[1].get_position()[0] + self.diameter/2 - (self.pieces)[1].get_radius() - self.spacing/4 + 5, self.pieces[0].get_position()[1]]

    def get_center_circle(self):
        return self.center_circle
    
    def get_radius_circle(self):
        return self.diameter / 2 - 5
    
    def alter_pieces(self, direction):
        if direction == 1:  # right
            self.pieces = [self.pieces[-1]] + self.pieces[:-1]
        else:  # left
            self.pieces = self.pieces[1:] + [self.pieces[0]]

        self.update_pieces_position()

    def get_position_on_track(self, d, cx, cy, width, r):

        top_len = width
        curve_len = math.pi * r
        bottom_len = width

        # top row
        if d < top_len:
            t = d / top_len
            x = cx - width / 2 + t * width
            y = cy - r
            return x, y

        d -= top_len

        if d < curve_len:
            t = d / curve_len
            angle = -math.pi / 2 + t * math.pi
            x = cx + width / 2 + r * math.cos(angle)
            y = cy + r * math.sin(angle)
            return x, y

        d -= curve_len

        if d < bottom_len:
            t = d / bottom_len
            x = cx + width / 2 - t * width
            y = cy + r
            return x, y

        d -= bottom_len

        t = d / curve_len
        angle = math.pi / 2 + t * math.pi
        x = cx - width / 2 + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        return x, y

    def update(self, game: Game):
        self.pieces = []
        radius = 30

        tiles = game.get_board_state().get_board().get_tiles()
        total = len(tiles)

        for i in range(total):
            self.pieces.append(Piece([0,0], tiles[i], radius))

        self.update_pieces_position()

    def update_pieces_position(self):
        total = len(self.pieces)

        cx, cy = 400, 300
        width = 350
        height = 250
        r = height / 2

        total_len = width + width + 2 * math.pi * r

        self.spacing = total_len / total

        for i in range(total):
            d = i * self.spacing
            x, y = self.get_position_on_track(d, cx, cy, width, r)
            self.pieces[i].position = [x,y]

    def display(self, screen, highlight_indices=None):
        # grey background
        pygame.draw.rect(
            screen,
            (166, 171, 175),
            pygame.Rect(400 - 350 / 2 - 20, 300 - 250 / 2 - 40, 350 + 40, 250 + 80),
        )
        pygame.draw.circle(screen, (166, 171, 175), [400 + 350 / 2, 300], 250 / 2 + 40)
        pygame.draw.circle(screen, (166, 171, 175), [400 - 350 / 2, 300], 250 / 2 + 40)

        # purple circle

        pygame.draw.circle(screen, (69, 92, 168), self.center_circle, self.diameter/2-5)


        for i, piece in enumerate(self.pieces):
            piece.display(
                screen,
                highlight=highlight_indices is not None and i in highlight_indices,
            )

    def move_left(self, screen):
        self.animate_side_move(-1, screen)

    def move_right(self, screen):
        self.animate_side_move(1, screen)

    def animate_side_move(self, direction, screen):
        steps = 10
        move_amount = self.spacing * direction / steps

        cx, cy = 400, 300
        width = 350
        height = 250
        r = height / 2

        total_len = width + width + 2 * math.pi * r

        # Get current distances of each piece
        distances = []
        for i in range(len(self.pieces)):
            d = i * self.spacing
            distances.append(d)

        for _ in range(steps):

            for i in range(len(self.pieces)):
                distances[i] = (distances[i] + move_amount) % total_len
                x, y = self.get_position_on_track(distances[i], cx, cy, width, r)
                self.pieces[i].position = [int(x), int(y)]

            self.display(screen)
            pygame.display.flip()
            pygame.time.delay(15)

        self.alter_pieces(direction)

    def flip_disks(self, screen):
        steps = 15

        for _ in range(steps):
            for j in range(1,self.turn_size+1):
                x, y = self.pieces[j].position

                # Translate to origin
                rel_x = x - self.center_circle[0]
                rel_y = y - self.center_circle[1]

                # Rotate
                new_x = rel_x * math.cos(math.pi/steps) - rel_y * math.sin(math.pi/steps)
                new_y = rel_x * math.sin(math.pi/steps) + rel_y * math.cos(math.pi/steps)

                # Translate back
                self.pieces[j].position = [int(self.center_circle[0] + new_x), int(self.center_circle[1] + new_y)]

            self.display(screen)
            pygame.display.flip()
            pygame.time.delay(15)

        self.pieces = [self.pieces[0]] + self.pieces[1:self.turn_size+1][::-1] + self.pieces[self.turn_size+1:]
