from src.algorithms.search import SearchAlgorithms
from src.algorithms.search_strategy import SearchStrategy


def _line_operators(state: int):
    nxt = []
    if state < 3:
        nxt.append((state + 1, 1))
    return nxt


def _weighted_graph_operators(state: str):
    graph = {
        "S": [("A", 10), ("B", 1)],
        "A": [("G", 1)],
        "B": [("G", 1)],
        "G": [],
    }
    return graph[state]


def _goal_int(state: int) -> bool:
    return state == 3


def _goal_graph(state: str) -> bool:
    return state == "G"


def test_bfs_reaches_goal_node():
    result = SearchAlgorithms.bfs(0, _goal_int, _line_operators)

    assert result is not None
    assert result.state == 3


def test_dfs_limited_respects_limit_and_then_finds_goal():
    result_limited = SearchAlgorithms.dfs_limited(0, _goal_int, _line_operators, 2)
    result_ok = SearchAlgorithms.dfs_limited(0, _goal_int, _line_operators, 3)

    assert result_limited is None
    assert result_ok is not None
    assert result_ok.state == 3


def test_iterative_deepening_finds_goal_within_max_depth():
    result = SearchAlgorithms.iterative_deepening_search(
        0, _goal_int, _line_operators, max_depth=3
    )

    assert result is not None
    assert result.state == 3


def test_uniform_cost_prefers_cheaper_path():
    result = SearchAlgorithms.uniform_cost("S", _goal_graph, _weighted_graph_operators)

    assert result is not None
    assert result.state == "G"
    assert result.cost == 2


def test_search_dispatch_uses_strategy_enum():
    result = SearchAlgorithms.search(SearchStrategy.BFS, 0, _goal_int, _line_operators)

    assert result is not None
    assert result.state == 3


def test_dfs_reaches_goal_node():
    result = SearchAlgorithms.dfs(0, _goal_int, _line_operators)

    assert result is not None
    assert result.state == 3


def test_bfs_respects_max_cost_cutoff():
    result = SearchAlgorithms.bfs(0, _goal_int, _line_operators, max_cost=1)

    assert result is None


def test_greedy_and_a_star_reach_graph_goal():
    heuristic = lambda node: 0

    greedy_result = SearchAlgorithms.greedy(
        "S", _goal_graph, _weighted_graph_operators, heuristic
    )
    a_star_result = SearchAlgorithms.a_star(
        "S", _goal_graph, _weighted_graph_operators, heuristic
    )

    assert greedy_result is not None
    assert greedy_result.state == "G"
    assert a_star_result is not None
    assert a_star_result.state == "G"


def test_weighted_a_star_reaches_goal_with_weight():
    heuristic = lambda node: 0

    result = SearchAlgorithms.weighted_a_star(
        "S", _goal_graph, _weighted_graph_operators, heuristic, w=1.7
    )

    assert result is not None
    assert result.state == "G"
