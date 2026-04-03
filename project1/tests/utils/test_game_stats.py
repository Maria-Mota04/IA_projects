from src.utils.game_stats import GameStats


def test_reset_restores_default_values():
    stats = GameStats()
    stats.score = 7
    stats.moves = 5
    stats.time_elapsed = 3.2
    stats.states_explored = 100
    stats.max_memory = 2048
    stats.solution_depth = 12
    stats.history = [1, 2, 3]

    stats.reset()

    assert stats.score == 0
    assert stats.moves == 0
    assert stats.time_elapsed == 0.0
    assert stats.states_explored == 0
    assert stats.max_memory == 0
    assert stats.solution_depth == 0
    assert stats.history == []


def test_print_outputs_summary(capsys):
    stats = GameStats()

    stats.print()
    captured = capsys.readouterr()

    assert "Game Stats" in captured.out
