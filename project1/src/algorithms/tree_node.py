class TreeNode:
    _counter = 0

    def __init__(self, state, parent=None, operator_cost=0) -> None:
        """
        @brief Create a search tree node.

        @param state State wrapped by this node.
        @param parent Parent node in the search tree.
        @param operator_cost Step cost from parent to this node.
        """
        self.state = state
        self.parent = parent
        self.cost = operator_cost if parent is None else parent.cost + operator_cost
        self._id = TreeNode._counter
        TreeNode._counter += 1

    def __lt__(self, other):
        """@brief Provide deterministic ordering for priority queues."""
        return self._id < other._id
