import logging
import os
import random
import warnings

import networkx as nx
import torch
from torch_geometric.datasets import Planetoid, TUDataset
from tqdm import tqdm

from nxlu.learning.augment import Paraphraser
from nxlu.learning.generate import generate_synthetic_graph
from nxlu.learning.gnn import GNNSubgraphSelector, GNNSubgraphSelectorConfig
from nxlu.learning.query import generate_query_and_top_k
from nxlu.utils.misc import set_seed

warnings.filterwarnings("ignore")

torch.set_num_threads(os.cpu_count())


logger = logging.getLogger("nxlu")

__all__ = ["convert_pyg_to_networkx", "prepare_training_dataset"]


QUERY_MAP = {
    "centrality": "Identify the most central nodes in the network based on degree "
    "centrality.",
    "pagerank": "Find the nodes with the highest PageRank scores.",
    "betweenness": "Find the nodes with the highest betweenness centrality.",
    "eigenvector": "Find the nodes with the highest eigenvector centrality.",
    "clustering": "Find the nodes with the highest clustering coefficients.",
    "k_core": "Find the nodes in the k-core of the network.",
    "random_walk": "Find nodes frequently visited in random walks.",
    "random": "Select a random subset of nodes in the graph.",
    "motif_participation": "Find nodes participating in the specified motif (triangle)."
    "",
}


def convert_pyg_to_networkx(data) -> nx.Graph:
    """Convert a PyTorch Geometric Data object to a NetworkX graph.

    Parameters
    ----------
    data : torch_geometric.data.Data
        The PyTorch Geometric Data object.

    Returns
    -------
    nx.Graph
        The corresponding NetworkX graph.
    """
    graph = nx.Graph()
    edge_index = data.edge_index.cpu().numpy()
    for i in range(edge_index.shape[1]):
        u, v = edge_index[0][i], edge_index[1][i]
        graph.add_edge(u, v)

    if data.x is not None:
        for i, node in enumerate(graph.nodes()):
            graph.nodes[node]["embedding"] = data.x[i].cpu().numpy()

    return graph


def prepare_training_dataset(
    num_synthetic: int = 1000, val_split: float = 0.2
) -> tuple[list[tuple[nx.Graph, str, int]], list[tuple[nx.Graph, str, int]]]:
    """Prepare the training dataset.

    This function loads a PyTorch Geometric dataset, converts it to NetworkX graphs,
    generates queries and top_k values, and augments with synthetic data.

    Parameters
    ----------
    num_synthetic : int, optional
        Number of synthetic graphs to generate, by default 1000.
    val_split : float, optional
        Proportion of the dataset to include in the validation split, by default 0.2.

    Returns
    -------
    Tuple[List[Tuple[nx.Graph, str, int]], List[Tuple[nx.Graph, str, int]]]
        The prepared training and validation datasets.
    """
    combined_dataset = []

    paraphraser = Paraphraser()

    for query_type in list(QUERY_MAP.keys()):
        logger.info("Query type: {query_type}")

        tu_dataset = TUDataset(root="/tmp/IMDB-BINARY", name="IMDB-BINARY")

        planetoid_dataset = Planetoid(root="/tmp/Cora", name="Cora")

        num_return_sequences = min(5, 5)  # cannot exceed num_beams=5

        queries = paraphraser.paraphrase_queries(
            [QUERY_MAP[query_type]],
            num_return_sequences=num_return_sequences,
        )

        for data in tqdm(tu_dataset, desc="Processing TUDataset"):
            graph = convert_pyg_to_networkx(data)
            top_k_nodes = generate_query_and_top_k(graph, query_type=query_type)
            query = random.choice(queries)
            combined_dataset.append((graph, query, top_k_nodes))

        for data in tqdm(planetoid_dataset, desc="Processing Planetoid Dataset"):
            graph = convert_pyg_to_networkx(data)
            top_k_nodes = generate_query_and_top_k(graph, query_type=query_type)
            query = random.choice(queries)
            combined_dataset.append((graph, query, top_k_nodes))

        for _ in tqdm(range(num_synthetic), desc="Generating Synthetic Graphs"):
            synthetic_graph, top_k_nodes = generate_synthetic_graph(
                query_type=query_type
            )
            query = random.choice(queries)
            combined_dataset.append((synthetic_graph, query, top_k_nodes))

    # shuffle the combined dataset
    random.shuffle(combined_dataset)

    # split into training and validation sets
    split_index = int(len(combined_dataset) * (1 - val_split))
    train_dataset = combined_dataset[:split_index]
    val_dataset = combined_dataset[split_index:]

    return train_dataset, val_dataset


def main():
    set_seed(42)

    train_dataset, val_dataset = prepare_training_dataset()

    config = GNNSubgraphSelectorConfig(
        device="cuda" if torch.cuda.is_available() else "cpu",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        batch_size=64,
        hidden_dim=384,
    )

    selector = GNNSubgraphSelector(config)

    selector.train(train_dataset, val_dataset, epochs=50, learning_rate=0.001)

    # validation_metrics = selector.evaluate(val_dataset)
    # logger.info(validation_metrics)

    selector.save_gnn_model("nxlu/data/gnn_model.pth")


if __name__ == "__main__":
    main()
