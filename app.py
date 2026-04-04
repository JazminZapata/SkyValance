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
from models.loader import buildByInsertion, buildByTopology
from services.flightService import FlightService


# ===============================
# CONFIGURACIÓN DE PÁGINA
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

# Referencias rápidas al service y sus árboles
service = st.session_state.service
avl = service.tree
bst = service.bst if service.bst else BST()


# ===============================
# FUNCIONES AUXILIARES
# ===============================


def build_graph(node, G=None, pos=None, x=0.0, y=0.0, layer=1):
    if G is None:
        G, pos = nx.DiGraph(), {}
    if node:
        label = node.getValue().codigo
        G.add_node(label)
        pos[label] = (x, y)

        if node.getLeftChild():
            G.add_edge(label, node.getLeftChild().getValue().codigo)
            build_graph(node.getLeftChild(), G, pos, x - 1/layer, y - 1, layer + 1)

        if node.getRightChild():
            G.add_edge(label, node.getRightChild().getValue().codigo)
            build_graph(node.getRightChild(), G, pos, x + 1/layer, y - 1, layer + 1)

    return G, pos


def draw_tree(avl):
    if not avl.root:
        st.info("Árbol vacío")
        return

    G, pos = build_graph(avl.root)
    recorrido = st.session_state.recorrido
    highlight = st.session_state.highlight

    # Build a lookup: to check isCritical
    node_map = {n.getValue().codigo: n for n in avl.copyBreadthFirstSearch()}

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

    fig, ax = plt.subplots(figsize=(10, 5))
    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=1400,
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

        recorrido.append(n.getValue().codigo)
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
# LAYOUT PRINCIPAL (3 columnas)
# ===============================
col1, col2, col3 = st.columns([1, 2, 1])


# ===============================
# COLUMNA IZQUIERDA — Controles
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

    # --- Carga de árbol ---
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
    
    #Modal para insertar nuevo vuelo
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
        # PASO 1 — buscar el vuelo
        if st.session_state.edit_flight_node is None:
            codigo_buscar = st.text_input("Enter Flight Code to edit", key="edit_search")
            if st.button("Search"):
                val = Flight.extractNum(codigo_buscar)
                nodo = avl.search(val)
                if nodo:
                    st.session_state.edit_flight_node = nodo
                else:
                    st.error("Flight not found")

        # PASO 2 — editar con campos prellenados
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
                    service.update_flight(f.codigo, {
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
            
            st.warning(f"Are you sure you want to delete flight **{f.codigo}**?")
            st.write(f"Route: {f.origen} → {f.destino}")
            st.write(f"Departure: {f.horaSalida}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Confirm Delete"):
                    service.delete_flight(f.codigo)
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
            
            st.error(f"This will cancel flight **{f.codigo}** and its entire subtree!")
            st.write(f"Route: {f.origen} → {f.destino}")
            st.write(f"Departure: {f.horaSalida}")
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Confirm Cancel"):
                    service.cancel_flight(f.codigo)
                    st.session_state.cancel_flight_node = None
                    st.rerun()
            with col_b:
                if st.button("Dismiss"):
                    st.session_state.cancel_flight_node = None
                    st.rerun()
                
    # --- Operaciones CRUD ---
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

    # Save version
    version_name = st.text_input("Version name", key="version_name")
    if st.button("Save Version", use_container_width=True):
        if not version_name.strip():
            st.warning("Enter a version name")
        elif avl.root is None:
            st.warning("Tree is empty")
        else:
            service.save_version(version_name.strip())
            st.success(f"Version '{version_name}' saved")

    # List and restore versions
    versions = service.list_versions()
    if versions:
        version_options = [v["name"] for v in versions] if isinstance(versions[0], dict) else versions
        selected = st.selectbox("Saved versions", version_options, key="version_select")

        col_r, col_d = st.columns(2)
        with col_r:
            if st.button("Restore", use_container_width=True):
                service.restore_version(selected)
                st.success(f"Restored '{selected}'")
                st.rerun()
        with col_d:
            if st.button("Delete", use_container_width=True):
                service.delete_version(selected)
                st.success(f"Deleted '{selected}'")
                st.rerun()
    else:
        st.caption("No saved versions yet")
    # End Item 2

    # --- Control de profundidad ---
    st.markdown("### Depth Control")
    depth = st.number_input("Max Depth", value=avl.limite)
    if depth != avl.limite:
        avl.setLimite(depth)
        st.rerun()

    # --- Eliminar nodo de menor rentabilidad ---
    if st.session_state.get("last_deleted"):
        d = st.session_state.last_deleted
        st.success(f"Deleted Node: **{d['code']}** — Profitability: **${d['profitability']:,.2f}**")

    if st.button("Remove Low Profit Node"):
        if avl.root is None:
            st.warning("Tree is empty")
        else:
            try:
                node = avl.findMinProfit()
                if node is None:
                    st.warning("There are no nodes to delete")
                else:
                    code = node.getValue().codigo
                    profitability = avl.getProfit(node)
                    avl.deleteMinProfit()
                    st.session_state.last_deleted = {
                        "code": code,
                        "profitability": profitability
                    }
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")


# ===============================
# COLUMNA CENTRAL — Visualización
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
        fig_bst, ax_bst = plt.subplots(figsize=(8, 4))
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
# MÉTRICAS (llamadas desde avl, tree y flightService)
# ===============================
metrics = service.get_metrics() if avl.root else {}
height = metrics.get("altura", 0)
leaves = metrics.get("hojas", 0)
rotations = metrics.get("rotaciones", {"LL": 0, "RR": 0, "LR": 0, "RL": 0})
mass_cancellations = metrics.get("cancelaciones_masivas", 0)
bst_height = bst.heightTree() if bst.root else 0
bst_leaves = bst.countLeaves() if bst.root else 0

# ===============================
# COLUMNA DERECHA — Métricas y búsqueda
# ===============================
with col3:

    # --- Métricas AVL ---
    st.subheader("AVL Metrics")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Height", height)
    m2.metric("Leaves", leaves)
    m3.metric("Rotations", sum(rotations.values()))
    m4.metric("Cancel", mass_cancellations)
    
    if avl.root:
        st.caption(f"LL: {rotations['LL']} | RR: {rotations['RR']} | LR: {rotations['LR']} | RL: {rotations['RL']}")

    st.divider()

    # --- Métricas BST ---
    st.subheader("BST Metrics")
    b1, b2 = st.columns(2)
    b1.metric("Height", bst_height)
    b2.metric("Leaves", bst_leaves)

    st.divider()

    # --- Recorridos animados ---
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

    # --- Búsqueda de vuelo ---
    st.subheader("Search Flight")
    code = st.text_input("Flight Code")

    if st.button("Search"):
        val = Flight.extractNum(code)
        nodo = avl.search(val)

        if nodo:
            f = nodo.getValue()
            st.session_state.highlight = f.codigo
            st.session_state.recorrido = []
            st.success("Found")
            with tree_container:
                draw_tree(avl)
            st.json({
                "codigo": f.codigo,
                "origen": f.origen,
                "destino": f.destino,
                "rentabilidad": avl.getProfit(nodo)
            })
        else:
            st.session_state.highlight = None
            st.error("Not found")