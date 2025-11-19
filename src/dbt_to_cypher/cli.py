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

        # Build graph
        graph = DependencyGraph()
        # TODO: Populate graph from dependencies
        print(f"Extracted dependencies: {len(dependencies)} groups")

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
