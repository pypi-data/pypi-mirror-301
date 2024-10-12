import logging
import random
import warnings

import networkx as nx
import numpy as np
import pytorch_lightning as pl
import torch
import torch.nn.functional as F
from sklearn.metrics import ndcg_score
from torch import nn
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from transformers import AutoModel, AutoTokenizer

from nxlu.utils.misc import set_seed

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")


def compute_ndcg(true_labels, predicted_scores, k=5):
    """Compute NDCG@k for a single instance.

    Parameters
    ----------
    true_labels : List[int]
        Binary labels indicating the presence of top-k items.
    predicted_scores : List[float]
        Predicted relevance scores for the items.
    k : int
        Rank position.

    Returns
    -------
    float
        NDCG@k score.
    """
    return ndcg_score([true_labels], [predicted_scores], k=k)


def precision_at_k(true_set, predicted_set, k):
    """Compute precision at k for top-k node/edge selection.

    Parameters
    ----------
    true_set : set
        Ground truth set of top-k node/edge indices.
    predicted_set : set
        Predicted set of top-k node/edge indices.
    k : int
        The number of top items to consider.

    Returns
    -------
    float
        Precision at k.
    """
    true_positives = len(true_set.intersection(predicted_set))
    return true_positives / k


def recall_at_k(true_set, predicted_set, k):
    """Compute recall at k for top-k node/edge selection.

    Parameters
    ----------
    true_set : set
        Ground truth set of top-k node/edge indices.
    predicted_set : set
        Predicted set of top-k node/edge indices.
    k : int
        The number of top items to consider.

    Returns
    -------
    float
        Recall at k.
    """
    if len(true_set) == 0:
        return 0.0
    true_positives = len(true_set.intersection(predicted_set))
    return true_positives / len(true_set)


class GNNSubgraphSelectorConfig:
    """Configuration for GNN-based subgraph selection."""

    def __init__(
        self,
        device: str = "cpu",
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        batch_size: int = 64,
        hidden_dim: int = 384,
        margin: float = 1.0,
        learning_rate: float = 0.001,
        early_stopping: bool = True,
        early_stopping_patience: int = 10,
        early_stopping_metric: str = "average_ndcg@5",
        early_stopping_mode: str = "max",
    ):
        """Initialize the configuration.

        Parameters
        ----------
        device : str
            Device to run the models on ('cpu' or 'cuda').
        model_name : str
            Pre-trained language model for encoding text queries and node texts.
        batch_size : int
            Batch size for embedding node texts.
        hidden_dim : int
            Dimension of the GNN embeddings.
        margin : float
            Margin value for the Margin Ranking Loss.
        learning_rate : float
            The learning rate of the optimizer.
        early_stopping : bool
            Whether to use early stopping.
        early_stopping_patience : int
            Number of epochs with no improvement after which training will be stopped.
        early_stopping_metric : str
            The metric to monitor for early stopping.
        early_stopping_mode : str
            One of 'min' or 'max'. In 'min' mode, training will stop when the monitored
            metric stops decreasing.
            In 'max' mode, it will stop when the monitored metric stops increasing.
        """
        self.device = device
        self.model_name = model_name
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.margin = margin
        self.learning_rate = learning_rate
        self.early_stopping = early_stopping
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_metric = early_stopping_metric
        self.early_stopping_mode = early_stopping_mode


class TextEncoder(nn.Module):
    """Text encoder using a pre-trained language model."""

    def __init__(self, model_name: str, device: str, batch_size: int, hidden_dim: int):
        super().__init__()
        self.device = device
        self.model = AutoModel.from_pretrained(model_name).to(device)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.projection = nn.Linear(self.model.config.hidden_size, hidden_dim).to(
            device
        )

    def encode_text(self, text: str) -> torch.Tensor:
        """Encode a single text into a vector embedding."""
        self.eval()
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, max_length=512
        ).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        # project to hidden_dim
        embedding = self.projection(embedding)
        return embedding  # [1, hidden_dim]

    def encode_texts(self, texts: list[str]) -> torch.Tensor:
        """Encode a list of texts into vector embeddings."""
        self.eval()
        embeddings = []
        for i in range(0, len(texts), self.batch_size):
            batch_texts = texts[i : i + self.batch_size]
            inputs = self.tokenizer(
                batch_texts,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512,
            ).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            batch_embeddings = outputs.last_hidden_state[:, 0, :]  # [CLS] token
            # project to hidden_dim
            batch_embeddings = self.projection(batch_embeddings)
            embeddings.append(batch_embeddings)
        embeddings = torch.cat(embeddings, dim=0)
        return embeddings  # [num_texts, hidden_dim]

    def encode_queries(self, queries: list[str]) -> torch.Tensor:
        """Encode a list of queries into vector embeddings."""
        return self.encode_texts(queries)


class TopKPredictor(nn.Module):
    """GNN model for predicting relevance scores for nodes."""

    def __init__(self, hidden_dim):
        super().__init__()
        self.conv1 = GCNConv(hidden_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim + hidden_dim, 1)  # relevance score

    def forward(self, data: Data, query_embedding: torch.Tensor):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = F.relu(self.conv2(x, edge_index))
        # expand query_embedding to match number of nodes
        query_embedding_expanded = query_embedding.repeat(x.size(0), 1)
        # concatenate node embeddings + query embedding
        combined = torch.cat([x, query_embedding_expanded], dim=1)
        node_scores = self.fc(combined).squeeze()
        return node_scores  # [num_nodes]


class GNNSubgraphSelector(pl.LightningModule):
    """LightningModule for GNN-based subgraph selection."""

    def __init__(self, config: GNNSubgraphSelectorConfig):
        super().__init__()
        self.config = config
        self.text_encoder = TextEncoder(
            config.model_name, config.device, config.batch_size, config.hidden_dim
        )
        self.gnn_model = TopKPredictor(config.hidden_dim).to(self.device)
        if torch.cuda.device_count() > 1:
            logger.info(f"Using {torch.cuda.device_count()} GPUs")
            self.gnn_model = nn.DataParallel(self.gnn_model)

        set_seed(42)

        self.loss_fn = nn.MarginRankingLoss(margin=self.config.margin)

    def forward(self, data: Data, query_embedding: torch.Tensor):
        return self.gnn_model(data, query_embedding)

    def prepare_node_features(self, graph: nx.Graph) -> tuple[torch.Tensor, list]:
        """Prepare node features by encoding node texts."""
        node_texts = []
        node_list = list(graph.nodes())

        for node in node_list:
            node_attrs = graph.nodes[node]
            if "text" in node_attrs and isinstance(node_attrs["text"], str):
                node_text = node_attrs["text"]
            else:
                node_text = f"Node {node}"
            node_texts.append(node_text)

        # encode node texts
        node_embeddings = self.text_encoder.encode_texts(node_texts)
        return node_embeddings, node_list

    def graph_to_data(self, graph: nx.Graph, node_features: torch.Tensor) -> Data:
        """Convert NetworkX graph to PyTorch Geometric Data object."""
        # relabel nodes to ensure labels are 0 to n-1
        mapping = {node: idx for idx, node in enumerate(graph.nodes())}
        graph = nx.relabel_nodes(graph, mapping)

        edge_index = (
            torch.tensor(list(graph.edges()), dtype=torch.long).t().contiguous()
        )

        if edge_index.numel() == 0:
            edge_index = torch.empty((2, 0), dtype=torch.long)

        data = Data(x=node_features, edge_index=edge_index)
        return data.to(self.config.device)

    def training_step(self, batch, batch_idx):
        graphs, queries, true_top_k_nodes = batch
        batch_size = len(graphs)
        total_loss = 0.0
        valid_instances = 0

        for graph, query, top_k in zip(graphs, queries, true_top_k_nodes):
            node_features, node_list = self.prepare_node_features(graph)
            data = self.graph_to_data(graph, node_features)
            query_embedding = self.text_encoder.encode_text(query)

            node_scores = self(data, query_embedding)

            # map true_top_k_nodes to indices
            node_to_idx = {node: idx for idx, node in enumerate(node_list)}
            positive_indices = [node_to_idx[n] for n in top_k if n in node_to_idx]
            negative_indices = [
                idx for idx in range(len(node_list)) if idx not in positive_indices
            ]

            if not positive_indices or not negative_indices:
                continue

            # sample negative indices
            num_pairs = min(len(positive_indices), len(negative_indices))
            sampled_positive_indices = random.sample(positive_indices, num_pairs)
            sampled_negative_indices = random.sample(negative_indices, num_pairs)

            pos_scores = node_scores[sampled_positive_indices]
            neg_scores = node_scores[sampled_negative_indices]

            # create labels: 1 means pos_score should be higher than neg_score
            y = torch.ones(len(pos_scores), device=self.device)

            loss = self.loss_fn(pos_scores, neg_scores, y)
            total_loss += loss
            valid_instances += 1

        if valid_instances > 0:
            avg_loss = total_loss / valid_instances
        else:
            avg_loss = torch.tensor(0.0, requires_grad=True).to(self.device)

        self.log(
            "train_loss",
            avg_loss,
            on_step=True,
            on_epoch=True,
            prog_bar=True,
            logger=True,
            batch_size=batch_size,
        )
        return avg_loss

    def validation_step(self, batch, batch_idx):
        graphs, queries, true_top_k_nodes = batch
        batch_size = len(graphs)
        total_ndcg = 0.0
        total_precision = 0.0
        total_recall = 0.0
        total_loss = 0.0
        valid_instances = 0

        for graph, query, top_k in zip(graphs, queries, true_top_k_nodes):
            node_features, node_list = self.prepare_node_features(graph)
            data = self.graph_to_data(graph, node_features)
            query_embedding = self.text_encoder.encode_text(query)

            node_scores = self(data, query_embedding)
            node_scores = node_scores.cpu().numpy()

            node_to_idx = {node: idx for idx, node in enumerate(node_list)}
            true_node_indices = [node_to_idx[n] for n in top_k if n in node_to_idx]

            # get ground truth labels (1 for top-k nodes, 0 otherwise)
            true_labels = np.zeros(len(node_list))
            true_labels[true_node_indices] = 1

            # NDCG@k
            ndcg = compute_ndcg(true_labels, node_scores, k=5)
            total_ndcg += ndcg

            # Precision@k and Recall@k
            top_k_predicted_indices = node_scores.argsort()[-5:][::-1]
            top_k_predicted_set = set(top_k_predicted_indices)
            top_k_true_set = set(true_node_indices)

            precision = precision_at_k(top_k_true_set, top_k_predicted_set, 5)
            recall = recall_at_k(top_k_true_set, top_k_predicted_set, 5)

            total_precision += precision
            total_recall += recall

            # compute validation Loss
            node_scores_tensor = torch.tensor(node_scores, device=self.device)

            # map true_top_k_nodes to indices
            positive_indices = [node_to_idx[n] for n in top_k if n in node_to_idx]
            negative_indices = [
                idx for idx in range(len(node_list)) if idx not in positive_indices
            ]

            if not positive_indices or not negative_indices:
                continue

            # sample negative indices
            num_pairs = min(len(positive_indices), len(negative_indices))
            sampled_positive_indices = random.sample(positive_indices, num_pairs)
            sampled_negative_indices = random.sample(negative_indices, num_pairs)

            pos_scores = node_scores_tensor[sampled_positive_indices]
            neg_scores = node_scores_tensor[sampled_negative_indices]

            # create labels: 1 means pos_score should be higher than neg_score
            y = torch.ones(len(pos_scores), device=self.device)

            # compute loss
            loss = self.loss_fn(pos_scores, neg_scores, y)
            total_loss += loss
            valid_instances += 1

        if valid_instances > 0:
            avg_ndcg = total_ndcg / valid_instances
            avg_precision = total_precision / valid_instances
            avg_recall = total_recall / valid_instances
            avg_loss = total_loss / valid_instances
        else:
            avg_ndcg = 0.0
            avg_precision = 0.0
            avg_recall = 0.0
            avg_loss = torch.tensor(0.0, requires_grad=True).to(self.device)

        self.log(
            "val_average_ndcg@5",
            avg_ndcg,
            on_epoch=True,
            prog_bar=True,
            logger=True,
            batch_size=batch_size,
        )
        self.log(
            "val_average_precision@5",
            avg_precision,
            on_epoch=True,
            prog_bar=True,
            logger=True,
            batch_size=batch_size,
        )
        self.log(
            "val_average_recall@5",
            avg_recall,
            on_epoch=True,
            prog_bar=True,
            logger=True,
            batch_size=batch_size,
        )
        self.log(
            "val_loss",
            avg_loss,
            on_epoch=True,
            prog_bar=True,
            logger=True,
            batch_size=batch_size,
        )

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=self.config.learning_rate)
        return optimizer
