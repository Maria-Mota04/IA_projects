from collections import deque


def precompute_flips(n, k):
    flips = []
    for i in range(n):
        indices = [(i + j) % n for j in range(k)]
        mapping = {indices[j]: indices[k - 1 - j] for j in range(k)}
        flips.append(mapping)
    return flips


def normalize_state(state, n):
    anchor = state[0]
    return tuple((p - anchor) % n for p in state)


def get_neighbors_pro(state, n, flips):
    neighbors = []

    for move_map in flips:
        new_pos = tuple(move_map[p] if p in move_map else p for p in state)
        neighbors.append(normalize_state(new_pos, n))

    return neighbors


def generate_pdb(n, k, num_pieces):
    print(f"Generating PDB for n={n}, k={k}, pieces={num_pieces}...")
    flips = precompute_flips(n, k)
    start_state = tuple(range(num_pieces))

    pdb = {start_state: 0}
    queue = deque([start_state])

    while queue:
        curr = queue.popleft()
        dist = pdb[curr]

        for nxt in get_neighbors_pro(curr, n, flips):
            if nxt not in pdb:
                pdb[nxt] = dist + 1
                queue.append(nxt)

    print(f"PDB generated with {len(pdb)} entries.")
    return pdb


def build_patterns(n, group_size=5):
    return [
        list(range(i, min(i + group_size, n + 1))) for i in range(1, n + 1, group_size)
    ]


def pattern_state_from_positions(pos_map, pattern, n):
    positions = [pos_map[p] for p in pattern]
    anchor = positions[0]
    return tuple((p - anchor) % n for p in positions)
