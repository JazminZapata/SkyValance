import json
from models.node import Node
from models.flight import Flight


# Building the tree by insertion (it means inserting one by one from the list found on JSON file)
# We receive an empty tree and the data from the JSON so we can start creating the nodes (flights)
def buildByInsertion(avl, bst, data):

    for flight_data in data["vuelos"]:

        flight = Flight(
            flight_data["codigo"],
            flight_data["origen"],
            flight_data["destino"],
            flight_data["horaSalida"],
            flight_data["precioBase"],
            flight_data["pasajeros"],
            flight_data["promocion"],
            flight_data["alerta"]
        )

        node_avl = Node(flight)
        avl.insert(node_avl)
        
        if bst is not None:
            node_bst = Node(flight)
            bst.insert(node_bst)

    
# When it comes to Topology we have to keep the structure described in JSON File, it means that we already have the descendants
def buildByTopology(data, parent=None):

    if data is None:
        return None

    flight = Flight(
        str(data["code"]),
        data["origin"],
        data["destination"],
        data["departureTime"],
        data["basePrice"],
        data["passengers"],
        data["promotion"],
        data["alert"]
    )

    # We just create the node with the flight and then we assign the balance factor, height and final price, then we call recursively for the left and right child until we reach a leaf (a node without descendants)
    node = Node(flight)
    # Assign the parent to the newly created node
    node.setParent(parent)
    
    node.setBalanceFactor(data.get("balanceFactor"))
    node.setHeight(data.get("height"))
    node.setFinalPrice(data.get("finalPrice"))
    node.setLeftChild(buildByTopology(data["left"], parent=node))
    node.setRightChild(buildByTopology(data["right"], parent=node))

    return node


def loadTree(avl, bst, file):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    tipo = data.get("tipo")

    if tipo == "INSERCION":
        buildByInsertion(avl, bst, data)
    elif tipo is None:
        avl.root = buildByTopology(data)