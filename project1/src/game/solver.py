from typing import List
from project1.src.states.game_state import GameState


class Solver:

    # Core functions
    def __init__(self, initial_state: GameState):
        self._state = initial_state

    def get_state(self):
        return self._state

    def set_state(self, state: GameState) -> None:
        self._state = state

    def solve():
        pass

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
