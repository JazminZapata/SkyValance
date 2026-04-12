import copy

class ActionHistory:

    def __init__(self):
        self.stack = []

    def save(self, tree, bst):
        capture = {
            "tree": copy.deepcopy(tree),
            "bst": copy.deepcopy(bst)
        }
        self.stack.append(capture)

    def undo(self, tree, bst):
        if not self.stack:
            print("No actions to undo")
            return

        previous = self.stack.pop()
        tree.root = previous["tree"].root
        bst.root = previous["bst"].root