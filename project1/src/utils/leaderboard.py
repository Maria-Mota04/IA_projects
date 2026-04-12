from __future__ import annotations
import json
from pathlib import Path


class Leaderboard:
    MAX_ENTRIES = 10
    _SCORES_FILE = Path(__file__).parent.parent.parent / "results" / "leaderboard.json"

    def add_entry(self, moves: int, time_seconds: float) -> None:
        """
        @brief Add a score entry and keep only the best records.

        @param moves Number of moves performed.
        @param time_seconds Completion time in seconds.
        """
        entries = self._load()
        entries.append({"moves": moves, "time": round(time_seconds, 2)})
        entries.sort(key=lambda e: (e["moves"], e["time"]))
        entries = entries[: self.MAX_ENTRIES]
        self._save(entries)

    def get_entries(self) -> list[dict]:
        """
        @brief Return all stored leaderboard entries.

        @return List of leaderboard dictionaries.
        """
        return self._load()

    def _load(self) -> list[dict]:
        """
        @brief Load leaderboard data from disk.

        @return List of entries, or an empty list on errors.
        """
        if self._SCORES_FILE.exists():
            try:
                with open(self._SCORES_FILE, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return []
        return []

    def _save(self, entries: list[dict]) -> None:
        """
        @brief Save leaderboard entries to disk.

        @param entries Entries to persist.
        """
        self._SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self._SCORES_FILE, "w") as f:
            json.dump(entries, f, indent=2)
