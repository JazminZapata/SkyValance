import copy
class ActionHistory:

    def __init__(self):
        self.stack = []

    def save(self, tree):
        capture = copy.deepcopy(tree)
        self.stack.append(capture)

    def undo(self, tree):
        if not self.stack:
            print("No actions to undo")
            return

        previousTree = self.stack.pop()
        tree.root = previousTree.root
        
        