# clase que permite instanciar nuevos nodos con sus atributo
class Node:

    # constructor para el nodo con hijos, padre y valor
    # We define the attributes (balaceFactor, finalPrice and height as specific attributes of the node)

    def __init__(self, flight):
        self.value = flight
        self.parent = None
        self.leftChild = None
        self.rightChild = None
        self.balanceFactor = None
        self.height = None
        self.finalPrice = None
        self.isCritical = False  # NodoCritico

    # asignación de un hijo derecho
    def setRightChild(self, node):
        self.rightChild = node

    # obtener el hijo derecho
    def getRightChild(self):
        return self.rightChild

    # asignar un hijo izquierdo
    def setLeftChild(self, node):
        self.leftChild = node

    # obtener el hijo izquierdo
    def getLeftChild(self):
        return self.leftChild

    # asignar un padre
    def setParent(self, node):
        self.parent = node

    # obtener el nodo padre
    def getParent(self):
        return self.parent

    # obtener el valor del nodo
    def getValue(self):
        return self.value

    def setBalanceFactor(self, balanceFactor):
        self.balanceFactor = balanceFactor
    
    def getBalanceFactor(self):
        return self.balanceFactor
    
    def setHeight(self, height):
        self.height = height
        
    def getHeight(self):
        return self.height
    
    def setFinalPrice(self, finalPrice):
        self.finalPrice = finalPrice
        
    def getFinalPrice(self, tree=None):
        # If tree is provided, compute dynamically based on criticality 25% surcharge
        if tree is not None:
            if tree.isCritical(self):
                return self.getValue().precioBase * 1.25
            return self.getValue().precioBase

        # or use cached finalPrice or precioBase
        if self.finalPrice is not None:
            return self.finalPrice
        return self.getValue().precioBase

    def setIsCritical(self, value: bool):
        # Sets whether this node is flagged as critical due to exceeding depth limit
        self.isCritical = value

    def getIsCritical(self):
        # Returns True if this node exceeds the tree's depth limit
        return self.isCritical
        
