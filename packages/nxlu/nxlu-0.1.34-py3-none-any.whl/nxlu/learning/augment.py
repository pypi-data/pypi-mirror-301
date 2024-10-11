import importlib.resources as pkg_resources
import logging
import random
import re
import warnings

import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from transformers import BartForConditionalGeneration, BartTokenizer

from nxlu.explanation.corpus import STANDARDIZED_ALGORITHM_NAMES

warnings.filterwarnings("ignore")

logger = logging.getLogger("nxlu")

__all__ = ["pre_tokenize_corpus", "Paraphraser"]


def pre_tokenize_corpus(corpus: list[str], tokenizer: BartTokenizer) -> list[str]:
    """Pre-tokenize graph theory terms into known subword units."""
    tokenized_corpus = []
    for term in corpus:
        tokens = tokenizer.tokenize(term)
        tokenized_term = tokenizer.convert_tokens_to_string(tokens)
        tokenized_corpus.append(tokenized_term)
    return tokenized_corpus


class Paraphraser:
    """A class to paraphrase text queries using a pre-trained BART model."""

    def __init__(
        self,
        model_name: str = "eugenesiow/bart-paraphrase",
        top_n: int = 3,
        replace_synonyms: bool = True,
        replacement_probability: float = 0.5,
    ):
        """Initialize the Paraphraser with a pre-trained BART model.

        Parameters
        ----------
        model_name : str, optional
            The pre-trained BART model to use, by default "eugenesiow/bart-paraphrase".
        top_n : int, optional
            The number of similar terms to store for each term, by default 3.
        replacement_probability : float, optional
            Probability of replacing a term with its synonym, by default 0.5.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = BartForConditionalGeneration.from_pretrained(model_name).to(
            self.device
        )
        self.tokenizer = BartTokenizer.from_pretrained(model_name)
        self.replace_synonyms = replace_synonyms
        if self.replace_synonyms:
            self.top_n = top_n
            self.replacement_probability = replacement_probability
            with pkg_resources.open_text("nxlu.data", "graph_theory_corpus.txt") as f:
                self.network_terms = f.read().splitlines()
            self.corpus = pre_tokenize_corpus(self.network_terms, self.tokenizer)
            self.term_embeddings = self.compute_term_embeddings(self.network_terms)
            self.similarity_mapping = self.build_similarity_mapping(
                self.network_terms, self.term_embeddings
            )

    def paraphrase(
        self, input_sentence: str, num_return_sequences: int = 3
    ) -> list[str]:
        """Paraphrase the input sentence.

        Parameters
        ----------
        input_sentence : str
            The sentence to paraphrase.
        num_return_sequences : int
            The number of paraphrased sentences to return.

        Returns
        -------
        List[str]
            A list of paraphrased sentences.
        """
        if self.replace_synonyms:
            tokenized_input = self.replace_terms_with_synonyms(input_sentence)
        else:
            tokenized_input = input_sentence

        batch = self.tokenizer(tokenized_input, return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(
            batch["input_ids"],
            num_beams=5,
            num_return_sequences=num_return_sequences,
            max_length=256,
            early_stopping=True,
        )
        paraphrases = self.tokenizer.batch_decode(
            generated_ids, skip_special_tokens=True
        )
        return paraphrases

    def compute_term_embeddings(self, terms: list[str]) -> dict[str, torch.Tensor]:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        term_embeddings = model.encode(terms, batch_size=32, convert_to_numpy=True)
        return dict(zip(terms, term_embeddings))

    def build_similarity_mapping(
        self, terms: list[str], embeddings: dict[str, torch.Tensor]
    ) -> dict[str, list[str]]:
        """Build a mapping from each term to its top N similar terms."""
        logger.info("Building similarity mapping...")

        term_list = terms
        embedding_matrix = np.stack([embeddings[term] for term in term_list])

        norms = np.linalg.norm(embedding_matrix, axis=1, keepdims=True)
        normalized_embeddings = embedding_matrix / norms

        similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)

        similarity_mapping = {}
        for idx, term in enumerate(term_list):
            similarities = similarity_matrix[idx]

            # exclude self-similarity
            similarities[idx] = -np.inf

            top_indices = np.argsort(-similarities)[: self.top_n]
            top_similar_terms = [term_list[i] for i in top_indices]

            similarity_mapping[term] = top_similar_terms

        logger.info("Completed building similarity mapping.")
        return similarity_mapping

    def replace_terms_with_synonyms(self, sentence: str) -> str:
        """
        Replace graph-theory terms in a sentence with their similar terms.

        Parameters
        ----------
        sentence : str
            The input sentence containing potential graph-theory terms.

        Returns
        -------
        str
            The sentence with some terms replaced by their synonyms.
        """
        sorted_terms = sorted(
            STANDARDIZED_ALGORITHM_NAMES, key=lambda x: len(x), reverse=True
        )

        for term in sorted_terms:
            pattern = re.compile(r"\b" + re.escape(term) + r"\b", flags=re.IGNORECASE)

            def replacement(match, term=term):
                if random.random() < self.replacement_probability:
                    similar_terms = self.similarity_mapping.get(term, [])
                    if similar_terms:
                        replacement_term = random.choice(similar_terms)

                        original_text = match.group()
                        if original_text.isupper():
                            replacement_term = replacement_term.upper()
                        elif original_text[0].isupper():
                            replacement_term = replacement_term.capitalize()
                        else:
                            replacement_term = replacement_term.lower()

                        if replacement_term.lower() != original_text.lower():
                            return replacement_term
                return match.group()

            sentence = pattern.sub(replacement, sentence)

        return sentence

    def paraphrase_queries(
        self, queries: list[str], num_return_sequences: int = 3
    ) -> list[str]:
        """Generate paraphrased versions of the input queries.

        Parameters
        ----------
        queries : List[str]
            The list of original queries to paraphrase.

        Returns
        -------
        List[str]
            A list of paraphrased queries.
        """
        augmented_queries = []
        for query in queries:
            paraphrased_versions = self.paraphrase(query, num_return_sequences)
            augmented_queries.extend(paraphrased_versions)
        return augmented_queries
