import sys
import os
import tempfile
import pytest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from src.utils.file_manager import FileManager, _INSTANCES_DIR, _RESULTS_DIR
from src.utils.game_stats import GameStats
from src.utils.game_timer import GameTimer
from src.states.board import Board
from src.states.game_state import GameState


def _make_state(tiles: list[int], k: int = 4) -> GameState:
    return GameState(Board(tiles, segment_size=k))


def _write_instance(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


class TestLoadInstance:

    def test_loads_tiles_correctly(self, tmp_path):
        f = tmp_path / "puzzle.txt"
        f.write_text("8 4\n3 1 4 2 7 5 6 8\n")
        state, n, k = FileManager.load_instance(str(f))
        assert n == 8
        assert k == 4
        assert state.get_board().get_tiles() == [3, 1, 4, 2, 7, 5, 6, 8]

    def test_ignores_blank_lines(self, tmp_path):
        f = tmp_path / "puzzle.txt"
        f.write_text("\n8 4\n\n3 1 4 2 7 5 6 8\n\n")
        state, n, k = FileManager.load_instance(str(f))
        assert n == 8
        assert state.get_board().get_tiles() == [3, 1, 4, 2, 7, 5, 6, 8]

    def test_already_solved_board(self, tmp_path):
        f = tmp_path / "solved.txt"
        f.write_text("5 4\n1 2 3 4 5\n")
        state, n, k = FileManager.load_instance(str(f))
        assert state.is_goal()

    def test_file_not_found_raises(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            FileManager.load_instance(str(tmp_path / "missing.txt"))

    def test_too_few_lines_raises(self, tmp_path):
        f = tmp_path / "bad.txt"
        f.write_text("8 4\n")
        with pytest.raises(ValueError):
            FileManager.load_instance(str(f))

    def test_wrong_header_raises(self, tmp_path):
        f = tmp_path / "bad.txt"
        f.write_text("8\n1 2 3 4 5 6 7 8\n")
        with pytest.raises(ValueError):
            FileManager.load_instance(str(f))

    def test_tile_count_mismatch_raises(self, tmp_path):
        f = tmp_path / "bad.txt"
        f.write_text("8 4\n1 2 3\n")
        with pytest.raises(ValueError):
            FileManager.load_instance(str(f))


class TestResolvePath:

    def test_bare_name_goes_to_instances_dir(self):
        resolved = FileManager._resolve_path("input", _INSTANCES_DIR)
        assert resolved == _INSTANCES_DIR / "input.txt"

    def test_bare_name_goes_to_results_dir(self):
        resolved = FileManager._resolve_path("output", _RESULTS_DIR)
        assert resolved == _RESULTS_DIR / "output.txt"

    def test_no_extension_gets_txt(self):
        resolved = FileManager._resolve_path("puzzle", _INSTANCES_DIR)
        assert resolved.suffix == ".txt"

    def test_existing_extension_kept(self):
        resolved = FileManager._resolve_path("puzzle.txt", _INSTANCES_DIR)
        assert resolved.suffix == ".txt"
        assert resolved == _INSTANCES_DIR / "puzzle.txt"

    def test_absolute_path_unchanged(self, tmp_path):
        abs_path = str(tmp_path / "my_file.txt")
        resolved = FileManager._resolve_path(abs_path, _INSTANCES_DIR)
        assert resolved == Path(abs_path)

    def test_relative_subpath_unchanged(self):
        resolved = FileManager._resolve_path("sub/puzzle.txt", _INSTANCES_DIR)
        assert resolved == Path("sub/puzzle.txt")


class TestLoadInstanceDefaultDir:

    def test_bare_name_loads_from_instances_dir(self):
        # instances/input.txt must exist with valid content
        state, n, k = FileManager.load_instance("input")
        assert n == 8
        assert k == 4
        assert state.get_board().get_tiles() == [3, 1, 4, 2, 7, 5, 6, 8]

    def test_bare_name_without_extension(self):
        state, n, k = FileManager.load_instance("input")
        assert n > 0


class TestSaveResultDefaultDir:

    def _default_stats(self) -> GameStats:
        stats = GameStats()
        stats.moves = 3
        stats.solution_depth = 3
        stats.states_explored = 10
        stats.max_memory = 50
        return stats

    def test_bare_name_saves_to_results_dir(self):
        FileManager.save_result(
            "test_output", "BFS", self._default_stats(), solved=True
        )
        out = _RESULTS_DIR / "test_output.txt"
        assert out.exists()
        out.unlink()


class TestSaveResult:

    def _default_stats(self) -> GameStats:
        stats = GameStats()
        stats.moves = 5
        stats.solution_depth = 5
        stats.states_explored = 42
        stats.max_memory = 100
        return stats

    def test_creates_file(self, tmp_path):
        out = str(tmp_path / "result.txt")
        FileManager.save_result(out, "BFS", self._default_stats(), solved=True)
        assert os.path.exists(out)

    def test_creates_parent_dirs(self, tmp_path):
        out = str(tmp_path / "nested" / "dir" / "result.txt")
        FileManager.save_result(out, "DFS", self._default_stats(), solved=False)
        assert os.path.exists(out)

    def test_content_fields_present(self, tmp_path):
        out = str(tmp_path / "result.txt")
        FileManager.save_result(
            out,
            "A_STAR",
            self._default_stats(),
            solved=True,
            heuristic_name="misplaced",
        )
        content = open(out).read()
        assert "Algorithm:        A_STAR" in content
        assert "Heuristic:        misplaced" in content
        assert "Solved:           True" in content
        assert "Moves:            5" in content
        assert "States explored:  42" in content
        assert "Time (s):" in content

    def test_no_heuristic_writes_none(self, tmp_path):
        out = str(tmp_path / "result.txt")
        FileManager.save_result(out, "BFS", self._default_stats(), solved=True)
        assert "Heuristic:        None" in open(out).read()

    def test_solution_path_written(self, tmp_path):
        out = str(tmp_path / "result.txt")
        path = [_make_state([3, 1, 2]), _make_state([1, 2, 3])]
        FileManager.save_result(
            out, "BFS", self._default_stats(), solved=True, solution_path=path
        )
        content = open(out).read()
        assert "Solution path:" in content
        assert "3 1 2" in content
        assert "1 2 3" in content

    def test_no_solution_path_writes_none(self, tmp_path):
        out = str(tmp_path / "result.txt")
        FileManager.save_result(out, "BFS", self._default_stats(), solved=False)
        assert "Solution path:    None" in open(out).read()

    def test_unsolved_flag(self, tmp_path):
        out = str(tmp_path / "result.txt")
        FileManager.save_result(out, "BFS", self._default_stats(), solved=False)
        assert "Solved:           False" in open(out).read()


class TestGameTimer:

    def test_get_time_increases(self):
        import time
        timer = GameTimer()
        t1 = timer.get_time()
        time.sleep(0.05)
        t2 = timer.get_time()
        assert t2 > t1

    def test_initial_time_near_zero(self):
        timer = GameTimer()
        assert timer.get_time() < 1.0

    def test_pause_freezes_time(self):
        import time
        timer = GameTimer()
        time.sleep(0.02)
        timer.pause()
        frozen = timer.get_time()
        time.sleep(0.05)
        assert timer.get_time() == frozen

    def test_resume_continues_time(self):
        import time
        timer = GameTimer()
        time.sleep(0.02)
        timer.pause()
        frozen = timer.get_time()
        time.sleep(0.05)
        timer.resume()
        time.sleep(0.02)
        assert timer.get_time() > frozen

    def test_paused_time_not_counted(self):
        import time
        timer = GameTimer()
        time.sleep(0.02)
        timer.pause()
        time.sleep(0.1)   # this should not count
        timer.resume()
        elapsed = timer.get_time()
        assert elapsed < 0.08  # well under 0.12 (0.02 running + 0.1 paused)

    def test_reset_restarts_clock(self):
        import time
        timer = GameTimer()
        time.sleep(0.05)
        timer.reset()
        assert timer.get_time() < 0.05

    def test_reset_clears_pause_state(self):
        timer = GameTimer()
        timer.pause()
        timer.reset()
        assert not timer.is_paused

    def test_double_pause_has_no_effect(self):
        import time
        timer = GameTimer()
        timer.pause()
        first_pause_start = timer.pause_start
        time.sleep(0.03)
        timer.pause()  # second call should be ignored
        assert timer.pause_start == first_pause_start

    def test_double_resume_has_no_effect(self):
        import time
        timer = GameTimer()
        timer.pause()
        time.sleep(0.02)
        timer.resume()
        paused = timer.paused_time
        timer.resume()  # second call should be ignored
        assert timer.paused_time == paused


class TestGameStatsTimer:

    def test_stats_has_timer(self):
        stats = GameStats()
        assert isinstance(stats.timer, GameTimer)

    def test_timer_starts_on_init(self):
        stats = GameStats()
        assert stats.timer.get_time() >= 0

    def test_reset_restarts_timer(self):
        import time
        stats = GameStats()
        time.sleep(0.05)
        stats.reset()
        assert stats.timer.get_time() < 0.05

    def test_save_result_writes_time(self, tmp_path):
        import time
        stats = GameStats()
        time.sleep(0.02)
        out = str(tmp_path / "result.txt")
        FileManager.save_result(out, "BFS", stats, solved=True)
        content = open(out).read()
        # extract the time value written
        for line in content.splitlines():
            if line.startswith("Time (s):"):
                written_time = float(line.split()[-1])
                assert written_time >= 0.02
                break
        else:
            pytest.fail("Time (s): line not found in output")
