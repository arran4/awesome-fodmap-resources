#!/usr/bin/env python3
"""
Concatenates markdown files into a single book.md for EPUB generation.
"""

import os
from pathlib import Path
import re

OUTPUT_FILE = "book.md"

# Order of files
FILES_ORDER = [
    "index.md",
    "rules.md",
    "recipes.md",
    "blogs.md",
    "research.md",
]

# Directories to include (sorted alphabetically)
DIRS_TO_INCLUDE = [
    "countries",
    "blogs",
]

def get_files_in_dir(dirname):
    path = Path(dirname)
    if not path.exists():
        return []
    return sorted([str(p) for p in path.glob("*.md")])

def read_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            # Ensure the file ends with a newline to prevent concatenation issues
            if not content.endswith("\n"):
                content += "\n"
            return content
    except FileNotFoundError:
        print(f"Warning: {filepath} not found, skipping.")
        return ""

def main():
    all_files = list(FILES_ORDER)

    for d in DIRS_TO_INCLUDE:
        all_files.extend(get_files_in_dir(d))

    print(f"Concatenating {len(all_files)} files into {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Add title and metadata for pandoc (optional, but good practice)
        # However, index.md has the main title.

        for filepath in all_files:
            print(f"Processing {filepath}...")
            content = read_file(filepath)

            # Here we might want to rewrite links, but for now we simply concatenate.
            # Pandoc might complain about links to other MD files if they are not in the list or if we don't fix them.
            # But fixing them robustly is complex. We'll leave them as is for this iteration.

            outfile.write(content)
            outfile.write("\n\n") # Ensure separation between files

    print("Done.")

if __name__ == "__main__":
    main()
