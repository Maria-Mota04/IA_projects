from src.game.game import Game
from src.gui.menu import Menu
from src.states.board import Board
from src.states.game_state import GameState
from src.utils.file_manager import FileManager


def test_is_solvable_k2_instance_named_unsolvable_is_true() -> None:
    state, _, k = FileManager.load_instance("test_n8_k2_unsolvable")
    tiles = state.get_board().get_tiles()

    assert k == 2
    assert Board.is_solvable(tiles, k) is True


def test_is_solvable_even_n_odd_k_reports_unsolvable() -> None:
    tiles = [1, 2, 3, 4, 5, 6, 7, 8]

    assert Board.is_solvable(tiles, 3) is False


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
