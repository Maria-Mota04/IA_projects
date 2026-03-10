from typing import List
from __future__ import annotations

from states.board import Board


class GameState:
    def __init__(self, board: Board):
        self._board = board

    def get_board(self) -> Board:
        return self._board

    def set_board(self, board: Board) -> None:
        self._board = board

    def is_goal(self) -> bool:
        return self._board.isOrdered()

    def get_possible_moves(self) -> List[Board]:
        pass

    def apply_move(self) -> GameState:
        pass

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
