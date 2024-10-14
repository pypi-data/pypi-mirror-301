import importlib.resources as pkg_resources
import json
import logging
import re
import threading
import unicodedata
import warnings
from collections import Counter
from collections.abc import Iterable
from difflib import SequenceMatcher
from pathlib import Path

import faiss
import networkx as nx
import numpy as np
import torch
from langchain.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from nltk import ngrams
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoModel, AutoTokenizer

from nxlu.constants import NOISE_PATTERNS, NX_TERM_BLACKLIST
from nxlu.io import load_algorithm_encyclopedia
from nxlu.utils.misc import normalize_name, parse_algorithms

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

SUPPORTED_ALGORITHMS, ALGORITHM_CATEGORIES, STANDARDIZED_ALGORITHM_NAMES = (
    parse_algorithms(load_algorithm_encyclopedia(), normalize_name)
)


def get_package_data_directory() -> Path:
    """Return the path to the `nxlu/data/` directory inside the package."""
    package_data_dir = pkg_resources.files("nxlu") / "data"
    return package_data_dir


class AlgorithmMatcher:
    """A class to map extracted algorithm names to standardized algorithm names.

    This class uses a pretrained MathBERTa model to generate embeddings for algorithm
    names and uses FAISS to perform efficient similarity searches.
    It returns a list of all standardized algorithm names that have a cosine similarity
    above a specified threshold with the extracted name.

    Attributes
    ----------
    standardized_names : Dict[str, str]
        Dictionary of standardized algorithm names mapped to their categories.
    tokenizer : transformers.PreTrainedTokenizer
        Tokenizer for the MathBERTa model.
    model : transformers.PreTrainedModel
        Pretrained MathBERTa model.
    index : faiss.IndexFlatIP
        FAISS index for efficient similarity search.
    standardized_embeddings : np.ndarray
        Normalized embeddings of the standardized algorithm names.

    Methods
    -------
    get_embedding(text: str) -> np.ndarray
        Generate embedding for the given text using MathBERTa.
    map_to_standard_name(extracted_name: str, threshold: float = 0.8, top_k: int = 10)
    -> List[Tuple[str, float]]
        Map an extracted algorithm name to a list of standardized names based on cosine
        similarity.
    """

    def __init__(
        self,
        standardized_names: list[str],
        model_name: str = "witiko/mathberta",
        semantic_weight: float = 0.6,
        syntactic_weight: float = 0.3,
    ):
        """Initialize the AlgorithmMatcher.

        Parameters
        ----------
        standardized_names_list : List[str]
            List of standardized algorithm names .
        model_name : str, optional
            HuggingFace model name for the tokenizer and model, by default
            "witiko/mathberta".
        semantic_weight : float, optional
            Weight for semantic similarity in the combined score, by default 0.7.
        syntactic_weight : float, optional
            Weight for syntactic similarity in the combined score, by default 0.3.
        """
        self.standardized_names_list = standardized_names
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name, device_map="cpu")
        self.model.eval()

        self.model_lock = threading.Lock()
        self.index_lock = threading.Lock()

        embeddings = []
        for name in self.standardized_names_list:
            embedding = self.get_embedding(name)
            embeddings.append(embedding)
        self.standardized_embeddings = np.vstack(embeddings).astype("float32")

        faiss.normalize_L2(self.standardized_embeddings)

        dimension = self.standardized_embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension)
        self.index.add(self.standardized_embeddings)

        self.semantic_weight = semantic_weight
        self.syntactic_weight = syntactic_weight

    @staticmethod
    def string_similarity(a: str, b: str) -> float:
        """
        Compute the string similarity between two strings using SequenceMatcher.

        Parameters
        ----------
        a : str
            First string.
        b : str
            Second string.

        Returns
        -------
        float
            Similarity ratio between 0 and 1.
        """
        return SequenceMatcher(None, a, b).ratio()

    def get_embedding(self, text: str) -> np.ndarray:
        """
        Generate embedding for the given text using MathBERTa.

        Parameters
        ----------
        text : str
            The text to encode.

        Returns
        -------
        np.ndarray
            1D array representing the [CLS] token embedding.
        """
        with self.model_lock:
            inputs = self.tokenizer(
                text, return_tensors="pt", padding=True, truncation=True
            )
            with torch.no_grad():
                outputs = self.model(**inputs)
            cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()

        return cls_embedding

    def map_to_standard_name(
        self,
        extracted_name: str,
        threshold: float = 0.8,
        top_k: int = 10,
    ) -> list[tuple[str, float]]:
        """Map an extracted algorithm name to a list of standardized names.

        Parameters
        ----------
        extracted_name : str
            The algorithm name extracted from the text.
        threshold : float, optional
            Minimum combined similarity score to consider a match valid (between 0 and
            1), by default 0.5.
        top_k : int, optional
            Maximum number of top matches to return, by default 10.

        Returns
        -------
        List[Tuple[str, float]]
            A list of tuples where each tuple contains the standardized algorithm name
            and its combined similarity score.
        """
        normalized_extracted = normalize_name(extracted_name)

        if normalized_extracted in self.standardized_names_list:
            logger.debug(f"Exact match found: '{normalized_extracted}'")
            return [(normalized_extracted, 1.0)]

        # Step 1: Compute syntactic similarity for all standardized names
        syntactic_scores = [
            (name, self.string_similarity(normalized_extracted, name))
            for name in self.standardized_names_list
        ]

        syntactic_scores.sort(key=lambda x: x[1], reverse=True)

        if syntactic_scores and syntactic_scores[0][1] > 0.8:
            return [syntactic_scores[0]]

        extracted_embedding = self.get_embedding(normalized_extracted).astype("float32")
        extracted_embedding /= np.linalg.norm(extracted_embedding)  # norm

        # FAISS 2D array for search
        extracted_embedding = extracted_embedding.reshape(1, -1)
        faiss.normalize_L2(extracted_embedding)

        with self.index_lock:
            distances, indices = self.index.search(extracted_embedding, top_k)

        similarities = distances[0]
        matched_indices = indices[0]

        matches = []
        for semantic_similarity, idx in zip(similarities, matched_indices):
            if semantic_similarity < threshold:
                continue

            matched_name = self.standardized_names_list[idx]

            syntactic_similarity = self.string_similarity(
                normalized_extracted, matched_name
            )

            combined_similarity = (
                self.semantic_weight * semantic_similarity
                + self.syntactic_weight * syntactic_similarity
            )

            if syntactic_similarity > 0.7 and semantic_similarity > threshold:
                return [(matched_name, combined_similarity)]

            if combined_similarity >= threshold:
                matches.append((matched_name, combined_similarity))
                logger.debug(
                    f"Matched '{extracted_name}' to '{matched_name}' with combined "
                    f"similarity {combined_similarity}"
                )

        matches.sort(key=lambda x: x[1], reverse=True)

        return matches


def load_documents_from_directory(
    directory_path, extract_func, chunk_size=750, chunk_overlap=500
):
    """Load and extract text from all PDFs in the given directory.

    Parameters
    ----------
    directory_path : str
        The path to the directory containing the PDF files.
    extract_func : function
        A function that extracts text chunks from a PDF file.
    chunk_size : int, optional
        The maximum size of each text chunk (default is 750).
    chunk_overlap : int, optional
        The overlap size between chunks (default is 500).

    Returns
    -------
    list
        A list of extracted document contents (each document's text content).
    """
    pdf_paths = Path(directory_path).glob("*.pdf")
    documents = []

    for pdf in pdf_paths:
        docs = extract_func(
            str(pdf), chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )
        documents.extend([doc.page_content for doc in docs if doc.page_content])

    return documents


def assemble_graph_theory_corpus(
    documents: list[str],
    networkx_terms: list[str],
    ngram_range: tuple[int, int] = (1, 3),
    max_features: int = 1000,
    min_freq: int = 5,
) -> list[str]:
    """Assemble a corpus of graph network science terms.

    Parameters
    ----------
    documents : list
        A list of document text content.
    networkx_terms : list
        A list of seed terms from the NetworkX API.
    ngram_range : tuple
        The range of n-grams to extract (default is unigrams to trigrams).
    max_features : int
        Maximum number of top terms to return.
    min_freq : int
        Minimum frequency threshold for n-grams to be considered.

    Returns
    -------
    list
        A list of the top graph theory-related terms.
    """
    lemmatizer = WordNetLemmatizer()

    stop_words = set(stopwords.words("english"))

    def preprocess_text(text: str) -> list[str]:
        text = unicodedata.normalize("NFKD", text)
        text = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = word_tokenize(text)
        tagged_tokens = pos_tag(tokens)
        lemmatized_tokens = [
            lemmatizer.lemmatize(word, pos=get_wordnet_pos(tag))
            for word, tag in tagged_tokens
            if word not in stop_words and word.isalpha() and len(word) >= 3
        ]
        return lemmatized_tokens

    def is_acronym(term: str) -> bool:
        return term.isupper()

    def get_wordnet_pos(treebank_tag):
        """Map POS tag to first character lemmatize() accepts"""
        if treebank_tag.startswith("J"):
            return "a"
        if treebank_tag.startswith("V"):
            return "v"
        if treebank_tag.startswith("N"):
            return "n"
        if treebank_tag.startswith("R"):
            return "r"
        return "n"

    processed_tokens = []
    for doc in documents:
        processed_tokens.extend(preprocess_text(doc))

    ngram_list = []
    for n in range(ngram_range[0], ngram_range[1] + 1):
        ngram_list.extend(ngrams(processed_tokens, n))

    ngram_counter = Counter(ngram_list)

    filtered_ngrams = [
        " ".join(ngram)
        for ngram, freq in ngram_counter.items()
        if freq >= min_freq and not is_acronym(" ".join(ngram))
    ]

    all_terms = set(filtered_ngrams).union(set(networkx_terms))

    tfidf_vectorizer = TfidfVectorizer(
        max_features=max_features, ngram_range=(1, 3), stop_words="english"
    )
    tfidf_matrix = tfidf_vectorizer.fit_transform(list(all_terms))

    feature_scores = tfidf_matrix.sum(axis=0).A1
    feature_names = tfidf_vectorizer.get_feature_names_out()
    tfidf_scores = list(zip(feature_names, feature_scores))

    sorted_terms = sorted(tfidf_scores, key=lambda x: x[1], reverse=True)

    top_terms = [term for term, score in sorted_terms[:max_features]]

    top_networkx_terms = [term for term in networkx_terms if term in top_terms]
    remaining_terms = [term for term in top_terms if term not in top_networkx_terms]

    final_terms = top_networkx_terms + remaining_terms

    logger.info(f"Extracted {len(final_terms)} graph theory terms.")

    return final_terms


def get_embedding(text, model):
    """Generate embeddings for the given text using the embedding model."""
    return model.encode(text, convert_to_tensor=True)


def filter_nodes_by_similarity(nodes, corpus_embeddings, model, threshold=0.6):
    """Filter nodes by calculating cosine similarity with the corpus embeddings.

    Parameters
    ----------
    nodes : list
        List of node dictionaries extracted by LLMGraphTransformer.
    corpus_embeddings : np.ndarray
        Precomputed embeddings for the graph theory corpus.
    model : SentenceTransformer
        The pre-trained SentenceTransformer model for embedding generation.
    threshold : float
        Similarity threshold for retaining nodes. Nodes with cosine similarity
        above this threshold are retained.

    Returns
    -------
    list
        List of filtered nodes.
    """
    filtered_nodes = []
    for node in nodes:
        node_embedding = get_embedding(node["name"], model)
        similarity_scores = cosine_similarity([node_embedding], corpus_embeddings)
        max_similarity = np.max(similarity_scores)
        if max_similarity > threshold:
            filtered_nodes.append(node)
    return filtered_nodes


def filter_relationships_by_similarity(
    relationships, corpus_embeddings, model, threshold=0.6
):
    """Filter relationships by calculating cosine similarity with the corpus embeddings.

    Parameters
    ----------
    relationships : list
        List of relationship dictionaries extracted by LLMGraphTransformer.
    corpus_embeddings : np.ndarray
        Precomputed embeddings for the graph theory corpus.
    model : SentenceTransformer
        The pre-trained SentenceTransformer model for embedding generation.
    threshold : float
        Similarity threshold for retaining relationships. Relationships with cosine
        similarity above this threshold are retained.

    Returns
    -------
    list
        List of filtered relationships.
    """
    filtered_relationships = []
    for relationship in relationships:
        relation_text = f"{relationship['source']} {relationship['relation']} "
        f"{relationship['target']}"
        relation_embedding = get_embedding(relation_text, model)
        similarity_scores = cosine_similarity([relation_embedding], corpus_embeddings)
        max_similarity = np.max(similarity_scores)
        if max_similarity > threshold:
            filtered_relationships.append(relationship)
    return filtered_relationships


def replace_algorithm_matches_in_text(
    page_content: str, algorithm_matcher: AlgorithmMatcher, threshold: float = 0.8
) -> str:
    """Find and replace matches of algorithm terms with standardized algorithm names.

    Parameters
    ----------
    page_content : str
        The content of the document page to clean.
    algorithm_matcher : AlgorithmMatcher
        An instance of the AlgorithmMatcher class to find algorithm matches.
    threshold : float, optional
        The similarity threshold for replacing the algorithm name, by default 0.8.

    Returns
    -------
    str
        The cleaned page content with close matches of algorithm names replaced.
    """
    words = page_content.split()
    cleaned_words = []

    for word in words:
        matches = algorithm_matcher.map_to_standard_name(word, threshold=threshold)

        if matches:
            best_match, similarity = matches[0]
            if similarity >= threshold:
                logger.debug(
                    f"Replacing '{word}' with standardized name '{best_match}'"
                )
                cleaned_words.append(best_match)
            else:
                cleaned_words.append(word)
        else:
            cleaned_words.append(word)

    return " ".join(cleaned_words)


def extract_text_by_chunk(
    doc_path: str,
    chunk_size: int = 10000,
    chunk_overlap: int = 750,
    algorithm_matcher: AlgorithmMatcher | None = None,
    match_threshold: float = 0.8,
    noise_threshold: float = 0.1,
) -> list:
    def remove_exotic_characters(text: str) -> str:
        """Remove non-mathematical exotic characters from the text."""
        text = unicodedata.normalize("NFKD", text)

        allowed_ranges = [
            ("\u0030", "\u0039"),  # digits
            ("\u0041", "\u005a"),  # uppercase ASCII letters
            ("\u0061", "\u007a"),  # lowercase ASCII letters
            ("\u0020", "\u002f"),  # space and basic punctuation
            ("\u003a", "\u0040"),  # symbols like :, ;, <, =, >, ?, @
            ("\u005b", "\u0060"),  # brackets and backslash
            ("\u007b", "\u007e"),  # curly brackets and tilde
            (
                "\u00a0",
                "\u00ff",
            ),  # Latin-1 Supplement characters (for accented letters)
            ("\u2200", "\u22ff"),  # Mathematical operators
            ("\u2190", "\u21ff"),  # Arrows (used in LaTeX formulas)
            ("\u2100", "\u214f"),  # Additional letter-like symbols
        ]

        def is_allowed(char):
            return (
                any(start <= char <= end for start, end in allowed_ranges)
                or char.isascii()
                and char.isprintable()
            )

        return "".join(c for c in text if is_allowed(c))

    def is_dominated_by_repeated_patterns(
        text: str,
        patterns: list | None = None,
        threshold: float = 0.1,
    ) -> bool:
        """Check if the text is dominated by repeated patterns.

        Parameters
        ----------
        text : str
            The text to evaluate.
        patterns : list, optional
            A list of regex patterns to identify repeated sequences.
        threshold : float, optional
            The maximum allowed ratio of matched patterns to total text length, by
            default 0.1 (10%).

        Returns
        -------
        bool
            True if the text is dominated by repeated patterns, False otherwise.
        """
        if patterns is None:
            patterns = ["(?:\\s*\\.\\s*){5,}", "(?:\\b\\d+\\s+){15,}\\b"]
        matched_length = 0
        for pattern in patterns:
            matches = re.findall(pattern, text)
            matched_length += sum(len(match) for match in matches)
        total_length = len(text)
        if total_length == 0:
            return False
        ratio = matched_length / total_length
        logger.debug(f"Repeated patterns ratio: {ratio:.2f}")
        return ratio > threshold

    def insert_missing_spaces(text: str) -> str:
        """Insert missing spaces between concatenated words and handle common issues."""
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
        text = re.sub(r"(\w)-(\w)", r"\1 - \2", text)

        return text

    def clean_pdf_text(text: str) -> str:
        """Clean and normalize the extracted text using noise patterns."""
        text = re.sub(r"(?i)\bReferences\b.*", "", text, flags=re.DOTALL)
        text = re.sub(r"(?i)\bBibliography\b.*", "", text, flags=re.DOTALL)
        text = re.sub(r"(?i)\bWorks\s+Cited\b.*", "", text, flags=re.DOTALL)

        for pattern in NOISE_PATTERNS:
            text = re.sub(pattern, "", text, flags=re.MULTILINE)

        text = re.sub(r"\n\s*\n", "\n", text)
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = remove_exotic_characters(text)
        text = re.sub(r"\s+", " ", text).strip()
        text = re.sub(r"(?<=\s)\.\s+(?=[A-Z])", ". ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*\.\s*", ". ", text)
        text = re.sub(r"(\w)-(\w)", r"\1 - \2", text)  # Handle hyphenated words
        text = insert_missing_spaces(text)
        text = text.strip()
        return text

    def contains_algorithm_terms(cleaned_text: str, algorithm_list: list[str]) -> bool:
        """Check if the cleaned text contains any algorithm terms."""
        cleaned_text = cleaned_text.lower()
        return any(algorithm in cleaned_text for algorithm in algorithm_list)

    try:
        loader = PyMuPDFLoader(doc_path)
        documents = loader.load()
        for doc in documents:
            if not doc.page_content:
                continue
            doc.page_content = clean_pdf_text(doc.page_content)
            if algorithm_matcher:
                doc.page_content = replace_algorithm_matches_in_text(
                    doc.page_content, algorithm_matcher, threshold=match_threshold
                )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)
        chunks_filtered = [
            chunk
            for chunk in chunks
            if (
                contains_algorithm_terms(
                    doc.page_content, list(ALGORITHM_CATEGORIES.keys())
                )
                and len(chunk.page_content) > 500
                and not is_dominated_by_repeated_patterns(
                    chunk.page_content,
                    patterns=[r"(?:\s*\.\s*){5,}", r"(?:\b\d+\s+){15,}\b"],
                    threshold=noise_threshold,
                )
            )
        ]
    except Exception:
        logger.exception(f"Failed to process file {doc_path}")
        return []
    else:
        return chunks_filtered


def is_camel_case(term: str) -> bool:
    """Check if the given term is in camel case format."""
    return bool(re.search(r"[a-z]+[A-Z]", term))


def remove_stop_words(term: str) -> str:
    """Remove stop words from the term."""
    words = term.split()
    stop_words = set(stopwords.words("english"))
    return " ".join([word for word in words if word.lower() not in stop_words])


def load_networkx_terms(submodules):
    """Load all public terms from the main networkx module and its submodules.

    Parameters
    ----------
    submodules : list
        A list of submodule names (as strings) from which to load additional terms.

    Returns
    -------
    list
        A list of unique public terms (function and class names) from networkx and its
        submodules.
    """
    networkx_terms = set(dir(nx))
    networkx_terms = {term for term in networkx_terms if not term.startswith("_")}

    for submodule in submodules:
        module = nx
        for level in submodule.split(".")[1:]:
            module = getattr(module, level)

        submodule_terms = set(dir(module))
        networkx_terms.update(
            {term for term in submodule_terms if not term.startswith("_")}
        )

    filtered_terms = [
        remove_stop_words(term.replace("_", " "))
        for term in list(set(networkx_terms))
        if term not in NX_TERM_BLACKLIST and not is_camel_case(term)
    ]
    return filtered_terms


def save_graph_theory_corpus_as_txt(
    corpus: list[str], file_name: str = "graph_theory_corpus.txt"
) -> None:
    """Save the graph theory corpus as a text file inside the package data directory."""
    package_data_dir = get_package_data_directory()
    file_path = package_data_dir / file_name

    package_data_dir.mkdir(parents=True, exist_ok=True)

    with file_path.open("w") as txt_file:
        for term in corpus:
            txt_file.write(term + "\n")


def load_graph_theory_corpus(file_path: Path) -> list[str]:
    """Load a graph theory corpus from a text file. Each line in the text file
    represents one graph theory-related term or phrase.

    Parameters
    ----------
    file_path : Path
        Path to the text file containing graph theory terms.

    Returns
    -------
    List[str]
        A list of graph theory terms loaded from the file.
    """
    corpus = []
    file_path = Path(file_path)
    try:
        with file_path.open(encoding="utf-8") as file:
            for line in file:
                term = line.strip()
                if term:
                    corpus.append(term)
    except FileNotFoundError:
        logging.exception(f"File not found: {file_path}")
        return []
    except Exception:
        logging.exception(f"Error loading corpus from {file_path}")
        return []
    else:
        return corpus


def save_docs_to_jsonl(
    array: Iterable["Document"], file_name: str = "rag_documents.jsonl"
) -> None:
    """Save a list of Document objects to a JSONL file inside package data directory."""
    package_data_dir = get_package_data_directory()
    file_path = package_data_dir / file_name

    package_data_dir.mkdir(parents=True, exist_ok=True)

    with file_path.open("w") as jsonl_file:
        for doc in array:
            jsonl_file.write(doc.json() + "\n")


def load_docs_from_jsonl(file_path: Path) -> list["Document"]:
    """Load a list of Document objects from a JSONL file.

    Each line of the input file is deserialized from JSON format into a Document
    object, and the resulting objects are returned as a list.

    Parameters
    ----------
    file_path : Path
        The path to the input JSONL file from which documents will be loaded.

    Returns
    -------
    list of Document
        A list of Document objects loaded from the file.
    """
    file_path = Path(file_path)
    array = []
    with file_path.open() as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array
