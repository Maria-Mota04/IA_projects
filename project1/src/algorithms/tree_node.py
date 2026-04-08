class TreeNode:
    def __init__(self, state, parent=None, operator_cost=0, path_set=None) -> None:
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = operator_cost if parent is None else parent.cost + operator_cost

        if path_set is not None:
            self.path_set = path_set.copy()
        else:
            self.path_set = set()
        self.path_set.add(state)

    def add_child(self, child_node, operator_cost=0) -> None:
        self.children.append(child_node)
        child_node.parent = self
        child_node.cost = self.cost + operator_cost
        child_node.path_set = self.path_set.copy()
        child_node.path_set.add(child_node.state)
