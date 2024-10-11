[![Python](https://img.shields.io/pypi/pyversions/nxlu.svg)](https://badge.fury.io/py/nxlu)
[![PyPI](https://badge.fury.io/py/nxlu.svg)](https://badge.fury.io/py/nxlu)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://pre-commit.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Network Language Understanding (NxLU)

<p align="center">
  <img src="doc/_static/NXLU_logo.png" alt="NxLU Logo" width="150"/>
</p>

NxLU is a framework designed to augment graph analysis and AI reasoning by seamlessly integrating graph topological inference with LLM-generated knowledge queries.

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Usage (Dispatch)](#usage-dispatch)
- [Enabling NxLU Backend](#enabling-nxlu-backend)
- [Graph Reasoning](#graph-reasoning)
- [Architecture](#architecture)
- [Usage (Interrogation)](#usage-interrogation)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

NxLU bridges the gap between graph-based data analysis and natural language understanding by integrating graph algorithms with AI-powered reasoning using Large Language Models (LLMs). Built on top of NetworkX, NxLU enhances existing graph workflows by allowing users to perform both graph analysis and AI reasoning tasks seamlessly.

## Key Features

- **Dynamic Algorithm Selection**: Infers user intent and dynamically selects appropriate graph algorithms to process queries.
- **Graph Integration**: Integrates the results of graph algorithms with LLMs to generate precise and contextually relevant responses.
- **Task-Agnostic Reasoning**: Supports a broad spectrum of applications including recommendations, explanations, diagnostics, clustering, ranking, and more.
- **Enhanced Decision-Making**: Utilizes graph algorithms like clustering, ranking, and matching for advanced data manipulations and analyses.
- **Complex Relationship Handling**: Leverages intricate relationships and dependencies in graph structures for deeper reasoning.
- **Dynamic Contextualization**: Adapts its reasoning process to the specific needs of each query, ensuring relevant and accurate outputs.
- **NetworkX Backend Integration**: Integrates with NetworkX as a backend, allowing for GPU-accelerated graph analytics when available.

## System Requirements

NxLU runs on Python version 3.10 or higher and NetworkX version 3.0 or higher, and requires the following additional non-standard dependencies:

- PyTorch version 2.2 or higher
- Transformers version 4.43 or higher
- Sentence-Transformers version 3.0 or higher
- LangChain version 0.3 or higher
- Llama-Index version 0.11 or higher
- Huggingface-Hub version 0.24 or higher

For a complete list of dependencies, please refer to the pyproject.toml file in the project repository.

## Installation

For the default installation of NxLU (using LangChain), run the following command:
```bash
pip install nxlu
```

To leverage the Llamaindex framework, run:
```bash
pip install nxlu[llamaindex]
```

Then, set up your API key:
```bash
export ANTHROPIC_API_KEY=YOUR_API_KEY
# or:
export OPENAI_API_KEY=YOUR_API_KEY
```

## Usage (Dispatch)

### Enabling NxLU Backend

To use NxLU as a backend for NetworkX, you can use any of the following methods that serve to activate NetworkX's [dispatch-plugin mechanism](https://networkx.org/documentation/stable/reference/backends.html):

1. **Environment Variable**:
   Set the `NETWORKX_AUTOMATIC_BACKENDS` environment variable to automatically dispatch to NxLU for supported APIs:

   ```bash
   export NETWORKX_AUTOMATIC_BACKENDS=nxlu
   python my_networkx_script.py
   ```

2. **Backend Keyword Argument**:
   Explicitly specify NxLU as the backend for particular API calls:

   ```python
   import os
   import networkx as nx

   openai_api_key = os.getenv("OPENAI_API_KEY")
   # or
   anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

   # enabling networkx's config for nxlu
   nx.config.backends.nxlu.active = True
   nx.config.backends.nxlu.set_openai_api_key(openai_api_key)

   # nx.config.backends.nxlu.set_verbosity_level(0) # 0 = No logging, 1 = Info, 2 = Debug
   # nx.config.backends.nxlu.set_model_name(OpenAIModel.GPT_4O_MINI.value) # default
   # nx.config.backends.nxlu.set_temperature(0.1) # default
   # nx.config.backends.nxlu.set_max_token(500) # default
   # nx.config.backends.nxlu.set_num_thread(8) # default
   # nx.config.backends.nxlu.set_num_gpu(0) # default

   G = nx.path_graph(4) # Create a random graph

   results = nx.betweenness_centrality(G, backend="nxlu") # Invoking networkx calls as you normally would, but with an additional backend keyword argument
   ```

3. **Type-Based Dispatching**:

   ```python
   import networkx as nx
   from nxlu.core.interface import LLMGraph

   G = nx.path_graph(4)
   H = LLMGraph(G)

   nx.betweenness_centrality(H)
   ```

By integrating with NetworkX's backend system, NxLU provides a seamless way to enhance existing graph analysis workflows with advanced natural language processing and reasoning capabilities.

### Graph Reasoning

#### Architecture

NxLU's graph reasoning mode invokes a multi-hop strategy of "interrogating" a graph's topology (with or without a user query):

- **User Intent Detection**: Identifies the goal of the user's query using zero-shot classification.
- **Graph Characterization**: Describes the input graph's domain and structure.
- **Graph Algorithm Selection**: Predicts the most applicable graph algorithms based on the user's intent and graph context.
- **Graph Preprocessing**: Applies necessary preprocessing routines to optimize the graph for selected algorithms.
- **Graph Algorithm Application**: Applies the selected graph algorithms to the preprocessed graph.
- **Response Generation**: Integrates algorithm results with LLMs to generate structured and contextually relevant responses.

### Usage (interrogation)

In python, first set up the configuration:

```python
import os
import networkx as nx
from nxlu.explanation.explain import GraphExplainer
from nxlu.config import get_config, OpenAIModel, AnthropicModel

config = get_config()

# set an LLM framework (both LangChain and LlamaIndex are supported, though LangChain is the default)
# config.set_llm_framework("llamaindex")

openai_api_key = os.getenv("OPENAI_API_KEY")
# or:
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

# Set the API key (use either OpenAI or Anthropic)
config.set_openai_api_key(openai_api_key)
# or
config.set_anthropic_api_key(anthropic_api_key)

# Set other configurations as needed
config.set_model_name("gpt-4o-mini")
config.set_temperature(0.1)
config.set_max_tokens(500)
config.set_verbosity_level(1)  # 0=No logging, 1=INFO, 2=DEBUG
```

In the following minimal example, we use the GraphExplainer to analyze a social network graph, with or without a specific query. This example shows both cases:

```python
G = nx.Graph()

G.add_edge('Elon Musk', 'Jeff Bezos', weight=30)
G.add_edge('Elon Musk', 'Tim Cook', weight=15)
G.add_edge('Elon Musk', 'Sundar Pichai', weight=12)
G.add_edge('Elon Musk', 'Satya Nadella', weight=20)
G.add_edge('Jeff Bezos', 'Warren Buffet', weight=25)
G.add_edge('Jeff Bezos', 'Bill Gates', weight=10)
G.add_edge('Jeff Bezos', 'Tim Cook', weight=18)
G.add_edge('Tim Cook', 'Sundar Pichai', weight=8)
G.add_edge('Tim Cook', 'Sheryl Sandberg', weight=9)
G.add_edge('Sundar Pichai', 'Bill Gates', weight=6)
G.add_edge('Sundar Pichai', 'Sheryl Sandberg', weight=7)
G.add_edge('Satya Nadella', 'Warren Buffet', weight=15)
G.add_edge('Satya Nadella', 'Sheryl Sandberg', weight=13)
G.add_edge('Bill Gates', 'Warren Buffet', weight=40)

# Initialize the explainer with configuration
explainer = GraphExplainer(config)

# Perform analysis without a specific query
response = explainer.explain(G)
print(response)

# Perform analysis with a specific query
query = "Which executive in this network is the most connected to the other executives?"
response = explainer.explain(G, query)
print(response)
```

Finally, it is also possible to exert fine-grained control over which algorithms get applied:

```python
# Optionally specify networkx algorithms by name to be included or excluded
config.set_include_algorithms(['betweenness_centrality', 'clustering'])
config.set_exclude_algorithms(['shortest_path'])
# config.enable_classification = False # the default is `True`, but if this is set to `False`, the system should rely solely on the include/exclude lists without performing zero-shot classification of the most "suitable" algorithms for the graph + query.
explainer = GraphExplainer(config) # reinitialize the graph explainer
```

### Supported Models

NxLU supports a wide range of language models from different providers, including [ollama](https://ollama.com/library) local models. You can configure NxLU to use one of the following models based on your needs:

**OpenAI Models**:

- GPT-4 Turbo (gpt-4-turbo)
- GPT-4 (gpt-4)
- GPT-4O (gpt-4o) (gpt-4o-2024-08-06)
- GPT-4O Mini (gpt-4o-mini)
- GPT-4O1 Preview (o1-preview)
- GPT-401 Mini (o1-mini)

**Anthropic Models**:

- Claude 2 (claude-2)
- Claude 2.0 (claude-2.0)
- Claude Instant (claude-instant)
- Claude Instant 1 (claude-instant-1)
- Claude Instant 1.1 (claude-instant-1.1)
- Claude 3 Sonnet (claude-3-sonnet)
- Claude 3.5 Sonnet (claude-3.5-sonnet)

**Local Models**:

- Llama 3 - 70B (llama3:70b)
- Llama 3 - 8B (llama3:8b)
- Gemma 2 - 9B (gemma2:9b)
- Qwen 2 - 7B (qwen2:7b)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request to discuss potential improvements or features. Before submitting, ensure that you read and follow the [CONTRIBUTING](CONTRIBUTING) guide.

## License

This project is licensed under the [MIT License](LICENSE).
