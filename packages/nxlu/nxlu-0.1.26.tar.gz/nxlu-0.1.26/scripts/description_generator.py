import argparse
import asyncio
import logging
import os

import nest_asyncio
from llama_index.core import Settings

from nxlu.config import NxluConfig
from nxlu.explanation.corpus import SUPPORTED_ALGORITHMS
from nxlu.explanation.rag import (
    AlgorithmDocstringSummarizer,
    save_algorithm_docs_to_json,
)
from nxlu.utils.control import init_llm_model

nest_asyncio.apply()

logger = logging.getLogger("nxlu")


async def main(
    output: str,
):
    config = NxluConfig(
        openai_api_key=os.environ.get("OPENAI_API_KEY"),
        model_name="gpt-4o-mini",
        temperature=0.2,
        llm_framework="llamaindex",
    )
    llm = init_llm_model(config)
    Settings.llm = llm

    summarizer = AlgorithmDocstringSummarizer(
        llm=llm,
        neo4j_uri=os.environ.get("NEO4J_URI", "neo4j://localhost:7687"),
        neo4j_user=os.environ.get("NEO4J_USERNAME", "neo4j"),
        neo4j_password=os.environ.get("NEO4J_PASSWORD", "neo4j"),
        neo4j_database="nxlu",
    )

    algorithm_summaries = await asyncio.gather(
        *[summarizer.summarize_algorithm(alg) for alg in SUPPORTED_ALGORITHMS]
    )

    algorithm_docs = dict(zip(SUPPORTED_ALGORITHMS, algorithm_summaries))

    save_algorithm_docs_to_json(algorithm_docs, output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="NxLU -- Algorithm Description Generator"
    )
    parser.add_argument(
        "--output",
        default="nxlu/data/algorithm_docs.json",
        help="Output JSON file for algorithm docs",
    )
    args = parser.parse_args()

    asyncio.run(
        main(
            args.output,
        )
    )
