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

    parser.add_argument(
        "--include-columns",
        action="store_true",
        help="Include column-level dependencies",
    )

    args = parser.parse_args()

    try:
        # Extract dependencies
        extractor = DbtDependencyExtractor(args.project_path)
        dependencies = extractor.extract_all()
        print('dependencies:', dependencies)
        # Build graph
        graph = DependencyGraph()

        # Populate graph from model-level dependencies
        models = dependencies.get("models", {}) if isinstance(dependencies, dict) else {}
        for model in models.keys():
            graph.add_model(model)

        for model, upstreams in models.items():
            for upstream in upstreams:
                # ensure upstream model node exists
                graph.add_model(upstream)
                graph.add_dependency(upstream, model)

        # Populate graph from column-level dependencies (if present)
        columns = dependencies.get("columns", {}) if isinstance(dependencies, dict) else {}
        for col_fqn, upstream_cols in columns.items():
            # split into model and column name
            if "." not in col_fqn:
                continue
            model_name, column_name = col_fqn.rsplit(".", 1)
            graph.add_model(model_name)
            graph.add_column(model_name, column_name)

            for up_col in upstream_cols:
                if "." not in up_col:
                    continue
                up_model, up_column = up_col.rsplit(".", 1)
                graph.add_model(up_model)
                graph.add_column(up_model, up_column)
                # add dependency edge from upstream column to this column
                graph.add_dependency(f"{up_model}.{up_column}", f"{model_name}.{column_name}")

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
