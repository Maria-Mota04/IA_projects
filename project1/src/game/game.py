from __future__ import annotations
import time

from src.states.game_state import GameState
from src.utils.game_stats import GameStats
from src.algorithms.search_strategy import SearchStrategy
from src.states.game_state import GameState
from src.utils.game_stats import GameStats
from .game_modes import gameMode
from .solver import Solver


class Game:

    # Core functions
    def __init__(
        self,
        initial_state: GameState,
        size: int = 20,
        segment_size: int = 4,
    ):
        self._n = size
        self._segment_size = segment_size
        self._solver = Solver(initial_state)
        self._game_stats = GameStats()
        self._start_time = None

    def get_board_size(self) -> int:
        return self._n

    def get_segment_size(self) -> int:
        return self._segment_size

    def get_board_state(self) -> GameState:
        return self._solver.get_state()

    def set_board_state(self, state: GameState) -> None:
        self._solver.set_state(state)

    def won(self) -> bool:
        return self._solver.get_state().is_goal()

    # Move Operations

    def make_move(self, move: int) -> None:
        if self._start_time is None:
            self._start_time = time.time()

        self._solver.set_state(
            self._solver.get_state().apply_move(move, self._segment_size)
        )
        self._game_stats.moves += 1
        self._game_stats.history.append(move)

    def make_rotate(self, steps: int = 1) -> None:
        if self._start_time is None:
            self._start_time = time.time()

        self._solver.set_state(self._solver.get_state().apply_rotate(steps))
        self._game_stats.history.append(f"rotate({steps})")

    def start_game(self) -> None:
        self._start_time = time.time()
        self._game_stats = GameStats()

    def undo_move(self) -> None:
        parent = self._solver.get_state()._

    # Utils

    def get_game_time(self) -> float:
        if self._start_time is None:
            return self._game_stats.time_elapsed

        self._game_stats.time_elapsed = time.time() - self._start_time
        return self._game_stats.time_elapsed

    def get_move_history(self) -> list:
        return self._game_stats.history

    def print_board(self) -> None:
        self._solver.get_state().print_board()

    def show_solution(self) -> None:
        pass

    def reset_statistics(self) -> None:
        self._game_stats.reset()

    def reset_game(self) -> None:
        self._solver.reset_game()

    # Score Utils

    def get_score(self) -> int:
        return self._game_stats.score

    def increment_score(self) -> None:
        self._game_stats.score += 1

    def reset_score(self) -> None:
        self._game_stats.score = 0

    def decrement_score(self) -> None:
        self._game_stats.score -= 1

    def print_scores(self) -> None:
        self._game_stats.print()

    # Solver

    def solve(
        self,
        mode: gameMode = gameMode.SEARCH_ALGORITHM,
        strategy: SearchStrategy = SearchStrategy.BFS,
        **kwargs,
    ) -> object:
        result = self._solver.solve(
            mode=mode,
            strategy=strategy,
            segment_size=self._segment_size,
            **kwargs,
        )

        if mode == gameMode.SEARCH_ALGORITHM and result is not None:
            self._solver.set_state(result.state)

        return result
