import pygame
from src.gui.menu import Menu

def main():
    """@brief Initialize pygame and run the main menu."""
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    initial_menu = Menu(screen)
    initial_menu.run()
    
    pygame.quit()