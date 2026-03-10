from __future__ import annotations
import time

from project1.src.states.game_state import GameState
from project1.src.utils.game_stats import GameStats


class Game:
    def __init__(self, size: int, initial_state: GameState):
        self._n = size
        self._state = initial_state
        self._game_stats = GameStats()
        self._start_time = None

    def get_board_size(self) -> int:
        return self._n

    def get_board_state(self) -> GameState:
        return self._state

    def set_board_state(self, state: GameState) -> None:
        self._state = state

    def make_move(self, move: int) -> None:
        if self._start_time is None:
            self._start_time = time.time()

        self._state = self._state.apply_move(move)
        self._game_stats.moves += 1
        self._game_stats.history.append(move)

    def won(self) -> bool:
        return self._state.is_goal()

    def start_game(self):
        self._start_time = time.time()
        self._game_stats = GameStats()

    def solve(self):
        pass

    def get_game_time(self):
        if self._start_time is None:
            return self._game_stats.time_elapsed

        self._game_stats.time_elapsed = time.time() - self._start_time
        return self._game_stats.time_elapsed

    def get_move_history(self):
        return self._game_stats.history

    def print_board(self) -> None:
        self._state.print_board()

    def show_solution(self):
        pass

    def undo_move(self):
        pass

    def get_score(self):
        return self._game_stats.score

    def increment_score(self) -> None:
        self._game_stats.score += 1

    def reset_score(self) -> None:
        self._game_stats.score = 0

    def decrement_score(self) -> None:
        self._game_stats.score -= 1

    def print_scores(self) -> None:
        self._game_stats.print()
