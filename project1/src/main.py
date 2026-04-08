import pygame
import random
from src.gui.menu import *
from src.gui.player_control import *

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    initial_menu = Menu(screen)
    initial_menu.run()
    
    pygame.quit()