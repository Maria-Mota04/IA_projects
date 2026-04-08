from __future__ import annotations
import os
from pathlib import Path
from datetime import datetime

from src.states.board import Board
from src.states.game_state import GameState
from src.utils.game_stats import GameStats


_PROJECT_ROOT = Path(__file__).parent.parent.parent
_INSTANCES_DIR = _PROJECT_ROOT / "instances"
_RESULTS_DIR = _PROJECT_ROOT / "results"


class FileManager:

    @staticmethod
    def _resolve_path(filepath: str, default_dir: Path) -> Path:
        p = Path(filepath)
        if not p.suffix:
            p = p.with_suffix(".txt")
        if not p.is_absolute() and len(p.parts) == 1:
            p = default_dir / p
        return p

    @staticmethod
    def load_instance(filepath: str) -> tuple[GameState, int, int]:
        """Load a puzzle instance from a .txt file.

        Instance file format (.txt):
            N K
            t1 t2 ... tN

        Example:
            8 4
            3 1 4 2 7 5 6 8

                Returns:
                    (initial_state, N, K)
        """
        path = FileManager._resolve_path(filepath, _INSTANCES_DIR)
        if not path.exists():
            raise FileNotFoundError(f"Instance file not found: {path}")

        with open(path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < 2:
            raise ValueError(
                f"Invalid instance file (need at least 2 lines): {filepath}"
            )

        header = lines[0].split()
        if len(header) != 2:
            raise ValueError(f"First line must be 'N K', got: {lines[0]!r}")

        n, k = int(header[0]), int(header[1])
        tiles = list(map(int, lines[1].split()))

        if len(tiles) != n:
            raise ValueError(f"Expected {n} tiles, got {len(tiles)}")

        state = GameState(Board(tiles, segment_size=k))
        return state, n, k

    @staticmethod
    def save_result(
        filepath: str,
        algorithm_name: str,
        stats: GameStats,
        solved: bool,
        solution_path: list[GameState] | None = None,
        heuristic_name: str | None = None,
    ) -> None:

        path = FileManager._resolve_path(filepath, _RESULTS_DIR)
        os.makedirs(path.parent, exist_ok=True)

        with open(path, "w") as f:
            f.write(
                f"Timestamp:        {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            f.write(f"Algorithm:        {algorithm_name}\n")
            f.write(f"Heuristic:        {heuristic_name or 'None'}\n")
            f.write(f"Solved:           {solved}\n")
            f.write(f"Moves:            {stats.moves}\n")
            f.write(f"Solution depth:   {stats.solution_depth}\n")
            f.write(f"States explored:  {stats.states_explored}\n")
            f.write(f"Max memory:       {stats.max_memory}\n")
            f.write(f"Time (s):         {stats.timer.get_time():.4f}\n")

            if solution_path:
                f.write("Solution path:\n")
                for state in solution_path:
                    tiles_str = " ".join(str(t) for t in state.get_board().get_tiles())
                    f.write(f"  {tiles_str}\n")
            else:
                f.write("Solution path:    None\n")
