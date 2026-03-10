from node import Node

class Tree:
  
  # constructor del árbol que se crea inicialmente con una raiz vacía
  def __init__(self):
    self.root = None

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
    #validar si existe una raíz en el árbol
    if self.root is None:
      raise Exception("El árbol no tiene una raíz.")
    else:
      return self.__search(self.root, value)

  # función recursiva para atender la búsqueda
  def __search(self, currentRoot, value):
    # validar si el valor buscado es igual a la raiz actual
    # print(f"El valor del nodo es: {currentRoot.getValue()}")
    # print(f"Comparación: {currentRoot.getValue() == value}" )
    if currentRoot.getValue() == value:
      # si es así se retorna la actual raiz
      return currentRoot
    # sino se valida si se debe ir por la derecha o por la izquierda
    elif value > currentRoot.getValue():
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
    if node.getValue() < node.getParent().getValue():
      node.getParent().setLeftChild(None)
    else:
      node.getParent().setRightChild(None)
    node.setParent(None)

  # Método que permite eliminar un nodo con un hijo del árbol
  def __deleteNodeWithOneChild(self, node):
    # preguntamos si el nodo a eliminar tiene hijo izquierdo
    if node.getLeftChild() is not None:
      #si tiene, entonces accedemos al padre de este nodo y preguntamos si el padre es mayor o menor
      #para determinar la posición final del hijo que reemplazará el nodo a eliminar
      if node.getParent().getValue() < node.getValue():
        node.getParent().setRightChild(node.getLeftChild())
      else:
        node.getParent().setLeftChild(node.getLeftChild())

      # Seteamos como nuevo padre del hijo izquierdo el que era su "abuelo" o padre del nodo a eliminar
      node.getLeftChild().setParent(node.getParent())
      node.setLeftChild(None)

    else:

      if node.getParent().getValue() > node.getValue():
        node.getParent().setLeftChild(node.getRightChild())
      else:
        node.getParent().setLeftChild(node.getRightChild())

      node.getRightChild().setParent(node.getParent())
      node.setRightChild(None)

    # Le quitamos el padre al nodo a eliminar
    node.setParent(None)
    

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

  # Método para identificar cuál es el caso de eliminación
  # 1. Nodo hoja
  # 2. Nodo con un hijo
  # 3. Nodo con 2 hijos
  def IdentifyDeletionCase(self, node):
    nodeCase = 2
    if(node.getLeftChild() is None and node.getRightChild() is None):
      nodeCase = 1
    elif(node.getLeftChild() is not None and node.getRightChild() is not None):
      nodeCase = 3
    return nodeCase