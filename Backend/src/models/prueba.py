from .flight import Flight
from .node import Node
from .avl import AVL
from .bst import BST
from .loader import loadTree

# Crear árboles
avl = AVL()
bst = BST()

print("--- SISTEMA DE CARGA DE VUELOS ---")
tipo = int(input("Ingresa un número (1- Insercion, 2- Topología): "))

if tipo == 1:
    ruta = "Backend/json/ModoInserción.json"
elif tipo == 2:
    ruta = "Backend/json/ModoTopología.json"
else:
    print("Opción no válida")
    exit()

# Cargar árbol correctamente
loadTree(avl, bst, ruta)

print("\n" + "=" * 30)
print("ÁRBOLES CARGADOS EXITOSAMENTE")
print("=" * 30)

modo = tipo  # guardamos el modo elegido

# MODO INSERCIÓN
if modo == 1:

    print("\n--- AVL ---")
    avl.print_tree()
    print(f"Total de vuelos: {avl.treeWeight()}")
    print(f"Altura: {avl.heightTree()}")
    print(f"Balance raíz: {avl.getBalanceFactor(avl.root)}")

    print("\n--- BST ---")
    bst.print_tree()
    print(f"Total de vuelos: {bst.treeWeight()}")
    print(f"Altura: {bst.heightTree()}")


#  MODO TOPOLOGÍA
elif modo == 2:

    print("\n--- AVL ---")
    avl.print_tree()
    print(f"Total de vuelos: {avl.treeWeight()}")
    print(f"Altura: {avl.heightTree()}")
    print(f"Balance raíz: {avl.getBalanceFactor(avl.root)}")

    print("\n--- BST ---")
    print("No aplica en modo topología")
    
nuevo = Flight("SB1010", "Cali", "Bogotá", "10:00", 200, 50, False, False)
node = Node(nuevo)

avl.insert(node)
print(node.getValue().origen)  # Imprime el código del vuelo insertado

print("Nodo insertado")

print("\n--- AVL ACTUALIZADO ---")
avl.print_tree()
print(f"Balance raíz: {avl.getBalanceFactor(avl.root)}")


# MOSTRAR RENTABILIDADES
print("\n--- RENTABILIDAD DE NODOS ---")
for n in avl.copyBreadthFirstSearch():
    print(n.getValue().codigo, "→", avl.getRentabilidad(n))

#  ELIMINAR MENOR RENTABILIDAD
print("\n--- ELIMINANDO NODO DE MENOR RENTABILIDAD ---")
avl.deleteMinRentabilidad()

#  MOSTRAR ÁRBOL FINAL
print("\n--- AVL DESPUÉS DE ELIMINACIÓN ---")
avl.print_tree()


opcion = input("¿Deseas exportar el árbol? (s/n): ")

if opcion.lower() == "s":
    nombre_archivo = input("Ingresa el nombre del archivo ")
    avl.exportTree(nombre_archivo + ".json")
    

