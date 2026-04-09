class TreeNode:
    def __init__(self, state, parent=None, operator_cost=0) -> None:
        self.state = state
        self.parent = parent
        self.cost = operator_cost if parent is None else parent.cost + operator_cost

    def add_child(self, child_node, operator_cost=0) -> None:
        child_node.parent = self
        child_node.cost = self.cost + operator_cost
