"""
Command-line interface for dbt-to-cypher.
"""

import os
import sys

from dotenv import load_dotenv

from dbt_to_cypher.extractor import DbtDependencyExtractor


def main():
    try:
        load_dotenv()  # Load .env file
        # Extract dependencies
        project_path = os.getenv("PROJECT_PATH")
        if not project_path:
            raise ValueError("PROJECT_PATH environment variable not set")

        extractor = DbtDependencyExtractor(project_path)
        extractor.load_file()
        nodes = extractor.extract_nodes()
        print(nodes)
        dependencies = extractor.extract_model_dependencies()
        print(dependencies)
        col_deps = extractor.extract_column_dependencies()
        print(col_deps)

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
