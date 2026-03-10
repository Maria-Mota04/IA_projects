from __future__ import annotations
from typing import List

from project1.src.states.board import Board


class GameState:
    def __init__(self, board: Board):
        self._board = board

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

    def apply_move(self, move: int, segment_size: int = 4) -> GameState:
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

    def print_board(self) -> None:
        self._board.print()
