from src.states.board import Board


def test_is_ordered_true_for_goal_sequence():
    board = Board([1, 2, 3, 4, 5])
    assert board.is_ordered() is True


def test_reverse_segment_changes_tiles_as_expected():
    board = Board([1, 2, 3, 4, 5])
    board.reverse_segment(start=1, segment_size=4)

    assert board.get_tiles() == [1, 5, 4, 3, 2]


def test_rotate_wheel_right_by_one():
    board = Board([1, 2, 3, 4])
    board.rotate_wheel(1)

    assert board.get_tiles() == [4, 1, 2, 3]


def test_reset_board_keeps_solvable_for_even_segment_size():
    board = Board([1, 2, 3, 4, 5, 6], segment_size=4)
    board.reset_board()

    assert Board.is_solvable(board.get_tiles(), segment_size=4) is True


def test_board_accessors_and_mutators():
    board = Board([1, 2, 3, 4])

    assert board.size() == 4
    assert board.at(2) == 3

    board.set(2, 9)
    assert board.at(2) == 9

    board.set_tiles([4, 3, 2, 1])
    assert board.get_tiles() == [4, 3, 2, 1]


def test_board_print_and_odd_k_solvable_rule():
    board = Board([1, 2, 3, 4])
    board.print()

    assert Board.is_solvable([2, 1, 3, 4], segment_size=3) is True
