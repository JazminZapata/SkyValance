from tree import Tree


class AVL(Tree):

    def __init__(self):
        super().__init__()
        self.rotations = {"LL": 0, "RR": 0, "LR": 0, "RL": 0}

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
        if node.getValue().codigo_comp == currentRoot.getValue().codigo_comp:
            print(f"El valor del nodo {node.getValue().codigo} ya existe en el árbol.")
        else:
            # se verifica si el valor a insertar es mayor que el actual raiz
            if node.getValue().codigo_comp > currentRoot.getValue().codigo_comp:
                # se verifica si existe un hijo derecho
                if currentRoot.getRightChild() is None:
                    # si no tiene hijo derecho, se asigna el nodo como hijo derecho
                    currentRoot.setRightChild(node)
                    # y el nuevo nodo tendrá como padre a la actual raiz
                    node.setParent(currentRoot)
                    # verificar desbalanceo
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
                    # verificar desbalanceo
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
        if bf > 1 or bf < -1:
            # se identifica el caso de desbalanceo (LL, RR, RL, LR)
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
                    self.__rotateRight(node.getLeftChild())
                    self.__rotateLeft(node)

                case "RL":
                    self.rotations["RL"] += 1
                    self.__rotateLeft(node.getRightChild())
                    self.__rotateRight(node)

        else:
            # se verifica que el nodo actual no sea la raiz, y se invoca el chequeo de balanceo con su padre.
            # cuando es la raiz se finaliza la evaluación
            if node != self.root:
                # if node.getParent() is not None:
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
        # caso negativo, va por R
        if bf < -1:
            bfChild = self.getBalanceFactor(node.getRightChild())
            # caso negativo, va por R
            if bfChild < 0:
                bfCase = "RR"
            else:
                # caso positivo va por L
                bfCase = "RL"
        # caso positivo L
        else:
            bfChild = self.getBalanceFactor(node.getLeftChild())
            # caso positivo, va por L
            if bfChild > 0:
                bfCase = "LL"
            else:
                # caso negativo va por R
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
      # Call parent delete logic
      super().delete(value)
      # After deletion, depths may change — recalculate critical flags and prices
      self.recalculatePrices()
    # deleteMinProfit MUST be implemented in AVL because it knows how to rebalance.
    # Item 8.

    def deleteMinProfit(self):
        # Find the node with the lowest profitability
        node = self.findMinProfit()

        if node is None:
            print("No hay nodos para eliminar")
            return

        codigo = node.getValue().codigo_comp
        print(f"Eliminando nodo: {node.getValue().codigo}")
        print(f"Rentabilidad: {self.getProfit(node)}")

        # Save the parent BEFORE deleting, to rebalance from there upward
        parentNode = node.getParent()

        # Delete using the BST logic inherited from Tree
        self.delete(codigo)

        # Rebalance upward from where the node was removed
        if parentNode is not None:
            self.checkBalance(parentNode)
        elif self.root is not None:
            # Deleted node was root, rebalance from new root
            self.checkBalance(self.root)    
    
    # End Item 8.
