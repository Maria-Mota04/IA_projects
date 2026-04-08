from typing import List
import random


class Board:

    # Core functions
    def __init__(self, tiles: int | List[int], segment_size: int = 4) -> None:
        self._segment_size = segment_size
        self._tiles = list(tiles)

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
        n = len(self._tiles)
        self._tiles = list(range(1, n + 1))
        self._shuffle_solvable(self._segment_size)

    @staticmethod
    def is_solvable(board: list[int], segment_size: int) -> bool:
        inversions = 0
        n = len(board)
        for i in range(n):
            for j in range(i + 1, n):
                if board[i] > board[j]:
                    inversions += 1

        if segment_size % 2 == 0:
            return inversions % 2 == 0
        else:
            return True

    def _shuffle_solvable(self, segment_size: int) -> None:
        while True:
            random.shuffle(self._tiles)
            if Board.is_solvable(self._tiles, segment_size):
                break
