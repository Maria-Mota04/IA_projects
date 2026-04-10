import pygame
from src.gui.menu import Menu

def main():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))

    initial_menu = Menu(screen)
    initial_menu.run()
    
    pygame.quit()

    """
    TOY ESTA É A FUNÇÃO QUE USA O HIGHLIGHT
    def animate_path(self, game: Game, screen, path, delay=1.0):
        gg = GameGraphics(game)
        prev_tiles = None

        for state in path:
            game.state = state
            gg.update(game)

            curr_tiles = state.get_board().get_tiles()
            if prev_tiles is not None:
                differing = {
                    i for i in range(len(curr_tiles)) if curr_tiles[i] != prev_tiles[i]
                }
                highlight = None if len(differing) == len(curr_tiles) else differing
            else:
                highlight = None
            prev_tiles = list(curr_tiles)

            screen.fill((60, 25, 60))
            gg.display(screen)
            gg.display(screen, highlight_indices=highlight)
            pygame.event.pump()
            pygame.display.flip()
            time.sleep(1)
            is_last = state is path[-1]
            time.sleep(delay * 3 if is_last else delay)
    """