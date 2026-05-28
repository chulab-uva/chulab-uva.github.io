#!/usr/bin/env python3
"""Fetch citation count from Google Scholar and update index.html."""
import re
import sys

SCHOLAR_ID = "0O-NG5YAAAAJ"

def get_citations():
    try:
        from scholarly import scholarly
        author = scholarly.search_author_id(SCHOLAR_ID)
        scholarly.fill(author, sections=["basics"])
        return int(author.get("citedby", 0))
    except Exception as e:
        print(f"scholarly failed: {e}", file=sys.stderr)
        return None

def update_html(citations):
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match the citations stat card value
    pattern = r'(<div class="font-display text-2xl font-bold text-indigo-400">)([\d,]+)(</div>\s*\n\s*<div class="text-xs text-slate-500 mt-0\.5">Citations)'
    replacement = rf'\g<1>{citations:,}\3'
    new_content, count = re.subn(pattern, replacement, content)

    if count == 0:
        print("Pattern not found in index.html — skipping update.", file=sys.stderr)
        return False

    if new_content == content:
        print(f"Citations already up to date ({citations:,}).")
        return False

    with open(path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Updated citations to {citations:,}.")
    return True

if __name__ == "__main__":
    citations = get_citations()
    if citations is None:
        print("Could not retrieve citation count — skipping.")
        sys.exit(0)  # Don't fail CI
    update_html(citations)
