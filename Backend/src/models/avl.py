from models.tree import Tree
from models.node import Node


class AVL(Tree):

    def __init__(self):
        super().__init__()
        self.rotations = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        self.auto_balance = True  #  Interruptor to enable/disable automatic balancing, used for stress testing

    # Method to insert a node when there's no root 
    # When there's no root, we simply assign the new node as the root of the tree
    # When there is a root, we call the recursive method __insert to find the correct position for the new node and insert it there
    def insert(self, node):
        # Check if the tree is empty (no root)
        if self.root is None:
            self.root = node
        else:
            self.__insert(self.root, node)

    # Recursive method to find the correct position for the new node and insert it there
    def __insert(self, currentRoot, node):
        if node.getValue().getCodigoComp() == currentRoot.getValue().getCodigoComp():
            print(f"El valor del nodo {node.getValue().getCodigo} ya existe en el árbol.")
        else:
            # We compare the value of the node to be inserted with the value of the current root to determine if it should go to the left or right subtree
            if node.getValue().getCodigoComp() > currentRoot.getValue().getCodigoComp():
                # Check if it has a right child
                if currentRoot.getRightChild() is None:
                    # If it doesn't have a right child, we assign the node as the right child of the current root
                    currentRoot.setRightChild(node)
                    # and the new node is assigned the current root as its parent
                    node.setParent(currentRoot)
                    # check for imbalance according to the stress mode
                    if self.auto_balance:
                        self.checkBalance(
                            currentRoot
                        )  # Here automatic balancing is triggered after insertion 
                else:
                    # if it has a right child, then we call recursively on the right child with the node to be inserted,
                    # then we call recursively on the right child with the node to be inserted.
                    self.__insert(currentRoot.getRightChild(), node)
            else:
                # Node's code is less than current root's code, so it should go to the left subtree
                # Check if it has a left child
                if currentRoot.getLeftChild() is None:
                    # If it doesn't have a left child, we assign the node as the left child of the current root
                    currentRoot.setLeftChild(node)
                    # and the new node is assigned the current root as its parent
                    node.setParent(currentRoot)
                    # check for imbalance according to the stress mode
                    if self.auto_balance:
                        self.checkBalance(currentRoot)
                else:
                    # if it has a left child, then we call recursively on the left child with the node to be inserted.
                    self.__insert(currentRoot.getLeftChild(), node)


    # AVL TREE BALACING METHODS
    # -----------------------------------------------------------

    # Method to check the balance of a node and perform the necessary rotations if it is unbalanced
    def checkBalance(self, node):
        if node is None:
            return
        self.__checkBalance(node)

    # Recursive method to validate the balancing of a tree
    def __checkBalance(self, node):
        bf = self.getBalanceFactor(node)
        print(f"checkBalance en {node.getValue().getCodigo()} bf={bf}")
        print(f"Chequeando {node.getValue().getCodigo()} | BF: {bf}")
        if bf > 1 or bf < -1:
            bfCase = self.getBalanceCase(node, bf)
            print(f"  → caso: {bfCase}")
            print(f"  → Desbalance detectado! Caso: {bfCase}")
            match bfCase:
                case "LL":
                    self.rotations["LL"] += 1
                    self.__rotateRight(node)
                case "RR":
                    self.rotations["RR"] += 1
                    self.__rotateLeft(node)
                case "LR":
                    self.rotations["LR"] += 1
                    self.__rotateLeft(node.getLeftChild())
                    self.__rotateRight(node)
                case "RL":
                    self.rotations["RL"] += 1
                    self.__rotateRight(node.getRightChild())
                    self.__rotateLeft(node)
        else:
            if node != self.root:
                self.__checkBalance(node.getParent())

    # Method for performing a simple right rotation
    def __rotateRight(self, topNode):
        # we get middle node
        middleNode = topNode.getLeftChild()

        if middleNode is None:
            return

        # we get the parent of the top node, when it's the root it will be None
        parentTopNode = topNode.getParent()

        # se obtiene el hijo derecho del nodo de la mitad
        rightChildOfMiddleNode = middleNode.getRightChild()

        # we move the top node as the right child of the middle node
        middleNode.setRightChild(topNode)
        topNode.setParent(middleNode)

        # reaccomodate the parent of the top node pointing to the middle node
        # check if the top node was the root
        if parentTopNode is None:
            self.root = middleNode
            middleNode.setParent(None)
        else:
            if parentTopNode.getLeftChild() == topNode:
                parentTopNode.setLeftChild(middleNode)
            else:
                parentTopNode.setRightChild(middleNode)
            # without caring if it was a left or right child, we assign that parent of the top node as the parent of the middle node
            middleNode.setParent(parentTopNode)
        # reassign the right child of the middle node to the top node that has already moved down as the right child of the middle node
        topNode.setLeftChild(rightChildOfMiddleNode)
        if rightChildOfMiddleNode is not None:
            rightChildOfMiddleNode.setParent(topNode)

        # After rotation, depths change: recalculate critical flags and prices
        self.recalculatePrices()

        # method for performing a simple left rotation

    def __rotateLeft(self, topNode):
        # we get middle node
        middleNode = topNode.getRightChild()

        if middleNode is None:
            return

        # we get the parent of the top node, when it's the root it will be None
        parentTopNode = topNode.getParent()

        # we get the left child of the middle node
        leftChildOfMiddleNode = middleNode.getLeftChild()

        # we move the top node as the left child of the middle node
        middleNode.setLeftChild(topNode)
        topNode.setParent(middleNode)

        # reaccomodate the parent of the top node pointing to the middle node
        # check if the top node was the root
        if parentTopNode is None:
            self.root = middleNode
            middleNode.setParent(None)
        else:
            if parentTopNode.getLeftChild() == topNode:
                parentTopNode.setLeftChild(middleNode)
            else:
                parentTopNode.setRightChild(middleNode)
            # without caring if it was a left or right child, we assign that parent of the top node as the parent of the middle node
            middleNode.setParent(parentTopNode)

        # reassign the left child of the middle node to the top node that has already moved down as the left child of the middle node
        topNode.setRightChild(leftChildOfMiddleNode)
        if leftChildOfMiddleNode is not None:
            leftChildOfMiddleNode.setParent(topNode)

        # After rotation, depths change: recalculate critical flags and prices
        self.recalculatePrices()

    # method for identifying the balancing case
    def getBalanceCase(self, node, bf):
        bfCase = ""
        if bf < -1:
            bfChild = self.getBalanceFactor(node.getRightChild())
            print(f"  → bfChild en caso R: {bfChild}")
            # case negative, goes by R
            if bfChild <= 0:
                bfCase = "RR"
            else:
                bfCase = "RL"
        else:
            bfChild = self.getBalanceFactor(node.getLeftChild())
            # case positive, goes by L
            if bfChild >= 0:
                bfCase = "LL"
            else:
                bfCase = "LR"
        return bfCase

    # Method for calculating the BF of a node
    def getBalanceFactor(self, node):
        if node is None:
            return 0
        leftChildHeight = self.getHeightNode(node.getLeftChild())
        rightChildHeight = self.getHeightNode(node.getRightChild())
        return leftChildHeight - rightChildHeight

    # Necessary to recalculate prices in case the critical node, after removal
    def delete(self, value):
        node = self.search(value)
        parent = node.getParent() if node else None
    
        # Call parent delete logic
        super().delete(value)
        
        if self.auto_balance and parent is not None:
            self.checkBalance(parent)
        
        # After deletion, depths may change — recalculate critical flags and prices
        self.recalculatePrices()


    # it doesn't balance automatically, it just rebuilds the tree in a balanced way, used for stress testing
    def enable_stress_mode(self):
        self.auto_balance = False

    # If it balances automatically, it's part of the stress test
    def enable_auto_balance(self):
        self.auto_balance = True

    def rebalance_all(self):
        if self.root is None:
            return {}

        initial_rotations = self.rotations.copy()

        # 1. Get leaves first (nodes without children) using postorder traversal
        # PostOrder guarantees that we process children before parents → bottom-up cascade
        nodes = self.posOrderTraversal()

        # 2. Apply checkBalance at each node from bottom to top

        # __checkBalance already recursively moves up to the parent if there's no imbalance,

        # but here we call it node by node to force the cascading check
        visited = set()

        for node in nodes:
            # Evitar procesar nodos que ya fueron rotados y reasignados
            node_id = id(node)
            if node_id in visited:
                continue
            visited.add(node_id)

            bf = self.getBalanceFactor(node)
            if bf > 1 or bf < -1:
                bfCase = self.getBalanceCase(node, bf)
                match bfCase:
                    case "LL":
                        self.rotations["LL"] += 1
                        self.__rotateRight(node)
                    case "RR":
                        self.rotations["RR"] += 1
                        self.__rotateLeft(node)
                    case "LR":
                        self.rotations["LR"] += 1
                        self.__rotateLeft(node.getLeftChild())
                        self.__rotateRight(node)
                    case "RL":
                        self.rotations["RL"] += 1
                        self.__rotateRight(node.getRightChild())
                        self.__rotateLeft(node)

        # Avoid processing nodes that have already been rotated and reassigned
        self.recalculatePrices()

        # 4. Return differential cost of rotations
        cost = {}
        for key in self.rotations:
            cost[key] = self.rotations[key] - initial_rotations[key]

        return cost
    
    def __build_balanced(self, nodes, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        root = nodes[mid]

        # Build children
        left = self.__build_balanced(nodes, start, mid - 1)
        right = self.__build_balanced(nodes, mid + 1, end)

        root.setLeftChild(left)
        root.setRightChild(right)

        if left:
            left.setParent(root)
        if right:
            right.setParent(root)

        root.setParent(None)

        return root
    
    # Item 7 — AVL Audit System
    def auditAVL(self):
        nodes = self.copyBreadthFirstSearch()
        report = []
        inconsistent = []

        for node in nodes:
            codigo = node.getValue().getCodigo()
            bf = self.getBalanceFactor(node)
            real_height = self.getHeightNode(node)
            depth = self.getDepth(node)
            critical = node.getIsCritical()

            bf_ok = bf in (-1, 0, 1)
            height_ok = node.getHeight() is None or node.getHeight() == real_height
            is_ok = bf_ok and height_ok

            entry = {
                "codigo": codigo,
                "depth": depth,
                "balance_factor": bf,
                "height": real_height,
                "critical": critical,
                "bf_ok": bf_ok,
                "height_ok": height_ok,
                "ok": is_ok
            }
            report.append(entry)
            if not is_ok:
                inconsistent.append(codigo)

        total = len(nodes)
        valid = total - len(inconsistent)
        score = round((valid / total) * 100) if total > 0 else 0

        return {
            "total": total,
            "valid": valid,
            "inconsistent_count": len(inconsistent),
            "inconsistent_nodes": inconsistent,
            "score": score,
            "details": report
        }
    # End Item 7