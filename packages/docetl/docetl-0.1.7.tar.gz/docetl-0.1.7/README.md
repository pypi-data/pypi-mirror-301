# DocETL: Powering Complex Document Processing Pipelines

[Website (Includes Demo)](https://docetl.com) | [Documentation](https://ucbepic.github.io/docetl) | [Discord](https://discord.gg/fHp7B2X3xx) | [NotebookLM Podcast](https://notebooklm.google.com/notebook/ef73248b-5a43-49cd-9976-432d20f9fa4f/audio?pli=1) (thanks Shabie from our Discord community!) | Paper (coming soon!)

![DocETL Figure](docs/assets/readmefig.png)

DocETL is a tool for creating and executing data processing pipelines, especially suited for complex document processing tasks. It offers a low-code, declarative YAML interface to define LLM-powered operations on complex data.

## When to Use DocETL

DocETL is the ideal choice when you're looking to maximize correctness and output quality for complex tasks over a collection of documents or unstructured datasets. You should consider using DocETL if:

- You want to perform semantic processing on a collection of data
- You have complex tasks that you want to represent via map-reduce (e.g., map over your documents, then group by the result of your map call & reduce)
- You're unsure how to best express your task to maximize LLM accuracy
- You're working with long documents that don't fit into a single prompt or are too lengthy for effective LLM reasoning
- You have validation criteria and want tasks to automatically retry when the validation fails

## Installation

See the documentation for installing from PyPI.

### Prerequisites

Before installing DocETL, ensure you have Python 3.10 or later installed on your system. You can check your Python version by running:

python --version

### Installation Steps (from Source)

1. Clone the DocETL repository:

```bash
git clone https://github.com/ucbepic/docetl.git
cd docetl
```

2. Install Poetry (if not already installed):

```bash
pip install poetry
```

3. Install the project dependencies:

```bash
poetry install
```

4. Set up your OpenAI API key:

Create a .env file in the project root and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

Alternatively, you can set the OPENAI_API_KEY environment variable in your shell.

5. Run the basic test suite to ensure everything is working (this costs less than $0.01 with OpenAI):

```bash
make tests-basic
```

That's it! You've successfully installed DocETL and are ready to start processing documents.

For more detailed information on usage and configuration, please refer to our [documentation](https://ucbepic.github.io/docetl).
