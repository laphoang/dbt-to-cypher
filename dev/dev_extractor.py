"""
Command-line interface for dbt-to-cypher.
"""

import os
import sys

from dbt_to_cypher.extractor import DbtDependencyExtractor
from dotenv import load_dotenv


def main():
    try:
        load_dotenv()  # Load .env file
        # Extract dependencies
        extractor = DbtDependencyExtractor(os.getenv("PROJECT_PATH"))
        dependencies = extractor.extract_model_dependencies()
        print(f"Extracted {len(dependencies)} models")

        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
