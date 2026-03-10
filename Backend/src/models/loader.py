import json
from models.node import Node
from models.flight import Flight


# Building the tree by insertion (it means inserting one by one from the list found on JSON file)
# We receive an empty tree and the data from the JSON so we can start creating the nodes (flights)
def buildByInsertion(tree, data):

    for flight_data in data["vuelos"]:

        flight = Flight(
            flight_data["codigo"],
            flight_data["origen"],
            flight_data["destino"],
            flight_data["horaSalida"],
            flight_data["precioBase"],
            flight_data["precioFinal"],
            flight_data["pasajeros"],
            flight_data["promocion"],
            flight_data["alerta"],
            flight_data["altura"],
            flight_data["factorEquilibrio"]
        )

        node = Node(flight)
        tree.insert(node)


# When it comes to Topology we have to keep the structure described in JSON File, it means that we already have the descendants
def buildByTopology(data):

    if data is None:
        return None

    flight = Flight(
        data["codigo"],
        data["origen"],
        data["destino"],
        data["horaSalida"],
        data["precioBase"],
        data["precioFinal"],
        data["pasajeros"],
        data["promocion"],
        data["alerta"],
        data["altura"],
        data["factorEquilibrio"]
    )

    node = Node(flight)

    node.setLeftChild(buildByTopology(data["izquierdo"]))
    node.setRightChild(buildByTopology(data["derecho"]))

    return node


def loadTree(tree, file):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data["tipo"] == "INSERCION":
        buildByInsertion(tree, data)
    else:
        tree.root = buildByTopology(data)