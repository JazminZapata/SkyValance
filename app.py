import sys
import os
import json
import time
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# backend
sys.path.append(os.path.abspath("Backend/src"))

from models.avl import AVL
from models.bst import BST
from models.tree import Tree
from models.flight import Flight
from models.node import Node
from models.loader import buildByInsertion, buildByTopology

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

    node_colors = []
    for n in G.nodes():
        if recorrido and n in recorrido:
            node_colors.append("#22c55e")  # 🟢 recorrido
        elif highlight and n == highlight:
            node_colors.append("#ef4444")  # 🔴 búsqueda
        else:
            node_colors.append("#679df3")  # 🔵 normal

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


if "avl" not in st.session_state:
    st.session_state.avl = AVL()
    st.session_state.bst = BST()
    st.session_state.mass_cancel = 0
    
if "recorrido" not in st.session_state:
    st.session_state.recorrido = []

if "highlight" not in st.session_state:
    st.session_state.highlight = None
    
if "show_export" not in st.session_state:
    st.session_state.show_export = False

avl = st.session_state.avl
bst = st.session_state.bst


st.set_page_config(layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #f5f7fb;
}

/* botones */
button {
    background-color: #e2e8f0 !important;
    color: black !important;
    border-radius: 8px !important;
    height: 38px;
    font-weight: 500;
}

/* métricas compactas */
[data-testid="metric-container"] {
    background: white;
    border-radius: 10px;
    padding: 6px !important;
    text-align: center;
}

/* reducir tamaño */
[data-testid="metric-container"] label {
    font-size: 11px !important;
}
[data-testid="metric-container"] div {
    font-size: 16px !important;
}

/* títulos */
h1, h2, h3 {
    color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

col_title, col_icons = st.columns([6,1])

with col_title:
    st.markdown(
    "<h1 style='margin:0; color:#1e293b; text-align:center;'>SkyBalance AVL Manager</h1>",
    unsafe_allow_html=True
    )

with col_icons:

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🗑️", key="del"):
            st.info("Delete próximamente")

    with c2:
        if st.button("🔗", key="share"):
            st.info("Share próximamente")

    with c3:
        if st.button("⬇️", key="export"):
            st.session_state.show_export = True

st.markdown("<hr>", unsafe_allow_html=True)

# ===============================
# EXPORT
# ===============================

if st.session_state.show_export:

    nombre_archivo = st.text_input("Nombre archivo")

    if st.button("Descargar JSON"):

        if not nombre_archivo:
            st.warning("Escribe un nombre")
        else:
            nombre_limpio = nombre_archivo.replace(".json", "").strip()
            filename = f"{nombre_limpio}.json"

            data = avl.toJSON(avl.root)
            json_str = json.dumps(data, indent=4, ensure_ascii=False)

            st.download_button(
                label="Descargar",
                data=json_str,
                file_name=filename,
                mime="application/json"
            )

# METRICS
def count_leaves(node):
    if not node:
        return 0
    if not node.getLeftChild() and not node.getRightChild():
        return 1
    return count_leaves(node.getLeftChild()) + count_leaves(node.getRightChild())

height = avl.heightTree() if avl.root else 0
leaves = count_leaves(avl.root)

def animar_recorrido(nodes, container):
    st.session_state.recorrido = []
    st.session_state.highlight = None
    st.session_state.stop_animacion = False
    st.session_state.animando = True
    

    recorrido = []
    text_container = st.empty()

    for n in nodes:

        # 🔥 cancelar
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

    # 🔥 limpiar TODO al final o cancelación
    st.session_state.recorrido = []
    st.session_state.stop_animacion = False
    st.session_state.animando = False  # 👈 clave

    with container:
        draw_tree(avl)
# ===============================
# LAYOUT
# ===============================

col1, col2, col3 = st.columns([1, 2, 1])

# ===============================
#  LEFT
# ===============================

with col1:
    
    archivo = st.file_uploader("Load JSON", type="json")
    tipo = st.radio("Mode", ["Insertion", "Topology"])

    if st.button("Load Tree"):
        if archivo:
            data = json.load(archivo)
            new_avl = AVL()
            new_bst = BST()

            if tipo == "Insertion":
                buildByInsertion(new_avl, new_bst, data)
            else:
                new_avl.root = buildByTopology(data)

            st.session_state.avl = new_avl
            st.session_state.bst = new_bst
            st.success("Tree loaded")
            st.rerun()
        else:
            st.warning("Upload JSON")

    st.divider()

    st.button("Insert Flight", use_container_width=True)
    st.button("Edit Flight", use_container_width=True)
    st.button("Delete Node", use_container_width=True)
    st.button("Cancel Flight", use_container_width=True)

    st.divider()

    st.markdown("### Depth Control")
    depth = st.number_input("Max Depth", value=5)
    avl.limite = depth

    if st.button("Remove Low Profit Node"):
        try:
            avl.deleteMinProfit()
            st.success("Node removed")
            st.rerun()
        except:
            st.warning("Error")

# ===============================
# CENTER
# ===============================

with col2:
    tree_container = st.empty()
    with tree_container:
        draw_tree(avl)

# ===============================
# RIGHT
# ===============================

with col3:
    st.subheader("Metrics")

    # métricas compactas en una fila
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Height", height)
    m2.metric("Leaves", leaves)
    m3.metric("Rotations", "N/A")
    m4.metric("Cancel", st.session_state.mass_cancel)

    st.divider()

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
      nodes = avl.copyBreadthFirstSearch() or []
      animar_recorrido(nodes, tree_container)
      

    st.divider()
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

        # 🔥 REDIBUJAR SIN REINICIAR
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

    
