from tree import Tree

class BST(Tree):

  def __init__(self):
    super().__init__()

  def insert(self, node):
    # verificar si no hay raiz para asignar el nuevo como raiz
    if self.root is None:
      self.root = node
    else:
      self.__insert(self.root, node)

  # Método recursivo para insertar un nodo cuando se tiene raiz en el árbol
  def __insert(self, currentRoot, node):
    if node.getValue() == currentRoot.getValue():
      print(f"El valor del nodo {node.getValue()} ya existe en el árbol.")
    else:
      # se verifica si el valor a insertar es mayor que el actual raiz
      if node.getValue() > currentRoot.getValue():
        # se verifica si existe un hijo derecho
        if currentRoot.getRightChild() is None:
          # si no tiene hijo derecho, se asigna el nodo como hijo derecho
          currentRoot.setRightChild(node)
          # y el nuevo nodo tendrá como padre a la actual raiz
          node.setParent(currentRoot)
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
        else:
          # si tiene hijo izquierdo, entonces se llama recursivamente por el hijo izquierdo con el nodo a insertar.
          self.__insert(currentRoot.getLeftChild(), node)

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

  

    
