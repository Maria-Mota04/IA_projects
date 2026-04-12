from collections import deque
import heapq
from typing import Callable, Iterable, Optional

from .search_strategy import SearchStrategy
from .tree_node import TreeNode
from ..states.game_state import GameState


class SearchAlgorithms:
    """
    @brief Collection of static search algorithms used to solve game states.

    Supports:
    - Breadth-First Search (BFS)
    - Depth-First Search (DFS)
    - Depth-Limited DFS
    - Iterative Deepening Search (IDS)
    - Greedy Search
    - A*
    - Weighted A*
    - Uniform Cost Search (UCS)
    """

    @staticmethod
    def _key(state) -> tuple:
        """
        @brief Produces a hashable key for a game state.

        @param state Game state.
        @return Tuple representation of board tiles.
        """
        return tuple(state.get_board().get_tiles())

    @staticmethod
    def search(strategy_enum, *args, **kwargs) -> TreeNode | None:
        """
        @brief Dispatches execution to the selected search algorithm.

        @param strategy_enum Search strategy enum or index.
        @param args Positional arguments for the chosen search function.
        @param kwargs Keyword arguments for the chosen search function.
        @return Goal node if a solution is found, otherwise None.
        """
        strategy_map = {
            SearchStrategy.BFS: SearchAlgorithms.bfs,
            SearchStrategy.DFS: SearchAlgorithms.dfs,
            SearchStrategy.DFS_LIMITED: SearchAlgorithms.dfs_limited,
            SearchStrategy.ITERATIVE_DEEPENING: SearchAlgorithms.iterative_deepening_search,
            SearchStrategy.GREEDY: SearchAlgorithms.greedy,
            SearchStrategy.A_STAR: SearchAlgorithms.a_star,
            SearchStrategy.WEIGHTED_A_STAR: SearchAlgorithms.weighted_a_star,
            SearchStrategy.UNIFORM_COST: SearchAlgorithms.uniform_cost,
        }

        if isinstance(strategy_enum, SearchStrategy):
            search_func = strategy_map[strategy_enum]
        else:
            search_funcs = [
                SearchAlgorithms.bfs,
                SearchAlgorithms.dfs,
                SearchAlgorithms.dfs_limited,
                SearchAlgorithms.iterative_deepening_search,
                SearchAlgorithms.greedy,
                SearchAlgorithms.a_star,
                SearchAlgorithms.weighted_a_star,
                SearchAlgorithms.uniform_cost,
            ]
            search_func = search_funcs[strategy_enum]

        return search_func(*args, **kwargs)

    @staticmethod
    def bfs(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Breadth-First Search.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print("[SEARCH] BFS started...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = deque([root])
        visited = {key(initial_state)}

        while frontier:
            node = frontier.popleft()

            if goal_state_func(node.state):
                print(f"[SUCCESS] BFS found a solution! Cost: {node.cost}")
                return node

            for next_state, operator_cost in operators_func(node.state):
                new_cost = node.cost + operator_cost
                state_key = key(next_state)

                if state_key not in visited and (
                    max_cost is None or new_cost <= max_cost
                ):
                    child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                    visited.add(state_key)
                    frontier.append(child)

        return None

    @staticmethod
    def _state_in_path(node: TreeNode, state_key: tuple) -> bool:
        """
        @brief Checks whether a state already exists in the current node path.

        Useful for cycle detection in path-based depth-first variants.

        @param node Current tree node.
        @param state_key Hashable state key.
        @return True if the state is already in the path, otherwise False.
        """
        current = node
        while current is not None:
            if SearchAlgorithms._key(current.state) == state_key:
                return True
            current = current.parent
        return False

    @staticmethod
    def dfs(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        depth_limit=None,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Depth-First Search.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param depth_limit Optional maximum depth.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print("[SEARCH] DFS started...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = deque([(root, 0)])
        visited = {key(initial_state)}

        while frontier:
            node, depth = frontier.pop()

            if goal_state_func(node.state):
                print(f"[SUCCESS] DFS found a solution! Depth: {depth}")
                return node

            if depth_limit is not None and depth >= depth_limit:
                continue

            for next_state, operator_cost in operators_func(node.state):
                new_cost = node.cost + operator_cost
                state_key = key(next_state)

                if state_key not in visited and (
                    max_cost is None or new_cost <= max_cost
                ):
                    child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                    visited.add(state_key)
                    frontier.append((child, depth + 1))

        return None

    @staticmethod
    def dfs_limited(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        depth_limit: int,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Depth-Limited DFS.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param depth_limit Maximum search depth.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print(f"[SEARCH] Depth-Limited DFS started (Limit: {depth_limit})...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = deque([(root, 0)])
        visited = {key(initial_state)}

        while frontier:
            node, depth = frontier.pop()

            if goal_state_func(node.state):
                print(f"[SUCCESS] Depth-Limited DFS found a solution at depth {depth}")
                return node

            if depth >= depth_limit:
                continue

            for next_state, operator_cost in operators_func(node.state):
                new_cost = node.cost + operator_cost
                state_key = key(next_state)

                if state_key not in visited and (
                    max_cost is None or new_cost <= max_cost
                ):
                    child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                    visited.add(state_key)
                    frontier.append((child, depth + 1))

        return None

    @staticmethod
    def iterative_deepening_search(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        depth_limit: int,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Iterative Deepening Search.

        Repeatedly runs depth-limited DFS from depth 0 up to @p depth_limit.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param depth_limit Maximum depth to explore.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print(f"[SEARCH] IDS started (Max depth: {depth_limit})...")

        for depth in range(depth_limit + 1):
            result = SearchAlgorithms.dfs_limited(
                initial_state,
                goal_state_func,
                operators_func,
                depth,
                max_cost=max_cost,
            )
            if result is not None:
                return result

        return None

    @staticmethod
    def greedy(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        heuristic_func: Callable,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Greedy Best-First Search.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param heuristic_func Heuristic function applied to tree nodes.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print("[SEARCH] Greedy Search started...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = [(heuristic_func(root), root)]
        visited = {key(initial_state)}

        while frontier:
            _, node = heapq.heappop(frontier)

            if goal_state_func(node.state):
                print(f"[SUCCESS] Greedy Search found a solution! Cost: {node.cost}")
                return node

            for next_state, operator_cost in operators_func(node.state):
                new_cost = node.cost + operator_cost
                state_key = key(next_state)

                if state_key not in visited and (
                    max_cost is None or new_cost <= max_cost
                ):
                    child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                    visited.add(state_key)
                    heapq.heappush(frontier, (heuristic_func(child), child))

        return None

    @staticmethod
    def a_star(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        heuristic_func: Callable,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes A* search.

        This is implemented as Weighted A* with weight = 1.0.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param heuristic_func Heuristic function applied to tree nodes.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        return SearchAlgorithms.weighted_a_star(
            initial_state,
            goal_state_func,
            operators_func,
            heuristic_func,
            weight=1.0,
            max_cost=max_cost,
        )

    @staticmethod
    def weighted_a_star(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        heuristic_func: Callable,
        weight: float = 1.0,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Weighted A* search.

        Uses:
        f(n) = g(n) + weight * h(n)

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param heuristic_func Heuristic function applied to tree nodes.
        @param weight Heuristic multiplier.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print(f"[SEARCH] Weighted A* started (Weight: {weight})...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = [(weight * heuristic_func(root), root)]
        best_cost = {key(initial_state): root.cost}

        while frontier:
            _, node = heapq.heappop(frontier)

            if goal_state_func(node.state):
                print(f"[SUCCESS] Weighted A* found a solution! Cost: {node.cost}")
                return node

            for next_state, operator_cost in operators_func(node.state):
                new_cost = node.cost + operator_cost
                state_key = key(next_state)

                if state_key not in best_cost or new_cost < best_cost[state_key]:
                    if max_cost is None or new_cost <= max_cost:
                        best_cost[state_key] = new_cost
                        child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                        f_score = child.cost + weight * heuristic_func(child)
                        heapq.heappush(frontier, (f_score, child))

        return None

    @staticmethod
    def uniform_cost(
        initial_state,
        goal_state_func: Callable,
        operators_func: Callable,
        max_cost=None,
    ) -> TreeNode | None:
        """
        @brief Executes Uniform Cost Search.

        @param initial_state Initial game state.
        @param goal_state_func Function that checks if a state is a goal.
        @param operators_func Function that generates successor states.
        @param max_cost Optional maximum allowed path cost.
        @return Goal node if found, otherwise None.
        """
        print("[SEARCH] Uniform Cost Search started...")

        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = [(0, root)]
        heapq.heapify(frontier)

        cost_so_far = {key(initial_state): 0}

        while frontier:
            current_cost, node = heapq.heappop(frontier)

            if goal_state_func(node.state):
                print(f"[SUCCESS] UCS found a solution! Cost: {node.cost}")
                return node

            node_key = key(node.state)
            if current_cost > cost_so_far.get(node_key, float("inf")):
                continue

            for next_state, operator_cost in operators_func(node.state):
                new_cost = current_cost + operator_cost
                state_key = key(next_state)

                if (state_key not in cost_so_far or new_cost < cost_so_far[state_key]) and (
                    max_cost is None or new_cost <= max_cost
                ):
                    child = TreeNode(next_state, parent=node, operator_cost=operator_cost)
                    cost_so_far[state_key] = new_cost
                    heapq.heappush(frontier, (new_cost, child))

        return None

    @staticmethod
    def extract_path(node: TreeNode) -> list[GameState]:
        """
        @brief Extracts the state path from the root to a goal node.

        @param node Goal node.
        @return Ordered list of game states from initial state to goal state.
        """
        path = []

        while node is not None:
            path.append(node.state)
            node = node.parent

        return list(reversed(path))