from src.algorithms.search_strategy import SearchStrategy
from src.game.game import Game
from src.game.game_modes import gameMode
from src.states.board import Board
from src.states.game_state import GameState


def test_make_move_updates_history_and_move_count():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)

    game.make_move(1)

    assert game.get_move_history() == [1]


def test_undo_move_restores_previous_state():
    initial = GameState(Board([1, 2, 3, 4]))
    game = Game(initial, size=4, segment_size=4)

    game.make_move(1)
    moved_tiles = game.get_board_state().get_board().get_tiles()
    game.undo_move()
    restored_tiles = game.get_board_state().get_board().get_tiles()

    assert moved_tiles != restored_tiles
    assert restored_tiles == [1, 2, 3, 4]


def test_game_solve_syncs_state_with_solver_result():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)

    result = game.solve(mode=gameMode.SEARCH_ALGORITHM, strategy=SearchStrategy.BFS)

    assert result is not None
    assert game.get_board_state().is_goal() is True


def test_game_basic_getters_and_setters():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)
    new_state = GameState(Board([2, 1, 3, 4]))

    game.set_board_state(new_state)

    assert game.get_board_size() == 4
    assert game.get_segment_size() == 4
    assert game.get_board_state() == new_state
    assert game.won() is False


def test_make_rotate_updates_history():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)

    game.make_rotate(1)

    assert game.get_move_history() == ["rotate(1)"]


def test_get_game_time_and_statistics_reset_flow():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)

    game.start_game()
    elapsed = game.get_game_time()
    game.reset_statistics()

    assert elapsed >= 0.0
    assert game.get_move_history() == []


def test_score_utility_methods():
    game = Game(GameState(Board([1, 2, 3, 4])), size=4, segment_size=4)

    game.increment_score()
    game.increment_score()
    game.decrement_score()

    assert game.get_score() == 1

    game.reset_score()

    assert game.get_score() == 0


def test_print_helpers_and_reset_game_do_not_crash():
    game = Game(GameState(Board([1, 2, 3, 4, 5, 6], segment_size=4)), size=6, segment_size=4)

    game.print_board()
    game.print_scores()
    game.reset_game()

    assert sorted(game.get_board_state().get_board().get_tiles()) == [1, 2, 3, 4, 5, 6]
