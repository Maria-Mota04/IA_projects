import math
from typing import Callable, List
from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.states.board import Board
from src.states.game_state import GameState
from .game_modes import gameMode
from src.gui.game_graphics import *
from src.game.game import *
import pygame
from src.game.pdb_heuristic import (pattern_state_from_positions)

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

            font = pygame.font.SysFont("arial", 40)
            quit_button = pygame.Rect(30, 30, 85, 50)
            quit_text = font.render("Quit", True, (255, 255, 255))

            undo_button = pygame.Rect(650, 30, 120, 50)
            undo_text = font.render("Undo", True, (255, 255, 255))

            while game_running:
                mouse = pygame.mouse.get_pos()

                pygame.draw.rect(
                    screen,
                    (
                        (170, 170, 170)
                        if quit_button.collidepoint(mouse)
                        else (100, 100, 100)
                    ),
                    quit_button,
                )
                screen.blit(quit_text, (40, 32))

                pygame.draw.rect(
                    screen,
                    (
                        (170, 170, 170)
                        if undo_button.collidepoint(mouse)
                        else (100, 100, 100)
                    ),
                    undo_button,
                )

                screen.blit(undo_text, (660, 32))

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
                        if (
                            math.sqrt(
                                math.pow(mouse[0] - center_circle[0], 2)
                                + math.pow(mouse[1] - center_circle[1], 2)
                            )
                            <= radius_circle
                        ):
                            game.make_move(1)
                            gg.update(game)

                        elif quit_button.collidepoint(mouse):
                            return 1
                        elif undo_button.collidepoint(mouse):
                            game.undo_move()
                            gg.update(game)

                gg.display(screen)

                center_circle = gg.get_center_circle()
                radius_circle = gg.get_radius_circle()

                pygame.display.flip()

                if game.won():
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
    def heuristic_misplaced(self, state: GameState) -> int:
        board = state.get_board()
        tiles = board.get_tiles()
        n = len(tiles)
        k = board.get_segment_size()

        start = tiles.index(1)

        misplaced = 0
        for i in range(n):
            if tiles[(start + i) % n] != i + 1:
                misplaced += 1

        return math.ceil(misplaced / k) if k > 0 else misplaced

    def heuristic_breakpoints(self, state: GameState) -> int:
        board = state.get_board()
        tiles = board.get_tiles()
        n = len(tiles)
        k = board.get_segment_size()

        breakpoints = 0

        for i in range(n):
            current = tiles[i]
            nxt = tiles[(i + 1) % n]
            expected_next = 1 if current == n else current + 1

            if nxt != expected_next:
                breakpoints += 1

        return math.ceil(breakpoints / k) if k > 0 else breakpoints

    def heuristic_distance(self, state: GameState) -> int:
        board = state.get_board()
        tiles = board.get_tiles()
        n = len(tiles)
        k = board.get_segment_size()

        if k <= 1:
            return 0

        start = tiles.index(1)
        max_distance = 0

        for i in range(n):
            tile = tiles[i]
            goal_pos = (start + (tile - 1)) % n

            diff = abs(i - goal_pos)
            circular_dist = min(diff, n - diff)

            max_distance = max(max_distance, circular_dist)

        return math.ceil(max_distance / (k - 1))

    def heuristic_pdb(self, state: GameState) -> int:
        tiles = state.get_board().get_tiles()
        n = len(tiles)

        pos_map = {tile: i for i, tile in enumerate(tiles)}

        best = 0
        for pattern in self._patterns:
            key = pattern_state_from_positions(pos_map, pattern, n)
            h = self._pdb_5.get(key, 0)
            best = max(best, h)

        return best

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
