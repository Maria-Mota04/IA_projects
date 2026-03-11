class TreeNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.cost = 0

    def add_child(self, child_node, operator_cost=0):
        self.children.append(child_node)
        child_node.cost = self.cost + operator_cost
        child_node.parent = self
