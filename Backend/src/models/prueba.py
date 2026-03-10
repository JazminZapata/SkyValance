from node import Node
from bst import BST
from loader import loadTree

# crear árbol
tree = BST()
tree2 = BST()


loadTree(tree2, "Backend/json/ModoTopología.json")
print("LOADING TREES . . .")
print(tree2.root.getValue().codigo)
print(tree2.root.getLeftChild().getValue().codigo)
print(tree2.root.getRightChild().getValue().codigo)


# valores que vamos a insertar
values = [10, 5, 15, 3, 7, 12, 18]

# insertar nodos
for v in values:
    node = Node(v)
    tree.insert(node)

tree.print_tree()

# probar recorridos
print("BFS:")
print(tree.breadthFirstSearch())

print("\nPreOrder:")
print([node.getValue() for node in tree.preOrderTraversal()])

print("\nInOrder:")
print([node.getValue() for node in tree.inOrderTraversal()])

print("\nPostOrder:")
print([node.getValue() for node in tree.posOrderTraversal()])

print("\nPeso del árbol:")
print(tree.treeWeight())

print("\nAltura del árbol:")
print(tree.getHeightNode(tree.getRoot()))

# probar búsqueda
node = tree.search(7)
if node:
    print("\nNodo encontrado:", node.getValue())
else:
    print("\nNodo no encontrado")

# ------------------------
print("\nEliminar hoja (3)")
tree.delete(3)
tree.print_tree()

# ------------------------
print("\nEliminar nodo con un hijo (5)")
tree.delete(5)
tree.print_tree()

# ------------------------
print("\nEliminar nodo con dos hijos (15)")
tree.delete(15)
tree.print_tree()

# ------------------------
print("\nRecorrido BFS final:")
print(tree.breadthFirstSearch())



