# dbt-to-cypher

Extract dependency graphs from dbt projects (including model and column dependencies) and convert them to Cypher queries for graph database visualization and analysis.

## Features

- 📊 **Model-level dependencies**: Extract relationships between dbt models
- 🔍 **Column-level lineage**: Track data flow at the column level
- 🔄 **Cypher generation**: Convert dependency graphs to Neo4j Cypher queries
- 🛠️ **CLI tool**: Easy command-line interface for quick conversions
- 📦 **Library API**: Programmatic access for integration into your workflows

## Installation

Using `uv` (recommended):

```bash
uv pip install dbt-to-cypher
```

Using `pip`:

```bash
pip install dbt-to-cypher
```

## Quick Start

### Command Line

```bash
# Basic usage
dbt-to-cypher /path/to/dbt/project

# Save output to file
dbt-to-cypher /path/to/dbt/project -o output.cypher

# Include column-level dependencies
dbt-to-cypher /path/to/dbt/project --include-columns
```

### Python API

```python
from dbt_to_cypher import DbtDependencyExtractor, DependencyGraph, CypherGenerator

# Extract dependencies from dbt project
extractor = DbtDependencyExtractor("/path/to/dbt/project")
dependencies = extractor.extract_all()

# Build dependency graph
graph = DependencyGraph()
# ... populate graph with dependencies

# Generate Cypher queries
generator = CypherGenerator(graph)
cypher_script = generator.generate_all_queries()
print(cypher_script)
```

## Development

See [DEVELOPMENT.md](DEVELOPMENT.md) for development setup instructions.

### Quick Development Setup

```bash
# Install uv
pip install uv

# Create virtual environment and install dependencies
uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

## Project Structure

```
dbt-to-cypher/
├── src/
│   └── dbt_to_cypher/
│       ├── __init__.py       # Package initialization and exports
│       ├── extractor.py      # dbt dependency extraction
│       ├── graph.py          # Dependency graph management
│       ├── cypher.py         # Cypher query generation
│       └── cli.py            # Command-line interface
├── tests/                    # Test suite
├── pyproject.toml           # PEP 621 project metadata
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
└── README.md
```

## Requirements

- Python 3.8+
- dbt project with generated `manifest.json` (run `dbt compile` or `dbt run` first)

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Roadmap

- [ ] Parse dbt `manifest.json` for model dependencies
- [ ] Extract column-level lineage from SQL queries
- [ ] Support for dbt sources and seeds
- [ ] Export to additional graph formats (GraphML, DOT)
- [ ] Interactive visualization tools
- [ ] Support for dbt metrics and exposures

## Author

laphoang

## Acknowledgments

Built with modern Python packaging standards (PEP 621) and best practices.
