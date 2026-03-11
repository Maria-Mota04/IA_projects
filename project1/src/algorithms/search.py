from collections import deque
from tree_node import TreeNode


class SearchAlgorithms:
    @staticmethod
    def bfs(initial_state, goal_state_func, operators_func):

        root = TreeNode(initial_state)
        queue = deque([root])
        visited = {root.state}

        while queue:
            node = queue.popleft()
            if goal_state_func(node.state):
                return node

            for state, cost in operators_func(node.state):
                if state not in visited:
                    visited.add(state)
                    newNode = TreeNode(state)
                    node.add_child(newNode, cost)
                    queue.append(newNode)

        return None

    @staticmethod
    def dfs(initial_state, goal_state_func, operators_func):
        root = TreeNode(initial_state)

        queue = deque([root])

        visited = {root.state}

        while queue:
            node = queue.pop()
            if goal_state_func(node.state):
                return node

            for state, _ in operators_func(node.state):
                if state not in visited:
                    visited.add(state)
                    newNode = TreeNode(state)
                    node.add_child(newNode)
                    queue.append(newNode)

        return None

    @staticmethod
    def dfs_limited(initial_state, goal_state_func, operators_func, depth_limit):
        root = TreeNode(initial_state)

        queue = deque([(root, 0)])

        visited = {root.state}

        while queue:
            node, depth = queue.pop()
            if goal_state_func(node.state):
                return node

            for state, _ in operators_func(node.state):
                if state not in visited and depth + 1 <= depth_limit:
                    newDepth = depth + 1
                    visited.add(state)
                    newNode = TreeNode(state)
                    node.add_child(newNode)
                    queue.append((newNode, newDepth))

        return None

    @staticmethod
    def iterative_deepening_search(
        initial_state, goal_state_func, operators_func, depth_limit
    ):
        depth = 0
        while depth <= depth_limit:
            result = SearchAlgorithms.dfs_limited(
                initial_state, goal_state_func, operators_func, depth
            )
            if result is not None:
                return result

            depth += 1

        return None

    @staticmethod
    def greedy(initial_state, goal_state_func, operators_func, heuristic_func):
        root = TreeNode(initial_state)
        queue = [(root, heuristic_func(root))]

        visited = {initial_state}

        while queue:
            (node, _) = queue.pop(0)
            if goal_state_func(node.state):
                return node

            for state, op_cost in operators_func(node.state):
                newNode = TreeNode(state)
                node.add_child(newNode, op_cost)
                queue.append((newNode, heuristic_func(newNode)))
                visited.add(state)

            queue.sort(key=lambda x: x[1])

        return None

    @staticmethod
    def a_star(initial_state, goal_state_func, operators_func, heuristic_func):
        root = TreeNode(initial_state)

        queue = [(root, 0 + heuristic_func(root))]
        visited = {initial_state}

        while queue:
            (node, _) = queue.pop(0)
            if goal_state_func(node.state):
                return node

            for state, op_cost in operators_func(node.state):
                if state not in visited:
                    newNode = TreeNode(state)

                    node.add_child(newNode, op_cost)

                    queue.append((newNode, newNode.cost + heuristic_func(newNode)))
                    visited.add(state)

            queue.sort(key=lambda x: x[1])

        return None
