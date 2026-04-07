from typing import Callable, List
from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.states.board import Board
from src.states.game_state import GameState
from .game_modes import gameMode
from src.gui.game_graphics import *
from src.game.game import *
import pygame

class Solver:

    def solve(
        self,
        game: Game,
        screen,
        mode: gameMode,
        strategy: SearchStrategy = SearchStrategy.BFS,
        segment_size: int = 4,
        depth_limit: int = 20,
        max_cost=None,
        weight: float = 1.0,
        heuristic_func: Callable[[object], float] | None = None,
    ) -> object:
        if mode == gameMode.NORMAL_GAME:
            game_running = True
            gg = GameGraphics(game)

            font = pygame.font.SysFont('arial', 40)
            quit_button = pygame.Rect(30, 30, 85, 50)            
            quit_text = font.render("Quit", True, (255,255,255))

            while game_running:
                mouse = pygame.mouse.get_pos()

                pygame.draw.rect(screen, (170,170,170) if quit_button.collidepoint(mouse) else (100,100,100), quit_button)
                screen.blit(quit_text, (40, 32))
                
                for event in pygame.event.get():

                    # event closing the window
                    if event.type == pygame.QUIT:
                        game_running = False
                        return -1

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

                        # the mouse is in the circle (turn circle)
                        if(math.sqrt(math.pow(mouse[0]-center_circle[0],2) + math.pow(mouse[1]-center_circle[1],2)) <= radius_circle):
                            game.make_move(1)
                            gg.update(game)
                    
                        elif(quit_button.collidepoint(mouse)):
                            return 1
            

                gg.display(screen)

                center_circle = gg.get_center_circle()
                radius_circle = gg.get_radius_circle()

                pygame.display.flip()

                if(game.won()):
                    return 0

        if mode != gameMode.SEARCH_ALGORITHM:
            raise ValueError(f"Unsupported game mode: {mode}")

        goal_state_func = lambda state: state.is_goal()
        operators_func = lambda state: self.generate_possible_moves(state, segment_size)

        heuristic = heuristic_func
        if heuristic is None:
            heuristic = lambda node: self.heuristic_misplaced(node.state)

        args = [game.get_board_state(), goal_state_func, operators_func]
        kwargs = {"max_cost": max_cost}

        if strategy in (
            SearchStrategy.DFS_LIMITED,
            SearchStrategy.ITERATIVE_DEEPENING,
        ):
            args.append(depth_limit)
        elif strategy in (
            SearchStrategy.GREEDY,
            SearchStrategy.A_STAR,
            SearchStrategy.WEIGHTED_A_STAR,
        ):
            args.append(heuristic)
            if strategy == SearchStrategy.WEIGHTED_A_STAR:
                kwargs["w"] = weight

        result = SearchAlgorithms.search(strategy, *args, **kwargs)

        if mode == gameMode.SEARCH_ALGORITHM and result is not None:
            game.set_board_state(result.state)

        return result

        

    # Heuristics
    def heuristic_misplaced(self, game: Game) -> int:
        pass

    def heuristic_inversions(self, game: Game) -> int:
        pass

    def heuristic_distance(self, game: Game) -> int:
        pass

    # Move generator
    def generate_possible_moves(
        self, state: GameState, segment_size: int
    ) -> List[tuple[GameState, int]]:
        moves = []
        board_size = state.get_board().size()

        for reverse_start in range(board_size):
            new_state = state.apply_move(reverse_start, segment_size)
            if new_state is not None:
                moves.append((new_state, self.get_move_cost(reverse_start)))

        rotated_state = GameState(Board(state.get_board().get_tiles())).apply_rotate(1)
        moves.append((rotated_state, self.get_move_cost(-1)))

        return moves

    # Next best move
    def next_best_move(self) -> GameState:
        pass

    # Utils
    def get_move_cost(self, move: int) -> int:
        _ = move
        return 1
