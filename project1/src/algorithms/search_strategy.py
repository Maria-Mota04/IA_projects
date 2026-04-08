from enum import IntEnum


class SearchStrategy(IntEnum):
    BFS = 0
    DFS = 1
    DFS_LIMITED = 2
    ITERATIVE_DEEPENING = 3
    GREEDY = 4
    A_STAR = 5
    WEIGHTED_A_STAR = 6
    UNIFORM_COST = 7
