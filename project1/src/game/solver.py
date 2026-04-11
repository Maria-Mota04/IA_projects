import math
import time
from typing import Callable, List
from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.states.board import Board
from src.states.game_state import GameState
from .game_modes import gameMode
from src.gui.game_graphics import *
from src.gui.controls_helper import ControlHelper
from src.game.game import *
import pygame
from src.game.pdb_heuristic import pattern_state_from_positions


class Solver:
    def __init__(self, pdb_5=None, patterns=None):
        self._pdb_5 = pdb_5 or {}
        self._patterns = patterns or []

        self._hint_strategy = SearchStrategy.A_STAR
        self._hint_heuristic_name = "misplaced"

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
        if heuristic_func is None:
            heuristic_func = self.heuristic_misplaced

        if mode == gameMode.NORMAL_GAME:
            game_running = True
            gg = GameGraphics(game)

            font = pygame.font.SysFont("arial", 40)
            small_font = pygame.font.SysFont("arial", 22)

            quit_button = pygame.Rect(30, 30, 85, 50)
            quit_text = font.render("Quit", True, (255, 255, 255))

            settings_button = pygame.Rect(30, 500, 170, 50)
            settings_text = small_font.render("Hint Settings", True, (255, 255, 255))

            hint_button = pygame.Rect(500, 30, 120, 50)
            hint_text = font.render("Hint", True, (255, 255, 255))

            undo_button = pygame.Rect(650, 30, 120, 50)
            undo_text = font.render("Undo", True, (255, 255, 255))

            control_helper_menu_button = pygame.Rect(650, 500, 50, 50)
            control_helper_menu_text = font.render("?", True, (255, 255, 255))

            BG = (60, 25, 60)
            hint_highlight = None
            center_circle = (0, 0)
            radius_circle = 0

            while game_running:
                screen.fill(BG)

                gg.display(screen, highlight_indices=hint_highlight)
                center_circle = gg.get_center_circle()
                radius_circle = gg.get_radius_circle()

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
                        if settings_button.collidepoint(mouse)
                        else (100, 100, 100)
                    ),
                    settings_button,
                )
                screen.blit(settings_text, (45, 515))

                pygame.draw.rect(
                    screen,
                    (
                        (170, 170, 170)
                        if hint_button.collidepoint(mouse)
                        else (100, 100, 100)
                    ),
                    hint_button,
                )
                screen.blit(hint_text, (520, 32))

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

                pygame.draw.rect(
                    screen,
                    (
                        (170, 170, 170)
                        if control_helper_menu_button.collidepoint(mouse)
                        else (100, 100, 100)
                    ),
                    control_helper_menu_button,
                )
                screen.blit(control_helper_menu_text, (660, 502))

                current_hint_label = small_font.render(
                    f"Hint: {self.get_strategy_label(self._hint_strategy)} / "
                    f"{self.get_heuristic_label(self._hint_heuristic_name)}",
                    True,
                    (230, 230, 230),
                )
                hint_label_rect = current_hint_label.get_rect(center=(400, 520))
                screen.blit(current_hint_label, hint_label_rect)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_running = False
                        return -1

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RIGHT:
                            game.make_rotate(1)
                            gg.move_right(screen)
                            hint_highlight = None

                        if event.key == pygame.K_LEFT:
                            game.make_rotate(-1)
                            gg.move_left(screen)
                            hint_highlight = None

                    if event.type == pygame.MOUSEBUTTONUP:
                        if (
                            math.sqrt(
                                math.pow(mouse[0] - center_circle[0], 2)
                                + math.pow(mouse[1] - center_circle[1], 2)
                            )
                            <= radius_circle
                        ):
                            game.make_move(1)
                            gg.flip_disks(screen)
                            hint_highlight = None

                        elif quit_button.collidepoint(mouse):
                            return 1

                        elif undo_button.collidepoint(mouse):
                            game.undo_move()
                            gg.update(game)
                            hint_highlight = None

                        elif settings_button.collidepoint(mouse):
                            panel_result = self.choose_hint_settings(screen)
                            if panel_result == -1:
                                return -1
                            gg.update(game)

                        elif hint_button.collidepoint(mouse):
                            current_state = game.get_board_state()
                            current_segment_size = game.get_segment_size()

                            hinted_state = self.next_best_move_with_search(
                                current_state,
                                strategy=self._hint_strategy,
                                segment_size=current_segment_size,
                                depth_limit=depth_limit,
                                max_cost=max_cost,
                                weight=weight,
                                heuristic_func=self.get_heuristic_by_name(
                                    self._hint_heuristic_name
                                ),
                            )

                            if hinted_state is not None:
                                current_tiles = current_state.get_board().get_tiles()
                                hinted_tiles = hinted_state.get_board().get_tiles()
                                print("Current:", current_tiles)
                                print("Hinted :", hinted_tiles)

                                hint_highlight = {
                                    i
                                    for i in range(len(current_tiles))
                                    if current_tiles[i] != hinted_tiles[i]
                                }
                            else:
                                hint_highlight = None

                            gg.update(game)

                        elif control_helper_menu_button.collidepoint(mouse):
                            ControlHelper(screen).run()
                            gg.update(game)

                pygame.display.flip()

                if game.won():
                    return 0

        if mode != gameMode.SEARCH_ALGORITHM:
            raise ValueError(f"Unsupported game mode: {mode}")

        nodes_explored = [0]
        _inner_ops = lambda state: self.generate_possible_moves(state, segment_size)

        def operators_func(state):
            nodes_explored[0] += 1
            return _inner_ops(state)

        goal_state_func = lambda state: state.is_goal()

        heuristic = heuristic_func
        if heuristic is None:
            heuristic = lambda node: self.heuristic_misplaced(node.state)

        args = [game.get_board_state(), goal_state_func, operators_func]
        kwargs = {"max_cost": max_cost}

        if strategy in (
            SearchStrategy.DFS,
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

        t0 = time.time()
        result = SearchAlgorithms.search(strategy, *args, **kwargs)
        elapsed = time.time() - t0

        if result is None:
            return None, {
                "nodes": nodes_explored[0],
                "time": elapsed,
                "depth": 0,
                "found": False,
            }

        path = SearchAlgorithms.extract_path(result)
        stats = {
            "nodes": nodes_explored[0],
            "time": elapsed,
            "depth": len(path) - 1,
            "found": True,
        }
        return path, stats

    def choose_hint_settings(self, screen):
        font = pygame.font.SysFont("arial", 28)
        title_font = pygame.font.SysFont("arial", 38)
        small_font = pygame.font.SysFont("arial", 20)

        WHITE = (255, 255, 255)
        LIGHT = (170, 170, 170)
        DARK = (100, 100, 100)
        BG = (60, 25, 60)
        SELECTED = (180, 80, 180)

        back_button = pygame.Rect(30, 30, 85, 50)
        confirm_button = pygame.Rect(300, 510, 200, 50)

        algo_buttons = [
            (pygame.Rect(60, 140, 320, 42), "BFS", SearchStrategy.BFS),
            (pygame.Rect(420, 140, 320, 42), "DFS", SearchStrategy.DFS),
            (pygame.Rect(60, 195, 320, 42), "Limited DFS", SearchStrategy.DFS_LIMITED),
            (
                pygame.Rect(420, 195, 320, 42),
                "Iterative Deepening",
                SearchStrategy.ITERATIVE_DEEPENING,
            ),
            (pygame.Rect(60, 250, 320, 42), "Uniform Cost", SearchStrategy.UNIFORM_COST),
            (pygame.Rect(420, 250, 320, 42), "Greedy", SearchStrategy.GREEDY),
            (pygame.Rect(60, 305, 320, 42), "A*", SearchStrategy.A_STAR),
            (
                pygame.Rect(420, 305, 320, 42),
                "Weighted A*",
                SearchStrategy.WEIGHTED_A_STAR,
            ),
        ]

        heur_buttons = [
            (pygame.Rect(60, 395, 150, 42), "Misplaced", "misplaced"),
            (pygame.Rect(230, 395, 170, 42), "Breakpoints", "breakpoints"),
            (pygame.Rect(420, 395, 150, 42), "Distance", "distance"),
        ]

        if self.has_pdb():
            heur_buttons.append((pygame.Rect(590, 395, 110, 42), "PDB", "pdb"))

        selected_strategy = self._hint_strategy
        selected_heuristic_name = self._hint_heuristic_name

        while True:
            screen.fill(BG)
            mouse = pygame.mouse.get_pos()

            title = title_font.render("Hint Settings", True, WHITE)
            algo_title = font.render("Choose algorithm", True, WHITE)
            heur_title = font.render("Choose heuristic", True, WHITE)
            note = small_font.render(
                "These settings are used by the Hint button during the human game.",
                True,
                (220, 220, 220),
            )

            screen.blit(title, (250, 50))
            screen.blit(algo_title, (255, 100))
            screen.blit(heur_title, (260, 355))
            screen.blit(note, (110, 470))

            pygame.draw.rect(
                screen,
                LIGHT if back_button.collidepoint(mouse) else DARK,
                back_button,
            )
            screen.blit(font.render("Back", True, WHITE), (35, 38))

            pygame.draw.rect(
                screen,
                LIGHT if confirm_button.collidepoint(mouse) else DARK,
                confirm_button,
            )
            screen.blit(font.render("Save", True, WHITE), (365, 518))

            for button, label, strategy in algo_buttons:
                color = (
                    SELECTED
                    if strategy == selected_strategy
                    else (LIGHT if button.collidepoint(mouse) else DARK)
                )
                pygame.draw.rect(screen, color, button)
                screen.blit(
                    small_font.render(label, True, WHITE),
                    (button.x + 10, button.y + 11),
                )

            for button, label, heuristic_name in heur_buttons:
                color = (
                    SELECTED
                    if heuristic_name == selected_heuristic_name
                    else (LIGHT if button.collidepoint(mouse) else DARK)
                )
                pygame.draw.rect(screen, color, button)
                screen.blit(
                    small_font.render(label, True, WHITE),
                    (button.x + 10, button.y + 11),
                )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1

                if event.type == pygame.MOUSEBUTTONUP:
                    if back_button.collidepoint(mouse):
                        return -2

                    for button, _, strategy in algo_buttons:
                        if button.collidepoint(mouse):
                            selected_strategy = strategy

                    for button, _, heuristic_name in heur_buttons:
                        if button.collidepoint(mouse):
                            selected_heuristic_name = heuristic_name

                    if confirm_button.collidepoint(mouse):
                        self._hint_strategy = selected_strategy
                        self._hint_heuristic_name = selected_heuristic_name
                        return 0

            pygame.display.update()

    def has_pdb(self) -> bool:
        return bool(self._pdb_5) and bool(self._patterns)

    def get_heuristic_by_name(
        self, heuristic_name: str
    ) -> Callable[[GameState], float] | None:
        if heuristic_name == "misplaced":
            return self.heuristic_misplaced
        if heuristic_name == "breakpoints":
            return self.heuristic_breakpoints
        if heuristic_name == "distance":
            return self.heuristic_distance
        if heuristic_name == "pdb" and self.has_pdb():
            return self.heuristic_pdb
        return self.heuristic_misplaced

    def get_strategy_label(self, strategy: SearchStrategy) -> str:
        labels = {
            SearchStrategy.BFS: "BFS",
            SearchStrategy.DFS: "DFS",
            SearchStrategy.DFS_LIMITED: "Limited DFS",
            SearchStrategy.ITERATIVE_DEEPENING: "Iterative Deepening",
            SearchStrategy.UNIFORM_COST: "Uniform Cost",
            SearchStrategy.GREEDY: "Greedy",
            SearchStrategy.A_STAR: "A*",
            SearchStrategy.WEIGHTED_A_STAR: "Weighted A*",
        }
        return labels.get(strategy, str(strategy))

    def get_heuristic_label(self, heuristic_name: str) -> str:
        labels = {
            "misplaced": "Misplaced",
            "breakpoints": "Breakpoints",
            "distance": "Distance",
            "pdb": "PDB",
        }
        return labels.get(heuristic_name, heuristic_name)

    def animate_path(self, game: Game, screen, path, delay=1.0):
        gg = GameGraphics(game)

        prior = path[0].get_board().get_tiles()
        initial_pos = 0
        gg.alter_pieces(1)

        gg.display(screen)
        pygame.display.flip()
        time.sleep(delay)

        for n in path[1:]:
            curBoard = n.get_board().get_tiles()

            print("board: ", curBoard)

            for i in range(initial_pos, len(prior)):
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
                        print("compare: ", prior[i - j], " ", curBoard[i - j])
                        print("index.", i - j)
                        if prior[i - j] == curBoard[i - j]:
                            different = False
                        else:
                            gg.move_right(screen)
                            j += 1
                            time.sleep(delay)

                    initial_pos = i - j + 1
                    break

            gg.flip_disks(screen)
            gg.display(screen)
            pygame.display.flip()

            prior = curBoard
            time.sleep(delay)

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

    def next_best_move_with_search(
        self,
        state: GameState,
        strategy: SearchStrategy,
        segment_size: int = 4,
        depth_limit: int = 20,
        max_cost=None,
        weight: float = 1.0,
        heuristic_func: Callable[[GameState], float] | None = None,
    ) -> GameState | None:
        if heuristic_func is None:
            heuristic_func = self.heuristic_misplaced

        _inner_ops = lambda s: self.generate_possible_moves(s, segment_size)

        def operators_func(s):
            return _inner_ops(s)

        goal_state_func = lambda s: s.is_goal()
        heuristic = lambda node: heuristic_func(node.state)

        args = [state, goal_state_func, operators_func]
        kwargs = {"max_cost": max_cost}

        if strategy in (
            SearchStrategy.DFS,
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

        if result is None:
            return self.next_best_move(
                state,
                segment_size=segment_size,
                heuristic_func=heuristic_func,
            )

        path = SearchAlgorithms.extract_path(result)

        if len(path) >= 2:
            return path[1]

        return None

    def next_best_move(
        self,
        state: GameState,
        segment_size: int = 4,
        heuristic_func: Callable[[GameState], float] | None = None,
    ) -> GameState | None:
        if heuristic_func is None:
            heuristic_func = self.heuristic_misplaced

        possible_moves = self.generate_possible_moves(state, segment_size)

        if not possible_moves:
            return None

        best_state = None
        best_score = float("inf")

        for next_state, _cost in possible_moves:
            score = heuristic_func(next_state)
            if score < best_score:
                best_score = score
                best_state = next_state

        return best_state


    # Utils
    def get_move_cost(self, move: int) -> int:
        _ = move
        return 1