from __future__ import annotations
from typing import List

from project1.src.states.board import Board


class GameState:
    def __init__(self, board: Board, move_history=None):
        self._board = board
        self._move_history = move_history or []

    def get_board(self) -> Board:
        return self._board

    def set_board(self, board: Board) -> None:
        self._board = board

    def is_goal(self) -> bool:
        return self._board.is_ordered()

    def get_possible_moves(self) -> List[Board]:
        pass

    def reverse_segment(self, start: int, segment_size: int) -> None:
        if segment_size <= 1:
            return

        end = min(start + segment_size - 1, self._board.size() - 1)
        self._board.reverse_segment(start, end)

    @staticmethod
    def move(func):

        def wrapper(self, move: int, segment_size: int = 4):
            new_state = GameState(self._board)

            value = func(new_state)
            if value:
                new_state._move_history.append(move)
                return new_state
            else:
                return None

        return wrapper

    @move
    def apply_move(self, move: int, segment_size: int = 4) -> GameState:
        if move < 0:
            return None

        self.reverse_segment(move, segment_size)
        return self

    def get_move_cost(move: int):
        pass

    def heuristic_misplaced():
        pass

    def heuristic_inversions():
        pass

    def heuristic_distance():
        pass

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return NotImplemented
        return self._board.get_tiles() == other._board.get_tiles()

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, GameState):
            return NotImplemented
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(tuple(self._board.get_tiles()))

    def __str__(self) -> str:
        return "GameState(" + " ".join(str(t) for t in self._board.get_tiles()) + ")"

    def print_board(self) -> None:
        self._board.print()
