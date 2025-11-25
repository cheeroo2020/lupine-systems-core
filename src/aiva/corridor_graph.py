import networkx as nx

def build_corridor_graph():
    """
    FX corridor graph for Aiva.
    Nodes = currencies
    Edges = FX tradeable routes with basic attributes.
    """
    G = nx.DiGraph()

    # Basic Phase 1 currency set
    currencies = ["AUD", "SGD", "USD", "EUR", "AED"]
    G.add_nodes_from(currencies)

    # FX corridors (simplified mock version)
    corridors = [
        ("AUD", "SGD"),
        ("AUD", "USD"),
        ("USD", "SGD"),
        ("USD", "EUR"),
        ("SGD", "EUR"),
        ("AED", "EUR"),
    ]
    G.add_edges_from(corridors)

    # Placeholder FX cost, volatility penalty, liquidity
    for u, v in G.edges():
        G[u][v]["spread"] = 0.004       # 40 bps spread (example)
        G[u][v]["stability"] = 0.95     # corridor stability
        G[u][v]["liquidity"] = 0.8      # mock liquidity depth

    return G


if __name__ == "__main__":
    graph = build_corridor_graph()
    print("Nodes:", list(graph.nodes()))
    print("Edges:", list(graph.edges(data=True)))

