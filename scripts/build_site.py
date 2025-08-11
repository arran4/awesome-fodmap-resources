#!/usr/bin/env python3
"""Build static HTML files from Markdown sources.

All .md files under the repository are converted to HTML and written under the
`site` directory preserving the directory structure. Each generated page
includes an "Edit this page" link pointing back to the source file on the main
branch of the GitHub repository.
"""

import os
from pathlib import Path
import markdown
import re

REPO_URL = os.environ.get("REPO_URL", "").rstrip("/")
SOURCE_DIR = Path(".")
OUTPUT_DIR = Path("site")

for md_path in SOURCE_DIR.rglob("*.md"):
    if ".git" in md_path.parts:
        continue
    rel_path = md_path.relative_to(SOURCE_DIR)
    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(md_text)
    html_body = re.sub(
        r'href="([^":]+)\.md(#[^"]*)?"',
        r'href="\1.html\2"',
        html_body,
    )
    edit_url = f"{REPO_URL}/blob/main/{rel_path.as_posix()}" if REPO_URL else ""
    full_html = f"""<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<title>{md_path.stem}</title>
</head>
<body>
{html_body}
<p><a href=\"{edit_url}\">Edit this page</a></p>
</body>
</html>
"""
    out_file = OUTPUT_DIR / rel_path.with_suffix(".html")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(full_html, encoding="utf-8")
    if rel_path == Path("index.md"):
        # Also publish index.html at repository root for GitHub Pages
        Path("index.html").write_text(full_html, encoding="utf-8")
