from collections import deque
from typing import Deque, Dict, List, Tuple


def precompute_flips(n: int, k: int) -> List[Dict[int, int]]:
    """
    @brief Precomputes all flip mappings for a circular board.

    For each possible starting index, this function computes how the positions
    in a segment of size @p k are remapped when reversed.

    @param n Total number of positions on the board.
    @param k Size of the flipped segment.
    @return A list of mappings, one for each possible move.
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

    The first element is used as an anchor, and all positions are shifted so
    that equivalent rotational configurations share the same representation.

    @param state Tuple representing piece positions.
    @param n Total number of positions on the board.
    @return Normalized state.
    """
    anchor = state[0]
    return tuple((position - anchor) % n for position in state)


def get_neighbors_pro(
    state: Tuple[int, ...],
    n: int,
    flip_mappings: List[Dict[int, int]],
) -> List[Tuple[int, ...]]:
    """
    @brief Generates all neighboring states from the current state.

    Each neighbor is produced by applying one of the precomputed flip mappings,
    followed by normalization.

    @param state Current pattern state.
    @param n Total number of positions on the board.
    @param flip_mappings Precomputed flip mappings.
    @return List of neighboring normalized states.
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
    @brief Generates a Pattern Database (PDB) using breadth-first search.

    The search starts from the canonical solved pattern state and explores all
    reachable normalized states. The resulting dictionary maps each state to its
    minimum distance from the start state.

    @param n Total number of positions on the board.
    @param k Size of the flipped segment.
    @param num_pieces Number of pieces included in the pattern.
    @return Dictionary mapping normalized states to their optimal distance.
    """
    print(f"Generating PDB for n={n}, k={k}, pieces={num_pieces}...")

    flip_mappings = precompute_flips(n, k)
    start_state = tuple(range(num_pieces))

    pdb: Dict[Tuple[int, ...], int] = {start_state: 0}
    queue: Deque[Tuple[int, ...]] = deque([start_state])

    while queue:
        current_state = queue.popleft()
        current_distance = pdb[current_state]

        for next_state in get_neighbors_pro(current_state, n, flip_mappings):
            if next_state not in pdb:
                pdb[next_state] = current_distance + 1
                queue.append(next_state)

    print(f"PDB generated with {len(pdb)} entries.")
    return pdb


def build_patterns(n: int, group_size: int = 5) -> List[List[int]]:
    """
    @brief Splits the full set of pieces into pattern groups.

    Patterns are created as consecutive groups of tile identifiers starting at 1.

    Example for n=10 and group_size=4:
    - [1, 2, 3, 4]
    - [5, 6, 7, 8]
    - [9, 10]

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
    @brief Extracts a normalized pattern state from a full board position map.

    The positions of the pieces in the given pattern are collected and then
    normalized relative to the first piece in that pattern.

    @param pos_map Mapping from tile value to board position.
    @param pattern List of tile identifiers belonging to the pattern.
    @param n Total number of positions on the board.
    @return Normalized tuple representing the pattern state.
    """
    positions = [pos_map[piece] for piece in pattern]
    anchor = positions[0]
    return tuple((position - anchor) % n for position in positions)