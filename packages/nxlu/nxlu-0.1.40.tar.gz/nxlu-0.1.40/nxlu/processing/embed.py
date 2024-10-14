import logging
import warnings
from typing import Any

import networkx as nx
import torch
from huggingface_hub import PyTorchModelHubMixin
from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.schema import TextNode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from torch import nn
from transformers import AutoModel

from nxlu.processing.preprocess import create_subgraph
from nxlu.utils.control import NetworkXGraphStore

warnings.filterwarnings("ignore")


logger = logging.getLogger("nxlu")


__all__ = ["CustomModel", "QuerySubgraph"]


class CustomModel(nn.Module, PyTorchModelHubMixin):
    """Custom neural network model for domain classification.

    Attributes
    ----------
    model : transformers.AutoModel
        The pre-trained transformer model.
    dropout : torch.nn.Dropout
        Dropout layer for regularization.
    fc : torch.nn.Linear
        Fully connected layer for classification.
    """

    def __init__(self, config):
        super().__init__()
        self.model = AutoModel.from_pretrained(config["base_model"])
        self.dropout = nn.Dropout(config["fc_dropout"])
        self.fc = nn.Linear(self.model.config.hidden_size, len(config["id2label"]))

    def forward(self, input_ids, attention_mask):
        """Forward pass through the network.

        Parameters
        ----------
        input_ids : torch.Tensor
            Token IDs.
        attention_mask : torch.Tensor
            Attention masks.

        Returns
        -------
        torch.Tensor
            Softmax probabilities for each class.
        """
        features = self.model(
            input_ids=input_ids, attention_mask=attention_mask
        ).last_hidden_state
        dropped = self.dropout(features)
        outputs = self.fc(dropped)
        return torch.softmax(outputs[:, 0, :], dim=1)


class QuerySubgraph:
    """A class to manage and query a subgraph using vector embeddings.

    It maintains separate node and edge indices for comprehensive querying.

    Attributes
    ----------
    data_graph : nx.Graph
        The NetworkX graph containing the data to be queried.
    graph_store : NetworkXGraphStore or None
        A store for managing the graph structure and data.
    index_nodes : VectorStoreIndex or None
        The vector store index for querying nodes in the graph.
    index_edges : VectorStoreIndex or None
        The vector store index for querying edges in the graph.
    embedding_model : HuggingFaceEmbedding
        The embedding model used for indexing and querying nodes and edges.
    similarity_metric : str
        The similarity metric used for querying (e.g., 'cosine').
    mmr_threshold : float
        The threshold for Maximal Marginal Relevance (MMR).
    """

    def __init__(
        self,
        similarity_metric: str = "cosine",
        mmr_threshold: float = 0.2,
        embedding_model_name: str = "all-MiniLM-L6-v2",
    ):
        """Initialize the QuerySubgraph class with an empty graph, a graph store,
        separate indices for nodes and edges, and an embedding model for vector-based
        queries. Includes caching capabilities to speed up repeated queries.

        Parameters
        ----------
        similarity_metric : str
            The similarity metric used for querying (e.g., 'cosine').
        mmr_threshold : float
            The threshold for Maximal Marginal Relevance (MMR).
        embedding_model_name : str
            The name of the pre-trained embedding model.
        """
        self.data_graph = nx.Graph()
        self.graph_store = NetworkXGraphStore(self.data_graph)
        self.similarity_metric = similarity_metric
        self.mmr_threshold = mmr_threshold
        self.index_nodes = None
        self.index_edges = None
        self.embedding_model = HuggingFaceEmbedding(model_name=embedding_model_name)

    def load_data_graph(
        self,
        data: list[tuple[str, str, dict[str, Any]]],
        nodes: dict[str, dict[str, Any]],
    ):
        """Load the actual data graph, ensuring token nodes are excluded.

        Parameters
        ----------
        data : List[Tuple[str, str, Dict[str, Any]]]
            A list of edges in the form of (node1, node2, attributes) where attributes
            contain edge information (e.g., weight).
        nodes : Dict[str, Dict[str, Any]]
            A dictionary where keys are node identifiers and values are dictionaries of
            node attributes.

        Returns
        -------
        None
        """
        if not isinstance(data, list) or not all(
            isinstance(edge, tuple) and len(edge) == 3 for edge in data
        ):
            logger.error("Invalid data format for edges.")
        if not isinstance(nodes, dict):
            logger.error("Invalid data format for nodes.")

        try:
            for node, attrs in nodes.items():
                if not self._is_token_node(node, attrs):
                    self.data_graph.add_node(node, **attrs)
                    logger.debug(f"Added node: {node} with attributes: {attrs}")

            filtered_data = [
                (u, v, d)
                for u, v, d in data
                if not self._is_token_node(u, nodes.get(u, {}))
                and not self._is_token_node(v, nodes.get(v, {}))
            ]

            if not filtered_data:
                logger.warning("No valid edges to add after filtering token nodes.")

            self.data_graph.add_weighted_edges_from(
                [(u, v, d.get("weight", 1.0)) for u, v, d in filtered_data]
            )
            logger.info(
                f"Data graph loaded with {self.data_graph.number_of_nodes()} nodes and "
                f"{self.data_graph.number_of_edges()} edges."
            )
        except Exception:
            logger.exception("Failed to load data graph")
            raise

    def _is_token_node(self, node: str, attrs: dict[str, Any]) -> bool:
        """Determine if a node is a token node based on attributes.

        Parameters
        ----------
        node : str
            The node identifier.
        attrs : Dict[str, Any]
            The attributes associated with the node.

        Returns
        -------
        bool
            True if the node is identified as a token node, False otherwise.
        """
        return attrs.get("type") == "token" if attrs else False

    def _extract_node_id(self, node_text: str) -> str:
        """Extract the node ID from the node text.

        Assumes the format: "Node: {node}, Attributes: {data}"

        Parameters
        ----------
        node_text : str
            The text representation of the node.

        Returns
        -------
        str
            The extracted node ID, or an empty string if extraction fails.
        """
        try:
            return node_text.split(",")[0].split(":")[1].strip()
        except IndexError:
            logger.warning(f"Unable to extract node ID from text: {node_text}")
            return ""
        except Exception:
            logger.exception("Error during node ID extraction.")
            return ""

    def _extract_edge_tuple(self, edge_text: str) -> tuple:
        """Extract the edge tuple (u, v) or (u, v, key) from the edge text.

        Assumes: "Edge: {u} -- {relation} (Weight: {weight}) --> {v} | ID: {edge_id}"

        Parameters
        ----------
        edge_text : str
            The text representation of the edge.

        Returns
        -------
        Tuple
            The extracted edge tuple.
        """
        try:
            edge_id = edge_text.split("| ID:")[1].strip()
            return tuple(edge_id.split("-"))
        except IndexError:
            logger.warning(f"Unable to extract edge tuple from text: {edge_text}")
            return ()
        except Exception:
            logger.exception("Error during edge tuple extraction.")
            return ()

    def prepare_node_index(self):
        """Prepare the VectorStoreIndex for nodes by indexing the data graph's nodes.
        Utilizes caching to avoid recomputing indices.

        Returns
        -------
        None
        """
        logger.info("Preparing node index for efficient querying.")

        storage_context_nodes = StorageContext.from_defaults(
            graph_store=self.graph_store
        )

        node_texts = [
            TextNode(text=f"Node: {node}, Attributes: {data}", id_=str(node))
            for node, data in self.data_graph.nodes(data=True)
            if not self._is_token_node(node, data)
        ]

        self.index_nodes = VectorStoreIndex(
            nodes=node_texts,
            storage_context=storage_context_nodes,
            embed_model=self.embedding_model,
        )

    def prepare_edge_index(self, subgraph: nx.Graph):
        """Prepare the VectorStoreIndex for edges by indexing the edges of a subgraph.
        Utilizes caching to avoid recomputing indices.

        Parameters
        ----------
        subgraph : nx.Graph or nx.MultiGraph
            The subgraph containing the nodes and edges to be indexed.

        Returns
        -------
        None
        """
        logger.info("Preparing edge index for efficient querying.")

        if isinstance(subgraph, (nx.MultiGraph, nx.MultiDiGraph)):
            edge_texts = [
                TextNode(
                    text=f"Edge: {u} -- {data.get('relation', 'EDGE')} "
                    f"(Weight: {data.get('weight', 'N/A')}) --> {v} | "
                    f"ID: {u}-{v}-{key}",
                    id_=f"{u}-{v}-{key}",
                )
                for u, v, key, data in subgraph.edges(keys=True, data=True)
                if not self._is_token_node(u, subgraph.nodes[u])
                and not self._is_token_node(v, subgraph.nodes[v])
            ]
        else:
            edge_texts = [
                TextNode(
                    text=f"Edge: {u} -- {data.get('relation', 'EDGE')} "
                    f"(Weight: {data.get('weight', 'N/A')}) --> {v} | ID: {u}-{v}",
                    id_=f"{u}-{v}",
                )
                for u, v, data in subgraph.edges(data=True)
                if not self._is_token_node(u, subgraph.nodes[u])
                and not self._is_token_node(v, subgraph.nodes[v])
            ]

        self.index_edges = VectorStoreIndex(
            nodes=edge_texts,
            storage_context=StorageContext.from_defaults(graph_store=self.graph_store),
            embed_model=self.embedding_model,
        )

    def query_graph(
        self,
        query: str,
        top_k_nodes: int = 1000,
        top_k_edges: int = 1000000,
    ) -> tuple[list[str], list[tuple[str, str]]]:
        """Query both the node and edge indices to retrieve relevant nodes and edges.

        Parameters
        ----------
        query : str
            The user's query to search for relevant nodes and edges.
        top_k_nodes : int, optional
            A count of the top relevant nodes to retrieve, by default 1000.
        top_k_edges : int, optional
            A count of the top relevant edges to retrieve, by default 1000000.

        Returns
        -------
        Tuple[List[str], List[Tuple[str, str]]]
            A tuple containing two lists:
            - List of node IDs that are most relevant to the query.
            - List of edge tuples that are most relevant to the query, constrained to
            the relevant nodes.
        """
        logger.info(f"Querying graph with: {query}")

        self.prepare_node_index()

        if not self.index_nodes:
            logger.error(
                "Node index has not been prepared. Call prepare_node_index first."
            )
            return [], []

        node_query_engine = self.index_nodes.as_query_engine(
            similarity_top_k=top_k_nodes,
            mmr_threshold=self.mmr_threshold,
            similarity_metric=self.similarity_metric,
        )
        node_response = node_query_engine.query(query)
        relevant_nodes_text = [node.text for node in node_response.source_nodes]
        logger.debug(f"Relevant nodes retrieved: {relevant_nodes_text}")

        node_ids = [
            self._extract_node_id(node_text) for node_text in relevant_nodes_text
        ]
        node_ids = [nid for nid in node_ids if nid]
        logger.debug(f"Extracted node IDs: {node_ids}")

        node_filtered_subgraph = create_subgraph(self.data_graph, node_subset=node_ids)

        self.prepare_edge_index(node_filtered_subgraph)

        if not self.index_edges:
            logger.error(
                "Edge index has not been prepared. Call prepare_edge_index first."
            )
            return node_ids, []

        edge_query_engine = self.index_edges.as_query_engine(
            similarity_top_k=top_k_edges
        )
        edge_response = edge_query_engine.query(query)
        relevant_edges_text = [edge.text for edge in edge_response.source_nodes]
        logger.debug(f"Relevant edges retrieved: {relevant_edges_text}")

        edge_tuples = [
            self._extract_edge_tuple(edge_text) for edge_text in relevant_edges_text
        ]
        edge_tuples = [et for et in edge_tuples if et]  # filter out empty tuples
        logger.debug(f"Extracted edge tuples: {edge_tuples}")

        return node_ids, edge_tuples

    @classmethod
    def slice_subgraph(
        cls,
        graph_data: nx.Graph,
        node_subset: list[str],
        edge_subset: list[tuple[str, str]] | None = None,
    ) -> nx.Graph:
        if edge_subset is None:
            edge_subset = []
        return create_subgraph(graph_data, node_subset, edge_subset)

    def create_query_subgraph(
        self,
        graph: nx.Graph,
        query: str,
        top_k_nodes: int = 1000,
        top_k_edges: int = 1000000,
    ) -> nx.Graph:
        """Create a subgraph based on the relevance to the given query.

        Parameters
        ----------
        graph : nx.Graph
            The complete graph to query from.
        query : str
            The query string to search for relevant nodes and edges.
        top_k_nodes : int, optional
            Number of top relevant nodes to retrieve, by default 1000.
        top_k_edges : int, optional
            Number of top relevant edges to retrieve, by default 1000000.

        Returns
        -------
        nx.Graph
            The resulting subgraph containing the most relevant nodes and edges.
        """
        try:
            self.load_data_graph(
                data=list(graph.edges(data=True)),
                nodes=dict(graph.nodes(data=True)),
            )
            logger.info("Data graph loaded into QuerySubgraph.")
        except Exception:
            logger.exception("Error loading data graph into QuerySubgraph.")
            raise

        try:
            node_ids, edge_tuples = self.query_graph(
                query=query,
                top_k_nodes=top_k_nodes,
                top_k_edges=top_k_edges,
            )
            subgraph = self.slice_subgraph(graph, node_ids, edge_tuples)
            logger.info(
                f"Subgraph created using {subgraph.number_of_nodes()} nodes and "
                f"{subgraph.number_of_edges()} edges."
            )
            if len(subgraph.nodes()) < 3 or not nx.is_connected(subgraph):
                logger.warning(
                    "Insufficient nodes and/or edges remaining after query similarity "
                    "retrieval. Ensure that your query is relevant to the network that "
                    "you are querying."
                )
        except Exception:
            logger.exception("Error during querying or slicing subgraph")
            raise

        return subgraph
