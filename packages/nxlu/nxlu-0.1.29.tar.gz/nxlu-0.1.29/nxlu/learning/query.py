import logging
import random
import warnings
from typing import TYPE_CHECKING

import networkx as nx

if TYPE_CHECKING:
    from collections.abc import Callable

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

__all__ = [
    "generate_query_and_top_k",
    "centrality_query",
    "pagerank_query",
    "betweenness_query",
    "eigenvector_query",
    "clustering_query",
    "k_core_query",
    "motif_participation_query",
    "random_query",
    "random_walk_query",
]


def generate_query_and_top_k(graph: nx.Graph, query_type: str = "centrality") -> list:
    """Generate a synthetic query for graph and determine top_k_nodes.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    query_type : str, optional
        The type of query generated, by default "centrality".

    Returns
    -------
    List
        A tuple containing the top_k_nodes.
    """
    query_functions: dict[str, Callable[[nx.Graph], list[int]]] = {
        "centrality": centrality_query,
        "pagerank": pagerank_query,
        "betweenness": betweenness_query,
        "eigenvector": eigenvector_query,
        "clustering": clustering_query,
        "k_core": k_core_query,
        "random_walk": random_walk_query,
        "random": random_query,
        "motif_participation": motif_participation_query,
    }

    query_func = query_functions.get(query_type, centrality_query)

    try:
        top_nodes = query_func(graph)
    except Exception:
        top_nodes = centrality_query(graph)

    if isinstance(top_nodes, int):
        top_k_nodes = [top_nodes]
    else:
        top_k_nodes = top_nodes

    return top_k_nodes


def centrality_query(
    graph: nx.Graph,
) -> list[int]:
    """Identify the most central nodes based on degree centrality.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    degree_dict = dict(graph.degree())
    sorted_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)  # Top 10% nodes or at least 1
    top_nodes = [node for node, degree in sorted_nodes[:top_k_nodes]]
    return top_nodes


def pagerank_query(graph: nx.Graph) -> list[int]:
    """Find the nodes with the highest PageRank scores.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    pagerank_dict = nx.pagerank(graph)
    sorted_nodes = sorted(pagerank_dict.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)
    top_nodes = [node for node, pr in sorted_nodes[:top_k_nodes]]
    return top_nodes


def betweenness_query(graph: nx.Graph) -> list[int]:
    """Find the nodes with the highest betweenness centrality.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    betweenness_dict = nx.betweenness_centrality(graph)
    sorted_nodes = sorted(betweenness_dict.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)
    top_nodes = [node for node, bc in sorted_nodes[:top_k_nodes]]
    return top_nodes


def eigenvector_query(graph: nx.Graph) -> list[int]:
    """Find the nodes with the highest eigenvector centrality.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    try:
        eigenvector_dict = nx.eigenvector_centrality(graph, max_iter=1000)
    except nx.NetworkXException:
        return centrality_query(graph)
    sorted_nodes = sorted(eigenvector_dict.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)
    top_nodes = [node for node, ec in sorted_nodes[:top_k_nodes]]
    return top_nodes


def clustering_query(graph: nx.Graph) -> list[int]:
    """Find nodes with the highest clustering coefficients.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    clustering_dict = nx.clustering(graph)
    sorted_nodes = sorted(clustering_dict.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)
    top_nodes = [node for node, cc in sorted_nodes[:top_k_nodes]]
    return top_nodes


def k_core_query(graph: nx.Graph, k: int = 2) -> list[int]:
    """Find nodes based on k-core decomposition.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    k : int, optional
        The core number to consider, by default 2.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    k_core_dict = nx.core_number(graph)
    sorted_nodes = sorted(k_core_dict.items(), key=lambda x: x[1], reverse=True)

    # extract nodes with core number >= k
    top_nodes = [node for node, core in sorted_nodes if core >= k]

    if not top_nodes:
        top_nodes = [sorted_nodes[0][0]]

    return top_nodes


def random_walk_query(
    graph: nx.Graph, source: int | None = None, walks: int = 100
) -> list[int]:
    """Determine node relevance based on random walk proximity.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    source : int, optional
        The source node for random walks. If None, select randomly, by default None.
    walks : int, optional
        Number of random walks to perform, by default 100.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    if source is None:
        source = random.choice(list(graph.nodes()))
    walk_counts = {node: 0 for node in graph.nodes()}
    for _ in range(walks):
        current = source
        walk_length = random.randint(1, 10)  # random walk length between 1 and 10
        for _ in range(walk_length):
            neighbors = list(graph.neighbors(current))
            if not neighbors:
                break
            current = random.choice(neighbors)
            walk_counts[current] += 1
    sorted_nodes = sorted(walk_counts.items(), key=lambda x: x[1], reverse=True)
    top_k_nodes = max(int(0.1 * len(sorted_nodes)), 1)
    top_nodes = [node for node, count in sorted_nodes[:top_k_nodes]]
    return top_nodes


def random_query(graph: nx.Graph) -> list[int]:
    """Select a random subset of nodes in the graph.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    top_k_nodes = max(int(0.1 * len(graph.nodes())), 1)
    top_nodes = random.sample(list(graph.nodes()), top_k_nodes)
    return top_nodes


def motif_participation_query(
    graph: nx.Graph, motif: nx.Graph | None = None
) -> list[int]:
    """Select nodes participating in specific motifs.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    motif : nx.Graph, optional
        The motif to search for, by default None.
        If None, use a default triangle motif.

    Returns
    -------
    List[int]
        List of top node IDs.
    """
    if motif is None:
        motif = nx.complete_graph(3)

    matcher = nx.algorithms.isomorphism.GraphMatcher(graph, motif)
    participating_nodes = set()
    for subgraph in matcher.subgraph_isomorphisms_iter():
        participating_nodes.update(subgraph.keys())

    top_k_nodes = max(int(0.1 * len(participating_nodes)), 1)
    top_nodes = list(participating_nodes)[:top_k_nodes]
    return top_nodes
