import json

class Tree:
    # constructor del árbol que se crea inicialmente con una raiz vacía
    def __init__(self):
            self.root = None
            self.limite = 3 
            self.queue = []# Limite de profundidad para considerar un nodo como crítico, se puede ajustar según necesidades

    # Item 6 :
    # Method for defining the critical depth limit
    def setLimite(self, nuevo_limite: int):
        # Updates the critical depth limit and triggers a full price recalculation
        # Can be called before loading JSON or at any point during execution
        self.limite = nuevo_limite
        self.recalculatePrices()

    def recalculatePrices(self):
        # Traverses all nodes and updates isCritical flag and finalPrice
        # Must be called after setLimite(), insertions, deletions or rebalancing
        # since rotations change node depths
        if self.root is None:
            return

        for node in self.copyBreadthFirstSearch():
            is_critical = self.isCritical(node)
            node.setIsCritical(is_critical)
            price = node.getValue().getPrecioBase()
            # Apply 25% surcharge if node exceeds depth limit
            if is_critical:
                price = price * 1.25
            # Apply 10% discount if flight has a promotion
            if node.getValue().getPromocion():
                price = price * 0.90
            node.setFinalPrice(price)  
    # Final Item 6.
    
    # Método para retornar la raiz del árbol
    def getRoot(self):
        return self.root
        
    def insert(self, node):
        # verificar si no hay raiz para asignar el nuevo como raiz
        if self.root is None:
            self.root = node
        else:
            self.__insert(self.root, node)

    # Método que permita realizar la búsqueda de un nodo mediante su valor
    # debe seguir la lógica de las reglas de un BST
    def search(self, value):
        # validar si existe una raíz en el árbol
        if self.root is None:
            return None
        else:
            return self.__search(self.root, value)

    # función recursiva para atender la búsqueda
    def __search(self, currentRoot, value):
        # validar si el valor buscado es igual a la raiz actual
        # print(f"El valor del nodo es: {currentRoot.getValue()}")
        # print(f"Comparación: {currentRoot.getValue() == value}" )
        if currentRoot.getValue().getCodigoComp() == value:
            # si es así se retorna la actual raiz
            return currentRoot
        # sino se valida si se debe ir por la derecha o por la izquierda
        elif value > currentRoot.getValue().getCodigoComp():
            # si es mayor, se verifica que exista un hijo derecho
            # en caso de no existir se genera
            if currentRoot.getRightChild() is None:
                return None
            else:
                # se pasa la solicitud de búsqueda al hijo derecho
                return self.__search(currentRoot.getRightChild(), value)
        else:
            # si es menor, se verifica que exista un hijo izquierdo
            # en caso de no existir se genera
            if currentRoot.getLeftChild() is None:
                return None
            else:
                # se pasa la solicitud de búsqueda al hijo izquierdo
                return self.__search(currentRoot.getLeftChild(), value)

    # Método para dibujar el árbol en forma de árbol
    def print_tree(self):
        if self.root is None:
            print("El árbol está vacío.")
        else:
            self.__print_tree(self.root, "", True)

    # Methodo para imprimir el árbol BST
    def __print_tree(self, node=None, prefix="", is_left=True):
        if node is not None:
            # Print right subtree
            if node.getRightChild():
                new_prefix = prefix + ("│   " if is_left else "    ")
                self.__print_tree(node.getRightChild(), new_prefix, False)

            # Print current node
            connector = "└── " if is_left else "┌── "
            print(prefix + connector + str(node.getValue()))

            # Print left subtree
            if node.getLeftChild():
                new_prefix = prefix + ("    " if is_left else "│   ")
                self.__print_tree(node.getLeftChild(), new_prefix, True)

    # Método para recorrido en anchura
    def breadthFirstSearch(self):
        # verificar si el árbol está vacío
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # se encola la raíz de primera
            queue = [self.root]
            # resultado del recorrido
            result = []
            # mientras existan elementos en la cola (nodos)
            # se debe procesar con: desencolar, imprimir y encolar hijos
            while len(queue) > 0:
                # desencolar
                currentNode = queue.pop(0)
                # imprimir que es agregar al resultado
                result.append(currentNode.getValue())
                # se valida que tenga hijo derecho para encolarlo
                if currentNode.getLeftChild() is not None:
                    queue.append(currentNode.getLeftChild())
                # se valida que tenga hijo izquierdo para encolarlo
                if currentNode.getRightChild() is not None:
                    queue.append(currentNode.getRightChild())
            return result

    def copyBreadthFirstSearch(self):
        # verificar si el árbol está vacío
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # se encola la raíz de primera
            queue = [self.root]
            # resultado del recorrido
            result = []
            # mientras existan elementos en la cola (nodos)
            # se debe procesar con: desencolar, imprimir y encolar hijos
            while len(queue) > 0:
                # desencolar
                currentNode = queue.pop(0)
                # imprimir que es agregar al resultado
                result.append(currentNode)
                # se valida que tenga hijo derecho para encolarlo
                if currentNode.getLeftChild() is not None:
                    queue.append(currentNode.getLeftChild())
                # se valida que tenga hijo izquierdo para encolarlo
                if currentNode.getRightChild() is not None:
                    queue.append(currentNode.getRightChild())
            return result

    # Método para realizar el recorrido en profundidad tipo  Pre-Order
    def preOrderTraversal(self):
        # validar si el árbol está vacío y mostrar mensaje
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # si el árbol no está vacío, se genera un result que tendrá el recorrido al final
            result = []
            # se inicia el llamado recursivo por la raiz del árbol
            self.__preOrderTraversal(self.root, result)
            return result

    # Método recursivo para el recorrido Pre-Order
    def __preOrderTraversal(self, currentRoot, result):
        # Se imprime (agrega a la cola) la raiz actual
        result.append(currentRoot)

        # se verifica si tiene hijo izquierdo para seguir el recorrido por él
        if currentRoot.getLeftChild() is not None:
            self.__preOrderTraversal(currentRoot.getLeftChild(), result)

        # se verifica si tiene hijo derecho para seguir el recorrido por él
        if currentRoot.getRightChild() is not None:
            self.__preOrderTraversal(currentRoot.getRightChild(), result)

    # Método para realizar el recorrido en profundidad tipo  In-Order
    def inOrderTraversal(self):
        # validar si el árbol está vacío y mostrar mensaje
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # si el árbol no está vacío, se genera un result que tendrá el recorrido al final
            result = []
            # se inicia el llamado recursivo por la raiz del árbol
            self.__inOrderTraversal(self.root, result)
            return result

    # Método recursivo para el recorrido In-Order
    def __inOrderTraversal(self, currentRoot, result):
        # se verifica si tiene hijo izquierdo para seguir el recorrido por él
        if currentRoot.getLeftChild() is not None:
            self.__inOrderTraversal(currentRoot.getLeftChild(), result)

        # Se imprime (agrega a la cola) la raiz actual
        result.append(currentRoot)

        # se verifica si tiene hijo derecho para seguir el recorrido por él
        if currentRoot.getRightChild() is not None:
            self.__inOrderTraversal(currentRoot.getRightChild(), result)

    # Método para realizar el recorrido en profundidad tipo  Pos-Order
    def posOrderTraversal(self):
        # validar si el árbol está vacío y mostrar mensaje
        if self.root is None:
            print("El árbol está vacío.")
        else:
            # si el árbol no está vacío, se genera un result que tendrá el recorrido al final
            result = []
            # se inicia el llamado recursivo por la raiz del árbol
            self.__posOrderTraversal(self.root, result)
            return result

    # Método recursivo para el recorrido Pos-Order
    def __posOrderTraversal(self, currentRoot, result):
        # se verifica si tiene hijo izquierdo para seguir el recorrido por él
        if currentRoot.getLeftChild() is not None:
            self.__posOrderTraversal(currentRoot.getLeftChild(), result)

        # se verifica si tiene hijo derecho para seguir el recorrido por él
        if currentRoot.getRightChild() is not None:
            self.__posOrderTraversal(currentRoot.getRightChild(), result)

        # Se imprime (agrega a la cola) la raiz actual
        result.append(currentRoot)

    # Cantidad de aristas que hay desde la raíz hasta la hoja más lejana  (Altura del árbol)
    def heightTree(self):
        # Obtenemos los nodos para buscar el último
        result = self.copyBreadthFirstSearch()

        if not result:
            return 0

        # Guardamos el último nodo visitado por BFS (el más profundo o lejano)
        lastNode = result[len(result) - 1]

        # Creamos la lista y agregamos el primer nodo
        parents = []
        parents.append(lastNode)

        # Mientras el nodo actual tenga padre, lo agregamos a la lista
        # Usamos un puntero simple en lugar de un índice 'n'
        currentNode = lastNode
        while currentNode.getParent() is not None:
            currentNode = currentNode.getParent()
            parents.append(currentNode)

        # La altura suele ser el número de aristas (nodos en el camino - 1)
        return len(parents) - 1

    # Método que permite calcular la altura de un nodo
    def getHeightNode(self, node):
        if node is None:
            return -1
        else:
            return self.__getHeightNode(node)

    # Cálculo recursivo de la altura de un nodo
    def __getHeightNode(self, node):
        # si es None se debe retornar -1 para equilibrar el +1 de su padre
        if node is None:
            return -1
        else:
            # se verifica altura por hijo izquierdo
            leftHeight = self.__getHeightNode(node.getLeftChild())
            # se verifica altura por hijo derecho
            rightHeight = self.__getHeightNode(node.getRightChild())
            # se obtiene el mayor valor de las alturas calculadas
            maxHeight = max(leftHeight, rightHeight)
            # se incrementa en 1 al retornar al padre para representar la arista que los une
            return maxHeight + 1

    # Cantidad de Nodos (Peso del árbol)
    def treeWeight(self):
        result = self.breadthFirstSearch()
        return len(result)

    # Método para eliminar
    def delete(self, value):
        if self.root is None:
            print("El árbol está vacío.")
        else:
            node = self.__search(self.root, value)
            if node is None:
                print(f"El valor {value} no se encuentra en el árbol.")
            else:
                self.__deleteNode(node)

    # Método que evalúa cada uno de los casos de eliminar y procede según sea
    def __deleteNode(self, node):
        # identificar el caso de eliminación
        nodeCase = self.IdentifyDeletionCase(node)
        match nodeCase:
            case 1:
                self.__deleteLeafNode(node)
            case 2:
                self.__deleteNodeWithOneChild(node)
            case 3:
                self.__deleteNodeWithTwoChildren(node)

    # Método que permite eliminar un nodo hoja del árbol
    def __deleteLeafNode(self, node):
        # Si el nodo es la raíz (no tiene padre), simplemente vaciar el árbol
        if node.getParent() is None:
            self.root = None
            return
        if node.getValue().getCodigoComp() < node.getParent().getValue().getCodigoComp():
            node.getParent().setLeftChild(None)
        else:
            node.getParent().setRightChild(None)
        node.setParent(None)

# Método que permite eliminar un nodo con un hijo del árbol
    def __deleteNodeWithOneChild(self, node):
        if node.getLeftChild() is not None:
            child = node.getLeftChild()
        else:
            child = node.getRightChild()

        if node.getParent() is not None:
            if node.getParent().getLeftChild() == node:
                node.getParent().setLeftChild(child)
            else:
                node.getParent().setRightChild(child)
        else:
            self.root = child

        if child is not None:
            child.setParent(node.getParent())

        # Desconectar el nodo eliminado del árbol
        node.setParent(None)
        node.setLeftChild(None)
        node.setRightChild(None)
    

    # eliminar nodo con dos hijos usando el predecesor
    def __deleteNodeWithTwoChildren(self, node):

        # buscar el predecesor
        predecesor = node.getLeftChild()

        while predecesor.getRightChild() is not None:
            predecesor = predecesor.getRightChild()

        parentPred = predecesor.getParent()

        # desconectar el predecesor de su posición actual
        if parentPred != node:
            parentPred.setRightChild(predecesor.getLeftChild())

            if predecesor.getLeftChild() is not None:
                predecesor.getLeftChild().setParent(parentPred)

            predecesor.setLeftChild(node.getLeftChild())
            node.getLeftChild().setParent(predecesor)

        # conectar hijo derecho del nodo eliminado
        predecesor.setRightChild(node.getRightChild())

        if node.getRightChild() is not None:
            node.getRightChild().setParent(predecesor)

        # conectar el predecesor con el padre del nodo eliminado
        parentNode = node.getParent()
        predecesor.setParent(parentNode)

        if parentNode is None:
            self.root = predecesor
        else:
            if parentNode.getLeftChild() == node:
                parentNode.setLeftChild(predecesor)
            else:
                parentNode.setRightChild(predecesor)

        # limpiar el nodo eliminado
        node.setLeftChild(None)
        node.setRightChild(None)
        node.setParent(None)

    # Obtener los nodos de un subárbol a partir de un nodo raíz dada.
    def get_subtree_nodes(self, node):
        nodes = []

        def traverse(n):
            if n is not None:
                nodes.append(n)
                traverse(n.getLeftChild())
                traverse(n.getRightChild())

        traverse(node)
        return nodes

    # Método para identificar cuál es el caso de eliminación
    # 1. Nodo hoja
    # 2. Nodo con un hijo
    # 3. Nodo con 2 hijos
    def IdentifyDeletionCase(self, node):
        nodeCase = 2
        if node.getLeftChild() is None and node.getRightChild() is None:
            nodeCase = 1
        elif node.getLeftChild() is not None and node.getRightChild() is not None:
            nodeCase = 3
        return nodeCase
    
    def toJSON(self, node):
        if node is None:
            return None

        flight = node.getValue()

        return {
            "codigo": flight.getCodigo(),
            "origen": flight.getOrigen(),
            "destino": flight.getDestino(),
            "horaSalida": flight.getHoraSalida(),
            "precioBase": flight.getPrecioBase(),
            "precioFinal": node.getFinalPrice(self),  # Calculate final price based on current critical status
            "pasajeros": flight.getPasajeros(),
            "promocion": flight.getPromocion(),
            "alerta": node.getIsCritical(),  # True if node exceeds the depth limit
            "altura": self.getHeightNode(node),
            "factorEquilibrio": self.getBalanceFactor(node),
            "prioridad": flight.getPriority(),
            "rentabilidad": self.getProfit(node),
            "izquierdo": self.toJSON(node.getLeftChild()),
            "derecho": self.toJSON(node.getRightChild())
        }

    def exportTree(self, filename="tree.json"):
        data = self.toJSON(self.root)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Árbol exportado correctamente")

    def isCritical(
        self, node
    ):  # “El método isCritical recibe un nodo como parámetro porque la condición de criticidad depende de su profundidad dentro del árbol.”
        profundidad = self.getDepth(node)
        return profundidad > self.limite

    def getDepth(self, node):
        profundidad = 0
        actual = node

        while actual.getParent() is not None:
            profundidad += 1
            actual = actual.getParent()

        return profundidad

    # Start Item 8.

    def getProfit(self, node):
        flight = node.getValue()
        #  We use the method finalPrice made by Andres to get the final price of the flight, this method already considers the promotion and the penalty if it applies, so we can be sure that we are using the correct price for the profitability calculation 
        finalPrice = node.getFinalPrice(self)
        # Base income
        profitability = flight.getPasajeros() * finalPrice
        # Discount
        if flight.getPromocion():
            profitability -= 50
        return profitability

    def findMinProfit(self):

        # We get all the nodes of the tree using BFS to evaluate them one by one and find the worst according to the criteria defined in the item 8.
        # We use BFS because we need to evaluate all the nodes and not just a path, and BFS allows us to do that level by level
        nodes = self.copyBreadthFirstSearch()

        # Variable to find the worst node 
        worst = None

        # We evaluate each node and compare it with the worst found so far 
        for node in nodes:

            # Calculate metrics for the current node
            p = self.getProfit(node)  # profitability
            depth = self.getDepth(node)  # depth
            codigo = node.getValue().getCodigoComp()  # numeric code

            # If it's the first node being evaluated, we set it as the worst by default
            if worst is None:
                worst = node
                continue

            # Calculate metrics for the worst node found so far
            p_worst = self.getProfit(worst)
            depth_worst = self.getDepth(worst)
            cod_worst = worst.getValue().getCodigoComp()

            # Lowest profibitality
            if p < p_worst:
                worst = node

            # Deeper in the tree if profitability is the same
            elif p == p_worst:
                if depth > depth_worst:
                    worst = node

                # If profitability and depth are the same, we choose the one with the higher code
                elif depth == depth_worst:
                    if codigo > cod_worst:
                        worst = node

        # Return selected node
        return worst

    # End Item 8.    
    
    def countLeaves(self):
        if self.root is None:
            return 0
        return self.__countLeaves(self.root)
    
    def __countLeaves(self, node):
        # caso base: si es hoja
        if node.getLeftChild() is None and node.getRightChild() is None:
            return 1

        leaves = 0

        # recorrer izquierda
        if node.getLeftChild() is not None:
            leaves += self.__countLeaves(node.getLeftChild())


        # recorrer derecha
        if node.getRightChild() is not None:
            leaves += self.__countLeaves(node.getRightChild())

        return leaves
    
    
    # Start Item 3.
    
    def insertionQueue(self, node):
        self.queue.append(node)
        
    
    def processNextInQueue(self):
      if len(self.queue) == 0:
        return None
    
      currentNode = self.queue.pop(0)
      self.insert(currentNode)
      
      conflict = None
      if self.isCritical(currentNode):
        conflict = f" {currentNode.getValue().getCodigo()} inserted at critical depth ({self.getDepth(currentNode)})"
    
      return currentNode, conflict
            
            
            
                    
        
        
