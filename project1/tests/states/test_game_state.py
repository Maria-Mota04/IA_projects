from src.states.board import Board
from src.states.game_state import GameState


def test_apply_move_returns_new_state_and_keeps_original_unchanged():
    state = GameState(Board([1, 2, 3, 4, 5]))

    moved = state.apply_move(1, segment_size=4)

    assert moved is not None
    assert state.get_board().get_tiles() == [1, 2, 3, 4, 5]
    assert moved.get_board().get_tiles() == [1, 5, 4, 3, 2]


def test_apply_move_negative_returns_none():
    state = GameState(Board([1, 2, 3, 4]))

    assert state.apply_move(-1, segment_size=4) is None


def test_hash_and_equality_work_for_same_tiles():
    s1 = GameState(Board([1, 2, 3, 4]))
    s2 = GameState(Board([1, 2, 3, 4]))

    assert s1 == s2
    assert hash(s1) == hash(s2)


def test_is_goal_tracks_ordered_board():
    goal = GameState(Board([1, 2, 3, 4]))
    not_goal = GameState(Board([2, 1, 3, 4]))

    assert goal.is_goal() is True
    assert not_goal.is_goal() is False


def test_apply_rotate_mutates_state_board():
    state = GameState(Board([1, 2, 3, 4]))

    state.apply_rotate(1)

    assert state.get_board().get_tiles() == [4, 1, 2, 3]


def test_reset_state_returns_to_valid_permutation():
    state = GameState(Board([4, 3, 2, 1], segment_size=4))

    state.reset_state()

    assert sorted(state.get_board().get_tiles()) == [1, 2, 3, 4]


def test_str_and_ne_behaviors():
    s1 = GameState(Board([1, 2, 3, 4]))
    s2 = GameState(Board([1, 3, 2, 4]))

    assert str(s1).startswith("GameState(")
    assert (s1 != s2) is True
