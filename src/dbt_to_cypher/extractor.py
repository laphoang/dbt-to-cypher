"""
Module for extracting dependencies from dbt projects.
"""

import json
from pathlib import Path
from typing import Any, Dict

from dbt_artifacts_parser.parser import parse_catalog, parse_manifest


class DbtDependencyExtractor:
    """
    Extract model and column-level dependencies from a dbt project.

    This class parses dbt manifest.json and other project files to build
    a comprehensive dependency graph including both model-level and
    column-level lineage.
    """

    def __init__(self, project_path: str):
        """
        Initialize the extractor with a dbt project path.

        Args:
            project_path: Path to the dbt project directory
        """
        self.project_path = Path(project_path)
        self.manifest_path = self.project_path / "target" / "manifest.json"
        self.catalog_path = self.project_path / "target" / "catalog.json"
        self.manifest: Any
        self.catalog: Any

    def load_file(self) -> None:
        """
        Load a dbt JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Dictionary containing the parsed JSON data

        Raises:
            FileNotFoundError: If the file does not exist
            json.JSONDecodeError: If the file is not valid JSON
        """
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"File not found: {self.manifest_path}")
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"File not found: {self.catalog_path}")

        with open(self.manifest_path, encoding="utf-8") as fp:
            manifest_dict = json.load(fp)

            # Filter out test nodes to avoid Pydantic validation errors in dbt-artifacts-parser, remove after dbt-artifacts-parser fix
            if "nodes" in manifest_dict:
                manifest_dict["nodes"] = {
                    k: v for k, v in manifest_dict["nodes"].items() if not k.startswith("test.")
                }

            self.manifest = parse_manifest(manifest=manifest_dict)

        with open(self.catalog_path, encoding="utf-8") as fp:
            catalog_dict = json.load(fp)

            # Remove extra metadata fields to avoid Pydantic validation errors in dbt-artifacts-parser, remove after dbt-artifacts-parser fix
            if "metadata" in catalog_dict:
                if "invocation_started_at" in catalog_dict["metadata"]:
                    del catalog_dict["metadata"]["invocation_started_at"]

            self.catalog = parse_catalog(catalog=catalog_dict)

        return

    def extract_nodes(self) -> Dict[str, Any]:
        """
        Extract nodes from the dbt project.

        Returns:
            Dictionary containing node information
        """
        nodes: Dict[str, Any] = {}
        for node_id, node in self.manifest.nodes.items():
            # Get catalog columns for this node
            catalog_node = self.catalog.nodes.get(node_id)
            columns = catalog_node.columns if catalog_node else {}

            # Convert node to dict and add computed fields
            node_dict = node.model_dump() if hasattr(node, "model_dump") else node.dict()
            node_dict["fqn"] = f"{node.database}.{node.schema_}.{node.name}"
            nodes[node_id] = node_dict
            node_dict["columns"] = columns
        return nodes

    def extract_model_dependencies(self) -> Dict:
        """
        Extract model-level dependencies from the dbt project.

        Returns:
            Dictionary containing model dependency information
        """
        # print(self.manifest)
        # print(self.catalog)

        for node_id, node in self.manifest.nodes.items():
            print(f"ID: {node_id}")
            print(f"Resource Type: {node.resource_type}")
            print(f"Name: {node.name}")
            print(node)
            print("---")

        raise NotImplementedError("Model dependency extraction not yet implemented")

    def extract_column_dependencies(self) -> Dict:
        """
        Extract column-level dependencies from the dbt project.

        Returns:
            Dictionary containing column lineage information
        """
        # TODO: Implement column lineage extraction
        raise NotImplementedError("Column dependency extraction not yet implemented")

    def extract_all(self) -> Dict:
        """
        Extract both model and column-level dependencies.

        Returns:
            Complete dependency graph data structure
        """
        return {
            "models": self.extract_model_dependencies(),
            "columns": self.extract_column_dependencies(),
        }
