import pytest

from src.algorithms.search_strategy import SearchStrategy
from src.game.game import Game
from src.game.game_modes import gameMode
from src.game.solver import Solver
from src.states.board import Board
from src.states.game_state import GameState


def test_moves_count_only_reverse_segments() -> None:
    board = Board([1, 2, 3, 4], segment_size=2)
    game = Game(GameState(board), size=4, segment_size=2)

    game.make_rotate(1)
    game.make_rotate(-1)
    game.make_move(0)
    game.make_move(1)

    assert game._game_stats.moves == 2
    assert len(game._game_stats.history) == 4


def test_search_stats_depth_and_nodes_are_consistent() -> None:
    board = Board([2, 1, 3, 4], segment_size=2)
    game = Game(GameState(board), size=4, segment_size=2)
    solver = Solver(n=4, k=2, group_size=2)

    path, stats = solver.solve(
        game=game,
        screen=None,
        mode=gameMode.SEARCH_ALGORITHM,
        strategy=SearchStrategy.BFS,
        segment_size=2,
        depth_limit=10,
        max_cost=None,
        weight=1.0,
        heuristic_func=solver.heuristic_misplaced,
    )

    assert stats["found"] is True
    assert path is not None
    assert stats["depth"] == 1
    assert len(path) - 1 == stats["depth"]
    assert stats["nodes"] > 0


@pytest.mark.parametrize(
    "strategy",
    [
        SearchStrategy.BFS,
        SearchStrategy.DFS,
        SearchStrategy.DFS_LIMITED,
        SearchStrategy.ITERATIVE_DEEPENING,
        SearchStrategy.GREEDY,
        SearchStrategy.A_STAR,
        SearchStrategy.WEIGHTED_A_STAR,
        SearchStrategy.UNIFORM_COST,
    ],
)
def test_all_strategies_report_consistent_depth(strategy: SearchStrategy) -> None:
    board = Board([3, 1, 2, 4], segment_size=2)
    game = Game(GameState(board), size=4, segment_size=2)
    solver = Solver(n=4, k=2, group_size=2)

    path, stats = solver.solve(
        game=game,
        screen=None,
        mode=gameMode.SEARCH_ALGORITHM,
        strategy=strategy,
        segment_size=2,
        depth_limit=10,
        max_cost=None,
        weight=1.3,
        heuristic_func=solver.heuristic_misplaced,
    )

    assert stats["found"] is True
    assert path is not None
    assert stats["depth"] == len(path) - 1
    assert stats["nodes"] > 0


def test_custom_play_stats_moves_and_depth() -> None:
    board = Board([2, 1, 3, 4], segment_size=2)
    game = Game(GameState(board), size=4, segment_size=2)

    # Side rotations should not affect moves counter.
    game.make_rotate(1)
    game.make_rotate(-1)

    # Reverse segment should count as one move and solve this board.
    game.make_move(0)
    assert game.won() is True
    assert game._game_stats.moves == 1

    # In the menu flow, custom play writes solution depth at win as done moves.
    game._game_stats.solution_depth = game._game_stats.moves
    assert game._game_stats.solution_depth == 1
