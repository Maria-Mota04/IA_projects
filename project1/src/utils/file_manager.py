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
        """
        @brief Resolve a user filepath to an absolute .txt path.

        @param filepath Input path or bare filename.
        @param default_dir Default directory for bare names.
        @return Resolved path.
        """
        p = Path(filepath)
        if not p.suffix:
            p = p.with_suffix(".txt")
        if not p.is_absolute() and len(p.parts) == 1:
            p = default_dir / p
        return p

    @staticmethod
    def load_instance(filepath: str) -> tuple[GameState, int, int]:
        """
        @brief Load a puzzle instance from a text file.

        @param filepath Relative or absolute instance file path.
        @return Tuple with initial state, board size (N), and segment size (K).
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
