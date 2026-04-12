# src/game/solver.py

import math
import time
from typing import Callable, List, Optional

import pygame

from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.game.game import *
from src.game.pdb_heuristic import (
    build_patterns,
    generate_pdb,
    pattern_state_from_positions,
)
from src.gui.controls_helper import ControlHelper
from src.gui.game_graphics import *
from src.gui.hint_settings import HintSettings
from src.states.game_state import GameState

from .game_modes import gameMode


class Solver:
    """
    @brief Core solver responsible for search algorithms and hint generation.
    """

    _shared_pdb = None
    _shared_patterns = None
    _shared_pdb_config = None

    def __init__(self, n: int = 20, k: int = 4, group_size: int = 5):
        """
        @brief Initializes the solver and generates the PDB once.

        The PDB is shared across all Solver instances with the same configuration.

        @param n Total number of tiles.
        @param k Segment size for moves.
        @param group_size Pattern size for PDB.
        """
        self._n = n
        self._k = k
        self._group_size = group_size

        config = (n, k, group_size)

        if (
            Solver._shared_pdb is None
            or Solver._shared_patterns is None
            or Solver._shared_pdb_config != config
        ):
            Solver._shared_patterns = build_patterns(n, group_size)

            print(f"[PDB] Generating PDB for {group_size} tiles... (n={n}, k={k})")
            Solver._shared_pdb = generate_pdb(n, k, group_size)
            Solver._shared_pdb_config = config
            print("[PDB] Successfully generated!")

        self._patterns = Solver._shared_patterns
        self._pdb_5 = Solver._shared_pdb

        self._hint_strategy = SearchStrategy.A_STAR
        self._hint_heuristic_name = "pdb"
        self._hint_config = {
            "depth_limit": 20,
            "max_cost": None,
            "weight": 1.0,
        }
        self._last_search_stats = {
            "nodes": 0,
            "depth": 0,
            "max_memory": 0,
            "found": False,
        }

    def strategy_uses_heuristic(self, strategy: SearchStrategy) -> bool:
        """
        @brief Checks if a strategy uses a heuristic.

        @param strategy Search strategy.
        @return True if heuristic-based.
        """
        return strategy in (
            SearchStrategy.GREEDY,
            SearchStrategy.A_STAR,
            SearchStrategy.WEIGHTED_A_STAR,
        )

    def strategy_uses_depth_limit(self, strategy: SearchStrategy) -> bool:
        """
        @brief Checks if a strategy uses depth limits.

        @param strategy Search strategy.
        @return True if depth-limited.
        """
        return strategy in (
            SearchStrategy.DFS_LIMITED,
            SearchStrategy.ITERATIVE_DEEPENING,
        )

    def strategy_uses_weight(self, strategy: SearchStrategy) -> bool:
        """
        @brief Checks if a strategy uses weighting.

        @param strategy Search strategy.
        @return True for Weighted A*.
        """
        return strategy == SearchStrategy.WEIGHTED_A_STAR

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
        heuristic_func: Optional[Callable[[object], float]] = None,
    ) -> object:
        """
        @brief Main entry point for solving or running the game loop.

        @param game Game instance.
        @param screen Pygame screen.
        @param mode Game mode.
        @param strategy Search strategy.
        @param segment_size Move segment size.
        @param depth_limit Depth limit if applicable.
        @param max_cost Maximum search cost.
        @param weight Heuristic weight for Weighted A*.
        @param heuristic_func Custom heuristic function.
        @return Search result or UI result code.
        """
        if heuristic_func is None:
            heuristic_func = self.heuristic_misplaced

        if mode == gameMode.NORMAL_GAME:
            return self._run_ui_loop(game, screen)

        if mode != gameMode.SEARCH_ALGORITHM:
            raise ValueError(f"Unsupported game mode: {mode}")

        return self._run_search(
            game=game,
            strategy=strategy,
            segment_size=segment_size,
            depth_limit=depth_limit,
            max_cost=max_cost,
            weight=weight,
            heuristic_func=heuristic_func,
        )

    def _run_ui_loop(self, game: Game, screen):
        """
        @brief Runs the interactive game UI loop.

        @param game Game instance.
        @param screen Pygame screen.
        @return Status code.
        """
        game_running = True
        graphics = GameGraphics(game)
        font = pygame.font.SysFont("arial", 40)

        quit_button = pygame.Rect(30, 30, 85, 50)
        hint_button = pygame.Rect(500, 30, 120, 50)
        undo_button = pygame.Rect(650, 30, 120, 50)
        settings_button = pygame.Rect(40, 510, 200, 50)
        help_button = pygame.Rect(650, 500, 50, 50)

        quit_text = font.render("Quit", True, (255, 255, 255))
        hint_text = font.render("Hint", True, (255, 255, 255))
        undo_text = font.render("Undo", True, (255, 255, 255))
        settings_text = font.render("Hint Settings", True, (255, 255, 255))
        help_text = font.render("?", True, (255, 255, 255))

        background_color = (60, 25, 60)
        hint_highlight = None

        while game_running:
            screen.fill(background_color)
            graphics.display(screen, highlight_indices=hint_highlight)

            center_circle = graphics.get_center_circle()
            radius_circle = graphics.get_radius_circle()
            mouse_pos = pygame.mouse.get_pos()

            self._draw_button(screen, quit_button, quit_text, mouse_pos, (40, 32))
            self._draw_button(screen, hint_button, hint_text, mouse_pos, (520, 32))
            self._draw_button(screen, undo_button, undo_text, mouse_pos, (660, 32))
            self._draw_button(
                screen, settings_button, settings_text, mouse_pos, (45, 515)
            )
            self._draw_button(screen, help_button, help_text, mouse_pos, (660, 502))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        game.make_rotate(1)
                        graphics.move_right(screen)
                        hint_highlight = None

                    elif event.key == pygame.K_LEFT:
                        game.make_rotate(-1)
                        graphics.move_left(screen)
                        hint_highlight = None

                if event.type == pygame.MOUSEBUTTONUP:
                    click_pos = event.pos
                    distance_to_center = math.sqrt(
                        (click_pos[0] - center_circle[0]) ** 2
                        + (click_pos[1] - center_circle[1]) ** 2
                    )

                    if distance_to_center <= radius_circle:
                        game.make_move(1)
                        graphics.flip_disks(screen)
                        hint_highlight = None

                    elif quit_button.collidepoint(click_pos):
                        return 1

                    elif undo_button.collidepoint(click_pos):
                        game.undo_move()
                        graphics.update(game)
                        hint_highlight = None

                    elif settings_button.collidepoint(click_pos):
                        if HintSettings(self).run(screen) == -1:
                            return -1
                        graphics.update(game)

                    elif hint_button.collidepoint(click_pos):
                        game._game_stats.hints_used += 1
                        print(
                            f"[UI] Hint requested with heuristic: "
                            f"{self._hint_heuristic_name}"
                        )

                        hinted_state, hint_stats = self.next_best_move_with_search(
                            game.get_board_state(),
                            strategy=self._hint_strategy,
                            segment_size=game.get_segment_size(),
                            depth_limit=self._hint_config["depth_limit"],
                            max_cost=self._hint_config["max_cost"],
                            weight=self._hint_config["weight"],
                            heuristic_func=self.get_heuristic_by_name(
                                self._hint_heuristic_name
                            ),
                            return_stats=True,
                        )

                        game._game_stats.states_explored += hint_stats["nodes"]
                        game._game_stats.solution_depth = hint_stats["depth"]
                        game._game_stats.max_memory = max(
                            game._game_stats.max_memory,
                            hint_stats["max_memory"],
                        )

                        if hinted_state:
                            current_tiles = (
                                game.get_board_state().get_board().get_tiles()
                            )
                            hinted_tiles = hinted_state.get_board().get_tiles()
                            hint_highlight = {
                                i
                                for i in range(len(current_tiles))
                                if current_tiles[i] != hinted_tiles[i]
                            }
                        else:
                            hint_highlight = None

                        graphics.update(game)

                    elif help_button.collidepoint(click_pos):
                        ControlHelper(screen).run()
                        graphics.update(game)

            pygame.display.flip()

            if game.won():
                return 0

    def _draw_button(self, screen, rect, text_surface, mouse_pos, text_pos):
        """
        @brief Draws a UI button.

        @param screen Pygame screen.
        @param rect Button rectangle.
        @param text_surface Rendered text surface.
        @param mouse_pos Current mouse position.
        @param text_pos Text position.
        """
        color = (170, 170, 170) if rect.collidepoint(mouse_pos) else (100, 100, 100)
        pygame.draw.rect(screen, color, rect)
        screen.blit(text_surface, text_pos)

    def _run_search(
        self,
        game: Game,
        strategy: SearchStrategy,
        segment_size: int,
        depth_limit: int,
        max_cost,
        weight: float,
        heuristic_func: Callable[[object], float],
    ):
        """
        @brief Runs the selected search algorithm.

        @param game Game instance.
        @param strategy Search strategy.
        @param segment_size Move segment size.
        @param depth_limit Depth limit.
        @param max_cost Maximum cost.
        @param weight Heuristic weight.
        @param heuristic_func Heuristic function.
        @return Path and search metrics.
        """
        nodes_explored = [0]

        def operators_func(state):
            """
            @brief Generate neighbors while tracking explored-state count.

            @param state Current state to expand.
            @return Iterable of successor states.
            """
            nodes_explored[0] += 1
            return self.generate_possible_moves(state, segment_size)

        goal_state_func = lambda state: state.is_goal()
        heuristic = lambda node: heuristic_func(node.state)

        args = [game.get_board_state(), goal_state_func, operators_func]
        kwargs = {"max_cost": max_cost}

        if self.strategy_uses_depth_limit(strategy):
            args.append(depth_limit)
        elif self.strategy_uses_heuristic(strategy):
            args.append(heuristic)
            if strategy == SearchStrategy.WEIGHTED_A_STAR:
                kwargs["weight"] = weight

        start_time = time.time()
        result = SearchAlgorithms.search(strategy, *args, **kwargs)
        elapsed_time = time.time() - start_time

        if result is None:
            return None, {
                "nodes": nodes_explored[0],
                "time": elapsed_time,
                "depth": 0,
                "found": False,
            }

        path = SearchAlgorithms.extract_path(result)

        return path, {
            "nodes": nodes_explored[0],
            "time": elapsed_time,
            "depth": len(path) - 1,
            "found": True,
        }

    def has_pdb(self) -> bool:
        """
        @brief Checks whether the PDB and patterns are available.

        @return True if PDB data is loaded.
        """
        return bool(self._pdb_5) and bool(self._patterns)

    def get_heuristic_by_name(
        self, heuristic_name: str
    ) -> Callable[[GameState], float]:
        """
        @brief Returns a heuristic function by name.

        @param heuristic_name Heuristic identifier.
        @return Matching heuristic function.
        """
        mapping = {
            "misplaced": self.heuristic_misplaced,
            "breakpoints": self.heuristic_breakpoints,
            "distance": self.heuristic_distance,
            "pdb": self.heuristic_pdb if self.has_pdb() else self.heuristic_misplaced,
        }
        return mapping.get(heuristic_name, self.heuristic_misplaced)

    def heuristic_misplaced(self, state: GameState) -> int:
        """
        @brief Counts misplaced tiles relative to the normalized goal ordering.

        @param state Current game state.
        @return Heuristic estimate.
        """
        tiles = state.get_board().get_tiles()
        n = len(tiles)
        k = state.get_board().get_segment_size()

        start = tiles.index(1)
        misplaced = sum(1 for i in range(n) if tiles[(start + i) % n] != i + 1)

        return math.ceil(misplaced / k) if k > 0 else misplaced

    def heuristic_breakpoints(self, state: GameState) -> int:
        """
        @brief Counts breakpoints in the circular ordering.

        @param state Current game state.
        @return Heuristic estimate.
        """
        tiles = state.get_board().get_tiles()
        n = len(tiles)
        k = state.get_board().get_segment_size()

        breakpoints = sum(
            1
            for i in range(n)
            if tiles[(i + 1) % n] != (1 if tiles[i] == n else tiles[i] + 1)
        )

        return math.ceil(breakpoints / k) if k > 0 else breakpoints

    def heuristic_distance(self, state: GameState) -> int:
        """
        @brief Computes a max circular distance heuristic.

        @param state Current game state.
        @return Heuristic estimate.
        """
        tiles = state.get_board().get_tiles()
        n = len(tiles)
        k = state.get_board().get_segment_size()

        if k <= 1:
            return 0

        start = tiles.index(1)
        max_distance = 0

        for index, tile in enumerate(tiles):
            goal_pos = (start + (tile - 1)) % n
            diff = abs(index - goal_pos)
            max_distance = max(max_distance, min(diff, n - diff))

        return math.ceil(max_distance / (k - 1))

    def heuristic_pdb(self, state: GameState) -> int:
        """
        @brief Pattern Database heuristic.

        @param state Current game state.
        @return Heuristic estimate from the PDB.
        """
        tiles = state.get_board().get_tiles()
        n = len(tiles)
        position_map = {tile: i for i, tile in enumerate(tiles)}

        max_h = 0
        for pattern in self._patterns:
            key = pattern_state_from_positions(position_map, pattern, n)
            h_value = self._pdb_5.get(key, 0)
            if h_value > max_h:
                max_h = h_value

        return max_h

    def generate_possible_moves(
        self, state: GameState, segment_size: int
    ) -> List[tuple[GameState, int]]:
        """
        @brief Generates all possible moves from a state.

        @param state Current game state.
        @param segment_size Move segment size.
        @return List of (next_state, cost) pairs.
        """
        moves = []

        for start in range(state.get_board().size()):
            new_state = state.apply_move(start, segment_size)
            if new_state:
                moves.append((new_state, 1))

        return moves

    def next_best_move_with_search(
        self,
        state,
        strategy,
        segment_size: int = 4,
        depth_limit: int = 20,
        max_cost=None,
        weight: float = 1.0,
        heuristic_func=None,
        return_stats: bool = False,
    ):
        """
        @brief Returns the next move from the best search path.

        @param state Current game state.
        @param strategy Search strategy.
        @param segment_size Move segment size.
        @param depth_limit Depth limit.
        @param max_cost Maximum cost.
        @param weight Heuristic weight.
        @param heuristic_func Heuristic function.
        @param return_stats If True, returns a tuple (state, stats).
        @return Next best state or fallback result.
        """
        heuristic = heuristic_func or self.heuristic_misplaced
        nodes_explored = [0]

        def operators(current_state):
            nodes_explored[0] += 1
            return self.generate_possible_moves(current_state, segment_size)

        goal = lambda current_state: current_state.is_goal()

        args = [state, goal, operators]
        kwargs = {"max_cost": max_cost}

        if self.strategy_uses_depth_limit(strategy):
            args.append(depth_limit)
        elif self.strategy_uses_heuristic(strategy):
            args.append(lambda node: heuristic(node.state))
            if strategy == SearchStrategy.WEIGHTED_A_STAR:
                kwargs["weight"] = weight

        result = SearchAlgorithms.search(strategy, *args, **kwargs)

        if result:
            path = SearchAlgorithms.extract_path(result)
            stats = {
                "nodes": nodes_explored[0],
                "depth": max(0, len(path) - 1),
                "max_memory": nodes_explored[0],
                "found": True,
            }
            self._last_search_stats = stats
            if len(path) >= 2:
                return (path[1], stats) if return_stats else path[1]

            return (path[0], stats) if return_stats else path[0]

        print(
            "[SOLVER] Search failed or already complete, using 1-step Greedy fallback"
        )
        fallback_state = self.next_best_move(state, segment_size, heuristic)
        stats = {
            "nodes": nodes_explored[0],
            "depth": 0,
            "max_memory": nodes_explored[0],
            "found": False,
        }
        self._last_search_stats = stats
        return (fallback_state, stats) if return_stats else fallback_state

    def next_best_move(self, state, segment_size: int = 4, heuristic_func=None):
        """
        @brief Returns the best immediate move according to a heuristic.

        @param state Current game state.
        @param segment_size Move segment size.
        @param heuristic_func Heuristic function.
        @return Best next state.
        """
        heuristic = heuristic_func or self.heuristic_misplaced
        moves = self.generate_possible_moves(state, segment_size)

        if not moves:
            return None

        return min(moves, key=lambda move: heuristic(move[0]))[0]

    def animate_path(self, game: Game, screen, path, delay: float = 1.0):
        """
        @brief Animate a full solution path on screen.

        @param game Game instance to update while animating.
        @param screen Pygame screen used for drawing.
        @param path Sequence of states from initial to goal.
        @param delay Delay in seconds between frames.
        @return -1 if user closes window during animation, else 0.
        """
        if not path:
            return
        
        print(len(path))

        gg = GameGraphics(game)

        prior = path[0].get_board().get_tiles()
        initial_pos = 0
        # compensate (rotate begins at 1)
        gg.alter_pieces(1)

        # display first state (og problem)
        gg.display(screen)
        pygame.display.flip()
        time.sleep(delay)

        for n in path[1:]:

            curBoard = n.get_board().get_tiles()

            print("board: ", curBoard)

            for i in range(initial_pos,len(prior)):
                if prior[i] == curBoard[i]:
                    gg.move_left(screen)
                    print("showing:", end=" ")
                    for p in gg.pieces:
                        print(p.num, end=" ")

                    print("end")
                    pygame.display.flip()
                    time.sleep(delay)
                else:
                    different = True
                    j = 1

                    while different:
                        print("compare: ", prior[i-j], " ", curBoard[i-j])
                        print("index.", i-j)
                        if prior[i-j] == curBoard[i-j]:
                            different = False
                        else:
                            gg.move_right(screen)
                            initial_pos -= 1
                            j += 1
                            time.sleep(delay)

                    initial_pos = i
                    initial_pos = i - j +1
                    break

            gg.flip_disks(screen)
            gg.display(screen)
            pygame.display.flip()

            prior = curBoard

            time.sleep(delay)
