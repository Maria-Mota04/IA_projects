from src.algorithms.search_strategy import SearchStrategy
from src.game.game_modes import gameMode
from src.game.solver import Solver
from src.states.board import Board
from src.states.game_state import GameState
import pytest


def test_get_move_cost_is_unitary_for_any_move_id():
    solver = Solver(GameState(Board([1, 2, 3, 4])))

    assert solver.get_move_cost(0) == 1
    assert solver.get_move_cost(10) == 1
    assert solver.get_move_cost(-1) == 1


def test_generate_possible_moves_returns_state_cost_pairs():
    solver = Solver(GameState(Board([1, 2, 3, 4])))
    state = solver.get_state()

    moves = solver.generate_possible_moves(state, segment_size=4)

    assert len(moves) == 5  # 4 reversals + 1 rotation
    assert all(isinstance(item, tuple) and len(item) == 2 for item in moves)
    assert all(cost == 1 for _, cost in moves)


def test_solve_search_algorithm_returns_goal_node_when_already_solved():
    solver = Solver(GameState(Board([1, 2, 3, 4])))

    result = solver.solve(
        mode=gameMode.SEARCH_ALGORITHM,
        strategy=SearchStrategy.BFS,
        segment_size=4,
    )

    assert result is not None
    assert result.state.is_goal() is True


def test_solve_normal_game_mode_returns_current_state():
    solver = Solver(GameState(Board([1, 2, 3, 4])))

    result = solver.solve(mode=gameMode.NORMAL_GAME)

    assert result == solver.get_state()


def test_solve_raises_for_unsupported_mode():
    solver = Solver(GameState(Board([1, 2, 3, 4])))

    with pytest.raises(ValueError):
        solver.solve(mode=99)


def test_unimplemented_heuristics_and_next_best_move_return_none():
    solver = Solver(GameState(Board([1, 2, 3, 4])))
    state = solver.get_state()

    assert solver.heuristic_misplaced(state) is None
    assert solver.heuristic_inversions(state) is None
    assert solver.heuristic_distance(state) is None
    assert solver.next_best_move() is None


def test_reset_game_replaces_state_with_valid_permutation():
    solver = Solver(GameState(Board([1, 2, 3, 4, 5, 6], segment_size=4)))

    solver.reset_game()
    tiles = solver.get_state().get_board().get_tiles()

    assert sorted(tiles) == [1, 2, 3, 4, 5, 6]
