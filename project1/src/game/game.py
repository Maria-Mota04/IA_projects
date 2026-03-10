from __future__ import annotations
from states.gameState import GameState


class Game:
    def __init__(self, size: int, initial_state: GameState):
        self._n = size
        self._state = initial_state

    def get_board_size(self) -> int:
        return self._n

    def get_board_state(self) -> GameState:
        return self._state

    def set_board_state(self, state: GameState) -> None:
        self._state = state

    def make_move(self, move: int) -> None:
        self._state = self._state.apply_move(move)

    def won(self) -> bool:
        return self._state.is_goal()

    def start_game(self):
        pass

    def solve(self):
        pass

    def get_game_time(self):
        pass

    def get_move_history(self):
        pass

    def print_board(self):
        pass

    def show_solution(self):
        pass

    def undo_move(self):
        pass

    def get_score(self):
        pass
