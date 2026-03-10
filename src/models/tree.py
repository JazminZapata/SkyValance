class Tree:
    
    
  # constructor del árbol que se crea inicialmente con una raiz vacía
  def __init__(self):
    self.root = None
    
    
  def insert(self, node):
    # verificar si no hay raiz para asignar el nuevo como raiz
    if self.root is None:
      self.root = node
    else:
      self.__insert(self.root, node)
      
    
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

  # Método recursivo para el recorrido Pre-Order
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

  # Método recursivo para el recorrido Pre-Order
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

    # Llamamos al recorrido por anchura que nos devolverá una hoja en el último nivel
    result = self.copyBreadthFirstSearch()

    # Guardamos ese nodo
    lastNode = result[len(result) - 1]
    parents = []
    parents[0] = lastNode
    n = 0

    # Mientras los nodos por encima de la última hoja tengan padre se llenará una lista con ellos (padres)
    while parents[n].getParent() is not None:
      parents[n+1] = parents[n].getParent()
      n = n + 1

    # La cantidad de padres encima de la hoja determinará el número de aristas que hay hasta llegar a el desde la raíz
    return len(parents)

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
    
    
    
    
