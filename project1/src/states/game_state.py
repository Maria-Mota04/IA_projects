from __future__ import annotations
from typing import Callable, List

from src.states.board import Board


class GameState:

    # Core functions
    def __init__(self, board: Board, move_history=None) -> None:
        """
        @brief Create a game state from a board and optional move history.

        @param board Board object for this state.
        @param move_history Optional sequence of previous moves.
        """
        self._board = board
        self._move_history = move_history or []

    def get_board(self) -> Board:
        """@brief Return the board associated with this state."""
        return self._board

    def is_goal(self) -> bool:
        """@brief Check whether the state is solved."""
        return self._board.is_ordered()

    # Move application

    def reverse_segment(self, start: int, segment_size: int) -> None:
        """
        @brief Apply a segment reversal on this state's board.

        @param start Segment start index.
        @param segment_size Segment length.
        """
        if segment_size <= 1:
            return

        self._board.reverse_segment(start, segment_size)

    def rotate_wheel(self, steps: int = 1) -> None:
        """
        @brief Rotate this state's board.

        @param steps Number of steps to rotate.
        """
        self._board.rotate_wheel(steps)

    @staticmethod
    def move(func) -> Callable:
        """
        @brief Decorator that applies a move on a copied state.

        @param func Move function operating on a GameState instance.
        @return Wrapped function returning a new state or None.
        """

        def wrapper(self, *args, **kwargs) -> GameState | None:
            """
            @brief Execute decorated move on a cloned state.

            @return New state if move is valid; otherwise None.
            """
            new_state = GameState(Board(self._board.get_tiles()))

            value = func(new_state, *args, **kwargs)
            if value:
                return new_state
            else:
                return None

        return wrapper

    @move
    def apply_move(self, move: int, segment_size: int = 4) -> GameState:
        """
        @brief Return a new state with the selected move applied.

        @param move Start index for segment reversal.
        @param segment_size Segment length.
        @return Updated state or None if move is invalid.
        """
        if move < 0:
            return None

        self.reverse_segment(move, segment_size)
        return self

    @move
    def apply_rotate(self, steps: int = 1) -> GameState:
        """
        @brief Return a new state after a wheel rotation.

        @param steps Number of rotation steps.
        @return Updated state.
        """
        self.rotate_wheel(steps)
        return self

    def __eq__(self, other: object) -> bool:
        """@brief Compare two states by tile arrangement."""
        if not isinstance(other, GameState):
            return NotImplemented
        return self._board.get_tiles() == other._board.get_tiles()

    def __ne__(self, other: object) -> bool:
        """@brief Compare two states for inequality."""
        if not isinstance(other, GameState):
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self) -> int:
        """@brief Return a hash based on tile values."""
        return hash(tuple(self._board.get_tiles()))

    def __str__(self) -> str:
        """@brief Return a readable string representation of the state."""
        return "GameState(" + " ".join(str(t) for t in self._board.get_tiles()) + ")"

    def print_board(self) -> None:
        """@brief Print this state's board."""
        self._board.print()
