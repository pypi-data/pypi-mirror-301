import logging
import random
import warnings

import networkx as nx
import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import ndcg_score
from torch import nn
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
from tqdm import tqdm
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
        """
        self.device = device
        self.model_name = model_name
        self.batch_size = batch_size
        self.hidden_dim = hidden_dim
        self.margin = margin


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


class GNNSubgraphSelector:
    """Class for performing subgraph selection using GNNs to rank nodes."""

    def __init__(self, config: GNNSubgraphSelectorConfig):
        self.config = config
        self.device = torch.device(config.device)
        self.text_encoder = TextEncoder(
            config.model_name, self.device, config.batch_size, config.hidden_dim
        )
        self.gnn_model = TopKPredictor(config.hidden_dim).to(self.device)
        set_seed(42)

    def load_pretrained_gnn(self, model_path: str):
        """Load a pretrained GNN model for predicting relevance scores."""
        self.gnn_model.load_state_dict(torch.load(model_path, map_location=self.device))

    def save_gnn_model(self, save_path: str):
        """Save the trained GNN model."""
        torch.save(self.gnn_model.state_dict(), save_path)

    def select_subgraph(
        self, graph: nx.Graph, query: str, k_nodes: int = 5
    ) -> nx.Graph:
        """
        Select the most relevant subgraph from the graph based on the query.

        Parameters
        ----------
        graph : nx.Graph
            The input graph from which to select subgraphs.
        query : str
            The input text query guiding the subgraph selection.
        k_nodes : int
            The number of top nodes to select.

        Returns
        -------
        nx.Graph
            The selected subgraph.
        """
        # 1. Prepare node features and graph data
        node_features, node_list = self.prepare_node_features(graph)
        data = self.graph_to_data(graph, node_features)

        # 2. Embed the text query
        query_embedding = self.text_encoder.encode_text(query)

        # 3. Predict relevance scores for nodes
        node_scores = self.gnn_model(data, query_embedding)
        node_scores = node_scores.cpu().numpy()

        # 4. Select top-k nodes based on predicted scores
        top_k_indices = node_scores.argsort()[-k_nodes:][::-1]
        top_k_nodes = [node_list[idx] for idx in top_k_indices]

        # 5. Extract subgraph containing top-k nodes
        subgraph = graph.subgraph(top_k_nodes).copy()
        return subgraph

    def prepare_node_features(self, graph: nx.Graph) -> tuple[torch.Tensor, list]:
        """Prepare node features by encoding node texts.

        Parameters
        ----------
        graph : nx.Graph
            The input graph.

        Returns
        -------
        torch.Tensor
            Tensor containing features for each node.
        List
            List of node identifiers (in the same order as the features).
        """
        node_texts = []
        node_list = list(graph.nodes())

        for node in node_list:
            node_attrs = graph.nodes[node]
            if "text" in node_attrs and isinstance(node_attrs["text"], str):
                node_text = node_attrs["text"]
            else:
                node_text = f"Node {node}"
            node_texts.append(node_text)

        # Encode node texts
        node_embeddings = self.text_encoder.encode_texts(node_texts)
        return node_embeddings, node_list

    def graph_to_data(self, graph: nx.Graph, node_features: torch.Tensor) -> Data:
        """Convert NetworkX graph to PyTorch Geometric Data object.

        Parameters
        ----------
        graph : nx.Graph
            The input graph.
        node_features : torch.Tensor
            Tensor containing features for each node.

        Returns
        -------
        Data
            PyTorch Geometric Data object.
        """
        # relabel nodes to ensure labels are 0 to n-1
        mapping = {node: idx for idx, node in enumerate(graph.nodes())}
        graph = nx.relabel_nodes(graph, mapping)

        edge_index = (
            torch.tensor(list(graph.edges()), dtype=torch.long).t().contiguous()
        )

        if edge_index.numel() == 0:
            edge_index = torch.empty((2, 0), dtype=torch.long)

        data = Data(x=node_features, edge_index=edge_index)
        return data.to(self.device)

    def train(
        self,
        train_dataset: list[tuple[nx.Graph, str, list[int]]],
        val_dataset: list[tuple[nx.Graph, str, list[int]]],
        epochs: int = 100,
        learning_rate: float = 0.001,
        k: int = 5,
    ):
        """Train the GNN model using Margin Ranking Loss with validation evaluation.

        Parameters
        ----------
        train_dataset : List[Tuple[nx.Graph, str, List[int]]]
            Training data consisting of tuples (graph, query, true_top_k_nodes).
        val_dataset : List[Tuple[nx.Graph, str, List[int]]]
            Validation data consisting of tuples (graph, query, true_top_k_nodes).
        epochs : int
            Number of training epochs.
        learning_rate : float
            Learning rate for the optimizer.
        k : int
            Number of top nodes for evaluation metrics.
        """
        self.gnn_model.train()
        optimizer = torch.optim.Adam(self.gnn_model.parameters(), lr=learning_rate)
        margin_loss_fn = nn.MarginRankingLoss(margin=self.config.margin)

        for epoch in range(epochs):
            total_loss = 0.0
            for graph, query, true_top_k_nodes in tqdm(
                train_dataset, desc=f"Epoch {epoch+1}/{epochs}"
            ):
                node_features, node_list = self.prepare_node_features(graph)
                data = self.graph_to_data(graph, node_features)
                query_embedding = self.text_encoder.encode_text(query)

                optimizer.zero_grad()
                node_scores = self.gnn_model(data, query_embedding)

                # map true_top_k_nodes to indices
                node_to_idx = {node: idx for idx, node in enumerate(node_list)}
                positive_indices = [
                    node_to_idx[n] for n in true_top_k_nodes if n in node_to_idx
                ]
                negative_indices = [
                    idx for idx in range(len(node_list)) if idx not in positive_indices
                ]

                if not positive_indices or not negative_indices:
                    continue  # skip if we can't create pairs

                # sample negative indices
                num_pairs = min(len(positive_indices), len(negative_indices))
                sampled_positive_indices = random.sample(positive_indices, num_pairs)
                sampled_negative_indices = random.sample(negative_indices, num_pairs)

                pos_scores = node_scores[sampled_positive_indices]
                neg_scores = node_scores[sampled_negative_indices]

                # create labels: 1 means pos_score should be higher than neg_score
                y = torch.ones(len(pos_scores), device=self.device)

                loss = margin_loss_fn(pos_scores, neg_scores, y)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()

            avg_train_loss = total_loss / len(train_dataset)
            logger.info(
                f"Epoch {epoch+1}/{epochs}, Training Loss: {avg_train_loss:.4f}"
            )

            # validate after each epoch
            val_metrics = self.evaluate(val_dataset, k=k)
            logger.info(
                f"Epoch {epoch+1}/{epochs}, "
                f"Validation NDCG@{k}: {val_metrics[f'average_ndcg@{k}']:.4f}, "
                f"Precision@{k}: {val_metrics[f'average_precision@{k}']:.4f}, "
                f"Recall@{k}: {val_metrics[f'average_recall@{k}']:.4f}"
            )

    def evaluate(
        self, val_dataset: list[tuple[nx.Graph, str, list[int]]], k: int = 5
    ) -> dict[str, float]:
        """Evaluate the GNN model on the validation dataset.

        Parameters
        ----------
        val_dataset : List[Tuple[nx.Graph, str, List[int]]]
            The validation dataset.
        k : int
            The number of top nodes to consider for metrics.

        Returns
        -------
        Dict[str, float]
            A dictionary containing evaluation metrics.
        """
        self.gnn_model.eval()
        total_ndcg = 0.0
        total_precision_at_k = 0.0
        total_recall_at_k = 0.0

        with torch.no_grad():
            for graph, query, true_top_k_nodes in tqdm(val_dataset, desc="Evaluating"):
                node_features, node_list = self.prepare_node_features(graph)
                data = self.graph_to_data(graph, node_features)
                query_embedding = self.text_encoder.encode_text(query)

                # predict node scores
                node_scores = self.gnn_model(data, query_embedding)
                node_scores = node_scores.cpu().numpy()

                # map nodes to indices
                node_to_idx = {node: idx for idx, node in enumerate(node_list)}
                true_node_indices = [
                    node_to_idx[n] for n in true_top_k_nodes if n in node_to_idx
                ]

                # get ground truth labels (1 for top-k nodes, 0 otherwise)
                true_labels = np.zeros(len(node_list))
                true_labels[true_node_indices] = 1

                # compute NDCG@k
                ndcg = ndcg_score([true_labels], [node_scores], k=k)
                total_ndcg += ndcg

                # compute Precision@k and Recall@k
                top_k_predicted_indices = node_scores.argsort()[-k:][::-1]
                top_k_predicted_set = set(top_k_predicted_indices)
                top_k_true_set = set(true_node_indices)

                precision = precision_at_k(top_k_true_set, top_k_predicted_set, k)
                recall = recall_at_k(top_k_true_set, top_k_predicted_set, k)

                total_precision_at_k += precision
                total_recall_at_k += recall

        num_samples = len(val_dataset)
        metrics = {
            f"average_ndcg@{k}": total_ndcg / num_samples,
            f"average_precision@{k}": total_precision_at_k / num_samples,
            f"average_recall@{k}": total_recall_at_k / num_samples,
        }
        return metrics
