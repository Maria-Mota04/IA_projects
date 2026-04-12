from collections import deque
import heapq
import itertools

from .tree_node import TreeNode
from .search_strategy import SearchStrategy
from ..states.game_state import GameState


class SearchAlgorithms:
    _counter = itertools.count()

    @staticmethod
    def _key(state: GameState) -> tuple:
        tiles = state.get_board().get_tiles()
        idx = tiles.index(1)
        normalized = tiles[idx:] + tiles[:idx]
        return tuple(normalized)

    @staticmethod
    def search(strategy_enum, *args, **kwargs) -> TreeNode | None:
        if not isinstance(strategy_enum, SearchStrategy):
            strategy_enum = SearchStrategy(strategy_enum)

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

        func = strategy_map[strategy_enum]
        return func(*args, **kwargs)

    @staticmethod
    def _push_heap(heap, priority, node):
        heapq.heappush(heap, (priority, next(SearchAlgorithms._counter), node))

    @staticmethod
    def _pop_heap(heap):
        priority, _, node = heapq.heappop(heap)
        return priority, node

    @staticmethod
    def _state_in_path(node: TreeNode, state_key: tuple) -> bool:
        current = node
        while current is not None:
            if SearchAlgorithms._key(current.state) == state_key:
                return True
            current = current.parent
        return False

    @staticmethod
    def bfs(initial_state, goal_state_func, operators_func, max_cost=None) -> TreeNode | None:
        root = TreeNode(initial_state)
        queue = deque([root])
        visited = {SearchAlgorithms._key(initial_state)}

        while queue:
            node = queue.popleft()

            if goal_state_func(node.state):
                return node

            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = SearchAlgorithms._key(state)

                if k in visited:
                    continue
                if max_cost is not None and new_total_cost > max_cost:
                    continue

                new_node = TreeNode(state, parent=node, operator_cost=cost)
                visited.add(k)
                queue.append(new_node)

        return None

    @staticmethod
    def dfs(initial_state, goal_state_func, operators_func, depth_limit=None, max_cost=None) -> TreeNode | None:
        root = TreeNode(initial_state)
        stack = deque([(root, 0)])

        while stack:
            node, depth = stack.pop()

            if goal_state_func(node.state):
                return node

            if depth_limit is not None and depth >= depth_limit:
                continue

            successors = operators_func(node.state)

            # reversed para manter ordem mais previsível
            for state, cost in reversed(successors):
                new_total_cost = node.cost + cost
                k = SearchAlgorithms._key(state)

                if SearchAlgorithms._state_in_path(node, k):
                    continue
                if max_cost is not None and new_total_cost > max_cost:
                    continue

                new_node = TreeNode(state, parent=node, operator_cost=cost)
                stack.append((new_node, depth + 1))

        return None

    @staticmethod
    def dfs_limited(initial_state, goal_state_func, operators_func, depth_limit, max_cost=None) -> TreeNode | None:
        return SearchAlgorithms.dfs(
            initial_state,
            goal_state_func,
            operators_func,
            depth_limit=depth_limit,
            max_cost=max_cost,
        )

    @staticmethod
    def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit, max_cost=None) -> TreeNode | None:
        for depth in range(depth_limit + 1):
            result = SearchAlgorithms.dfs_limited(
                initial_state,
                goal_state_func,
                operators_func,
                depth_limit=depth,
                max_cost=max_cost,
            )
            if result is not None:
                return result
        return None

    @staticmethod
    def greedy(initial_state, goal_state_func, operators_func, heuristic_func, max_cost=None) -> TreeNode | None:
        root = TreeNode(initial_state)
        frontier = []
        SearchAlgorithms._push_heap(frontier, heuristic_func(root), root)

        visited = set()

        while frontier:
            _, node = SearchAlgorithms._pop_heap(frontier)
            k_node = SearchAlgorithms._key(node.state)

            if k_node in visited:
                continue
            visited.add(k_node)

            if goal_state_func(node.state):
                return node

            for state, cost in operators_func(node.state):
                new_total_cost = node.cost + cost
                k = SearchAlgorithms._key(state)

                if k in visited:
                    continue
                if max_cost is not None and new_total_cost > max_cost:
                    continue

                new_node = TreeNode(state, parent=node, operator_cost=cost)
                SearchAlgorithms._push_heap(frontier, heuristic_func(new_node), new_node)

        return None

    @staticmethod
    def a_star(initial_state, goal_state_func, operators_func, heuristic_func, max_cost=None) -> TreeNode | None:
        return SearchAlgorithms.weighted_a_star(
            initial_state,
            goal_state_func,
            operators_func,
            heuristic_func,
            weight=1.0,
            max_cost=max_cost,
        )

    @staticmethod
    def weighted_a_star(initial_state, goal_state_func, operators_func, heuristic_func, weight=1.0, max_cost=None) -> TreeNode | None:
        root = TreeNode(initial_state)
        frontier = []

        root_f = root.cost + weight * heuristic_func(root)
        SearchAlgorithms._push_heap(frontier, root_f, root)

        best_g = {SearchAlgorithms._key(initial_state): 0}

        while frontier:
            _, node = SearchAlgorithms._pop_heap(frontier)
            k_node = SearchAlgorithms._key(node.state)

            if node.cost > best_g.get(k_node, float("inf")):
                continue

            if goal_state_func(node.state):
                return node

            for state, cost in operators_func(node.state):
                new_cost = node.cost + cost
                k = SearchAlgorithms._key(state)

                if max_cost is not None and new_cost > max_cost:
                    continue

                if new_cost < best_g.get(k, float("inf")):
                    best_g[k] = new_cost
                    new_node = TreeNode(state, parent=node, operator_cost=cost)
                    f_score = new_cost + weight * heuristic_func(new_node)
                    SearchAlgorithms._push_heap(frontier, f_score, new_node)

        return None

    @staticmethod
    def uniform_cost(initial_state, goal_state_func, operators_func, max_cost=None) -> TreeNode | None:
        root = TreeNode(initial_state)
        frontier = []
        SearchAlgorithms._push_heap(frontier, 0, root)

        cost_so_far = {SearchAlgorithms._key(initial_state): 0}

        while frontier:
            current_cost, node = SearchAlgorithms._pop_heap(frontier)
            k_node = SearchAlgorithms._key(node.state)

            if current_cost > cost_so_far.get(k_node, float("inf")):
                continue

            if goal_state_func(node.state):
                return node

            for state, op_cost in operators_func(node.state):
                new_cost = current_cost + op_cost
                k = SearchAlgorithms._key(state)

                if max_cost is not None and new_cost > max_cost:
                    continue

                if new_cost < cost_so_far.get(k, float("inf")):
                    cost_so_far[k] = new_cost
                    new_node = TreeNode(state, parent=node, operator_cost=op_cost)
                    SearchAlgorithms._push_heap(frontier, new_cost, new_node)

        return None

    @staticmethod
    def extract_path(node: TreeNode) -> list[GameState]:
        path = []
        while node is not None:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))