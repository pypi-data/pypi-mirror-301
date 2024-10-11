import argparse
import logging

from langchain.schema import Document

from nxlu.constants import ALGORITHM_SUBMODULES
from nxlu.explanation.corpus import (
    assemble_graph_theory_corpus,
    extract_text_by_chunk,
    load_documents_from_directory,
    load_networkx_terms,
    save_docs_to_jsonl,
    save_graph_theory_corpus_as_txt,
)

logger = logging.getLogger("nxlu")


def main(pdfs_directory: str):
    logger.info(f"Processing PDFs in directory: {pdfs_directory}")

    # algorithm_matcher = AlgorithmMatcher(STANDARDIZED_ALGORITHM_NAMES)

    documents = load_documents_from_directory(
        pdfs_directory,
        extract_func=lambda path, chunk_size, chunk_overlap: extract_text_by_chunk(
            path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            # algorithm_matcher=algorithm_matcher,
            # match_threshold=0.8,
        ),
    )

    document_objects = [Document(page_content=doc) for doc in documents]

    save_docs_to_jsonl(document_objects)

    networkx_terms = load_networkx_terms(ALGORITHM_SUBMODULES)

    graph_theory_corpus = assemble_graph_theory_corpus(
        documents, networkx_terms, ngram_range=(1, 3), max_features=10000
    )

    logger.info(f"Extracted graph theory terms: {graph_theory_corpus}")

    save_graph_theory_corpus_as_txt(graph_theory_corpus)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process a directory of PDFs and extract graph theory terms."
    )
    parser.add_argument(
        "pdfs_path",
        type=str,
        help="The path to the directory containing the PDFs to process.",
    )

    args = parser.parse_args()

    main(args.pdfs_path)
