import re
import warnings
from collections.abc import Callable
from enum import Enum

import numpy as np

from _nxlu.config import NxluConfig, _config

from _nxlu.enums import (  # isort: skip # noqa: F401
    AnthropicModel,
    LocalModel,
    OpenAIModel,
    Framework,
)

warnings.filterwarnings("ignore")


def get_config() -> NxluConfig:
    """Return the singleton configuration instance."""
    return _config


CostFunction = Callable[[int, int], float]

COMPLEXITY_COST_MAPPING: dict[str, CostFunction] = {
    "constant": lambda n, m: 1.0,  # O(1)
    "logarithmic": lambda n, m: np.log(n),  # O(log n)
    "linear": lambda n, m: n,  # O(n)
    "linear + m": lambda n, m: n + m,  # O(n + m)
    "loglinear": lambda n, m: n * np.log(n),  # O(n log n)
    "quadratic": lambda n, m: n**2,  # O(n^2)
    "quadratic + m": lambda n, m: n**2 + m,  # O(n^2 + m)
    "cubic": lambda n, m: n**3,  # O(n^3)
    "exponential": lambda n, m: 2**n,  # O(2^n)
    "polynomial": lambda n, m: n**2 + m,  # O(n^2 + m)
}


def normalize_name(name: str) -> str:
    """Normalize the algorithm name

    Parameters
    ----------
    name : str
        The name to normalize.

    Returns
    -------
    str
        The normalized name.
    """
    name = name.lower()
    name = re.sub(r"[_\-]+", " ", name)
    name = re.sub(r"\s+", " ", name)
    name = (
        name.replace("coefficient", "")
        .replace("index", "")
        .replace("best_partition", "louvain")
    )
    return name.strip()


def parse_supported_algorithms(
    encyclopedia: dict, normalize_func: Callable
) -> tuple[list, dict, list]:
    """Load and normalize algorithm names from an encyclopedia.

    Parameters
    ----------
    encyclopedia : dict
        An algorithm encyclopedia dictionary.
    normalize_func : function
        A function that normalizes the algorithm names.

    Returns
    -------
    tuple
        A tuple containing:
        - A list of supported algorithms.
        - A dictionary mapping normalized algorithm names to their categories.
        - A list of the supported algorithms with standardized names.
    """
    supported_algorithms = list(encyclopedia.keys())

    algorithm_categories = {
        normalize_func(alg).lower(): metadata.get("algorithm_category", "Unknown")
        for alg, metadata in encyclopedia.items()
    }

    standardized_names = list(algorithm_categories.keys())

    return supported_algorithms, algorithm_categories, standardized_names


class RescalingMethod(str, Enum):
    normalize = "normalize"
    standardize = "standardize"
    invert = "invert"
    binarize = "binarize"


class Intent(Enum):
    # 1. Information Seeking and Retrieval
    FACT_RETRIEVAL = "Fact Retrieval"
    CLARIFICATION = "Clarification"
    CONTEXTUAL_SEARCH = "Contextual Search"
    VERIFICATION = "Verification"
    EXPLORATION = "Exploration"

    # 2. Reasoning and Explanation
    CAUSAL_EXPLANATION = "Causal Explanation"
    PROCEDURAL_EXPLANATION = "Procedural Explanation"
    CONCEPTUAL_EXPLANATION = "Conceptual Explanation"
    COMPARATIVE_EXPLANATION = "Comparative Explanation"
    SEQUENTIAL_REASONING = "Sequential Reasoning"

    # 3. Decision-Making and Recommendations
    RECOMMENDATION = "Recommendation"
    PRIORITIZATION = "Prioritization"
    DECISION_SUPPORT = "Decision Support"
    ACTION_SUGGESTION = "Action Suggestion"
    ALTERNATIVES_EXPLORATION = "Alternatives Exploration"

    # 4. Diagnostic and Analytical
    DIAGNOSTIC_REASONING = "Diagnostic Reasoning"
    ROOT_CAUSE_ANALYSIS = "Root Cause Analysis"
    ERROR_DETECTION = "Error Detection"
    FAULT_IDENTIFICATION = "Fault Identification"
    PATTERN_RECOGNITION = "Pattern Recognition"

    # 5. Instruction and Guidance
    STEP_BY_STEP_GUIDANCE = "Step-by-Step Guidance"
    TASK_COMPLETION = "Task Completion"
    PROCESS_OPTIMIZATION = "Process Optimization"
    TROUBLESHOOTING = "Troubleshooting"

    # 6. Creative and Ideation
    IDEA_GENERATION = "Idea Generation"
    CONTENT_CREATION = "Content Creation"
    BRAINSTORMING = "Brainstorming"
    STORYTELLING = "Storytelling"

    # 7. Classification and Categorization
    CATEGORIZATION = "Categorization"
    CLASSIFICATION = "Classification"
    TAGGING = "Tagging"
    SORTING = "Sorting"

    # 8. Summarization and Information Condensation
    SUMMARIZATION = "Summarization"
    ABSTRACTION = "Abstraction"
    HIGHLIGHTING = "Highlighting"

    # 9. Personalization and Adaptation
    PERSONALIZATION = "Personalization"
    CUSTOMIZATION = "Customization"
    CONTEXTUAL_ADAPTATION = "Contextual Adaptation"

    # 10. Planning and Scheduling
    PLANNING = "Planning"
    GOAL_SETTING = "Goal Setting"
    SCHEDULING = "Scheduling"

    # 11. Navigation and Direction
    LOCATION_BASED_NAVIGATION = "Location-Based Navigation"
    RESOURCE_NAVIGATION = "Resource Navigation"
    PATHFINDING = "Pathfinding"

    # 12. Prediction and Forecasting
    PREDICTION = "Prediction"
    TREND_ANALYSIS = "Trend Analysis"
    FORECASTING = "Forecasting"
    OUTCOME_ESTIMATION = "Outcome Estimation"

    # 13. Problem-Solving and Strategy
    PROBLEM_SOLVING = "Problem Solving"
    STRATEGY_DEVELOPMENT = "Strategy Development"
    OPTIMIZATION = "Optimization"
    RISK_ASSESSMENT = "Risk Assessment"

    # 14. Collaboration and Coordination
    COLLABORATION = "Collaboration"
    TASK_DELEGATION = "Task Delegation"
    SYNCHRONIZATION = "Synchronization"
    SHARING = "Sharing"

    # 15. Miscellaneous High-Level Intents
    EMOTION_ANALYSIS = "Emotion Analysis"
    FEEDBACK = "Feedback"
