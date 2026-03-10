from node import Node
from bst import BST
from loader import loadTree

# Create an instance of the BST
tree = BST()

# Select the mode (we have to change this so the user can browse the file or select it from a list of options)
print("--- SISTEMA DE CARGA DE VUELOS ---")
tipo = int(input("Ingresa un número (1- Insercion, 2- Topología): "))

if tipo == 1:
    ruta = "Backend/json/ModoInserción.json" 
elif tipo == 2:
    ruta = "Backend/json/ModoTopología.json" 
else:
    print("Opción no válida")
    exit()

# LOADING THE TREE
# loadTree calls to buildByInsertion or buildByTopology 

loadTree(tree, ruta)

print("\n" + "="*30)
print("ÁRBOL CARGADO EXITOSAMENTE")
print("="*30)

#
# We use the method print_tree from Tree class to show it.
tree.print_tree()

print(f"\nTotal de vuelos (Peso): {tree.treeWeight()}")
print(f"Altura del árbol: {tree.heightTree()}")
print(f"Factor de balanceo del nodo raíz: {tree.root.getBalanceFactor()}")


print("--- CONSULTA DE NODOS  ---")

codigo = input("Ingresa el código del vuelo a consultar SU ALTURA: ")
node1 = tree.search(codigo)

print(f"Consultar altura de un nodo específico: {tree.getHeightNode(node1)}")