import math
import time
from typing import Callable, List
import pygame

from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.game.game import *
from src.game.pdb_heuristic import pattern_state_from_positions, build_patterns, generate_pdb
from src.gui.controls_helper import ControlHelper
from src.gui.game_graphics import *
from src.states.board import Board
from src.states.game_state import GameState
from src.gui.hint_settings import HintSettings
from .game_modes import gameMode

class Solver:
    def __init__(self, n=20, k=4, group_size=5):
        self._patterns = build_patterns(n, group_size)
        print(f"[PDB] A gerar PDB para {group_size} peças... (n={n}, k={k})")
        self._pdb_5 = generate_pdb(n, k, group_size)
        print("[PDB] Gerada com sucesso!")

        self._hint_strategy = SearchStrategy.A_STAR
        self._hint_heuristic_name = "pdb"
        self._hint_config = {
            "depth_limit": 20,
            "max_cost": None,
            "weight": 1.0,
        }

    def strategy_uses_heuristic(self, strategy: SearchStrategy) -> bool:
        return strategy in (SearchStrategy.GREEDY, SearchStrategy.A_STAR, SearchStrategy.WEIGHTED_A_STAR)

    def strategy_uses_depth_limit(self, strategy: SearchStrategy) -> bool:
        return strategy in (SearchStrategy.DFS, SearchStrategy.DFS_LIMITED, SearchStrategy.ITERATIVE_DEEPENING)

    def strategy_uses_weight(self, strategy: SearchStrategy) -> bool:
        return strategy == SearchStrategy.WEIGHTED_A_STAR

    def solve(self, game: Game, screen, mode: gameMode, strategy: SearchStrategy = SearchStrategy.BFS, segment_size: int = 4, depth_limit: int = 20, max_cost=None, weight: float = 1.0, heuristic_func: Callable[[object], float] | None = None) -> object:
        if heuristic_func is None:
            heuristic_func = self.heuristic_misplaced

        if mode == gameMode.NORMAL_GAME:
            game_running = True
            gg = GameGraphics(game)
            font = pygame.font.SysFont("arial", 40)
            
            quit_button = pygame.Rect(30, 30, 85, 50)
            quit_text = font.render("Quit", True, (255, 255, 255))
            settings_button_hint = pygame.Rect(40, 510, 200, 50)
            settings_text = font.render("Hint Settings", True, (255, 255, 255))
            hint_button = pygame.Rect(500, 30, 120, 50)
            hint_text = font.render("Hint", True, (255, 255, 255))
            undo_button = pygame.Rect(650, 30, 120, 50)
            undo_text = font.render("Undo", True, (255, 255, 255))
            control_helper_menu_button = pygame.Rect(650, 500, 50, 50)
            control_helper_menu_text = font.render("?", True, (255, 255, 255))

            BG = (60, 25, 60)
            hint_highlight = None

            while game_running:
                screen.fill(BG)
                gg.display(screen, highlight_indices=hint_highlight)
                center_circle = gg.get_center_circle()
                radius_circle = gg.get_radius_circle()
                mouse = pygame.mouse.get_pos()

                for btn, txt, pos in [(quit_button, quit_text, (40, 32)), (settings_button_hint, settings_text, (45, 515)), (hint_button, hint_text, (520, 32)), (undo_button, undo_text, (660, 32)), (control_helper_menu_button, control_helper_menu_text, (660, 502))]:
                    color = (170, 170, 170) if btn.collidepoint(mouse) else (100, 100, 100)
                    pygame.draw.rect(screen, color, btn)
                    screen.blit(txt, pos)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: return -1
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
                        dist = math.sqrt((mouse[0]-center_circle[0])**2 + (mouse[1]-center_circle[1])**2)
                        if dist <= radius_circle:
                            game.make_move(1)
                            gg.flip_disks(screen)
                            hint_highlight = None
                        elif quit_button.collidepoint(mouse): return 1
                        elif undo_button.collidepoint(mouse):
                            game.undo_move()
                            gg.update(game)
                            hint_highlight = None
                        elif settings_button_hint.collidepoint(mouse):
                            if HintSettings(self).run(screen) == -1: return -1
                            gg.update(game)
                        elif hint_button.collidepoint(mouse):
                            print(f"[UI] Hint solicitada com heurística: {self._hint_heuristic_name}")
                            hinted_state = self.next_best_move_with_search(game.get_board_state(), strategy=self._hint_strategy, segment_size=game.get_segment_size(), depth_limit=self._hint_config["depth_limit"], max_cost=self._hint_config["max_cost"], weight=self._hint_config["weight"], heuristic_func=self.get_heuristic_by_name(self._hint_heuristic_name))
                            if hinted_state:
                                c_tiles = game.get_board_state().get_board().get_tiles()
                                h_tiles = hinted_state.get_board().get_tiles()
                                hint_highlight = {i for i in range(len(c_tiles)) if c_tiles[i] != h_tiles[i]}
                            else: hint_highlight = None
                            gg.update(game)
                        elif control_helper_menu_button.collidepoint(mouse):
                            ControlHelper(screen).run()
                            gg.update(game)
                pygame.display.flip()
                if game.won(): return 0

        if mode != gameMode.SEARCH_ALGORITHM: raise ValueError(f"Unsupported game mode: {mode}")

        nodes_explored = [0]
        def operators_func(state):
            nodes_explored[0] += 1
            return self.generate_possible_moves(state, segment_size)

        goal_state_func = lambda state: state.is_goal()
        heuristic = (lambda node: heuristic_func(node.state)) if heuristic_func else (lambda node: self.heuristic_misplaced(node.state))
        args = [game.get_board_state(), goal_state_func, operators_func]
        kwargs = {"max_cost": max_cost}

        if self.strategy_uses_depth_limit(strategy): args.append(depth_limit)
        elif self.strategy_uses_heuristic(strategy):
            args.append(heuristic)
            if strategy == SearchStrategy.WEIGHTED_A_STAR: kwargs["weight"] = weight

        t0 = time.time()
        result = SearchAlgorithms.search(strategy, *args, **kwargs)
        elapsed = time.time() - t0
        if result is None: return None, {"nodes": nodes_explored[0], "time": elapsed, "depth": 0, "found": False}
        path = SearchAlgorithms.extract_path(result)
        return path, {"nodes": nodes_explored[0], "time": elapsed, "depth": len(path) - 1, "found": True}

    def has_pdb(self) -> bool: return bool(self._pdb_5) and bool(self._patterns)

    def get_heuristic_by_name(self, heuristic_name: str) -> Callable[[GameState], float]:
        mapping = {"misplaced": self.heuristic_misplaced, "breakpoints": self.heuristic_breakpoints, "distance": self.heuristic_distance, "pdb": self.heuristic_pdb if self.has_pdb() else self.heuristic_misplaced}
        return mapping.get(heuristic_name, self.heuristic_misplaced)

    def heuristic_misplaced(self, state: GameState) -> int:
        tiles = state.get_board().get_tiles()
        n, k = len(tiles), state.get_board().get_segment_size()
        start = tiles.index(1)
        misplaced = sum(1 for i in range(n) if tiles[(start + i) % n] != i + 1)
        return math.ceil(misplaced / k) if k > 0 else misplaced

    def heuristic_breakpoints(self, state: GameState) -> int:
        tiles = state.get_board().get_tiles()
        n, k = len(tiles), state.get_board().get_segment_size()
        breakpoints = sum(1 for i in range(n) if tiles[(i + 1) % n] != (1 if tiles[i] == n else tiles[i] + 1))
        return math.ceil(breakpoints / k) if k > 0 else breakpoints

    def heuristic_distance(self, state: GameState) -> int:
        tiles = state.get_board().get_tiles()
        n, k = len(tiles), state.get_board().get_segment_size()
        if k <= 1: return 0
        start, max_dist = tiles.index(1), 0
        for i, tile in enumerate(tiles):
            goal_pos = (start + (tile - 1)) % n
            diff = abs(i - goal_pos)
            max_dist = max(max_dist, min(diff, n - diff))
        return math.ceil(max_dist / (k - 1))

    def heuristic_pdb(self, state: GameState) -> int:
        tiles = state.get_board().get_tiles()
        n = len(tiles)
        pos_map = {tile: i for i, tile in enumerate(tiles)}
        max_h = 0
        for pattern in self._patterns:
            key = pattern_state_from_positions(pos_map, pattern, n)
            h = self._pdb_5.get(key, 0)
            if h > max_h: max_h = h
        return max_h

    def generate_possible_moves(self, state: GameState, segment_size: int) -> List[tuple[GameState, int]]:
        moves = []
        for start in range(state.get_board().size()):
            new_s = state.apply_move(start, segment_size)
            if new_s: moves.append((new_s, 1))
        return moves

    def next_best_move_with_search(self, state, strategy, segment_size=4, depth_limit=20, max_cost=None, weight=1.0, heuristic_func=None):
        h_func = heuristic_func or self.heuristic_misplaced
        ops = lambda s: self.generate_possible_moves(s, segment_size)
        goal = lambda s: s.is_goal()
        args = [state, goal, ops]
        kwargs = {"max_cost": max_cost}
        if self.strategy_uses_depth_limit(strategy): args.append(depth_limit)
        elif self.strategy_uses_heuristic(strategy):
            args.append(lambda node: h_func(node.state))
            if strategy == SearchStrategy.WEIGHTED_A_STAR: kwargs["weight"] = weight
        result = SearchAlgorithms.search(strategy, *args, **kwargs)
        if result:
            path = SearchAlgorithms.extract_path(result)
            if len(path) >= 2: return path[1]
        print("[SOLVER] Busca falhou ou completa, a usar fallback Greedy 1-step")
        return self.next_best_move(state, segment_size, h_func)

    def next_best_move(self, state, segment_size=4, heuristic_func=None):
        h_func = heuristic_func or self.heuristic_misplaced
        moves = self.generate_possible_moves(state, segment_size)
        if not moves: return None
        return min(moves, key=lambda m: h_func(m[0]))[0]