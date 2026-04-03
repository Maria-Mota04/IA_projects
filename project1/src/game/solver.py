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
        pass

    def heuristic_inversions(self, state: GameState) -> int:
        pass

    def heuristic_distance(self, state: GameState) -> int:
        pass

    # Move generator
    def generate_possible_moves(self, segment_size: int) -> List[GameState]:
        moves = []
        for reverse_start in range(self.state.get_board().size):
            new_state = self._state.apply_move(reverse_start, segment_size)
            if new_state is not None:
                moves.append(new_state)
        return moves

    # Next best move
    def next_best_move(self) -> GameState:
        pass

    # Utils
    def get_move_cost(self, move: int) -> int:
        pass

    def reset_game(self) -> None:
        self._state.reset_state()
