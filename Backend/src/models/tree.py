import json

class Tree:
    # constructor of the tree that is initially created with an empty root and the limit for critical depth is set to 3 by default, also we create a queue to store the nodes that are going to be inserted in the tree when we use the insertion method for item 3.
    def __init__(self):
            self.root = None
            self.limite = 3 
            self.queue = []

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
            # Set alert flag based on critical status
            node.getValue().setAlerta(is_critical)
            price = node.getValue().getPrecioBase()
            # Apply 25% surcharge if node exceeds depth limit
            if is_critical:
                price = price * 1.25
            # Apply 10% discount if flight has a promotion
            if node.getValue().getPromocion():
                price = price * 0.90
            node.setFinalPrice(price)
    # Final Item 6.
    
    # Method to get the root of the tree
    def getRoot(self):
        return self.root
        
    def insert(self, node):
        # Verify if there is no root to assign the new node as root
        if self.root is None:
            self.root = node
        else:
            self.__insert(self.root, node)

    # Method that allows searching for a node in the tree based on the value of its flight code
    # It must follow the rules of a BST
    def search(self, value):
        # Verify if there is a root in the tree
        if self.root is None:
            return None
        else:
            return self.__search(self.root, value)

    # recursive function to handle the search
    def __search(self, currentRoot, value):
        # validate if the searched value is equal to the current root
        if currentRoot.getValue().getCodigoComp() == value:
            # if so, return the current root
            return currentRoot
        # otherwise, validate if we should go right or left
        elif value > currentRoot.getValue().getCodigoComp():
            # if it's greater, check if there's a right child
            # in case there isn't one, return None
            if currentRoot.getRightChild() is None:
                return None
            else:
                # Then pass the search request to the right child
                return self.__search(currentRoot.getRightChild(), value)
        else:
            # if it's smaller, check if there's a left child
            # in case there isn't one, return None
            if currentRoot.getLeftChild() is None:
                return None
            else:
                # Then pass the search request to the left child
                return self.__search(currentRoot.getLeftChild(), value)

    # Method to draw the tree in tree form
    def print_tree(self):
        if self.root is None:
            print("El árbol está vacío.")
        else:
            self.__print_tree(self.root, "", True)

    # Method to print the BST in tree form, it is similar to print_tree but it has a different structure to represent the BST properties
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

    # Method for breadth-first search
    def breadthFirstSearch(self):
        # verify if the tree is empty
        if self.root is None:
            print("The tree is empty.")
        else:
            # enqueue the root first
            queue = [self.root]
            # resultado del recorrido
            result = []
            # while there are elements in the queue (nodes)
            # process with: dequeue, print and enqueue children
            while len(queue) > 0:
                # dequeue
                currentNode = queue.pop(0)
                # print the current node's value
                result.append(currentNode.getValue())
                # validate if the current node has a right child to enqueue it
                if currentNode.getLeftChild() is not None:
                    queue.append(currentNode.getLeftChild())
                # validate if the current node has a left child to enqueue it
                if currentNode.getRightChild() is not None:
                    queue.append(currentNode.getRightChild())
            return result

    def copyBreadthFirstSearch(self):
        # verify if the tree is empty
        if self.root is None:
            print("The tree is empty.")
        else:
            # enqueue the root first
            queue = [self.root]
            # resultado del recorrido
            result = []
            # while there are elements in the queue (nodes)
            # process with: dequeue, print and enqueue children
            while len(queue) > 0:
                # dequeue
                currentNode = queue.pop(0)
                # print the current node's value
                result.append(currentNode)
                # validate if the current node has a right child to enqueue it
                if currentNode.getLeftChild() is not None:
                    queue.append(currentNode.getLeftChild())
                # validate if the current node has a left child to enqueue it
                if currentNode.getRightChild() is not None:
                    queue.append(currentNode.getRightChild())
            return result

    # Method for pre-order traversal
    def preOrderTraversal(self):
        # verify if the tree is empty and display message
        if self.root is None:
            print("The tree is empty.")
        else:
            # if the tree is not empty, generate a result that will have the traversal at the end
            result = []
            # initiate the recursive call from the root of the tree
            self.__preOrderTraversal(self.root, result)
            return result

    # Recursive method for pre-order traversal
    def __preOrderTraversal(self, currentRoot, result):
        # Print the current root
        result.append(currentRoot)

        # Check if the current root has a left child to continue the traversal
        if currentRoot.getLeftChild() is not None:
            self.__preOrderTraversal(currentRoot.getLeftChild(), result)

        # Check if the current root has a right child to continue the traversal
        if currentRoot.getRightChild() is not None:
            self.__preOrderTraversal(currentRoot.getRightChild(), result)

    # Method for in-order traversal
    def inOrderTraversal(self):
        # verify if the tree is empty and display message
        if self.root is None:
            print("The tree is empty.")
        else:
            # if the tree is not empty, generate a result that will have the traversal at the end
            result = []
            # initiate the recursive call from the root of the tree
            self.__inOrderTraversal(self.root, result)
            return result

    # Recursive method for in-order traversal
    def __inOrderTraversal(self, currentRoot, result):
        # Check if the current root has a left child to continue the traversal
        if currentRoot.getLeftChild() is not None:
            self.__inOrderTraversal(currentRoot.getLeftChild(), result)

        # Print the current root
        result.append(currentRoot)

        # Check if the current root has a right child to continue the traversal
        if currentRoot.getRightChild() is not None:
            self.__inOrderTraversal(currentRoot.getRightChild(), result)

    # Method for post-order traversal
    def posOrderTraversal(self):
        # verify if the tree is empty and display message
        if self.root is None:
            print("The tree is empty.")
        else:
            # if the tree is not empty, generate a result that will have the traversal at the end
            result = []
            # initiate the recursive call from the root of the tree
            self.__posOrderTraversal(self.root, result)
            return result

    # Recursive method for post-order traversal
    def __posOrderTraversal(self, currentRoot, result):
        # check if it has a left child to continue the traversal
        if currentRoot.getLeftChild() is not None:
            self.__posOrderTraversal(currentRoot.getLeftChild(), result)

        # check if it has a right child to continue the traversal
        if currentRoot.getRightChild() is not None:
            self.__posOrderTraversal(currentRoot.getRightChild(), result)

        # print (add to the list) the current root
        result.append(currentRoot)

    # Quantity of edges from the root to the farthest leaf (Height of the tree)
    def heightTree(self):
        # Get the nodes to find the last one
        result = self.copyBreadthFirstSearch()

        if not result:
            return 0

        # Save the last visited node by BFS (the deepest or farthest)
        lastNode = result[len(result) - 1]

        # We create the list and add the las node to it 
        parents = []
        parents.append(lastNode)

        # While current node has a parent, we add it to the list 
        # We use a simple pointer instead of an 'n'
        currentNode = lastNode
        while currentNode.getParent() is not None:
            currentNode = currentNode.getParent()
            parents.append(currentNode)

        # The height is usually the number of edges (nodes on the path - 1)
        return len(parents) - 1

    # MMethod that allows calculating the height of a node
    def getHeightNode(self, node):
        if node is None:
            return -1
        else:
            return self.__getHeightNode(node)

    # Recursive calculation of the height of a node
    def __getHeightNode(self, node):
        # if it is None, -1 should be returned to balance the +1 of its parent
        if node is None:
            return -1
        else:
            # height is verified by left child
            leftHeight = self.__getHeightNode(node.getLeftChild())
            # height is verified by right child
            rightHeight = self.__getHeightNode(node.getRightChild())
            # the maximum value of the calculated heights is obtained
            maxHeight = max(leftHeight, rightHeight)
            # It increases by 1 when returning to the parent to represent the edge that joins them
            return maxHeight + 1

    # Number of Nodes (Tree Weight)
    def treeWeight(self):
        result = self.breadthFirstSearch()
        return len(result)

    # Method to delete 
    def delete(self, value):
        if self.root is None:
            print("El árbol está vacío.")
        else:
            node = self.__search(self.root, value)
            if node is None:
                print(f"El valor {value} no se encuentra en el árbol.")
            else:
                self.__deleteNode(node)

    # Method that evaluates each case of elimination and proceeds accordingly
    def __deleteNode(self, node):
        # Identify deletion case
        nodeCase = self.IdentifyDeletionCase(node)
        match nodeCase:
            case 1:
                self.__deleteLeafNode(node)
            case 2:
                self.__deleteNodeWithOneChild(node)
            case 3:
                self.__deleteNodeWithTwoChildren(node)

    # Method that allows deleting a leaf node from the tree
    def __deleteLeafNode(self, node):
        # If the node is the root (has no parent), simply empty the tree
        if node.getParent() is None:
            self.root = None
            return
        if node.getValue().getCodigoComp() < node.getParent().getValue().getCodigoComp():
            node.getParent().setLeftChild(None)
        else:
            node.getParent().setRightChild(None)
        node.setParent(None)

# Method that allows deleting a node with one child from the tree
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

        # Disconnect the removed node from the tree
        node.setParent(None)
        node.setLeftChild(None)
        node.setRightChild(None)
    

    # Delete node with two children using the predecessor
    def __deleteNodeWithTwoChildren(self, node):

        # Look for the predecessor (the largest node in the left subtree)
        predecesor = node.getLeftChild()

        while predecesor.getRightChild() is not None:
            predecesor = predecesor.getRightChild()

        parentPred = predecesor.getParent()

        # Disconnect the predecessor from its current position
        if parentPred != node:
            parentPred.setRightChild(predecesor.getLeftChild())

            if predecesor.getLeftChild() is not None:
                predecesor.getLeftChild().setParent(parentPred)

            predecesor.setLeftChild(node.getLeftChild())
            node.getLeftChild().setParent(predecesor)

        # connect the predecessor with the right child of the node to be deleted
        predecesor.setRightChild(node.getRightChild())

        if node.getRightChild() is not None:
            node.getRightChild().setParent(predecesor)

        # connect the predecessor with the parent of the node to be deleted
        parentNode = node.getParent()
        predecesor.setParent(parentNode)

        if parentNode is None:
            self.root = predecesor
        else:
            if parentNode.getLeftChild() == node:
                parentNode.setLeftChild(predecesor)
            else:
                parentNode.setRightChild(predecesor)

        # Clean the eliminated node
        node.setLeftChild(None)
        node.setRightChild(None)
        node.setParent(None)

    # Get the nodes of a subtree starting from a given root node.
    def get_subtree_nodes(self, node):
        nodes = []

        def traverse(n):
            if n is not None:
                nodes.append(n)
                traverse(n.getLeftChild())
                traverse(n.getRightChild())

        traverse(node)
        return nodes

    # Method for identifying the deletion case
    # 1. Leaf node
    # 2. Node with one child
    # 3. Node with two children
    def IdentifyDeletionCase(self, node):
        nodeCase = 2
        if node.getLeftChild() is None and node.getRightChild() is None:
            nodeCase = 1
        elif node.getLeftChild() is not None and node.getRightChild() is not None:
            nodeCase = 3
        return nodeCase  
    
    # Start item 1.3
    
    def toJSON(self, node):
        if node is None:
            return None

        flight = node.getValue()

        return {
            "code": flight.getCodigo(),
            "origin": flight.getOrigen(),
            "destination": flight.getDestino(),
            "departureTime": flight.getHoraSalida(),
            "basePrice": flight.getPrecioBase(),
            "finalPrice": node.getFinalPrice(self),  # Calculate final price based on current critical status
            "passengers": flight.getPasajeros(),
            "promotion": flight.getPromocion(),
            "alert": node.getIsCritical(),  # True if node exceeds the depth limit
            "height": self.getHeightNode(node),
            "balanceFactor": self.getBalanceFactor(node),
            "profit": self.getProfit(node),
            "left": self.toJSON(node.getLeftChild()),
            "right": self.toJSON(node.getRightChild())
        }

    def exportTree(self, filename="tree.json"):
        # Convert the tree to a JSON-serializable structure starting from the root
        data = self.toJSON(self.root)
        
        # Write the JSON data to a file with indentation for readability and ensure_ascii=False to preserve special characters
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print("Tree exported correctly")
        
    # End item 1.3

    def isCritical(self, node):  # The isCritical method receives a node as a parameter because the criticality condition depends on its depth within the tree.”
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

        # Traverse left
        if node.getLeftChild() is not None:
            leaves += self.__countLeaves(node.getLeftChild())


        # Traverse right
        if node.getRightChild() is not None:
            leaves += self.__countLeaves(node.getRightChild())

        return leaves
    
    
    # Start Item 3.
    
    # Adds a node to the insertion queue.
    #This method does not insert the node into the tree immediately
    #Instead, it stores the node in a queue so it can be processed later, allowing controlled or step-by-step insertions
    def insertionQueue(self, node):
        self.queue.append(node)
        
    
    def processNextInQueue(self):
      if len(self.queue) == 0:
        return None
    
      #Get the next node in FIFO order
      currentNode = self.queue.pop(0)
      
      # Insert the node into the tree
      self.insert(currentNode)
      
      
      # Check for a critical condition after insertion
      conflict = None
      if self.isCritical(currentNode):
        conflict = f" {currentNode.getValue().getCodigo()} inserted at critical depth ({self.getDepth(currentNode)})"
    
      return currentNode, conflict
  
    # End Item 3.
            
            
            
                    
        
        
