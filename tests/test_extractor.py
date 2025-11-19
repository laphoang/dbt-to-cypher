"""Tests for the DbtDependencyExtractor class."""

from pathlib import Path

import pytest
from dbt_to_cypher.extractor import DbtDependencyExtractor


def test_extractor_initialization():
    """Test that the extractor initializes correctly."""
    project_path = Path("/fake/project")
    extractor = DbtDependencyExtractor(project_path)

    assert extractor.project_path == project_path
    assert extractor.manifest_path == project_path / "target" / "manifest.json"
    assert extractor.catalog_path == project_path / "target" / "catalog.json"


def test_extract_model_dependencies_not_implemented():
    """Test that extract_model_dependencies raises NotImplementedError."""
    extractor = DbtDependencyExtractor(Path("/fake/project"))

    with pytest.raises(NotImplementedError):
        extractor.extract_model_dependencies()


def test_extract_column_dependencies_not_implemented():
    """Test that extract_column_dependencies raises NotImplementedError."""
    extractor = DbtDependencyExtractor(Path("/fake/project"))

    with pytest.raises(NotImplementedError):
        extractor.extract_column_dependencies()
