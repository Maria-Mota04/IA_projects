import math
from typing import Callable, List
from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy
from src.states.board import Board
from src.states.game_state import GameState
from .game_modes import gameMode


class Solver:

    # Core functions
    def __init__(self, initial_state: GameState) -> None:
        self._state = initial_state

    def get_state(self) -> GameState:
        return self._state

    def set_state(self, state: GameState) -> None:
        self._state = state

    def solve(
        self,
        mode: gameMode,
        strategy: SearchStrategy = SearchStrategy.BFS,
        segment_size: int = 4,
        depth_limit: int = 20,
        max_cost=None,
        weight: float = 1.0,
        heuristic_func: Callable[[object], float] | None = None,
    ) -> object:
        if mode == gameMode.NORMAL_GAME:
            pass  # TODO

        if mode != gameMode.SEARCH_ALGORITHM:
            raise ValueError(f"Unsupported game mode: {mode}")

        goal_state_func = lambda state: state.is_goal()
        operators_func = lambda state: self.generate_possible_moves(state, segment_size)

        heuristic = heuristic_func
        if heuristic is None:
            heuristic = lambda node: self.heuristic_misplaced(node.state)

        args = [self._state, goal_state_func, operators_func]
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

        return SearchAlgorithms.search(strategy, *args, **kwargs)

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

        return math.ceil(misplaced / k)
        

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

        return math.ceil(breakpoints / k)

    def heuristic_distance(self, state: GameState) -> int:
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

    def reset_game(self) -> None:
        self._state.reset_state()
