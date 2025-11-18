# Development Setup

## Installation with uv

```bash
# Install uv if you haven't already
pip install uv

# Create a virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

## Development Commands

```bash
# Run tests
pytest

# Run tests with coverage
pytest --cov=src --cov-report=html

# Format code
black src tests
isort src tests

# Lint code
flake8 src tests

# Run pre-commit on all files
pre-commit run --all-files
```

## Building and Publishing

```bash
# Build the package
uv pip install build
python -m build

# Upload to PyPI (requires twine)
uv pip install twine
twine upload dist/*
```
