import importlib
import inspect
from typing import TYPE_CHECKING

from nxlu.constants import ALGORITHM_SUBMODULES, CUSTOM_ALGORITHMS
from nxlu.io import load_algorithm_encyclopedia

if TYPE_CHECKING:
    from collections.abc import Callable


def get_algorithm_category(module_name: str) -> str:
    """Extract the category (last part of the module name)."""
    return module_name.split(".")[-1]


def get_supported_algorithms(encyclopedia: dict):
    return list(encyclopedia.keys())


def get_available_algorithms(nxlu_only=True):
    """Get algorithms from specified NetworkX submodules and custom
    algorithms.

    Returns
    -------
    Dict[str, Callable]
        Dictionary of available algorithms.
    """
    supported_algs = get_supported_algorithms(load_algorithm_encyclopedia())

    nx_algorithm_dict: dict[str, Callable] = {}

    for module_name in ALGORITHM_SUBMODULES:
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue

        for attr_name in dir(module):
            if not attr_name.startswith("_") and not any(
                attr_name.startswith(prefix)
                for prefix in [
                    "is_",
                    "has_",
                    "get_",
                    "set_",
                    "find_",
                    "contains_",
                    "write_",
                    "read_",
                    "to_",
                    "from_",
                    "generate_",
                    "make_",
                    "create_",
                    "build_",
                    "delete_",
                    "remove_",
                ]
            ):
                if nxlu_only and attr_name not in supported_algs:
                    continue
                try:
                    attr = getattr(module, attr_name)
                except AttributeError:
                    continue
                if inspect.isfunction(attr) and attr.__module__.startswith(
                    "networkx.algorithms"
                ):
                    nx_algorithm_dict[attr_name] = attr

    return {**nx_algorithm_dict, **CUSTOM_ALGORITHMS}
