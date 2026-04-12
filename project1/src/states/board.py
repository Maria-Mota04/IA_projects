from typing import List
import random


class Board:

    def __init__(self, tiles: int | List[int], segment_size: int = 4) -> None:
        """
        @brief Build a board with initial tiles and segment size.

        @param tiles Initial tile sequence.
        @param segment_size Segment length used by reverse moves.
        """
        self._segment_size = segment_size
        self._tiles = list(tiles)
        self._initial_tiles = list(tiles)

    def get_tiles(self) -> List[int]:
        """@brief Return the current tile list."""
        return self._tiles

    def set_tiles(self, tiles: List[int]) -> None:
        """
        @brief Replace board tiles.

        @param tiles New tile sequence.
        """
        self._tiles = list(tiles)

    def get_segment_size(self) -> int:
        """@brief Return the configured segment size."""
        return self._segment_size

    def size(self) -> int:
        """@brief Return number of tiles."""
        return len(self._tiles)

    def is_ordered(self) -> bool:
        """@brief Check if tiles are in circular ascending order."""
        n = len(self._tiles)
        return all(
            self._tiles[(i + 1) % n] == (self._tiles[i] % n) + 1 for i in range(n)
        )

    def reverse_segment(self, start: int, segment_size: int) -> None:
        """
        @brief Reverse a circular segment of the board in-place.

        @param start Start index.
        @param segment_size Segment length.
        """
        n = self.size()

        for i in range(segment_size // 2):
            left = (start + i) % n
            right = (start + segment_size - 1 - i) % n
            self._tiles[left], self._tiles[right] = (
                self._tiles[right],
                self._tiles[left],
            )

    def rotate_wheel(self, steps=1) -> None:
        """
        @brief Rotate all tiles circularly.

        @param steps Number of steps to rotate.
        """
        n = self.size()
        steps = steps % n
        self._tiles = self._tiles[-steps:] + self._tiles[:-steps]

    def print(self) -> None:
        """@brief Print the board in a single line."""
        print("Board:", " ".join(str(tile) for tile in self._tiles))

    def reset_board(self) -> None:
        """@brief Reset tiles to the initial configuration."""
        self.set_tiles(self._initial_tiles)

    def shuffle_board(self, n_moves: int = 8) -> None:
        """
        @brief Shuffle the board from solved state using valid random moves.

        @param n_moves Number of random moves to apply.
        """
        self._tiles = list(range(1, len(self._tiles) + 1))
        self._shuffle_by_moves(n_moves)
        self._initial_tiles = list(self._tiles)

    def _shuffle_by_moves(self, n_moves: int) -> None:
        """
        @brief Internal helper that shuffles via reverse moves.

        @param n_moves Number of moves to apply.
        """
        n = len(self._tiles)
        last_start = None

        for _ in range(n_moves):
            possible_starts = list(range(n))

            # evita desfazer imediatamente a jogada anterior
            if last_start is not None and n > 1:
                possible_starts = [s for s in possible_starts if s != last_start]

            start = random.choice(possible_starts)
            self.reverse_segment(start, self._segment_size)
            last_start = start

    @staticmethod
    def is_solvable(board: list[int], segment_size: int) -> bool:
        """
        @brief Heuristic solvability check for given board and segment size.

        @param board Tile sequence to evaluate.
        @param segment_size Segment length used by the puzzle.
        @return True if considered solvable.
        """
        n = len(board)
        t = segment_size
        inversions = 0

        for i in range(n):
            for j in range(i + 1, n):
                if board[i] > board[j]:
                    inversions += 1

        if t == 2 and n >= 3:
            return True
        if n % 2 == 0 and t % 2 == 0:
            return True

        if n % 2 == 1 and t % 4 in [0, 1]:
            return False
        if n % 2 == 0 and t % 2 == 1:
            return False
        if n >= 4 and t == n - 1:
            return False

        if n % 2 == 1 and t % 4 == 3:
            return True
        if n % 2 == 1 and t <= n - 2 and t % 4 == 2:
            return True

        return inversions % 2 == 0
