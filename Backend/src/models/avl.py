from models.tree import Tree
from models.node import Node


class AVL(Tree):

    def __init__(self):
        super().__init__()
        self.rotations = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}
        self.auto_balance = True  #  Interruptor para balancear automaticamente

    # método de insertar para verificar si no hay raíz
    # cuando no hay raíz, se crea el nodo y se asigna como raiz
    # cuando si hay raiz se procede a insertar llamando a la función privada con la raiz del árbol y el nodo a insertar
    def insert(self, node):
        # verificar si no hay raiz para asignar el nuevo como raiz
        if self.root is None:
            self.root = node
        else:
            self.__insert(self.root, node)

    # Método recursivo para insertar un nodo cuando se tiene raiz en el árbol
    def __insert(self, currentRoot, node):
        if node.getValue().getCodigoComp() == currentRoot.getValue().getCodigoComp():
            print(f"El valor del nodo {node.getValue().getCodigo} ya existe en el árbol.")
        else:
            # se verifica si el valor a insertar es mayor que el actual raiz
            if node.getValue().getCodigoComp() > currentRoot.getValue().getCodigoComp():
                # se verifica si existe un hijo derecho
                if currentRoot.getRightChild() is None:
                    # si no tiene hijo derecho, se asigna el nodo como hijo derecho
                    currentRoot.setRightChild(node)
                    # y el nuevo nodo tendrá como padre a la actual raiz
                    node.setParent(currentRoot)
                    # verificar si se desbalancea segun el modo estres
                    if self.auto_balance:
                        self.checkBalance(
                            currentRoot
                        )  # Aqui sucederia el balanceo automatico
                else:
                    # ya tiene hijo derecho, entonces se debe procesar la inserción desde el hijo derecho
                    # haciendo el llamado recursivo con ese hijo
                    self.__insert(currentRoot.getRightChild(), node)
            else:
                # el valor del nodo a insertar es menor que el valor de la actual raiz
                # se verifica si tiene hijo izquierdo
                if currentRoot.getLeftChild() is None:
                    # si no tiene se asigna el nodo como hijo izquierdo
                    currentRoot.setLeftChild(node)
                    # y al nuevo nodo se le asigna como padre a la actual raiz
                    node.setParent(currentRoot)
                    # verificar desbalanceo segun el modo estres
                    if self.auto_balance:
                        self.checkBalance(currentRoot)
                else:
                    # si tiene hijo izquierdo, entonces se llama recursivamente por el hijo izquierdo con el nodo a insertar.
                    self.__insert(currentRoot.getLeftChild(), node)

    # INICIO DE MÉTODOS DEL BALANCEO DEL ÁRBOL AVL
    # -----------------------------------------------------------

    # Método para chequear el balanceo de un árbol a partir de un nodo
    def checkBalance(self, node):
        if node is None:
            return
        self.__checkBalance(node)

    # Método recursivo para validar el balanceo de un árbol
    def __checkBalance(self, node):
        bf = self.getBalanceFactor(node)
        print(f"checkBalance en {node.getValue().getCodigo} bf={bf}")
        print(f"Chequeando {node.getValue().getCodigo} | BF: {bf}")
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

    # método para el giro simple a la derecha
    def __rotateRight(self, topNode):
        # se obtiene el nodo de la mitad
        middleNode = topNode.getLeftChild()

        if middleNode is None:
            return

        # se obtiene el padre del nodo superior, cuando es la raiz será None
        parentTopNode = topNode.getParent()

        # se obtiene el hijo derecho del nodo de la mitad
        rightChildOfMiddleNode = middleNode.getRightChild()

        # se mueve el superior como hijo derecho del nodo de la mitad
        middleNode.setRightChild(topNode)
        topNode.setParent(middleNode)

        # reacomodar al nodo padre del superior apuntando al de la mitad
        # verificar si el superior era la raiz
        if parentTopNode is None:
            self.root = middleNode
            middleNode.setParent(None)
        else:
            if parentTopNode.getLeftChild() == topNode:
                parentTopNode.setLeftChild(middleNode)
            else:
                parentTopNode.setRightChild(middleNode)
            # sin importar si era hijo izq o derecho, se asigna ese padre del superior como padre del nodo de la mitad
            middleNode.setParent(parentTopNode)
        # reasignar el hijo derecho del nodo de la mitad al nodo superior que ya bajó como hijo derecho del nodo de la mitad
        topNode.setLeftChild(rightChildOfMiddleNode)
        if rightChildOfMiddleNode is not None:
            rightChildOfMiddleNode.setParent(topNode)

        # After rotation, depths change: recalculate critical flags and prices
        self.recalculatePrices()

        # método para el giro simple a la izquierda

    def __rotateLeft(self, topNode):
        # se obtiene el nodo de la mitad
        middleNode = topNode.getRightChild()

        if middleNode is None:
            return

        # se obtiene el padre del nodo superior, cuando es la raiz será None
        parentTopNode = topNode.getParent()

        # se obtiene el hijo izquierdo del nodo de la mitad
        leftChildOfMiddleNode = middleNode.getLeftChild()

        # se mueve el superior como hijo izquierdo del nodo de la mitad
        middleNode.setLeftChild(topNode)
        topNode.setParent(middleNode)

        # reacomodar al nodo padre del superior apuntando al de la mitad
        # verificar si el superior era la raiz
        if parentTopNode is None:
            self.root = middleNode
            middleNode.setParent(None)
        else:
            if parentTopNode.getLeftChild() == topNode:
                parentTopNode.setLeftChild(middleNode)
            else:
                parentTopNode.setRightChild(middleNode)
            # sin importar si era hijo izq o derecho, se asigna ese padre del superior como padre del nodo de la mitad
            middleNode.setParent(parentTopNode)

        # reasignar el hijo izquierdo del nodo de la mitad al nodo superior que ya bajó como hijo izquierdo del nodo de la mitad
        topNode.setRightChild(leftChildOfMiddleNode)
        if leftChildOfMiddleNode is not None:
            leftChildOfMiddleNode.setParent(topNode)

        # After rotation, depths change: recalculate critical flags and prices
        self.recalculatePrices()

    # método para identificar el caso de desbalanceo
    def getBalanceCase(self, node, bf):
        bfCase = ""
        if bf < -1:
            bfChild = self.getBalanceFactor(node.getRightChild())
            print(f"  → bfChild en caso R: {bfChild}")
            # caso negativo, va por R
            if bfChild <= 0:
                bfCase = "RR"
            else:
                bfCase = "RL"
        else:
            bfChild = self.getBalanceFactor(node.getLeftChild())
            # caso positivo, va por L
            if bfChild >= 0:
                bfCase = "LL"
            else:
                bfCase = "LR"
        return bfCase

    # Método para calcular el BF de un nodo
    def getBalanceFactor(self, node):
        if node is None:
            return 0
        leftChildHeight = self.getHeightNode(node.getLeftChild())
        rightChildHeight = self.getHeightNode(node.getRightChild())
        return leftChildHeight - rightChildHeight

    # deleteMinRentabilidad sí o sí debe estar en AVL porque es quien sabe rebalancear.

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


    # No balancea automaticamente, hace parte de la prueba estres
    def enable_stress_mode(self):
        self.auto_balance = False

    # Si se balancea automaticamente, hace parte de la prueba estres
    def enable_auto_balance(self):
        self.auto_balance = True

    def rebalance_all(self):
        if self.root is None:
            return {}

        initial_rotations = self.rotations.copy()

        # 1. Obtener nodos en orden (BST ordenado)
        nodes = self.inOrderTraversal()

        # 2. Reconstruir árbol balanceado
        self.root = self.__build_balanced(nodes, 0, len(nodes) - 1)

        # 3. Recalcular precios
        self.recalculatePrices()

        # 4. Calcular costo (simulado)
        cost = {}
        for key in self.rotations:
            cost[key] = self.rotations[key] - initial_rotations[key]

        return cost
    
    def __build_balanced(self, nodes, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        root = nodes[mid]

        # Construir hijos
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