"""
Command-line interface for dbt-to-cypher.
"""

import argparse
import sys
from pathlib import Path

from dbt_to_cypher import __version__
from dbt_to_cypher.cypher import CypherGenerator
from dbt_to_cypher.extractor import DbtDependencyExtractor
from dbt_to_cypher.graph import DependencyGraph


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Extract dbt dependencies and convert to Cypher queries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"dbt-to-cypher {__version__}",
    )

    parser.add_argument(
        "project_path",
        type=Path,
        help="Path to the dbt project directory",
    )

    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file for Cypher queries (default: stdout)",
    )

    args = parser.parse_args()

    try:
        print(f"Loading dbt project from: {args.project_path}")
        # Extract dependencies
        extractor = DbtDependencyExtractor(args.project_path)
        dependencies = extractor.extract_all()
        print('dependencies:', dependencies)
        # Build graph
        graph = DependencyGraph()

        # Populate graph from model-level dependencies
        models = dependencies.get("models", {}) if isinstance(dependencies, dict) else {}
        for model, model_data in models.items():
            graph.add_model(model, metadata=model_data)

        columns = dependencies.get("columns", {}) if isinstance(dependencies, dict) else {}
        for column, col_data in columns.items():
            graph.add_column(column, metadata=col_data)
            graph.add_dependency(col_data.get("model_name", ""), column, relationship="has_column")

        model_dependencies = dependencies.get("model_dependencies", {}) if isinstance(dependencies, dict) else {}
        for model, upstreams in model_dependencies.items():
            for upstream in upstreams:
                # ensure upstream model node exists
                graph.add_dependency(model, upstream)

        column_dependencies = dependencies.get("column_dependencies", {}) if isinstance(dependencies, dict) else {}
        for column, upstreams in column_dependencies.items():
            for upstream in upstreams:
                # ensure upstream model node exists
                graph.add_dependency(column, upstream)


        print(f"Extracted dependencies: {len(models)} model groups, {len(columns)} column entries")

        # Generate Cypher
        generator = CypherGenerator(graph)
        cypher_script = generator.generate_all_queries()

        # Output
        if args.output:
            args.output.write_text(cypher_script)
            print(f"Cypher queries written to {args.output}")
        else:
            print(cypher_script)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
