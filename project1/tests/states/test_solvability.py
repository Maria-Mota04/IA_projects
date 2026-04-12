from src.game.game import Game
from src.gui.menu import Menu
from src.states.board import Board
from src.states.game_state import GameState
from src.utils.file_manager import FileManager


def test_is_solvable_k2_instance_named_unsolvable_is_true() -> None:
    tiles = [2, 1, 3, 4, 5, 6, 7, 8]
    assert Board.is_solvable(tiles, 2) is True


def test_is_solvable_even_n_odd_k_reports_unsolvable() -> None:
    tiles = [1, 2, 3, 4, 5, 6, 7, 8]

    assert Board.is_solvable(tiles, 3) is False


def test_is_solvable_k4_unsolvable_instance_is_false() -> None:
    state, _, k = FileManager.load_instance("test_n20_k4_unsolvable")
    tiles = state.get_board().get_tiles()

    assert k == 4
    assert Board.is_solvable(tiles, k) is False


def test_is_solvable_k_equals_n_false_positive_regression_even() -> None:
    tiles = [1, 2, 3, 4, 6, 5]
    assert Board.is_solvable(tiles, 6) is False


def test_is_solvable_k_equals_n_false_positive_regression_odd() -> None:
    tiles = [1, 2, 3, 4, 5, 7, 6]
    assert Board.is_solvable(tiles, 7) is False


def test_menu_uses_same_unsolvable_rule_as_board() -> None:
    menu = Menu(None)

    uns_game = Game(
        GameState(Board([1, 2, 3, 4, 5, 6, 7, 8], segment_size=3)),
        size=8,
        segment_size=3,
    )
    sol_game = Game(
        GameState(Board([2, 1, 3, 4, 5, 6, 7, 8], segment_size=2)),
        size=8,
        segment_size=2,
    )

    assert menu._is_current_game_solvable(uns_game) is False
    assert menu._is_current_game_solvable(sol_game) is True
