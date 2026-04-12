import sys
import os
import json
import time
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# ===============================
# BACKEND PATH
# ===============================
sys.path.append(os.path.abspath("Backend/src"))

from models.avl import AVL
from models.bst import BST
from models.flight import Flight
from models.node import Node
from models.loader import buildByInsertion, buildByTopology
from services.flightService import FlightService


# ===============================
# PAGE CONFIGURATION
# ===============================
st.set_page_config(layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f7fb;
}
button {
    background-color: #e2e8f0 !important;
    color: black !important;
    border-radius: 8px !important;
    height: 38px;
    font-weight: 500;
}
[data-testid="metric-container"] {
    background: white;
    border-radius: 10px;
    padding: 6px !important;
    text-align: center;
}
[data-testid="metric-container"] label {
    font-size: 11px !important;
}
[data-testid="metric-container"] div {
    font-size: 16px !important;
}
h1, h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# SESSION STATE
# ===============================

if "service" not in st.session_state:
    st.session_state.service = FlightService()
    st.session_state.mass_cancel = 0

if "recorrido" not in st.session_state:
    st.session_state.recorrido = []

if "highlight" not in st.session_state:
    st.session_state.highlight = None

if "show_export" not in st.session_state:
    st.session_state.show_export = False

if "show_insert" not in st.session_state:
    st.session_state.show_insert = False
    
if "edit_flight_node" not in st.session_state:
    st.session_state.edit_flight_node = None
    
if "delete_flight_node" not in st.session_state:
    st.session_state.delete_flight_node = None
    
if "cancel_flight_node" not in st.session_state:
    st.session_state.cancel_flight_node = None
    
if "stress_mode" not in st.session_state:
    st.session_state.stress_mode = False

if "rebalance_cost" not in st.session_state:
        st.session_state.rebalance_cost = None
                
if "insertion_queue" not in st.session_state:
    st.session_state.insertion_queue = []
    
if "processing_queue" not in st.session_state:
    st.session_state.processing_queue = False

if "insertion_queue_snapshot" not in st.session_state:
    st.session_state.insertion_queue_snapshot = []

# Quick references to the service and its trees
service = st.session_state.service
avl = service.tree
bst = service.bst if service.bst else BST()


# ===============================
# HELPER FUNCTIONS
# ===============================


def build_graph(node, G=None, pos=None, x=0.0, y=0.0, layer=1):
    if G is None:
        G, pos = nx.DiGraph(), {}
    if node:
        label = node.getValue().getCodigo()
        G.add_node(label)
        pos[label] = (x, y)

        # Each level spreads nodes by a fixed offset that does not shrink with depth
        offset = 4 / (layer * 0.7)

        if node.getLeftChild():
            G.add_edge(label, node.getLeftChild().getValue().getCodigo())
            build_graph(node.getLeftChild(), G, pos, x - offset, y - 1, layer + 1)

        if node.getRightChild():
            G.add_edge(label, node.getRightChild().getValue().getCodigo())
            build_graph(node.getRightChild(), G, pos, x + offset, y - 1, layer + 1)

    return G, pos



def draw_tree(avl):
    if not avl.root:
        st.info("Árbol vacío")
        return

    G, pos = build_graph(avl.root)
    recorrido = st.session_state.recorrido
    highlight = st.session_state.highlight

    # Build a lookup: to check isCritical
    node_map = {n.getValue().getCodigo(): n for n in avl.copyBreadthFirstSearch()}

    node_colors = []
    for n in G.nodes():
        if recorrido and n in recorrido:
            node_colors.append("#22c55e")       # Green — traversal
        elif highlight and n == highlight:
            node_colors.append("#ef4444")       # Red — search result
        elif node_map.get(n) and node_map[n].getIsCritical():
            node_colors.append("#f97316")       # Orange — critical node - Item #6
        else:
            node_colors.append("#679df3")       # Blue — normal

    fig, ax = plt.subplots(figsize=(20, 8))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        font_color="white",
        edge_color="#94a3b8"
    )
    st.pyplot(fig)
    plt.close(fig)


def animar_recorrido(nodes, container):
    st.session_state.recorrido = []
    st.session_state.highlight = None
    st.session_state.stop_animacion = False
    st.session_state.animando = True

    recorrido = []
    text_container = st.empty()

    for n in nodes:
        if st.session_state.stop_animacion:
            break

        recorrido.append(n.getValue().getCodigo())
        st.session_state.recorrido = recorrido.copy()

        with container:
            draw_tree(avl)

        with text_container:
            st.markdown(
                f"""
                <div style="
                    background:white;
                    padding:10px;
                    border-radius:8px;
                    border:1px solid #e5e7eb;
                    font-family: monospace;
                ">
                {" → ".join(recorrido)}
                </div>
                """,
                unsafe_allow_html=True
            )
        time.sleep(0.4)

    st.session_state.recorrido = []
    st.session_state.stop_animacion = False
    st.session_state.animando = False

    with container:
        draw_tree(avl)


# Item 7 — AVL Audit modal (defined here so it's available globally)
@st.dialog("AVL Audit Report")
def audit_modal(audit):
    # Health score
    score = audit["score"]
    color = "🟢" if score == 100 else "🟡" if score >= 70 else "🔴"
    st.markdown(f"### {color} Tree Health: {score}%")

    # Summary metrics
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Total Nodes", audit["total"])
    col_b.metric("Valid", audit["valid"])
    col_c.metric("Inconsistent", audit["inconsistent_count"])

    st.divider()

    # Node details
    st.markdown("### Node Details")
    for entry in audit["details"]:
        icon = "🟢" if entry["ok"] else "🔴"
        critical_tag = "Critical" if entry["critical"] else ""
        st.markdown(
            f"{icon} **{entry['codigo']}**{critical_tag} | "
            f"BF: `{entry['balance_factor']}` {'✅' if entry['bf_ok'] else '❌'} | "
            f"Height: `{entry['height']}` {'✅' if entry['height_ok'] else '❌'} | "
            f"Depth: `{entry['depth']}`"
        )

    st.divider()

    # Recommendation
    if audit["inconsistent_count"] == 0:
        st.success("Tree is a valid AVL — no issues found")
    else:
        st.error(f"{audit['inconsistent_count']} inconsistent node(s) found")
        st.warning("Recommendation: Run *Rebalance Now* to fix the tree")
# End Item 7


# ===============================
# HEADER
# ===============================
st.markdown(
    "<h1 style='margin:0; color:#1e293b; text-align:center;'>SkyBalance AVL Manager</h1>",
    unsafe_allow_html=True
)

# ===============================
# MAIN LAYOUT (3 columns)
# ===============================
col1, col2, col3 = st.columns([1, 2, 1])


# ===============================
# LEFT COLUMN — Controls
# ===============================
with col1:
    
    # --- Export ---
    st.markdown("### Export Tree")
    export_name = st.text_input("File name", key="export_name")
    export_name_clean = export_name.replace(".json", "").strip()
    export_data = avl.toJSON(avl.root)
    export_json = json.dumps(export_data, indent=4, ensure_ascii=False)
    st.download_button(
        label="Download JSON",
        data=export_json,
        file_name=f"{export_name_clean}.json" if export_name_clean else "tree.json",
        mime="application/json",
        disabled=not export_name_clean,
        use_container_width=True
    )

    st.divider()

    # --- Tree loading ---
    archivo = st.file_uploader("Load JSON", type="json")
    tipo = st.radio("Mode", ["Insertion", "Topology"])

    if st.button("Load Tree"):
        if archivo:
            data = json.load(archivo)
            new_service = FlightService()
            if tipo == "Insertion":
                buildByInsertion(new_service.tree, new_service.bst, data)
            else:
                new_service.tree.root = buildByTopology(data)
            st.session_state.service = new_service
            st.success("Tree loaded")
            st.rerun()
        else:
            st.warning("Upload JSON")

    st.divider()

    # --- Stress Mode ---
    st.markdown("### Stress Mode")

    if st.session_state.stress_mode:
        st.warning("⚠️ Stress mode active — no auto balance")
        if st.button("Disable Stress Mode", use_container_width=True):
            avl.enable_auto_balance()
            st.session_state.stress_mode = False
            st.rerun()
        if st.button("Rebalance Now", use_container_width=True):
            cost = avl.rebalance_all()
            avl.enable_auto_balance()
            st.session_state.stress_mode = False
            st.session_state.rebalance_cost = cost
            st.rerun()
        # Item 7 — only available in stress mode
        if st.button("Verify AVL Property", use_container_width=True):
            result = avl.auditAVL()
            audit_modal(result)
        # End Item 7
    else:
        if st.button("Enable Stress Mode", use_container_width=True):
            avl.enable_stress_mode()
            st.session_state.stress_mode = True
            st.rerun()

    if st.session_state.get("rebalance_cost"):
        cost = st.session_state.rebalance_cost
        st.success("Rebalance done!")
        st.caption(f"LL: {cost['LL']} | RR: {cost['RR']} | LR: {cost['LR']} | RL: {cost['RL']}")
        
    st.divider()
    
    # Modal to insert a new flight
    @st.dialog("Insert New Flight")
    def insert_modal():
        codigo = st.text_input("Flight Code", key="insert_codigo")
        precio = st.number_input("Base Price", min_value=0, key="insert_precio")
        pasajeros = st.number_input("Passengers", min_value=0, key="insert_pasajeros")
        origen = st.text_input("Origin", key="insert_origen")
        destino = st.text_input("Destination", key="insert_destino")
        hora = st.text_input("Departure Time (HH:MM)", key="insert_hora")
        promocion = st.checkbox("Discount", key="insert_promocion")
        alerta = st.checkbox("Alert", key="insert_alerta")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Confirm Insert"):
                if not codigo:
                    st.warning("Flight code is required")
                else:
                    flight = Flight(codigo, origen, destino, hora, precio, pasajeros, promocion, alerta)
                    service.create_flight(flight)
                    st.rerun()
        with col_b:
            if st.button("Cancel"):
                st.rerun()
                
                
    @st.dialog("Edit Flight")
    def edit_modal():
        # Step 1 — search the flight
        if st.session_state.edit_flight_node is None:
            codigo_buscar = st.text_input("Enter Flight Code to edit", key="edit_search")
            if st.button("Search"):
                val = Flight.extractNum(codigo_buscar)
                nodo = avl.search(val)
                if nodo:
                    st.session_state.edit_flight_node = nodo
                else:
                    st.error("Flight not found")

        # Step 2 — edit with pre-filled fields
        if st.session_state.edit_flight_node is not None:
            nodo = st.session_state.edit_flight_node
            f = nodo.getValue()

            origen = st.text_input("Origin", value=f.origen, key="edit_origen")
            destino = st.text_input("Destination", value=f.destino, key="edit_destino")
            hora = st.text_input("Departure Time", value=f.horaSalida, key="edit_hora")
            precio = st.number_input("Base Price", value=f.precioBase, min_value=0, key="edit_precio")
            pasajeros = st.number_input("Passengers", value=f.pasajeros, min_value=0, key="edit_pasajeros")
            promocion = st.checkbox("Discount", value=f.promocion, key="edit_promocion")
            alerta = st.checkbox("Alert", value=f.alerta, key="edit_alerta")

            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Confirm Edit"):
                    service.update_flight(f.getCodigo(), {
                        "origen": origen,
                        "destino": destino,
                        "horaSalida": hora,
                        "precioBase": precio,
                        "pasajeros": pasajeros,
                        "promocion": promocion,
                        "alerta": alerta
                    })
                    st.session_state.edit_flight_node = None
                    st.rerun()
            with col_b:
                if st.button("Cancel Edit"):
                    st.session_state.edit_flight_node = None
                    st.rerun()
                    
    @st.dialog("Delete Flight")
    def delete_modal():
        codigo_buscar = st.text_input("Enter Flight Code to delete", key="delete_search")
        
        if st.button("Search"):
            val = Flight.extractNum(codigo_buscar)
            nodo = avl.search(val)
            if nodo:
                st.session_state.delete_flight_node = nodo
            else:
                st.error("Flight not found")
        
        if st.session_state.get("delete_flight_node") is not None:
            nodo = st.session_state.delete_flight_node
            f = nodo.getValue()
            
            st.warning(f"Are you sure you want to delete flight **{f.getCodigo()}**?")
            st.write(f"Route: {f.getOrigen()} → {f.getDestino()}")
            st.write(f"Departure: {f.getHoraSalida()}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Confirm Delete"):
                    service.delete_flight(f.getCodigo())
                    st.session_state.delete_flight_node = None
                    st.rerun()
            with col_b:
                if st.button("Cancel Delete"):
                    st.session_state.delete_flight_node = None
                    st.rerun()
                
                
    @st.dialog("Cancel Flight")
    def cancel_modal():
        codigo_buscar = st.text_input("Enter Flight Code to cancel", key="cancel_search")
        
        if st.button("Search"):
            val = Flight.extractNum(codigo_buscar)
            nodo = avl.search(val)
            if nodo:
                st.session_state.cancel_flight_node = nodo
            else:
                st.error("Flight not found")
        
        if st.session_state.get("cancel_flight_node") is not None:
            nodo = st.session_state.cancel_flight_node
            f = nodo.getValue()
            
            st.error(f"This will cancel flight **{f.getCodigo()}** and its entire subtree!")
            st.write(f"Route: {f.getOrigen()} → {f.getDestino()}")
            st.write(f"Departure: {f.getHoraSalida()}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Confirm Cancel"):
                    service.cancel_flight(f.getCodigo())
                    st.session_state.cancel_flight_node = None
                    st.rerun()
            with col_b:
                if st.button("Dismiss"):
                    st.session_state.cancel_flight_node = None
                    st.rerun()
                    
    # Item 3.                
    
    @st.dialog("Add Flight to Queue")
    def queue_modal():
        codigo = st.text_input("Flight Code", key="queue_codigo")
        precio = st.number_input("Base Price", min_value=0, key="queue_precio")
        pasajeros = st.number_input("Passengers", min_value=0, key="queue_pasajeros")
        origen = st.text_input("Origin", key="queue_origen")
        destino = st.text_input("Destination", key="queue_destino")
        hora = st.text_input("Departure Time (HH:MM)", key="queue_hora")
        promocion = st.checkbox("Discount", key="queue_promocion")
        alerta = st.checkbox("Alert", key="queue_alerta")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Add to Queue"):
               if not codigo:
                st.warning("Flight code is required")
               else:
                  val = Flight.extractNum(codigo)
                  # Check if it's already in the AVL tree
                  if avl.search(val) is not None:
                    st.error(f"Flight {codigo} already exists in the tree")
                  # Check if it's already in the queue
                  elif any(n.getValue().getCodigoComp() == val for n in st.session_state.insertion_queue):
                    st.error(f"Flight {codigo} is already in the queue")
                  else:
                    flight = Flight(codigo, origen, destino, hora, precio, pasajeros, promocion, alerta)
                    node = Node(flight)
                    st.session_state.insertion_queue.append(node)
                    st.success(f"Flight {codigo} added to queue")
                    st.rerun()
        with col_b:
            if st.button("Cancel"):
                st.rerun()
                
    @st.dialog("Pending Insertions")
    def queue_dialog():
        if not st.session_state.insertion_queue:
            st.info("No pending insertions")
            return

        st.markdown("### Flights in queue")
        for i, n in enumerate(st.session_state.insertion_queue):
            f = n.getValue()
            st.markdown(f"""
            <div style="
                display:flex;
                align-items:center;
                gap:10px;
                padding:8px 12px;
                margin-bottom:6px;
                background:#f8fafc;
                border:1px solid #e2e8f0;
                border-radius:8px;
                font-size:13px;
            ">
                <span style="
                    background:#f59e0b;
                    color:white;
                    border-radius:50%;
                    width:22px;
                    height:22px;
                    display:inline-flex;
                    align-items:center;
                    justify-content:center;
                    font-weight:700;
                    font-size:11px;
                ">{i+1}</span>
                <strong>{f.getCodigo()}</strong>
                <span style="color:#64748b">{f.getOrigen()} → {f.getDestino()}</span>
                <span style="margin-left:auto; color:#94a3b8">${f.getPrecioBase()}</span>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("▶ Process Queue", use_container_width=True, key="process_q"):
                for n in st.session_state.insertion_queue:
                  avl.insertionQueue(n)
                st.session_state.insertion_queue = []
                st.session_state.processing_queue = True
                st.rerun()
        with col_b:
            if st.button("🗑 Clear", use_container_width=True, key="clear_q"):
                st.session_state.insertion_queue = []
                st.rerun()
    # End Item 3.      
    # --- CRUD Operations ---
    if st.button("Insert Flight", use_container_width=True): 
        insert_modal()

    if st.button("Edit Flight", use_container_width=True): 
        edit_modal()
        
    if st.button("Delete Node", use_container_width=True):
        delete_modal()
        
    if st.button("Cancel Flight", use_container_width=True):
        cancel_modal()
        
    if st.button("↩️ Undo", use_container_width=True):
        if service.history.stack:
            service.undo()
            st.rerun()
        else:
            st.toast("No hay acciones para deshacer", icon="⚠️")
        
    st.divider()
    
# Item 2 — Version management
    st.markdown("### Versions")

    # Input field where the user types the name for the new version
    version_name = st.text_input("Version name", key="version_name")
    if st.button("Save Version", use_container_width=True):
        # Validate that the name is not empty
        if not version_name.strip():
            st.warning("Enter a version name")
        # Validate that the tree has at least one node before saving
        elif avl.root is None:
            st.warning("Tree is empty")
        else:
            # Save the current tree state under the given name
            service.save_version(version_name.strip())
            st.success(f"Version '{version_name}' saved")

    # Load the list of saved versions from disk
    versions = service.list_versions()
    if versions:
        # Support both plain string lists and lists of dicts with a "name" key
        version_options = [v["name"] for v in versions] if isinstance(versions[0], dict) else versions
        # Dropdown so the user can pick which version to restore or delete
        selected = st.selectbox("Saved versions", version_options, key="version_select")

        col_r, col_d = st.columns(2)
        with col_r:
            # Restore rebuilds the tree from the saved JSON snapshot
            if st.button("Restore", use_container_width=True):
                service.restore_version(selected)
                st.success(f"Restored '{selected}'")
                st.rerun()
        with col_d:
            # Delete removes the version from memory and from disk
            if st.button("Delete", use_container_width=True):
                service.delete_version(selected)
                st.success(f"Deleted '{selected}'")
                st.rerun()
    else:
        # Shown when no versions have been saved yet
        st.caption("No saved versions yet")
    # End Item 2

    # --- Depth Control ---
    st.markdown("### Depth Control")
    depth = st.number_input("Max Depth", value=avl.limite)
    if depth != avl.limite:
        avl.setLimite(depth)
        st.rerun()

    # --- Remove least profitable node ---
    if st.session_state.get("last_deleted"):
        d = st.session_state.last_deleted
        st.success(f"Deleted Node: **{d['code']}** — Profitability: **${d['profitability']:,.2f}**")

    if st.button("Remove Low Profit Node"):
        if avl.root is None:
            st.warning("Tree is empty")
        else:
            try:
                codigo, profitability = service.deleteMinProfit()
                if codigo is None:
                    st.warning("There are no nodes to delete")
                else:
                    st.session_state.last_deleted = {
                        "code": codigo,
                        "profitability": profitability
                    }
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    
    if st.button("🔍 Debug Balance"):
     if avl.root:
        nodes = avl.copyBreadthFirstSearch()
        debug_info = []
        for n in nodes:
            bf = avl.getBalanceFactor(n)
            depth = avl.getDepth(n)
            debug_info.append({
                "codigo": n.getValue().getCodigo(),
                "bf": bf,
                "depth": depth,
                "parent": n.getParent().getValue().getCodigo() if n.getParent() else "ROOT"
            })
        st.json(debug_info)

# ===============================
# CENTER COLUMN — Visualization
# ===============================
with col2:

    # AVL
    tree_container = st.empty()
    with tree_container:
        draw_tree(avl)

    st.divider()

    # BST
    if not bst.root:
        st.info("BST vacío")
    else:
        G_bst, pos_bst = build_graph(bst.root)
        fig_bst, ax_bst = plt.subplots(figsize=(12, 6))
        nx.draw(
            G_bst, pos_bst,
            with_labels=True,
            node_color="#94a3b8",
            node_size=1200,
            font_color="white",
            edge_color="#cbd5f5"
        )
        st.markdown("### BST")
        st.pyplot(fig_bst)
        plt.close(fig_bst)

# ===============================
# METRICS (from avl, tree and flightService)
# ===============================
metrics = service.get_metrics() if avl.root else {}
height = metrics.get("altura", 0)
leaves = metrics.get("hojas", 0)
rotations = metrics.get("rotaciones", {"LL": 0, "RR": 0, "LR": 0, "RL": 0})
mass_cancellations = metrics.get("cancelaciones_masivas", 0)
bst_height = bst.heightTree() if bst.root else 0
bst_leaves = bst.countLeaves() if bst.root else 0

# Item 3 — Process insertion queue
if st.session_state.get("processing_queue"):
    st.session_state.processing_queue = False

    while len(avl.queue) > 0:
        node, conflict = avl.processNextInQueue()  
        if node:
            bst.insertionQueue(Node(node.getValue()))
            bst.processNextInQueue() 

            avl.recalculatePrices()
            tree_container.empty()
            with tree_container:
                draw_tree(avl)
                
            if conflict:
             st.toast(conflict, icon="⚠️") 
             
            time.sleep(0.6)

    st.rerun()
    
# End Item 3

# ===============================
# RIGHT COLUMN — Metrics and search
# ===============================
with col3:

    # --- AVL Metrics ---
    st.subheader("AVL Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Height", height)
    m2.metric("Leaves", leaves)
    m3.metric("Rotations", sum(rotations.values()))
    m4.metric("Cancel", mass_cancellations)
    
    if avl.root:
        st.caption(f"LL: {rotations['LL']} | RR: {rotations['RR']} | LR: {rotations['LR']} | RL: {rotations['RL']}")

    st.divider()

    # --- BST Metrics ---
    st.subheader("BST Metrics")
    b1, b2 = st.columns(2)
    b1.metric("Height", bst_height)
    b2.metric("Leaves", bst_leaves)

    st.divider()

    # --- Animated traversals ---
    st.subheader("Traversals")
    t1, t2 = st.columns(2)
    t3, t4 = st.columns(2)

    if t1.button("Preorder", key="pre"):
        animar_recorrido(avl.preOrderTraversal() or [], tree_container)
    if t2.button("Inorder", key="in"):
        animar_recorrido(avl.inOrderTraversal() or [], tree_container)
    if t3.button("Postorder", key="post"):
        animar_recorrido(avl.posOrderTraversal() or [], tree_container)
    if t4.button("BFS", key="bfs"):
        animar_recorrido(avl.copyBreadthFirstSearch() or [], tree_container)

    st.divider()

    # --- Flight search ---
    st.subheader("Search Flight")
    code = st.text_input("Flight Code")

    if st.button("Search"):
        val = Flight.extractNum(code)
        nodo = avl.search(val)

        if nodo:
            f = nodo.getValue()
            st.session_state.highlight = f.getCodigo()
            st.session_state.recorrido = []
            st.success("Found")
            with tree_container:
                draw_tree(avl)
            st.json({
                "codigo": f.getCodigo(),
                "origen": f.getOrigen(),
                "destino": f.getDestino(),
                "precio_final": nodo.getFinalPrice(),
                "es_critico": nodo.getIsCritical(), 
                "promocion": f.getPromocion(),
                "alerta": f.getAlerta(),
                "rentabilidad": avl.getProfit(nodo)
            })
        else:
            st.session_state.highlight = None
            st.error("Not found")
            

    # Item 3 — Queue button + dialog
    if st.session_state.insertion_queue:
        count = len(st.session_state.insertion_queue)

        st.markdown(f"""
        <div style="
            margin-top: 8px;
            padding: 10px 14px;
            background: linear-gradient(135deg, #fef3c7, #fde68a);
            border-left: 4px solid #f59e0b;
            border-radius: 8px;
            cursor: pointer;
        ">
            <span style="font-size:13px; font-weight:600; color:#92400e;">
                ✈️ {count} pending insertion{'s' if count > 1 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Pending Insertions", use_container_width=True, key="open_queue_dialog"):
            queue_dialog()

    if st.button("Queue Flight", use_container_width=True):
        queue_modal()
            
    # End Item 3 Button