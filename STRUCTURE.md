# Project Structure

```
dbt-to-cypher/
│
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI/CD workflow
│
├── src/
│   └── dbt_to_cypher/
│       ├── __init__.py              # Package initialization & exports
│       ├── cli.py                   # Command-line interface
│       ├── cypher.py                # Cypher query generation
│       ├── extractor.py             # dbt dependency extraction
│       └── graph.py                 # Dependency graph management
│
├── tests/
│   ├── __init__.py                  # Test package marker
│   ├── conftest.py                  # pytest configuration & fixtures
│   ├── test_cypher.py               # CypherGenerator tests
│   ├── test_extractor.py            # DbtDependencyExtractor tests
│   └── test_graph.py                # DependencyGraph tests
│
├── examples/
│   ├── basic_usage.py               # Basic usage examples
│   └── README.md                    # Examples documentation
│
├── .flake8                          # Flake8 linter configuration
├── .gitignore                       # Git ignore patterns
├── .pre-commit-config.yaml          # Pre-commit hooks config
├── DEVELOPMENT.md                   # Development setup guide
├── justfile                         # Just task runner recipes
├── LICENSE                          # MIT License
├── pyproject.toml                   # PEP 621 project metadata
├── README.md                        # Project documentation
├── setup_dev.py                     # Automated setup script
└── SETUP_CHECKLIST.md              # Setup verification checklist
```

## Core Modules

### `extractor.py`

Extracts dependency information from dbt projects by parsing `manifest.json` and `catalog.json` files.

**Key Class**: `DbtDependencyExtractor`

- `extract_model_dependencies()` - Extract model-level dependencies
- `extract_column_dependencies()` - Extract column-level lineage
- `extract_all()` - Extract both model and column dependencies

### `graph.py`

Manages the dependency graph structure using NetworkX.

**Key Class**: `DependencyGraph`

- `add_model()` - Add a model node
- `add_column()` - Add a column node
- `add_dependency()` - Add a dependency edge
- `get_upstream_dependencies()` - Query upstream dependencies
- `get_downstream_dependencies()` - Query downstream dependencies
- `to_dict()` - Export graph structure

### `cypher.py`

Generates Cypher queries from the dependency graph.

**Key Class**: `CypherGenerator`

- `generate_node_queries()` - Generate node creation queries
- `generate_relationship_queries()` - Generate relationship queries
- `generate_all_queries()` - Generate complete Cypher script

### `cli.py`

Command-line interface for the tool.

**Usage**:

```bash
dbt-to-cypher <project_path> [-o output.cypher] [--include-columns]
```

## Configuration Files

### `pyproject.toml`

Modern Python packaging configuration following PEP 621:

- Project metadata (name, version, description)
- Dependencies and optional dependencies
- Build system configuration (hatchling)
- Tool configurations (black, isort, pytest, coverage)

### `.pre-commit-config.yaml`

Pre-commit hooks that run before each commit:

- `black` - Code formatter (line length: 100)
- `isort` - Import sorter (black profile)
- `flake8` - Linter (max line length: 100)
- Additional checks (trailing whitespace, YAML, JSON, etc.)

### `.flake8`

Flake8 linter configuration:

- Max line length: 100
- Extends ignore: E203, W503 (black compatibility)
- Per-file ignores for `__init__.py`

## Development Tools

### Package Manager: uv

Fast Python package installer and resolver.

```bash
uv pip install <package>
uv pip install -e ".[dev]"
```

### Task Runner: just (optional)

Command runner for development tasks.

```bash
just test         # Run tests
just format       # Format code
just lint         # Lint code
just check        # Format + lint
```

### Testing: pytest

Test framework with coverage support.

```bash
pytest                              # Run all tests
pytest --cov=src                    # Run with coverage
pytest tests/test_graph.py          # Run specific test file
```

## Code Quality Standards

### Formatting

- **Black**: Line length 100, Python 3.8+ target
- **isort**: Black profile, sorted imports

### Linting

- **Flake8**: Line length 100, complexity max 10
- Extends ignore: E203, W503

### Testing

- **pytest**: Unit tests for all modules
- **Coverage**: Aim for >80% coverage
- Test files: `tests/test_*.py`

## Dependencies

### Core Dependencies

- `pyyaml>=6.0` - YAML parsing
- `networkx>=3.0` - Graph data structures

### Development Dependencies

- `pytest>=7.0` - Testing framework
- `pytest-cov>=4.0` - Coverage plugin
- `black>=23.0` - Code formatter
- `isort>=5.12` - Import sorter
- `flake8>=6.0` - Linter
- `pre-commit>=3.0` - Git hooks

## Entry Points

### Command-line

```bash
dbt-to-cypher = dbt_to_cypher.cli:main
```

### Python API

```python
from dbt_to_cypher import (
    DbtDependencyExtractor,
    DependencyGraph,
    CypherGenerator,
)
```

## Build System

**Backend**: Hatchling (PEP 517 compliant)

```bash
python -m build          # Build source and wheel distributions
python -m twine upload   # Upload to PyPI
```
