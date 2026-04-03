import pygame

class Menu:
    def __init__(self, screen):
        self.screen = screen

    def run(self):
        game_running = True
        font = pygame.font.SysFont('arial', 40)

        while game_running:
