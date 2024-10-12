import logging
import os
import random
import warnings
from pathlib import Path

import networkx as nx
import pytorch_lightning as pl
import torch
from pytorch_lightning.callbacks import EarlyStopping, ModelCheckpoint
from torch.utils.data import DataLoader, Dataset
from torch_geometric.datasets import Planetoid, TUDataset
from tqdm import tqdm

from nxlu.learning.augment import Paraphraser
from nxlu.learning.generate import generate_synthetic_graph
from nxlu.learning.gnn import GNNSubgraphSelector, GNNSubgraphSelectorConfig
from nxlu.learning.query import generate_query_and_top_k
from nxlu.utils.misc import set_seed

warnings.filterwarnings("ignore")

torch.backends.cudnn.benchmark = True

torch.set_num_threads(min(8, os.cpu_count()))

logger = logging.getLogger("nxlu")

__all__ = [
    "convert_pyg_to_networkx",
    "GraphDataset",
    "prepare_training_dataset",
    "custom_collate",
]


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


class GraphDataset(Dataset):
    """Custom Dataset for graph data."""

    def __init__(self, dataset):
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        graph, query, true_top_k_nodes = self.dataset[idx]
        return graph, query, true_top_k_nodes


def prepare_training_dataset(
    num_synthetic: int = 1000, val_split: float = 0.2
) -> tuple[GraphDataset, GraphDataset]:
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
    Tuple[GraphDataset, GraphDataset]
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

    return GraphDataset(train_dataset), GraphDataset(val_dataset)


def custom_collate(batch):
    graphs, queries, top_ks = zip(*batch)
    return list(graphs), list(queries), list(top_ks)


def main():
    set_seed(42)

    train_dataset, val_dataset = prepare_training_dataset()

    config = GNNSubgraphSelectorConfig(
        device="cuda" if torch.cuda.is_available() else "cpu",
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        batch_size=128,
        hidden_dim=384,
        early_stopping=True,
        early_stopping_patience=10,
        early_stopping_metric="average_ndcg@5",
        early_stopping_mode="max",
    )

    model = GNNSubgraphSelector(config)

    train_loader = DataLoader(
        train_dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=4,
        collate_fn=custom_collate,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=4,
        collate_fn=custom_collate,
    )

    early_stop_callback = EarlyStopping(
        monitor=config.early_stopping_metric,
        patience=config.early_stopping_patience,
        mode=config.early_stopping_mode,
        verbose=True,
    )

    checkpoint_callback = ModelCheckpoint(
        monitor=config.early_stopping_metric,
        dirpath=Path.home() / ".nxlu" / "checkpoints",
        filename="gnn_model-{epoch:02d}-{average_ndcg@5:.4f}",
        save_top_k=1,
        mode=config.early_stopping_mode,
    )

    trainer = pl.Trainer(
        max_epochs=100,
        accelerator="auto",
        devices=torch.cuda.device_count() if torch.cuda.is_available() else "cpu",
        callbacks=[early_stop_callback, checkpoint_callback],
        precision=(16 if torch.cuda.is_available() else 32),
        log_every_n_steps=10,
    )

    trainer.fit(model, train_loader, val_loader)

    save_dir = Path.home() / ".nxlu" / "models"
    save_dir.mkdir(parents=True, exist_ok=True)

    final_save_path = save_dir / "gnn_model_final.pth"
    torch.save(model.state_dict(), final_save_path)
    logger.info(f"Saved final model: {final_save_path}")


if __name__ == "__main__":
    main()
