import copy

class ActionHistory:

    def __init__(self):
        self.stack = []

    def save(self, tree, bst=None):
        capture = {
            "tree": copy.deepcopy(tree),
            "bst": copy.deepcopy(bst) if bst else None
        }
        self.stack.append(capture)

    def undo(self, tree, bst=None):
        if not self.stack:
            print("No actions to undo")
            return

        previous = self.stack.pop()
        tree.root = previous["tree"].root
        if bst and previous["bst"]:
            bst.root = previous["bst"].root