import networkx as nx

def build_hop_graph():
    """
    Base settlement hop graph for Aiva.

    Nodes = institutions (banks, PSPs, correspondents)
    Edges = settlement pathways with base attributes.
    """
    G = nx.DiGraph()

    # Define institutions (Phase 1 basic version)
    nodes = [
        "AU_BANK_A",
        "AU_BANK_B",
        "SG_CORR_1",
        "SG_CORR_2",
        "EU_BANK_X",
        "EU_BANK_Y",
    ]
    G.add_nodes_from(nodes)

    # Settlement pathways (simple version)
    edges = [
        ("AU_BANK_A", "SG_CORR_1"),
        ("SG_CORR_1", "EU_BANK_X"),
        ("AU_BANK_B", "SG_CORR_2"),
        ("SG_CORR_2", "EU_BANK_Y"),
        ("SG_CORR_1", "SG_CORR_2"),   # intra-SG corridor
    ]
    G.add_edges_from(edges)

    # Add base weights (will be refined by Scoring Engine)
    for u, v in G.edges():
        G[u][v]["latency"] = 120         # seconds
        G[u][v]["reliability"] = 0.98    # 98% success probability

    return G


# For quick local testing (optional)
if __name__ == "__main__":
    G = build_hop_graph()
    print("Nodes:", list(G.nodes()))
    print("Edges:", list(G.edges(data=True)))

