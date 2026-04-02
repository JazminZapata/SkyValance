from models.flight import Flight
from models.node import Node
from models.avl import AVL
from models.bst import BST
from models.loader import loadTree

# Create trees
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

# Item 6 — set critical depth limit before loading JSON
limite_inicial = int(input("Ingresa la profundidad límite para nodos críticos: "))
avl.setLimite(limite_inicial)

# Load tree
loadTree(avl, bst, ruta)

print("\n" + "=" * 30)
print("ÁRBOLES CARGADOS EXITOSAMENTE")
print("=" * 30)

modo = tipo

# INSERTION MODE
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

# TOPOLOGY MODE
elif modo == 2:
    print("\n--- AVL ---")
    avl.print_tree()
    print(f"Total de vuelos: {avl.treeWeight()}")
    print(f"Altura: {avl.heightTree()}")
    print(f"Balance raíz: {avl.getBalanceFactor(avl.root)}")

    print("\n--- BST ---")
    print("No aplica en modo topología")

# Item 6 — show critical status after loading
print("\n--- PENALIZACIÓN POR PROFUNDIDAD CRÍTICA ---")
print(f"Límite actual: {avl.limite}")
for n in avl.copyBreadthFirstSearch():
    codigo = n.getValue().codigo
    depth = avl.getDepth(n)
    critical = n.getIsCritical()
    base = n.getValue().precioBase
    final = n.getFinalPrice()
    print(f"{codigo} | profundidad: {depth} | crítico: {critical} | base: ${base} | final: ${final}")

# Insert new node
nuevo = Flight("SB1010", "Cali", "Bogotá", "10:00", 200, 50, False, False)
node = Node(nuevo)
avl.insert(node)
print(node.getValue().origen) 

print("Nodo insertado")

print("\n--- AVL ACTUALIZADO ---")
avl.print_tree()
print(f"Balance raíz: {avl.getBalanceFactor(avl.root)}")

# Item 6 — show critical status after insertion (depths may have changed due to rotations)
print("\n--- PENALIZACIÓN TRAS INSERCIÓN ---")
print(f"Límite actual: {avl.limite}")
for n in avl.copyBreadthFirstSearch():
    codigo = n.getValue().codigo
    depth = avl.getDepth(n)
    critical = n.getIsCritical()
    base = n.getValue().precioBase
    final = n.getFinalPrice()
    print(f"{codigo} | profundidad: {depth} | crítico: {critical} | base: ${base} | final: ${final}")

# Show profitability
print("\n--- RENTABILIDAD DE NODOS ---")
for n in avl.copyBreadthFirstSearch():
    print(n.getValue().codigo, "→", avl.getProfit(n))


# Delete least profitable node
print("\n--- ELIMINANDO NODO DE MENOR RENTABILIDAD ---")
avl.deleteMinProfit()

print("\n--- AVL DESPUÉS DE ELIMINACIÓN ---")
avl.print_tree()

# Item 6 — show critical status after deletion
print("\n--- PENALIZACIÓN TRAS ELIMINACIÓN ---")
print(f"Límite actual: {avl.limite}")
for n in avl.copyBreadthFirstSearch():
    codigo = n.getValue().codigo
    depth = avl.getDepth(n)
    critical = n.getIsCritical()
    base = n.getValue().precioBase
    final = n.getFinalPrice()
    print(f"{codigo} | profundidad: {depth} | crítico: {critical} | base: ${base} | final: ${final}")

# Item 6 — allow runtime limit update
cambiar = input("\n¿Deseas cambiar el límite de profundidad? (s/n): ")
if cambiar.lower() == "s":
    nuevo_limite = int(input("Nuevo límite: "))
    avl.setLimite(nuevo_limite)
    print(f"\n--- PRECIOS RECALCULADOS CON LÍMITE {nuevo_limite} ---")
    for n in avl.copyBreadthFirstSearch():
        codigo = n.getValue().codigo
        depth = avl.getDepth(n)
        critical = n.getIsCritical()
        base = n.getValue().precioBase
        final = n.getFinalPrice()
        print(f"{codigo} | profundidad: {depth} | crítico: {critical} | base: ${base} | final: ${final}")

# Export tree
opcion = input("\n¿Deseas exportar el árbol? (s/n): ")
if opcion.lower() == "s":
    nombre_archivo = input("Ingresa el nombre del archivo: ")
    avl.exportTree(nombre_archivo + ".json")