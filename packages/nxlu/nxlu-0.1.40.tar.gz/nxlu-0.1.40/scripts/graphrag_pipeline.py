import argparse

from nxlu.explanation.rag import GraphRAGPipeline


def main(documents_path: str, corpus_path: str):
    """Run the GraphRAGPipeline with the provided paths.

    Parameters
    ----------
    documents_path : str
        Path to the JSONL file containing the documents to be processed.
    corpus_path : str
        Path to the text file containing the graph theory corpus.
    """
    pipeline = GraphRAGPipeline(
        documents_path=documents_path,
        graph_theory_corpus_path=corpus_path,
    )
    pipeline.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="NxLU -- GraphRAG Pipeline")
    parser.add_argument(
        "--documents_path",
        default="nxlu/data/rag_documents.jsonl",
        help="Path to the JSONL file containing the documents to process. "
        "Default: 'nxlu/data/rag_documents.jsonl'.",
    )
    parser.add_argument(
        "--corpus_path",
        default="nxlu/data/graph_theory_corpus.txt",
        help="Path to the text file containing the graph theory corpus. "
        "Default: 'nxlu/data/graph_theory_corpus.txt'.",
    )
    args = parser.parse_args()

    main(args.documents_path, args.corpus_path)
