from models.loader import loadTree
from models.node import Node
from models.flight import Flight
from models.avl import AVL
from models.bst import BST
from models.actionHistory import ActionHistory
from models.versionManager import VersionManager
import json


class FlightService:

    def __init__(self):
        self.tree = AVL()
        self.bst = BST()
        self.history = ActionHistory()
        self.versions = VersionManager()
        self.mass_cancellations = 0
        self.load_type = None  # Para rastrear el tipo de carga (inserción o topología)
        
        
    #LOAD FROM JSON
    def load_from_json(self, filepath):
        self.filepath = filepath
        self.history.save(self.tree, self.bst)  # Guardar estado antes de cargar nuevo árbol

        import json
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.load_type = data.get("tipo")

        loadTree(self.tree, self.bst, filepath)
    
    #Save json    
    def save_to_json(self):
        if self.load_type == "INSERCION":
            self.__save_as_insertion()
        else:
            self.tree.exportTree(self.filepath)
            
    def __save_as_insertion(self):

        vuelos = []

        for node in self.tree.copyBreadthFirstSearch():
            f = node.getValue()
            vuelos.append({
                "codigo": f.codigo,
                "origen": f.origen,
                "destino": f.destino,
                "horaSalida": f.horaSalida,
                "precioBase": f.precioBase,
                "pasajeros": f.pasajeros,
                "promocion": f.promocion,
                "alerta": f.alerta
            })

        data = {
            "tipo": "INSERCION",
            "vuelos": vuelos
        }

        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # CREATE
    def create_flight(self, flight):
        # Guardar estado antes del cambio (para undo)
        self.history.save(self.tree, self.bst)

        node = Node(flight)
        self.tree.insert(node)
        
        #Para actualizar el bst 
        if self.bst:
            self.bst.insert(Node(flight))

        print(f"Vuelo {flight.codigo} creado correctamente")

    # DELETE
    def delete_flight(self, codigo):
        numero = Flight.extractNum(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree, self.bst)

            self.tree.delete(numero)
            
            if self.bst:
                self.bst.delete(numero)

            print(f"Vuelo {codigo} eliminado correctamente")
        else:
            print("Vuelo no encontrado")

    # UPDATE
    def update_flight(self, codigo, new_data):
        numero = Flight.extractNum(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree , self.bst)

            # Obtener datos actuales
            old_data = node.getValue()

            # Crear copia de seguridad
            old_copy = Flight(
                old_data.codigo,
                old_data.origen,
                old_data.destino,
                old_data.horaSalida,
                old_data.precioBase,
                old_data.pasajeros,
                old_data.promocion,
                old_data.alerta,
            )

            # Actualizar atributos dinámicamente
            for key, value in new_data.items():
                setattr(node.getValue(), key, value)

            print(f"Vuelo {codigo} actualizado correctamente")
        else:
            print("Vuelo no encontrado")


    # CANCEL (subárbol completo)
    def cancel_flight(self, codigo):
        numero = Flight.extractNum(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree, self.bst)

            # Obtener todos los nodos del subárbol
            subtree_nodes = self.tree.get_subtree_nodes(node)

            # Eliminar desde hojas hacia arriba
            for n in reversed(subtree_nodes):
                self.tree.delete(n.getValue().codigo_comp)
                if self.bst:
                    self.bst.delete(n.getValue().codigo_comp)
                
            self.mass_cancellations += 1

            print(f"Vuelo {codigo} y su subárbol fueron cancelados correctamente")
        else:
            print("Vuelo no encontrado")

    # UNDO (Ctrl + Z)
    def undo(self):
        self.history.undo(self.tree, self.bst)

    # FIND (Buscar vuelo por código)
    def find_flight(self, codigo):
        numero = Flight.extractNum(codigo)

        node = self.tree.search(numero)

        if node:
            return node.getValue()
        else:
            return None

    # Item 2.

    # Saves the current tree state under a user-defined name
    def save_version(self, name: str):
        self.versions.save(name, self.tree, self.bst)

    # Restores the tree to a previously saved named version
    def restore_version(self, name: str):
        self.versions.restore(name, self.tree, self.bst)

    # Returns all saved versions with their name, timestamp and depth limit
    def list_versions(self) -> list:
        return self.versions.list_versions()

    # Deletes a named version from disk and the index
    def delete_version(self, name: str):
        self.versions.delete_version(name)

    # End Item 2.
        
    
    def get_metrics(self):
        metrics = {}

        # Altura
        metrics["altura"] = self.tree.heightTree()

        # Total nodos
        metrics["total_nodos"] = self.tree.treeWeight()

        # Hojas
        metrics["hojas"] = self.tree.countLeaves()

        # Rotaciones
        metrics["rotaciones"] = self.tree.rotations

        # Cancelaciones masivas
        metrics["cancelaciones_masivas"] = self.mass_cancellations

        # Recorrido en anchura (BFS)
        metrics["recorrido_anchura"] = [
            node.getValue().codigo for node in self.tree.copyBreadthFirstSearch()
        ]

        # Recorrido en profundidad (DFS - PreOrder)
        metrics["recorrido_profundidad"] = [
            node.getValue().codigo for node in self.tree.preOrderTraversal()
        ]

        return metrics
    
    def export_metrics(self, filename="metrics.json"):
        import json

        metrics = self.get_metrics()

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4, ensure_ascii=False)

        print("Métricas exportadas correctamente")
        
    #Sync BST (for staying updated with AVL changes)
    def create_flight(self, flight):
        self.history.save(self.tree)
        self.tree.insert(Node(flight))
        # Sync BST — insert without balancing
        if self.bst:
            self.bst.insert(Node(flight))
        print(f"Flight {flight.codigo} created.")

    def delete_flight(self, codigo):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            self.history.save(self.tree)
            self.tree.delete(numero)
            # Sync BST
            if self.bst:
                self.bst.delete(numero)
            print(f"Flight {codigo} deleted.")
        else:
            print("Flight not found.")

    def update_flight(self, codigo, new_data):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            self.history.save(self.tree)
            for key, value in new_data.items():
                setattr(node.getValue(), key, value)
            # Sync BST — same node reference, update reflects automatically
            if self.bst:
                bst_node = self.bst.search(numero)
                if bst_node:
                    for key, value in new_data.items():
                        setattr(bst_node.getValue(), key, value)
            print(f"Flight {codigo} updated.")
        else:
            print("Flight not found.")

    def cancel_flight(self, codigo):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            self.history.save(self.tree)
            codes = [n.getValue().codigo_comp for n in self.tree.get_subtree_nodes(node)]
            for code in reversed(codes):
                self.tree.delete(code)
                # Sync BST
                if self.bst:
                    self.bst.delete(code)
            print(f"Flight {codigo} and subtree cancelled.")
        else:
            print("Flight not found.")
            
    # Item 8.        
    def deleteMinProfit(self):
      node = self.tree.findMinProfit()

      if node is None:
        return None, None

      codigo = node.getValue().codigo
      profitability = self.tree.getProfit(node)

    # Cancel node with minimum profitability
      self.cancel_flight(codigo)

    # Rebalance and recalculate prices after cancellation
      if self.tree.root is not None:
        self.tree.checkBalance(self.tree.root)
        self.tree.recalculatePrices()

      return codigo, profitability