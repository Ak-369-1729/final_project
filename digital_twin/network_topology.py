import networkx as nx
import matplotlib.pyplot as plt

from node_isolation.isolation_engine import get_isolated_nodes

# =========================================================
# CREATE DIGITAL TWIN NETWORK
# =========================================================
def create_network():

    G = nx.Graph()

    nodes = [
        "Node_A",
        "Node_B",
        "Node_C",
        "Node_D",
        "Node_E"
    ]

    edges = [
        ("Node_A", "Node_B"),
        ("Node_A", "Node_C"),
        ("Node_B", "Node_D"),
        ("Node_C", "Node_D"),
        ("Node_D", "Node_E")
    ]

    G.add_nodes_from(nodes)

    G.add_edges_from(edges)

    return G

# =========================================================
# DRAW NETWORK
# =========================================================
def draw_network(
    G,
    node_status=None,
    anomaly_nodes=None
):

    plt.figure(figsize=(10, 7))

    pos = nx.spring_layout(G, seed=42)

    isolated_nodes = get_isolated_nodes()

    node_colors = []

    # -----------------------------------------------------
    # NODE COLOR LOGIC
    # -----------------------------------------------------
    for node in G.nodes():

        if node in isolated_nodes:

            node_colors.append("red")

        elif anomaly_nodes and node in anomaly_nodes:

            node_colors.append("orange")

        else:

            node_colors.append("green")

    # -----------------------------------------------------
    # DRAW GRAPH
    # -----------------------------------------------------
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=3000,
        font_size=10,
        font_weight="bold",
        node_color=node_colors,
        edge_color="gray"
    )

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------
    plt.title(
        "AI-Based Cybersecurity Digital Twin",
        fontsize=14,
        fontweight="bold"
    )

    # -----------------------------------------------------
    # LEGEND
    # -----------------------------------------------------
    from matplotlib.lines import Line2D

    legend_elements = [

        Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            label='Active',
            markerfacecolor='green',
            markersize=12
        ),

        Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            label='Suspicious',
            markerfacecolor='orange',
            markersize=12
        ),

        Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            label='Isolated',
            markerfacecolor='red',
            markersize=12
        )
    ]

    plt.legend(
        handles=legend_elements,
        loc='upper right'
    )

    plt.tight_layout()

    plt.show()

# =========================================================
# MAIN
# =========================================================
if __name__ == "__main__":

    G = create_network()

    draw_network(G)