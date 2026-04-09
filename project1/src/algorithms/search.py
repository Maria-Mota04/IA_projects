from collections import deque
from .tree_node import TreeNode
import heapq
from .search_strategy import SearchStrategy
from ..states.game_state import GameState


class SearchAlgorithms:

    @staticmethod
    def _key(state) -> tuple:
        return tuple(state.get_board().get_tiles())

    # Core function
    @staticmethod
    def search(strategy_enum, *args, **kwargs) -> TreeNode | None:
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
        func = search_funcs[strategy_enum]
        return func(*args, **kwargs)

    # Algorithms

    @staticmethod
    def bfs(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        queue = deque([root])
        visited = {key(initial_state)}
        count = 0

        while queue:
            node = queue.popleft()
            count += 1
            if count % 10000 == 0:
                print(
                    f"[BFS] nodes expanded: {count}, frontier: {len(queue)}, visited: {len(visited)}"
                )
            if goal_state_func(node.state):
                print(f"[BFS] solved in {count} expansions")
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = key(state)
                if k not in visited and (
                    max_cost is None or new_total_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    visited.add(k)
                    queue.append(new_node)
        return None

    @staticmethod
    def dfs(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        stack = deque([root])
        visited = {key(initial_state)}

        while stack:
            node = stack.pop()
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = key(state)
                if k not in visited and (
                    max_cost is None or new_total_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    visited.add(k)
                    stack.append(new_node)
        return None

    @staticmethod
    def dfs_limited(
        initial_state, goal_state_func, operators_func, depth_limit, max_cost=None
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        stack = deque([(root, 0)])
        visited = {key(initial_state)}

        while stack:
            node, depth = stack.pop()
            if goal_state_func(node.state):
                return node
            if depth >= depth_limit:
                continue
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = key(state)
                if k not in visited and (
                    max_cost is None or new_total_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    visited.add(k)
                    stack.append((new_node, depth + 1))
        return None

    @staticmethod
    def iterative_deepening_search(
        initial_state, goal_state_func, operators_func, max_depth, max_cost=None
    ) -> TreeNode | None:
        for depth in range(max_depth + 1):
            result = SearchAlgorithms.dfs_limited(
                initial_state, goal_state_func, operators_func, depth, max_cost=max_cost
            )
            if result:
                return result
        return None

    @staticmethod
    def greedy(
        initial_state, goal_state_func, operators_func, heuristic_func, max_cost=None
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        queue = [(heuristic_func(root), root)]
        visited = {key(initial_state)}
        count = 0

        while queue:
            _, node = heapq.heappop(queue)
            count += 1
            if count % 10000 == 0:
                print(
                    f"[Greedy] nodes: {count}, frontier: {len(queue)}, visited: {len(visited)}"
                )
            if goal_state_func(node.state):
                print(f"[Greedy] solved in {count} expansions")
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = key(state)
                if k not in visited and (
                    max_cost is None or new_total_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    visited.add(k)
                    heapq.heappush(queue, (heuristic_func(new_node), new_node))
        return None

    @staticmethod
    def a_star(
        initial_state, goal_state_func, operators_func, heuristic_func, max_cost=None
    ) -> TreeNode | None:
        return SearchAlgorithms.weighted_a_star(
            initial_state,
            goal_state_func,
            operators_func,
            heuristic_func,
            w=1.0,
            max_cost=max_cost,
        )

    @staticmethod
    def weighted_a_star(
        initial_state,
        goal_state_func,
        operators_func,
        heuristic_func,
        w=1.0,
        max_cost=None,
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        queue = [(heuristic_func(root), root)]
        visited = {key(initial_state)}

        while queue:
            _, node = heapq.heappop(queue)
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = key(state)
                if k not in visited and (
                    max_cost is None or new_total_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    visited.add(k)
                    total_cost = new_node.cost + w * heuristic_func(new_node)
                    heapq.heappush(queue, (total_cost, new_node))
        return None

    @staticmethod
    def uniform_cost(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        key = SearchAlgorithms._key
        root = TreeNode(initial_state)
        frontier = [(0, root)]
        heapq.heapify(frontier)
        cost_so_far = {key(initial_state): 0}

        while frontier:
            current_cost, node = heapq.heappop(frontier)
            if goal_state_func(node.state):
                return node
            k_node = key(node.state)
            if current_cost > cost_so_far.get(k_node, float("inf")):
                continue
            for state, op_cost in operators_func(node.state):
                new_cost = current_cost + op_cost
                k = key(state)
                if (k not in cost_so_far or new_cost < cost_so_far[k]) and (
                    max_cost is None or new_cost <= max_cost
                ):
                    new_node = TreeNode(state, parent=node, operator_cost=op_cost)
                    cost_so_far[k] = new_cost
                    heapq.heappush(frontier, (new_cost, new_node))
        return None

    @staticmethod
    def extract_path(node: TreeNode) -> list[GameState]:
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))
