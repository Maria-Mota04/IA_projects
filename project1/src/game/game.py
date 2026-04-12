from __future__ import annotations
import time

from src.states.game_state import GameState
from src.utils.game_stats import GameStats


class Game:

    # Core functions
    def __init__(
        self,
        state: GameState,
        size: int = 20,
        segment_size: int = 4,
    ):
        """
        @brief Initialize a game session with state and board configuration.

        @param state Initial game state.
        @param size Board size.
        @param segment_size Segment length used by move operations.
        """
        self._n = size
        self._segment_size = segment_size
        self.state = state
        self._last_state = None
        self._game_stats = GameStats()
        self._start_time = None

    def get_segment_size(self) -> int:
        """@brief Return the segment size used for reversing moves."""
        return self._segment_size

    def get_board_state(self) -> GameState:
        """@brief Return the current board state."""
        return self.state

    def set_board_state(self, state: GameState) -> None:
        """
        @brief Replace the current board state.

        @param state New game state.
        """
        self.state = state

    def won(self) -> bool:
        """@brief Check whether the current state is a goal state."""
        return self.state.is_goal()

    def start_game(self) -> None:
        """@brief Start timing and reset game statistics."""
        self._start_time = time.time()
        self._game_stats = GameStats()

    # Move Operations

    def make_move(self, move: int) -> None:
        """
        @brief Apply a reverse-segment move and register it in history.

        @param move Start index for the segment reversal.
        """
        if self._start_time is None:
            self._start_time = time.time()

        self._last_state = self.state
        self.state = self.state.apply_move(move, self._segment_size)
        self._game_stats.moves += 1
        self._game_stats.history.append(move)

    def make_rotate(self, steps: int = 1) -> None:
        """
        @brief Rotate the wheel and register the operation in history.

        @param steps Number of rotation steps.
        """
        if self._start_time is None:
            self._start_time = time.time()

        self._last_state = self.state
        self.state = self.state.apply_rotate(steps)
        self._game_stats.history.append(f"rotate({steps})")

    def undo_move(self) -> None:
        """@brief Restore the previous state when available."""
        if self._last_state is not None:
            self.state = self._last_state
            self._last_state = None

    # Utils

    def get_game_time(self) -> float:
        """
        @brief Return elapsed game time in seconds.

        @return Elapsed time in seconds.
        """
        if self._start_time is None:
            return getattr(self._game_stats, "time_elapsed", 0.0)

        self._game_stats.time_elapsed = time.time() - self._start_time
        return self._game_stats.time_elapsed

    def finalize_game_time(self) -> float:
        """
        @brief Freeze elapsed time so it no longer increases after game end.

        @return Final elapsed time in seconds.
        """
        final_time = self.get_game_time()
        self._start_time = None
        return final_time

    def print_board(self) -> None:
        """@brief Print the current board to standard output."""
        self.state.print_board()
