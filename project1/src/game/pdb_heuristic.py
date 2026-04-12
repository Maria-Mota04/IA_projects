# src/game/pdb_heuristic.py

from collections import deque
from typing import Deque, Dict, List, Tuple


def precompute_flips(n: int, k: int) -> List[Dict[int, int]]:
    """
    @brief Precomputes all flip mappings for a circular board.

    @param n Total number of positions on the board.
    @param k Size of the flipped segment.
    @return List of flip mappings.
    """
    flip_mappings: List[Dict[int, int]] = []

    for start in range(n):
        indices = [(start + offset) % n for offset in range(k)]
        mapping = {
            indices[offset]: indices[k - 1 - offset]
            for offset in range(k)
        }
        flip_mappings.append(mapping)

    return flip_mappings


def normalize_state(state: Tuple[int, ...], n: int) -> Tuple[int, ...]:
    """
    @brief Normalizes a state relative to its first element.

    @param state Tuple representing piece positions.
    @param n Total number of positions on the board.
    @return Normalized state.
    """
    anchor = state[0]
    return tuple((position - anchor) % n for position in state)


def get_pattern_neighbors(
    state: Tuple[int, ...],
    n: int,
    flip_mappings: List[Dict[int, int]],
) -> List[Tuple[int, ...]]:
    """
    @brief Generates all neighboring normalized pattern states.

    @param state Current pattern state.
    @param n Total number of positions on the board.
    @param flip_mappings Precomputed flip mappings.
    @return Neighboring normalized states.
    """
    neighbors: List[Tuple[int, ...]] = []

    for move_mapping in flip_mappings:
        new_state = tuple(
            move_mapping[position] if position in move_mapping else position
            for position in state
        )
        neighbors.append(normalize_state(new_state, n))

    return neighbors


def generate_pdb(n: int, k: int, num_pieces: int) -> Dict[Tuple[int, ...], int]:
    """
    @brief Generates a Pattern Database using breadth-first search.

    @param n Total number of positions on the board.
    @param k Size of the flipped segment.
    @param num_pieces Number of pieces included in the pattern.
    @return Dictionary mapping normalized states to optimal distances.
    """
    print(f"Generating PDB for n={n}, k={k}, pieces={num_pieces}...")

    flip_mappings = precompute_flips(n, k)
    start_state = tuple(range(num_pieces))

    pdb: Dict[Tuple[int, ...], int] = {start_state: 0}
    queue: Deque[Tuple[int, ...]] = deque([start_state])

    while queue:
        current_state = queue.popleft()
        current_distance = pdb[current_state]

        for next_state in get_pattern_neighbors(current_state, n, flip_mappings):
            if next_state not in pdb:
                pdb[next_state] = current_distance + 1
                queue.append(next_state)

    print(f"PDB generated with {len(pdb)} entries.")
    return pdb


def build_patterns(n: int, group_size: int = 5) -> List[List[int]]:
    """
    @brief Splits piece identifiers into consecutive pattern groups.

    @param n Total number of pieces.
    @param group_size Number of pieces per pattern.
    @return List of patterns.
    """
    return [
        list(range(start, min(start + group_size, n + 1)))
        for start in range(1, n + 1, group_size)
    ]


def pattern_state_from_positions(
    pos_map: Dict[int, int],
    pattern: List[int],
    n: int,
) -> Tuple[int, ...]:
    """
    @brief Extracts a normalized pattern state from a full position map.

    @param pos_map Mapping from tile value to board position.
    @param pattern Pattern tile identifiers.
    @param n Total number of positions on the board.
    @return Normalized pattern state.
    """
    positions = [pos_map[piece] for piece in pattern]
    anchor = positions[0]
    return tuple((position - anchor) % n for position in positions)