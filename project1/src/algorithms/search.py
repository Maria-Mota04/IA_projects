from collections import deque
from .tree_node import TreeNode
import heapq
from .search_strategy import SearchStrategy


class SearchAlgorithms:

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
        func = search_funcs[strategy_enum.value]
        return func(*args, **kwargs)

    # Algorithms

    @staticmethod
    def bfs(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        root = TreeNode(initial_state, path_set={initial_state})
        queue = deque([root])
        visited = {initial_state}

        while queue:
            node = queue.popleft()
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                if (
                    state not in node.path_set
                    and state not in visited
                    and (max_cost is None or new_total_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=cost, path_set=node.path_set
                    )
                    node.add_child(new_node, cost)
                    visited.add(state)
                    queue.append(new_node)
        return None

    @staticmethod
    def dfs(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        root = TreeNode(initial_state, path_set={initial_state})
        stack = deque([root])
        visited = {initial_state}

        while stack:
            node = stack.pop()
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                if (
                    state not in node.path_set
                    and state not in visited
                    and (max_cost is None or new_total_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=cost, path_set=node.path_set
                    )
                    node.add_child(new_node, cost)
                    visited.add(state)
                    stack.append(new_node)
        return None

    @staticmethod
    def dfs_limited(
        initial_state, goal_state_func, operators_func, depth_limit, max_cost=None
    ) -> TreeNode | None:
        root = TreeNode(initial_state, path_set={initial_state})
        stack = deque([(root, 0)])
        visited = {initial_state}

        while stack:
            node, depth = stack.pop()
            if goal_state_func(node.state):
                return node
            if depth >= depth_limit:
                continue
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                if (
                    state not in node.path_set
                    and state not in visited
                    and (max_cost is None or new_total_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=cost, path_set=node.path_set
                    )
                    node.add_child(new_node, cost)
                    visited.add(state)
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
        root = TreeNode(initial_state, path_set={initial_state})
        queue = [(root, heuristic_func(root))]
        visited = {initial_state}

        while queue:
            node, _ = queue.pop(0)
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                if (
                    state not in node.path_set
                    and state not in visited
                    and (max_cost is None or new_total_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=cost, path_set=node.path_set
                    )
                    node.add_child(new_node, cost)
                    visited.add(state)
                    queue.append((new_node, heuristic_func(new_node)))
            queue.sort(key=lambda x: x[1])
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
        root = TreeNode(initial_state, path_set={initial_state})
        queue = [(root, heuristic_func(root))]
        visited = {initial_state}

        while queue:
            node, _ = queue.pop(0)
            if goal_state_func(node.state):
                return node
            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                if (
                    state not in node.path_set
                    and state not in visited
                    and (max_cost is None or new_total_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=cost, path_set=node.path_set
                    )
                    node.add_child(new_node, cost)
                    visited.add(state)
                    total_cost = new_node.cost + w * heuristic_func(new_node)
                    queue.append((new_node, total_cost))
            queue.sort(key=lambda x: x[1])
        return None

    @staticmethod
    def uniform_cost(
        initial_state, goal_state_func, operators_func, max_cost=None
    ) -> TreeNode | None:
        root = TreeNode(initial_state, path_set={initial_state})
        frontier = [(0, root)]
        heapq.heapify(frontier)
        cost_so_far = {initial_state: 0}

        while frontier:
            current_cost, node = heapq.heappop(frontier)
            if goal_state_func(node.state):
                return node
            for state, op_cost in operators_func(node.state):
                new_cost = current_cost + op_cost
                if (
                    state not in node.path_set
                    and (state not in cost_so_far or new_cost < cost_so_far[state])
                    and (max_cost is None or new_cost <= max_cost)
                ):
                    new_node = TreeNode(
                        state, parent=node, cost=op_cost, path_set=node.path_set
                    )
                    node.add_child(new_node, op_cost)
                    cost_so_far[state] = new_cost
                    heapq.heappush(frontier, (new_cost, new_node))
        return None
