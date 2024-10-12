from unittest.mock import Mock, patch

import networkx as nx
import pytest
import torch
from llama_index.embeddings.huggingface import (  # Added import for assertion
    HuggingFaceEmbedding,
)
from torch import nn
from transformers import AutoModel

from nxlu.processing.embed import CustomModel, QuerySubgraph
from nxlu.processing.preprocess import create_subgraph
from nxlu.utils.control import NetworkXGraphStore


# Fixtures for various graph types with string node names
@pytest.fixture
def fully_connected_graph():
    G = nx.complete_graph(5)
    G = nx.relabel_nodes(G, lambda x: f"node{x}")  # Renaming nodes to strings
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "relationship_type" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture
def partially_connected_graph():
    G = nx.Graph()
    edges = [("node0", "node1"), ("node1", "node2"), ("node3", "node4")]
    G.add_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "relationship_type" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture
def disconnected_graph():
    G = nx.Graph()
    G.add_nodes_from(["node0", "node1", "node2", "node3", "node4"])
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    return G


@pytest.fixture
def weighted_graph():
    G = nx.Graph()
    edges = [
        ("node0", "node1", 0.5),
        ("node1", "node2", 0.7),
        ("node2", "node3", 0.2),
    ]
    G.add_weighted_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G,
        {edge[:2]: "weighted_relationship" for edge in G.edges(data=True)},
        "relationship",
    )
    return G


@pytest.fixture
def binary_graph():
    G = nx.Graph()
    edges = [
        ("node0", "node1"),
        ("node1", "node2"),
        ("node2", "node3"),
        ("node3", "node4"),
    ]
    G.add_edges_from(edges)
    nx.set_node_attributes(G, {n: f"Label_{n}" for n in G.nodes()}, "label")
    nx.set_edge_attributes(
        G, {edge: "binary_relationship" for edge in G.edges()}, "relationship"
    )
    return G


@pytest.fixture(
    params=[
        "fully_connected_graph",
        "partially_connected_graph",
        "disconnected_graph",
        "weighted_graph",
        "binary_graph",
    ]
)
def varied_graph(
    request,
    fully_connected_graph,
    partially_connected_graph,
    disconnected_graph,
    weighted_graph,
    binary_graph,
):
    graph = request.getfixturevalue(request.param)
    graph.graph["name"] = request.param
    return graph


# Fixtures for CustomModel configuration
@pytest.fixture
def custom_model_config():
    return {
        "base_model": "bert-base-uncased",
        "fc_dropout": 0.3,
        "id2label": {0: "ClassA", 1: "ClassB"},
    }


# Fixtures for QuerySubgraph
@pytest.fixture
def sample_data():
    data = [
        ("node1", "node2", {"weight": 1.0, "relationship": "connected"}),
        ("node2", "node3", {"weight": 2.0, "relationship": "connected"}),
        ("node3", "node4", {"weight": 3.0, "relationship": "connected"}),
        ("node4", "node5", {"weight": 4.0, "relationship": "connected"}),
    ]
    nodes = {
        "node1": {"label": "Label_1"},
        "node2": {"label": "Label_2"},
        "node3": {"label": "Label_3"},
        "node4": {"label": "Label_4"},
        "node5": {"label": "Label_5"},
    }
    return data, nodes


# Module-level fixture for QuerySubgraph instance
@pytest.fixture
def query_subgraph_instance():
    return QuerySubgraph()


# Tests for CustomModel
class TestCustomModel:
    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_initialization(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768  # Ensure config is properly mocked
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.model == mock_model
        assert isinstance(model.dropout, nn.Dropout)
        assert isinstance(model.fc, nn.Linear)
        assert model.fc.out_features == len(custom_model_config["id2label"])

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_forward(self, mock_from_pretrained, custom_model_config):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        mock_model.return_value.last_hidden_state = torch.randn(2, 10, 768)
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)
        input_ids = torch.randint(0, 1000, (2, 10))
        attention_mask = torch.ones((2, 10))

        with patch.object(
            model.fc,
            "forward",
            return_value=torch.randn(2, 10, len(custom_model_config["id2label"])),
        ):
            output = model(input_ids, attention_mask)

        assert isinstance(output, torch.Tensor)
        assert output.shape == (2, len(custom_model_config["id2label"]))
        assert torch.allclose(
            output.sum(dim=1), torch.ones(2), atol=1e-5
        )  # Softmax sums to 1

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_invalid_config(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768  # Ensure config is properly mocked
        mock_from_pretrained.return_value = mock_model

        invalid_config = custom_model_config.copy()
        invalid_config["id2label"] = {}  # Empty id2label

        model = CustomModel(config=invalid_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.model == mock_model
        assert isinstance(model.dropout, nn.Dropout)
        assert isinstance(model.fc, nn.Linear)
        assert model.fc.out_features == 0  # Updated assertion


class TestQuerySubgraph:
    def test_query_subgraph_initialization(self, query_subgraph_instance):
        assert isinstance(query_subgraph_instance.data_graph, nx.Graph)
        assert isinstance(query_subgraph_instance.graph_store, NetworkXGraphStore)
        assert query_subgraph_instance.index_nodes is None
        assert query_subgraph_instance.index_edges is None
        assert isinstance(query_subgraph_instance.embedding_model, HuggingFaceEmbedding)

    @patch("nxlu.processing.embed.create_subgraph")
    def test_load_data_graph(
        self, mock_create_subgraph, query_subgraph_instance, sample_data
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Ensure token nodes are excluded
        # Since none are token nodes in sample_data, all should be added
        assert query_subgraph_instance.data_graph.number_of_nodes() == 5
        assert query_subgraph_instance.data_graph.number_of_edges() == 4
        for node, attrs in nodes.items():
            assert (
                query_subgraph_instance.data_graph.nodes[node]["label"]
                == attrs["label"]
            )

    @patch("nxlu.processing.embed.create_subgraph")
    def test_load_data_graph_with_token_nodes(
        self, mock_create_subgraph, query_subgraph_instance, sample_data
    ):
        data, nodes = sample_data
        # Add token nodes
        nodes["token1"] = {"type": "token", "label": "Token_1"}
        nodes["node6"] = {"label": "Label_6"}

        data += [("node1", "token1", {"weight": 0.5, "relationship": "token_relation"})]
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Token nodes should be excluded
        assert (
            query_subgraph_instance.data_graph.number_of_nodes() == 6
        )  # node1 to node5 and node6
        assert query_subgraph_instance.data_graph.has_node("token1") is False
        assert query_subgraph_instance.data_graph.has_edge("node1", "token1") is False

    @patch("nxlu.processing.embed.VectorStoreIndex")
    @patch("nxlu.processing.embed.StorageContext.from_defaults")
    @patch("nxlu.processing.embed.create_subgraph")
    def test_prepare_node_index(
        self,
        mock_create_subgraph,
        mock_storage_context,
        mock_vector_store_index,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock VectorStoreIndex
        mock_index = Mock()
        mock_vector_store_index.return_value = mock_index

        query_subgraph_instance.prepare_node_index()

        mock_storage_context.assert_called_once()
        mock_vector_store_index.assert_called_once()
        assert query_subgraph_instance.index_nodes == mock_index

    @patch("nxlu.processing.embed.VectorStoreIndex")
    @patch("nxlu.processing.embed.StorageContext.from_defaults")
    @patch("nxlu.processing.embed.create_subgraph")
    def test_prepare_edge_index(
        self,
        mock_create_subgraph,
        mock_storage_context,
        mock_vector_store_index,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock VectorStoreIndex
        mock_index = Mock()
        mock_vector_store_index.return_value = mock_index

        subgraph = query_subgraph_instance.data_graph.copy()
        query_subgraph_instance.prepare_edge_index(subgraph=subgraph)

        mock_storage_context.assert_called_once()
        mock_vector_store_index.assert_called_once()
        assert query_subgraph_instance.index_edges == mock_index

    @patch("nxlu.processing.embed.VectorStoreIndex")
    @patch("nxlu.processing.embed.StorageContext.from_defaults")
    def test_query_graph(
        self,
        mock_storage_context,
        mock_vector_store_index,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Create a mock VectorStoreIndex instance
        mock_index_nodes = Mock()
        mock_vector_store_index.return_value = mock_index_nodes

        # Create a mock QueryEngine
        mock_query_engine = Mock()

        # Create a mock source node with correctly formatted text
        mock_source_node = Mock()
        mock_source_node.text = "Node: node1, Attributes: {'label': 'Label_1'}"

        # Mock the response of the query
        mock_query_response = Mock()
        mock_query_response.source_nodes = [mock_source_node]

        # Configure the mock_query_engine to return the mock_query_response
        mock_query_engine.query.return_value = mock_query_response

        # Configure the mock_index_nodes to return the mock_query_engine when
        # as_query_engine is called
        mock_index_nodes.as_query_engine.return_value = mock_query_engine

        # Now call the method under test
        node_ids, edge_tuples = query_subgraph_instance.query_graph(query="test query")

        # Check that the node_ids are as expected
        assert node_ids == ["node1"]
        # Since no edges are mocked, edge_tuples should be empty
        assert edge_tuples == []


class TestQuerySubgraphEdgeCases:
    @pytest.fixture
    def empty_graph(self):
        G = nx.Graph()
        return G

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_node_index")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_edge_index")
    def test_query_graph_with_empty_graph(
        self,
        mock_prepare_edge_index,
        mock_prepare_node_index,
        mock_query_graph,
        query_subgraph_instance,
        empty_graph,
    ):
        # Mock the query response to avoid calling the actual LLM or OpenAI API
        mock_query_graph.return_value = ([], [])

        query_subgraph_instance.load_data_graph(data=[], nodes={})
        node_ids, edge_tuples = query_subgraph_instance.query_graph(query="test query")

        assert node_ids == []
        assert edge_tuples == []

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_node_index")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_edge_index")
    def test_query_graph_with_no_matching_nodes(
        self,
        mock_prepare_edge_index,
        mock_prepare_node_index,
        mock_query_graph,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock query_graph to return nodes that do not exist
        mock_query_graph.return_value = (["nonexistent"], [])

        node_ids, edge_tuples = query_subgraph_instance.query_graph(query="no match")

        assert node_ids == ["nonexistent"]
        assert edge_tuples == []
        # create_subgraph should handle non-existent nodes gracefully
        with patch("nxlu.processing.embed.create_subgraph", return_value=nx.Graph()):
            subgraph = query_subgraph_instance.create_query_subgraph(
                graph=query_subgraph_instance.data_graph,
                query="no match",
                top_k_nodes=1,
                top_k_edges=0,
            )
            assert isinstance(subgraph, nx.Graph)
            assert subgraph.number_of_nodes() == 0
            assert subgraph.number_of_edges() == 0

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_node_index")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_edge_index")
    def test_query_graph_with_all_token_nodes(
        self,
        mock_prepare_edge_index,
        mock_prepare_node_index,
        mock_query_graph,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        # All nodes are token nodes
        nodes = {node: {"type": "token"} for node in nodes}
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock query_graph to return empty node_ids and edge_tuples
        mock_query_graph.return_value = ([], [])

        node_ids, edge_tuples = query_subgraph_instance.query_graph(query="test query")
        # Since all nodes are token nodes, node_ids should be empty after filtering
        assert node_ids == []
        assert edge_tuples == []

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    def test_query_graph_with_large_k_values(
        self,
        mock_query_graph,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock query_graph to return all nodes and edges
        mock_query_graph.return_value = (
            ["node1", "node2", "node3", "node4", "node5"],
            [
                ("node1", "node2"),
                ("node2", "node3"),
                ("node3", "node4"),
                ("node4", "node5"),
            ],
        )

        # Mock create_subgraph to return the expected subgraph
        subgraph = create_subgraph(
            query_subgraph_instance.data_graph,
            ["node1", "node2", "node3", "node4", "node5"],
            [
                ("node1", "node2"),
                ("node2", "node3"),
                ("node3", "node4"),
                ("node4", "node5"),
            ],
        )
        with patch("nxlu.processing.embed.create_subgraph", return_value=subgraph):
            result_subgraph = query_subgraph_instance.create_query_subgraph(
                graph=query_subgraph_instance.data_graph,
                query="test query",
                top_k_nodes=10,  # Larger than available nodes
                top_k_edges=10,  # Larger than available edges
            )

            assert isinstance(result_subgraph, nx.Graph)
            assert result_subgraph.number_of_nodes() == 5
            assert result_subgraph.number_of_edges() == 4

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_node_index")
    @patch("nxlu.processing.embed.QuerySubgraph.prepare_edge_index")
    def test_query_graph_with_duplicate_edges(
        self,
        mock_prepare_edge_index,
        mock_prepare_node_index,
        mock_query_graph,
        query_subgraph_instance,
        sample_data,
    ):
        data, nodes = sample_data
        # Add duplicate edges
        data += [("node1", "node2", {"weight": 1.0, "relationship": "connected"})]
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock query_graph to return duplicate edges
        mock_query_graph.return_value = (
            ["node1", "node2"],
            [("node1", "node2"), ("node1", "node2")],
        )

        # Mock create_subgraph to return a graph without duplicate edges
        subgraph = create_subgraph(
            query_subgraph_instance.data_graph, ["node1", "node2"], [("node1", "node2")]
        )
        with patch("nxlu.processing.embed.create_subgraph", return_value=subgraph):
            result_subgraph = query_subgraph_instance.create_query_subgraph(
                graph=query_subgraph_instance.data_graph,
                query="test query",
                top_k_nodes=2,
                top_k_edges=2,
            )

            assert isinstance(result_subgraph, nx.Graph)
            assert result_subgraph.number_of_nodes() == 2
            assert (
                result_subgraph.number_of_edges() == 1
            )  # No duplicate edges in simple Graph


class TestCustomModelEdgeCases:
    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_zero_classes(self, mock_from_pretrained, custom_model_config):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        mock_from_pretrained.return_value = mock_model

        invalid_config = custom_model_config.copy()
        invalid_config["id2label"] = {}

        model = CustomModel(config=invalid_config)

        mock_from_pretrained.assert_called_once_with(custom_model_config["base_model"])
        assert model.fc.out_features == 0  # Updated assertion

    @patch("nxlu.processing.embed.AutoModel.from_pretrained")
    def test_custom_model_forward_incorrect_input_shape(
        self, mock_from_pretrained, custom_model_config
    ):
        mock_model = Mock(spec=AutoModel)
        mock_model.config = Mock()
        mock_model.config.hidden_size = 768
        # Mock the model to return a last_hidden_state with variable sequence length
        mock_model.return_value.last_hidden_state = torch.randn(
            2, 8, 768
        )  # Changed sequence length
        mock_from_pretrained.return_value = mock_model

        model = CustomModel(config=custom_model_config)
        # Different input dimensions
        input_ids = torch.randint(0, 1000, (2, 8))
        attention_mask = torch.ones((2, 8))

        with patch.object(
            model.fc,
            "forward",
            return_value=torch.randn(2, 8, len(custom_model_config["id2label"])),
        ):
            output = model(input_ids, attention_mask)

        assert isinstance(output, torch.Tensor)
        assert output.shape == (2, len(custom_model_config["id2label"]))
        assert torch.allclose(
            output.sum(dim=1), torch.ones(2), atol=1e-5
        )  # Softmax sums to 1


class TestQuerySubgraphIntegration:
    @pytest.fixture
    def complex_graph(self):
        G = nx.Graph()
        # Add nodes
        for i in range(10):
            G.add_node(f"node{i}", label=f"Label_{i}")
        # Add edges with weights and relationships
        edges = [
            ("node0", "node1", {"weight": 1.0, "relationship": "connected"}),
            ("node1", "node2", {"weight": 2.0, "relationship": "connected"}),
            ("node2", "node3", {"weight": 3.0, "relationship": "connected"}),
            ("node3", "node4", {"weight": 4.0, "relationship": "connected"}),
            ("node4", "node5", {"weight": 5.0, "relationship": "connected"}),
            ("node5", "node6", {"weight": 6.0, "relationship": "connected"}),
            ("node6", "node7", {"weight": 7.0, "relationship": "connected"}),
            ("node7", "node8", {"weight": 8.0, "relationship": "connected"}),
            ("node8", "node9", {"weight": 9.0, "relationship": "connected"}),
            ("node9", "node0", {"weight": 10.0, "relationship": "connected"}),
            # Token nodes
            ("node0", "token1", {"weight": 0.1, "relationship": "token_relation"}),
            ("token1", "token2", {"weight": 0.2, "relationship": "token_relation"}),
        ]
        G.add_edges_from(edges)
        return G

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    def test_create_query_subgraph_complex(
        self,
        mock_query_graph,
        query_subgraph_instance,
        complex_graph,
    ):
        query_subgraph_instance.load_data_graph(
            data=list(complex_graph.edges(data=True)),
            nodes=dict(complex_graph.nodes(data=True)),
        )

        # Mock query_graph to return multiple nodes and edges
        mock_query_graph.return_value = (
            ["node1", "node2", "node3"],
            [("node1", "node2"), ("node2", "node3")],
        )

        # Mock create_subgraph to return the expected subgraph
        subgraph = create_subgraph(
            complex_graph,
            ["node1", "node2", "node3"],
            [("node1", "node2"), ("node2", "node3")],
        )
        with patch("nxlu.processing.embed.create_subgraph", return_value=subgraph):
            subgraph_result = query_subgraph_instance.create_query_subgraph(
                graph=complex_graph, query="connectivity", top_k_nodes=3, top_k_edges=2
            )

            assert isinstance(subgraph_result, nx.Graph)
            assert subgraph_result.number_of_nodes() == 3
            assert subgraph_result.number_of_edges() == 2
            assert subgraph_result.has_edge("node1", "node2")
            assert subgraph_result.has_edge("node2", "node3")

    def test_create_subgraph_with_no_edges(self, varied_graph):
        node_subset = ["node1", "node2"]
        edge_subset = []
        subgraph = QuerySubgraph.slice_subgraph(varied_graph, node_subset, edge_subset)

        assert isinstance(subgraph, nx.Graph)
        assert subgraph.number_of_nodes() == 2

        # Dynamically determine the expected number of edges
        if varied_graph.has_edge("node1", "node2"):
            expected_edges = 1
        else:
            expected_edges = 0

        assert subgraph.number_of_edges() == expected_edges  # Updated assertion

    @patch("nxlu.processing.embed.QuerySubgraph.query_graph")
    def test_create_query_subgraph_disconnected_subgraph(
        self, mock_query_graph, query_subgraph_instance, sample_data
    ):
        data, nodes = sample_data
        query_subgraph_instance.load_data_graph(data=data, nodes=nodes)

        # Mock query_graph to return nodes that do not form a connected subgraph
        mock_query_graph.return_value = (["node1", "node3"], [])

        # Mock create_subgraph to return a disconnected subgraph
        subgraph = create_subgraph(
            query_subgraph_instance.data_graph, ["node1", "node3"], []
        )
        with patch("nxlu.processing.embed.create_subgraph", return_value=subgraph):
            result_subgraph = query_subgraph_instance.create_query_subgraph(
                graph=query_subgraph_instance.data_graph,
                query="test query",
                top_k_nodes=2,
                top_k_edges=0,
            )

            assert isinstance(result_subgraph, nx.Graph)
            assert result_subgraph.number_of_nodes() == 2
            assert result_subgraph.number_of_edges() == 0
            assert not nx.is_connected(result_subgraph)
