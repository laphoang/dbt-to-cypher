#!/usr/bin/env python3
"""
release.py

Cross-platform script to bump version, commit, tag, and push for PyPI release.
Usage: python release.py --version x.x.x

"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def update_version_in_pyproject(version: str, file_path: Path = Path("pyproject.toml")):
    """Update the version in pyproject.toml."""
    content = file_path.read_text()
    new_content, count = re.subn(
        r'^version\s*=\s*".*"$',
        f'version = "{version}"',
        content,
        flags=re.MULTILINE,
    )
    if count == 0:
        print("Could not find version line in pyproject.toml")
        sys.exit(1)
    file_path.write_text(new_content)
    print(f"Updated version to {version} in pyproject.toml")


def run_command(cmd: list[str], check=True):
    """Run a shell command and print output."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False, text=True)
    if check and result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        sys.exit(result.returncode)


def main():
    parser = argparse.ArgumentParser(description="Release new version")
    parser.add_argument("--version", required=True, help="New version, e.g. 0.2.0")
    args = parser.parse_args()

    version = args.version

    # Step 1: Update pyproject.toml
    update_version_in_pyproject(version)

    # Step 2: Commit the change
    run_command(["git", "add", "pyproject.toml"])
    run_command(["git", "commit", "-m", f"Bump version to {version}"])

    # Step 3: Create git tag
    run_command(["git", "tag", f"v{version}"])

    # Step 4: Push tag to origin
    run_command(["git", "push", "origin", f"v{version}"])

    print(f"Done! GitHub Actions will now publish v{version} if set up.")


if __name__ == "__main__":
    main()
