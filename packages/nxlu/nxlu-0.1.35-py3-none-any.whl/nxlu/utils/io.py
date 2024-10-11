import importlib
import json
import logging
import warnings
from typing import Any

import networkx as nx

from nxlu.constants import ALGORITHM_SUBMODULES, CUSTOM_ALGORITHMS

warnings.filterwarnings("ignore")


logger = logging.getLogger("nxlu")

__all__ = [
    "load_algorithm_encyclopedia",
    "load_algorithm_docs",
    "get_algorithm_function",
]


def load_algorithm_encyclopedia() -> dict[str, dict[str, Any]]:
    """Load the encyclopedia of algorithm applicability conditions from a JSON file.

    Returns
    -------
    Dict[str, Dict[str, Any]]
        Dictionary containing algorithm applicability conditions.
    """
    try:
        with importlib.resources.open_text(
            "nxlu.data", "algorithm_encyclopedia.json"
        ) as file:
            applicability = json.load(file)
    except FileNotFoundError:
        error_message = "Algorithm encyclopedia file not found."
        logger.exception(error_message)
        raise FileNotFoundError(error_message)
    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON: {e}"
        logger.exception(error_message)
        raise ValueError(error_message)
    else:
        logger.info("Loaded algorithm encyclopedia successfully.")
        return applicability


def load_algorithm_docs(algorithm_name: str | None = None) -> dict:
    """Load algorithm documentation from a JSON file using pathlib.

    Returns
    -------
    dict
        Dictionary containing algorithm documentation.
    """
    try:
        with importlib.resources.open_text("nxlu.data", "algorithm_docs.json") as file:
            alg_docs = json.load(file)
    except FileNotFoundError:
        error_message = "Algorithm documentation file not found."
        logger.exception(error_message)
        raise FileNotFoundError(error_message)
    except json.JSONDecodeError as e:
        error_message = f"Error decoding JSON: {e}"
        logger.exception(error_message)
        raise ValueError(error_message)
    else:
        logger.info("Loaded algorithm documentation successfully.")
        if algorithm_name:
            return alg_docs[algorithm_name]
        return alg_docs


def get_algorithm_function(algorithm_name: str):
    """Retrieve the appropriate algorithm function by name."""
    if algorithm_name in CUSTOM_ALGORITHMS:
        return CUSTOM_ALGORITHMS[algorithm_name]
    if hasattr(nx.algorithms, algorithm_name):
        return getattr(nx.algorithms, algorithm_name)
    for module in ALGORITHM_SUBMODULES:
        if hasattr(module, algorithm_name):
            return getattr(module, algorithm_name)
    raise ValueError(f"Algorithm '{algorithm_name}' not found.")
