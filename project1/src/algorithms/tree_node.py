class TreeNode:
    _counter = 0

    def __init__(self, state, parent=None, operator_cost=0) -> None:
        self.state = state
        self.parent = parent
        self.cost = operator_cost if parent is None else parent.cost + operator_cost
        self._id = TreeNode._counter
        TreeNode._counter += 1

    def __lt__(self, other):
        return self._id < other._id

    def add_child(self, child_node, operator_cost=0) -> None:
        child_node.parent = self
        child_node.cost = self.cost + operator_cost
