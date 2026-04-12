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
        self.load_type = None  # Tracks the load type (insertion or topology)

    # LOAD FROM JSON
    def load_from_json(self, filepath):
        self.filepath = filepath
        self.history.save(self.tree, self.bst)  # Save state before loading a new tree
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.load_type = data.get("tipo")
        loadTree(self.tree, self.bst, filepath)

    # Save json
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
                "codigo": f.getCodigo(),
                "origen": f.getOrigen(),
                "destino": f.getDestino(),
                "horaSalida": f.getHoraSalida(),
                "precioBase": f.getPrecioBase(),
                "pasajeros": f.getPasajeros(),
                "promocion": f.getPromocion(),
                "alerta": f.getAlerta()
            })
        data = {"tipo": "INSERCION", "vuelos": vuelos}
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    # CREATE
    def create_flight(self, flight):
        # Save state before the change (for undo)
        self.history.save(self.tree, self.bst)
        self.tree.insert(Node(flight))
        # Sync BST — insert without balancing
        if self.bst:
            self.bst.insert(Node(flight))
        print(f"Flight {flight.getCodigo()} created.")

    # DELETE
    def delete_flight(self, codigo):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            # Save state before the change
            self.history.save(self.tree, self.bst)
            self.tree.delete(numero)
            # Sync BST
            if self.bst:
                self.bst.delete(numero)
            print(f"Flight {codigo} deleted.")
        else:
            print("Flight not found.")

    # UPDATE
    def update_flight(self, codigo, new_data):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            # Save state before the change
            self.history.save(self.tree, self.bst)
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

    # CANCEL — removes the node and its entire subtree
    def cancel_flight(self, codigo):
        numero = Flight.extractNum(codigo)
        node = self.tree.search(numero)
        if node:
            # Save state before the change
            self.history.save(self.tree, self.bst)
            # Collect codes before deleting to avoid stale references after rebalancing
            codes = [n.getValue().getCodigoComp() for n in self.tree.get_subtree_nodes(node)]
            for code in reversed(codes):
                self.tree.delete(code)
                if self.bst:
                    self.bst.delete(code)
            self.mass_cancellations += 1
            print(f"Flight {codigo} and subtree cancelled.")
        else:
            print("Flight not found.")

    # UNDO (Ctrl + Z)
    def undo(self):
        self.history.undo(self.tree, self.bst)

    # FIND
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

        # Tree height
        metrics["altura"] = self.tree.heightTree()

        # Total nodes
        metrics["total_nodos"] = self.tree.treeWeight()

        # Leaf count
        metrics["hojas"] = self.tree.countLeaves()

        # Rotations
        metrics["rotaciones"] = self.tree.rotations

        # Mass cancellations
        metrics["cancelaciones_masivas"] = self.mass_cancellations

        # Breadth-first traversal (BFS)
        metrics["recorrido_anchura"] = [
            node.getValue().getCodigo() for node in self.tree.copyBreadthFirstSearch()
        ]

        # Depth-first traversal (DFS - PreOrder)
        metrics["recorrido_profundidad"] = [
            node.getValue().getCodigo() for node in self.tree.preOrderTraversal()
        ]

        return metrics

    def export_metrics(self, filename="metrics.json"):
        metrics = self.get_metrics()
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=4, ensure_ascii=False)
        print("Metrics exported successfully")

    # Item 8.
    def deleteMinProfit(self):
        node = self.tree.findMinProfit()
        if node is None:
            return None, None
        codigo = node.getValue().getCodigo()
        profitability = self.tree.getProfit(node)
        # Cancel node with minimum profitability
        self.cancel_flight(codigo)
        # Rebalance and recalculate prices after cancellation
        if self.tree.root is not None:
            self.tree.checkBalance(self.tree.root)
            self.tree.recalculatePrices()
        return codigo, profitability
    # End Item 8.
