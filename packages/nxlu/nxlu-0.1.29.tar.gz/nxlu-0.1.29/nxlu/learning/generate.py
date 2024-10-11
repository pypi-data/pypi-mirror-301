import random

import networkx as nx

from nxlu.learning.query import generate_query_and_top_k

__all__ = ["generate_synthetic_graph"]


def generate_synthetic_graph(
    query_type: str = "centrality",
) -> tuple[nx.Graph, list]:
    """Generate a synthetic graph along with a query and top_k values.

    Parameters
    ----------
    query_type : str, optional
        The type of query to generate, by default "centrality".

    Returns
    -------
    Tuple[nx.Graph, List]
        A tuple containing the synthetic graph, top_k_nodes.
    """
    num_nodes = random.randint(20, 100)
    p = random.uniform(0.05, 0.2)
    graph = nx.erdos_renyi_graph(n=num_nodes, p=p)
    if not nx.is_connected(graph):
        largest_cc = max(nx.connected_components(graph), key=len)
        graph = graph.subgraph(largest_cc).copy()

    for node in graph.nodes():
        graph.nodes[node]["attributes"] = [random.random() for _ in range(10)]

    top_k_nodes = generate_query_and_top_k(graph, query_type)
    return graph, top_k_nodes
