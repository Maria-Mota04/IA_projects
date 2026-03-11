from typing import List


class Board:
    def __init__(self, tiles: int | List[int]):
        if isinstance(tiles, int):
            self._tiles: List[int] = [0] * tiles
        else:
            self._tiles = list(tiles)

    def get_tiles(self) -> List[int]:
        return self._tiles

    def set_tiles(self, tiles: List[int]) -> None:
        self._tiles = list(tiles)

    def size(self) -> int:
        return len(self._tiles)

    def at(self, index: int) -> int:
        return self._tiles[index]

    def set(self, index: int, value: int) -> int:
        self._tiles[index] = value

    def is_ordered(self) -> bool:
        return all(self._tiles[i] == i + 1 for i in range(len(self._tiles)))

    def reverse_segment(self, start: int, segment_size: int):

        n = self.size()

        for i in range(segment_size // 2):

            left = (start + i) % n
            right = (start + segment_size - 1 - i) % n

            self._tiles[left], self._tiles[right] = (
                self._tiles[right],
                self._tiles[left],
            )

    def rotate_wheel():
        pass

    def print(self) -> None:
        print("Board:", " ".join(str(tile) for tile in self._tiles))
