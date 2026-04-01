from ..models.loader import loadTree
from ..models.node import Node
from ..models.flight import Flight
from ..models.avl import AVL
from ..models.actionHistory import ActionHistory


class FlightService:

    def __init__(self):
        self.tree = AVL()
        self.bst = None
        self.history = ActionHistory()
        
        
    #LOAD FROM JSON
    def load_from_json(self, filepath):
        self.history.save(self.tree)
        loadTree(self.tree, self.bst, filepath)
        print(f"JSON cargado correctamente desde {filepath}")

    # CREATE
    def create_flight(self, flight):
        # Guardar estado antes del cambio (para undo)
        self.history.save(self.tree)

        node = Node(flight)
        self.tree.insert(node)

        print(f"Vuelo {flight.codigo} creado correctamente")

    # DELETE
    def delete_flight(self, codigo):
        numero = Flight.extraerNumero(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree)

            self.tree.delete(numero)

            print(f"Vuelo {codigo} eliminado correctamente")
        else:
            print("Vuelo no encontrado")

    # UPDATE
    def update_flight(self, codigo, new_data):
        numero = Flight.extraerNumero(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree)

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
        numero = Flight.extraerNumero(codigo)

        node = self.tree.search(numero)

        if node:
            # Guardar estado antes del cambio
            self.history.save(self.tree)

            # Obtener todos los nodos del subárbol
            subtree_nodes = self.tree.get_subtree_nodes(node)

            # Eliminar desde hojas hacia arriba
            for n in reversed(subtree_nodes):
                self.tree.delete(n.getValue().codigo_comp)

            print(f"Vuelo {codigo} y su subárbol fueron cancelados correctamente")
        else:
            print("Vuelo no encontrado")

    # UNDO (Ctrl + Z)
    def undo(self):
        self.history.undo(self.tree)


    # FIND (Buscar vuelo por código)
    def find_flight(self, codigo):
        numero = Flight.extraerNumero(codigo)

        node = self.tree.search(numero)

        if node:
            return node.getValue()
        else:
            return None
