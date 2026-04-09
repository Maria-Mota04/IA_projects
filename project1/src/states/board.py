from typing import List
import random


class Board:

    # Core functions
    def __init__(self, tiles: int | List[int], segment_size: int = 4) -> None:
        self._segment_size = segment_size
        self._tiles = list(tiles)
        self._initial_tiles = list(tiles)

    def get_tiles(self) -> List[int]:
        return self._tiles

    def set_tiles(self, tiles: List[int]) -> None:
        self._tiles = list(tiles)

    def get_segment_size(self) -> int:
        return self._segment_size

    def size(self) -> int:
        return len(self._tiles)

    def at(self, index: int) -> int:
        return self._tiles[index]

    def set(self, index: int, value: int) -> int:
        self._tiles[index] = value

    def is_ordered(self) -> bool:
        n = len(self._tiles)
        return all(
            self._tiles[(i + 1) % n] == (self._tiles[i] % n) + 1 for i in range(n)
        )

    # Moves

    def reverse_segment(self, start: int, segment_size: int) -> None:

        n = self.size()

        for i in range(segment_size // 2):

            left = (start + i) % n
            right = (start + segment_size - 1 - i) % n

            self._tiles[left], self._tiles[right] = (
                self._tiles[right],
                self._tiles[left],
            )

    def rotate_wheel(self, steps=1) -> None:
        n = self.size()
        steps = steps % n
        self._tiles = self._tiles[-steps:] + self._tiles[:-steps]

    # Utils

    def print(self) -> None:
        print("Board:", " ".join(str(tile) for tile in self._tiles))

    def reset_board(self) -> None:
        self.set_tiles(self._initial_tiles)

    def shuffle_board(self) -> None:
        n = len(self._tiles)
        self._tiles = list(range(1, n + 1))
        self._shuffle_solvable(self._segment_size)

    def shuffle_few_moves(self, n_moves: int = 8) -> None:
        """Shuffle by applying n_moves random moves from solved state."""
        import random as _random

        n = len(self._tiles)
        self._tiles = list(range(1, n + 1))
        for _ in range(n_moves):
            start = _random.randrange(n)
            self.reverse_segment(start, self._segment_size)

    @staticmethod
    def is_solvable(board: list[int], segment_size: int) -> bool:
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

    def _shuffle_solvable(self, segment_size: int) -> None:
        while True:
            random.shuffle(self._tiles)
            if Board.is_solvable(self._tiles, segment_size):
                break
