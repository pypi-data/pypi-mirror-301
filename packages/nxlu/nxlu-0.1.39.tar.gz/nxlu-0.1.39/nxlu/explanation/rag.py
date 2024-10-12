import asyncio
import json
import logging
import os
import re
from pathlib import Path

import nest_asyncio
import networkx as nx
import numpy as np
from community import community_louvain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.graphs import Neo4jGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from llama_index.core import get_response_synthesizer
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.core.schema import NodeWithScore, TextNode
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from nxlu.explanation.corpus import (
    STANDARDIZED_ALGORITHM_NAMES,
    load_docs_from_jsonl,
    load_graph_theory_corpus,
    normalize_name,
)

nest_asyncio.apply()

logger = logging.getLogger("nxlu")

__all__ = [
    "Neo4jHelper",
    "GraphRAGPipeline",
    "get_nodes_by_type",
    "AlgorithmDocstringSummarizer",
    "save_algorithm_docs_to_json",
    "load_algorithm_docs_from_json",
]


class Neo4jHelper:
    def __init__(self, uri, user, password, database):
        """Initialize the Neo4jHelper.

        Parameters
        ----------
        uri : str
            The URI for the Neo4j database.
        user : str
            The username for the Neo4j database.
        password : str
            The password for the Neo4j database.
        database : str
            The database name to connect to.
        """
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        """Close the Neo4j database connection."""
        self.driver.close()

    def add_relationship(self, source_node, target_node, relationship):
        """Add a relationship between two nodes in the Neo4j database.

        Parameters
        ----------
        source_node : Node
            The source node.
        target_node : Node
            The target node.
        relationship : dict
            A dictionary containing the relationship type and description.
        """
        with self.driver.session(database=self.database) as session:
            session.write_transaction(
                self._create_relationship, source_node, target_node, relationship
            )

    @staticmethod
    def _create_relationship(tx, source_node, target_node, relationship):
        """Create a relationship between two nodes in a transaction.

        Parameters
        ----------
        tx : Transaction
            The Neo4j transaction object.
        source_node : Node
            The source node.
        target_node : Node
            The target node.
        relationship : dict
            A dictionary containing the relationship type and description.
        """
        relationship_type = relationship["relation"].replace(" ", "_")
        query = (
            "MATCH (a:Node {name: $source_name}) "
            "MATCH (b:Node {name: $target_name}) "
            f"MERGE (a)-[r:{relationship_type}]->(b) "
            "SET r.description = $description"
        )
        tx.run(
            query,
            source_name=source_node.properties.get("name", ""),
            target_name=target_node.properties.get("name", ""),
            description=relationship.get("description", ""),
        )

    def delete_nodes_in_list(self, node_names):
        """Delete nodes from the Neo4j database that are in the provided list.

        Parameters
        ----------
        node_names : list of str
            List of node names to delete.
        """
        query = """
        MATCH (n)
        WHERE toLower(n.name) IN $names
        DETACH DELETE n
        """
        node_names = [name.lower() for name in node_names]

        with self.driver.session(database=self.database) as session:
            result = session.run(query, names=node_names)
            deleted_count = result.consume().counters.nodes_deleted
            logger.info(f"Deleted {deleted_count} nodes present in the provided list.")

    def delete_null_nodes(self):
        """Delete nodes from the Neo4j database where the 'name' property is NULL."""
        query = """
        MATCH (n)
        WHERE n.name IS NULL OR n.name = ''
        DETACH DELETE n
        """
        with self.driver.session(database=self.database) as session:
            result = session.run(query)
            deleted_count = result.consume().counters.nodes_deleted
            logger.info(
                f"Deleted {deleted_count} nodes with empty or null 'name' properties."
            )


class GraphRAGPipeline:
    def __init__(self, documents_path, graph_theory_corpus_path):
        """Initialize the GraphRAGPipeline.

        Parameters
        ----------
        documents_path : str
            Path to the documents in JSONL format.
        graph_theory_corpus_path : str
            Path to the graph theory corpus text file.
        """
        self.documents_path = documents_path
        self.graph_theory_corpus_path = graph_theory_corpus_path
        self.documents = []
        self.combined_texts = []
        self.graph_documents = []
        self.all_nodes = []
        self.filtered_nodes = []
        self.bad_node_names = []
        self.corpus_embeddings = None
        self.model = None
        self.prompt = None
        self.kg_transformer = None
        self.graph = None
        self.neo4j_helper = None
        self.embedding_model = None
        self.graph_theory_corpus = []

    def load_documents(self):
        """Load documents from a JSONL file."""
        self.documents = load_docs_from_jsonl(self.documents_path)

    def split_and_combine_texts(self):
        """Split and combine texts into chunks suitable for processing."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=10000,
            chunk_overlap=750,
            separators=["\n\n", "\n", " ", ""],
        )
        combined_texts = []
        current_text = ""
        max_length = 10000

        chunks = text_splitter.split_documents(self.documents)
        for doc in chunks:
            if len(current_text) + len(doc.page_content) + 1 < max_length:
                current_text += " " + doc.page_content
            else:
                combined_texts.append(Document(page_content=current_text.strip()))
                current_text = doc.page_content

        if current_text:
            combined_texts.append(Document(page_content=current_text.strip()))

        self.combined_texts = combined_texts

    def prepare_prompt_and_model(self):
        """Prepare the prompt template and initialize the language model."""
        user_input = """
        Analyze the following text to extract information relevant to graph theory or
        network science, focusing on definitions, use-cases, and interrelationships of
        graph algorithms.

        **Tasks:**
        1. **Identify Algorithms (entities):**
            - Extract graph algorithms explicitly mentioned in the text.
            - For each identified algorithm, provide:
                - **Name**: The exact name of the algorithm.
                - **Type**: The category or type of the algorithm.
                    - Permissible values are:
                        ['assortativity', 'bridges', 'centrality', 'clique', 'cluster',
                        'coloring', 'community', 'components', 'connectivity', 'core',
                        'cycles', 'distance', 'efficiency', 'flow', 'link prediction',
                        'lowest common ancestors', 'path', 'richclub', 'tree', 'triads',
                        'vitality']
                - **Description**: A meaningful description, of at least 25 characters,
                based on the immediate context in the text and relevant to graph theory
                or network science only.

        2. **Determine Relationships (relations):**
            - Extract meaningful relationships between the identified algorithms based
            on their respective contexts in the text.
            - For each relationship, specify:
                - **Source**: The name of the first identified algorithm.
                - **Target**: The name of the second identified algorithm.
                - **Relation**: The type of relationship.
                - **Description**: How the two identified algorithms relate **within the
                context** of the text in which they appear.

        **Output Format:**
        - Provide the extracted information in **valid JSON** format as shown below.
        - **Do not include any additional text**, explanations, or markdown. The
        response should be **pure JSON**.

        **Example:**

        *Given the text:*
        "We applied k-core decomposition and used the PageRank algorithm to rank nodes
        by importance in the identified dense subgraphs."

        *The extracted entities and relations should be:*
        ```json
        {{
            "entities": [
                {{"name": "k-core", "type": "Centrality", "description": "Algorithm to
                identify dense subgraphs."}},
                {{"name": "PageRank", "type": "Centrality", "description": "Algorithm
                used to rank nodes by importance in a network."}}
            ],
            "relations": [
                {{"source": "k-core", "target": "PageRank", "relation": "Dependency",
                "description": "PageRank ranks nodes within the dense subgraphs
                identified by k-core."}}
            ]
        }}
        ```

        **Please respond strictly in the above JSON format without any additional text
        or explanations:**

        """

        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a mathematician with specialization in graph theory.",
                ),
                ("user", user_input),
            ]
        )

        self.model = ChatOpenAI(temperature=0.1, model_name="gpt-4o-2024-08-06")

    def process_documents(self):
        """Process documents to extract graph information and store in Neo4j."""
        self.kg_transformer = LLMGraphTransformer(
            llm=self.model,
            prompt=self.prompt,
            allowed_nodes=STANDARDIZED_ALGORITHM_NAMES,
            node_properties=["name", "type", "description"],
            relationship_properties=["source", "target", "relation", "description"],
            strict_mode=True,
        )

        self.graph = Neo4jGraph(
            url=os.environ.get("NEO4J_URI", "neo4j"),
            username=os.environ.get("NEO4J_USERNAME", "neo4j"),
            password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
            database="nxlu",
        )

        self.graph_documents = self.kg_transformer.convert_to_graph_documents(
            self.combined_texts
        )

        self.graph.add_graph_documents(
            self.graph_documents, include_source=True, baseEntityLabel=True
        )

    def filter_nodes(self):
        """Filter nodes based on predefined criteria."""
        self.all_nodes = []
        for graph_doc in self.graph_documents:
            self.all_nodes.extend(list(graph_doc.nodes))

        self.filtered_nodes = []
        for graph_doc in self.graph_documents:
            self.filtered_nodes.extend(
                [
                    node
                    for node in graph_doc.nodes
                    if node.type.lower() in STANDARDIZED_ALGORITHM_NAMES
                    and node.properties != {}
                    and node.properties.get("name")
                    and node.properties.get("description")
                    and not len(str(node.properties.get("description"))) < 20
                    and node.id
                ]
            )
        self.bad_node_names = [
            node.properties.get("name", "").strip()
            for node in self.all_nodes
            if node not in self.filtered_nodes
        ]

    def load_graph_theory_corpus(self):
        """Load the graph theory corpus from a text file."""
        self.graph_theory_corpus = load_graph_theory_corpus(
            self.graph_theory_corpus_path
        )

    def encode_corpus(self):
        """Encode the graph theory corpus using a SentenceTransformer."""
        self.embedding_model = SentenceTransformer("witiko/mathberta")
        self.corpus_embeddings = self.embedding_model.encode(
            self.graph_theory_corpus, convert_to_tensor=False
        )

    def delete_bad_nodes(self):
        """Delete nodes that do not meet the criteria from the Neo4j database."""
        self.neo4j_helper = Neo4jHelper(
            uri=os.environ.get("NEO4J_URI", "neo4j://localhost:7687"),
            user=os.environ.get("NEO4J_USERNAME", "neo4j"),
            password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
            database="nxlu",
        )
        self.neo4j_helper.delete_nodes_in_list(self.bad_node_names)

    def is_graph_theory_related(self, text: str, corpus: list) -> bool:
        """Determine if a given text is related to graph theory.

        Parameters
        ----------
        text : str
            The text to evaluate.
        corpus : list
            List of keywords related to graph theory.

        Returns
        -------
        bool
            True if related to graph theory, False otherwise.
        """
        if not text:
            return False
        text = text.lower()
        return any(keyword.lower() in text for keyword in corpus)

    def prune_node(self, node) -> bool:
        """Check if a node is related to graph theory.

        Parameters
        ----------
        node : Node
            The node to check.

        Returns
        -------
        bool
            True if the node is related, False otherwise.
        """
        name = node.properties.get("name", "")
        description = node.properties.get("description", "")
        return self.is_graph_theory_related(
            name, STANDARDIZED_ALGORITHM_NAMES
        ) or self.is_graph_theory_related(description, STANDARDIZED_ALGORITHM_NAMES)

    def prune_relationship(self, relation) -> bool:
        """Check if a relationship is relevant to graph theory.

        Parameters
        ----------
        relation : dict
            The relationship to check.

        Returns
        -------
        bool
            True if the relationship is relevant, False otherwise.
        """
        description = relation.get("description", "")
        related = self.is_graph_theory_related(
            description, STANDARDIZED_ALGORITHM_NAMES
        )
        if related:
            logger.debug(f"Relationship '{description}' is related to graph theory.")
        else:
            logger.debug(
                f"Relationship '{description}' is NOT related to graph theory."
            )
        return related

    def get_embedding(self, text):
        """Generate embeddings for the given text.

        Parameters
        ----------
        text : str
            The text to encode.

        Returns
        -------
        np.ndarray
            The embedding vector.
        """
        return self.embedding_model.encode(text, convert_to_tensor=False)

    def filter_nodes_by_similarity(self, nodes, corpus_embeddings, threshold=0.95):
        """Filter nodes by calculating cosine similarity with the corpus embeddings.

        Parameters
        ----------
        nodes : list
            List of Node objects.
        corpus_embeddings : np.ndarray
            Precomputed embeddings for the graph theory corpus.
        threshold : float, optional
            Similarity threshold for retaining nodes.

        Returns
        -------
        list
            List of filtered nodes.
        """
        filtered_nodes = []
        for node in nodes:
            node_name = node.properties.get("name", "")
            node_description = node.properties.get("description", "")
            node_type = node.properties.get("type", "")
            if not node_name or not node_description or not node_type:
                continue
            node_embedding = self.get_embedding(
                f"{node_name} {node_type} {node_description}"
            )
            similarity_scores = cosine_similarity([node_embedding], corpus_embeddings)
            max_similarity = np.max(similarity_scores)
            if max_similarity > threshold:
                filtered_nodes.append(node)
        return filtered_nodes

    def determine_relationship(self, node_a, node_b) -> dict | None:
        """Determine the relationship between two nodes.

        Parameters
        ----------
        node_a : Node
            The first node.
        node_b : Node
            The second node.

        Returns
        -------
        dict or None
            The relationship dictionary or None if not applicable.
        """
        prompt = f"""
        Given the following two graph algorithms:

        **Algorithm 1:**
        - **Name:** {{node_a.properties.get('name', '')}}
        - **Type:** {{node_a.properties.get('type', '')}}
        - **Description:** {node_a.properties.get('description', '')}

        **Algorithm 2:**
        - **Name:** {{node_b.properties.get('name', '')}}
        - **Type:** {{node_b.properties.get('type', '')}}
        - **Description:** {{node_b.properties.get('description', '')}}

        **Task:** Determine if there is a meaningful, graph theoretical relationship
        between these two algorithms. If so, specify the type of relationship and
        provide a brief description.

        **Output Format:**
        {{
            "relation": "RelationshipType",
            "description": "Brief description of the relationship."
        }}
        """

        try:
            response = self.model(prompt)

            if hasattr(response, "content"):
                content = response.content
            elif hasattr(response, "text"):
                content = response.text
            elif hasattr(response, "generations") and len(response.generations) > 0:
                content = response.generations[0].message.content
            else:
                logger.error("Unexpected response structure from the model.")

            logger.debug(f"Raw model response: {content}")

            content = re.sub(r"^```json\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
            content = content.strip()

            logger.debug(f"Cleaned model response: {content}")

            if not (content.startswith("{") and content.endswith("}")):
                logger.error(
                    f"Response does not start with '{{' or end with '}}': {content}"
                )

            relationship = json.loads(content)

            if "relation" in relationship and "description" in relationship:
                logger.debug(f"Valid relationship determined: {relationship}")
                return relationship
            logger.warning(f"Invalid relationship format received: {relationship}")

        except json.JSONDecodeError:
            logger.exception("Failed to parse relationship JSON")
            logger.exception(f"Content received: {content}")
            return None
        except Exception:
            logger.exception("An error occurred while determining relationship")
            return None
        else:
            return None

    def link_and_prune_nodes(self):
        """Link and prune nodes and relationships across documents."""
        logger.info(f"Starting to link and prune {len(self.filtered_nodes)} nodes.")
        total_relationships_added = 0

        filtered_nodes = self.filter_nodes_by_similarity(
            self.filtered_nodes, self.corpus_embeddings, threshold=0.98
        )
        logger.info(f"Filtered {len(self.filtered_nodes) - len(filtered_nodes)} nodes.")

        for i, node_a in enumerate(filtered_nodes):
            if not self.prune_node(node_a):
                logger.debug(
                    f"Skipping node '{node_a.properties.get('name', '')}' as it's not "
                    f"related to graph theory."
                )
                continue

            for j, node_b in enumerate(filtered_nodes):
                if i >= j:
                    continue
                if not self.prune_node(node_b):
                    logger.debug(
                        f"Skipping node '{node_b.properties.get('name', '')}' as it's "
                        f"not related to graph theory."
                    )
                    continue

                relationship = self.determine_relationship(node_a, node_b)

                if relationship and self.prune_relationship(relationship):
                    try:
                        self.neo4j_helper.add_relationship(node_a, node_b, relationship)
                        logger.info(
                            f"Added relationship between "
                            f"'{node_a.properties.get('name', '')}' and "
                            f"'{node_b.properties.get('name', '')}'."
                        )
                        total_relationships_added += 1
                    except Exception:
                        logger.exception(
                            f"Failed to add relationship between "
                            f"'{node_a.properties.get('name', '')}' and "
                            f"'{node_b.properties.get('name', '')}'"
                        )

        logger.info(
            f"Finished linking and pruning nodes. Total relationships added: "
            f"{total_relationships_added}."
        )
        self.neo4j_helper.close()

    def run(self):
        """Execute the full analysis pipeline."""
        self.load_documents()
        self.split_and_combine_texts()
        self.prepare_prompt_and_model()
        self.process_documents()
        self.filter_nodes()
        self.load_graph_theory_corpus()
        self.encode_corpus()
        self.delete_bad_nodes()
        try:
            self.link_and_prune_nodes()
        except Exception:
            logger.exception("An error occurred while linking and pruning nodes")


def get_nodes_by_type(
    algorithm_type: str, uri: str, user: str, password: str, database: str
) -> list:
    """
    Retrieve nodes from Neo4j based on the algorithm type.

    Parameters
    ----------
    algorithm_type : str
        The type of the algorithm (node.type).
    uri : str
        The Bolt URI for Neo4j connection.
    user : str
        Neo4j username.
    password : str
        Neo4j password.
    database : str
        The Neo4j database name.

    Returns
    -------
    list
        A list of dictionaries containing node details.
    """
    driver = GraphDatabase.driver(uri, auth=(user, password))
    nodes = []
    try:
        with driver.session(database=database) as session:
            cypher_query = """
            CALL apoc.cypher.run(
                'MATCH (n) WHERE $label IN labels(n) RETURN n',
                {label: $algorithm_type}
            ) YIELD value
            RETURN value.n AS n
            """
            result = session.run(cypher_query, algorithm_type=algorithm_type)

            for record in result:
                node = record["n"]
                nodes.append(
                    {
                        "id": node.id,
                        "labels": list(node.labels),
                        "properties": dict(node),
                    }
                )
    except Exception:
        logger.exception(f"Failed to retrieve nodes for label '{algorithm_type}'")
    finally:
        driver.close()
    return nodes


class AlgorithmDocstringSummarizer:
    """Summarize algorithm docstrings using graph-based knowledge indexing."""

    def __init__(
        self,
        llm,
        neo4j_uri: str,
        neo4j_user: str,
        neo4j_password: str,
        neo4j_database: str,
        max_concurrent_tasks: int = 5,
    ):
        """
        Initialize the summarizer.

        Parameters
        ----------
        llm : object
            The language model to use for summarization.
        neo4j_uri : str
            The URI for the Neo4j database.
        neo4j_user : str
            The username for the Neo4j database.
        neo4j_password : str
            The password for the Neo4j database.
        neo4j_database : str
            The database name to connect to.
        max_concurrent_tasks : int, optional
            The maximum number of concurrent summarization tasks, by default 5.
        """
        self.llm = llm
        self.neo4j_uri = neo4j_uri
        self.neo4j_user = neo4j_user
        self.neo4j_password = neo4j_password
        self.neo4j_database = neo4j_database
        self.response_synthesizer = get_response_synthesizer(
            response_mode=ResponseMode.COMPACT
        )
        self.semaphore = asyncio.Semaphore(max_concurrent_tasks)

    @staticmethod
    def _clean_docstring(docstring: str) -> str:
        """
        Clean and normalize the docstring.

        Parameters
        ----------
        docstring : str
            The original docstring.

        Returns
        -------
        str
            The cleaned and normalized docstring.
        """
        docstring = docstring.split("References")[0]
        docstring = re.sub(r"-+\n", " ", docstring)
        docstring = re.sub(r"\[\d+\]_", "", docstring)
        docstring = re.sub(r"\s+", " ", docstring).strip()
        return docstring

    def _get_related_knowledge(self, algorithm_name: str) -> tuple[str, list]:
        """Retrieve related knowledge and nodes for an algorithm using a retriever.

        Parameters
        ----------
        algorithm_name : str
            The name of the algorithm.

        Returns
        -------
        tuple of str and list
            A tuple containing the related knowledge string and a list of NodeWithScore.
        """
        try:
            nodes_dicts = get_nodes_by_type(
                algorithm_type=algorithm_name.capitalize(),
                uri=self.neo4j_uri,
                user=self.neo4j_user,
                password=self.neo4j_password,
                database=self.neo4j_database,
            )
            if not nodes_dicts:
                logger.warning(f"No nodes retrieved for '{algorithm_name}'.")
                return "", []

            nodes = []
            for node_dict in nodes_dicts:
                content = node_dict["properties"].get("description", "")
                text_node = TextNode(text=content)
                node_with_score = NodeWithScore(node=text_node)
                nodes.append(node_with_score)

            related_knowledge = "\n".join([n.node.get_content() for n in nodes])

            logger.info(
                f"Retrieved context for '{algorithm_name}': {related_knowledge}"
            )
            logger.debug(f"Retrieved Nodes: {nodes}")

        except Exception:
            logger.exception(f"Failed to retrieve knowledge for '{algorithm_name}'")
            return "", []
        else:
            return related_knowledge, nodes

    async def summarize_algorithm(self, algorithm_name: str) -> dict:
        """
        Generate technical and colloquial summaries for an algorithm.

        Parameters
        ----------
        algorithm_name : str
            The name of the algorithm to summarize.

        Returns
        -------
        dict
            A dictionary containing 'technical' and 'colloquial' summaries.
        """
        async with self.semaphore:
            try:
                docstring = self._clean_docstring(
                    self._retrieve_docstring(algorithm_name)
                )
                related_knowledge, nodes = self._get_related_knowledge(
                    normalize_name(algorithm_name).capitalize()
                )
                if not nodes:
                    logger.warning(
                        f"No nodes retrieved for '{algorithm_name}'. Skipping summary."
                    )
                    return {"technical": "", "colloquial": ""}

                prompt_technical = (
                    f"You are a graph theorist and mathematician. Here is some relevant"
                    f" knowledge: {related_knowledge}\n\n"
                    f"Please summarize the following docstring in technical terms:\n"
                    f"{docstring}"
                )
                prompt_colloquial = (
                    f"You are a teacher and expert communicator. Here is some relevant "
                    f"knowledge: {related_knowledge}\n\n"
                    f"Please summarize the following docstring in colloquial terms "
                    f"(i.e. without any technical jargon):\n"
                    f"{docstring}"
                )

                technical_summary = await self.synthesize_summary(
                    prompt_technical, related_knowledge, nodes
                )
                colloquial_summary = await self.synthesize_summary(
                    prompt_colloquial, related_knowledge, nodes
                )
            except Exception:
                logger.exception(f"Failed to summarize '{algorithm_name}'")
                return {"technical": "", "colloquial": ""}
            else:
                return {
                    "technical": technical_summary,
                    "colloquial": colloquial_summary,
                }

    async def synthesize_summary(self, prompt: str, context: str, nodes: list) -> str:
        """
        Generate a summary using the ResponseSynthesizer.

        Parameters
        ----------
        prompt : str
            The prompt to send to the synthesizer.
        context : str
            The related knowledge context.
        nodes : list
            A list of NodeWithScore objects.

        Returns
        -------
        str
            The synthesized summary.
        """
        try:
            response = await asyncio.to_thread(
                self.response_synthesizer.synthesize,
                query=prompt,
                context=context,
                nodes=nodes,
            )
        except Exception:
            logger.exception("Failed to synthesize summary")
            return ""
        else:
            return response.response

    def _retrieve_docstring(self, algorithm_name: str) -> str:
        """
        Retrieve the docstring of a NetworkX algorithm.

        Parameters
        ----------
        algorithm_name : str
            The name of the algorithm.

        Returns
        -------
        str
            The docstring of the algorithm or an empty string if not found.
        """
        if algorithm_name in ["girvan_newman", "greedy_modularity_communities"]:
            alg_func = getattr(nx.algorithms.community, algorithm_name, None)
        elif algorithm_name == "best_partition":
            alg_func = getattr(community_louvain, algorithm_name, None)
        else:
            alg_func = getattr(nx, algorithm_name, None)

        if alg_func is None:
            logger.error(f"NetworkX has no attribute '{algorithm_name}'")
            return ""
        return alg_func.__doc__ or ""


def save_algorithm_docs_to_json(algorithm_docs: dict, filename: str):
    """
    Save algorithm_docs to a JSON file.

    Parameters
    ----------
    algorithm_docs : dict
        A dictionary containing algorithm documentation.
    filename : str
        The path to the JSON file where the documentation will be saved.

    Returns
    -------
    None
    """
    try:
        Path(filename).parent.mkdir(parents=True, exist_ok=True)

        with Path(filename).open(mode="w") as f:
            json.dump(algorithm_docs, f, indent=4)
        logger.info(f"algorithm_docs successfully saved to {filename}")
    except Exception:
        logger.exception(f"Failed to save algorithm_docs to {filename}")


def load_algorithm_docs_from_json(filename: str) -> dict:
    """
    Load algorithm_docs from a JSON file.

    Parameters
    ----------
    filename : str
        The path to the JSON file to load.

    Returns
    -------
    dict
        A dictionary containing the loaded algorithm documentation.
    """
    try:
        with Path(filename).open(mode="r") as f:
            algorithm_docs = json.load(f)
    except Exception:
        logger.exception(f"Failed to load algorithm_docs from {filename}")
        return {}
    else:
        return algorithm_docs
