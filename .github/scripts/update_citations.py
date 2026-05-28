#!/usr/bin/env python3
"""Fetch citation counts from Google Scholar and update index.html."""
import re
import sys

SCHOLAR_ID = "0O-NG5YAAAAJ"
BAYESPRISM_KEYWORD = "bayesprism"


def get_author_data():
    from scholarly import scholarly
    author = scholarly.search_author_id(SCHOLAR_ID)
    scholarly.fill(author, sections=["basics", "publications"])
    return author


def get_citations(author):
    return int(author.get("citedby", 0))


def get_bayesprism_citations(author):
    for pub in author.get("publications", []):
        title = pub.get("bib", {}).get("title", "").lower()
        if BAYESPRISM_KEYWORD in title:
            try:
                from scholarly import scholarly
                filled = scholarly.fill(pub)
                return int(filled.get("num_citations", 0))
            except Exception as e:
                print(f"Could not fill BayesPrism pub: {e}", file=sys.stderr)
                return int(pub.get("num_citations", 0))
    print("BayesPrism publication not found in author list.", file=sys.stderr)
    return None


def update_html(total_citations, bayesprism_citations):
    path = "index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    changed = False

    pattern1 = r'(<div class="font-display text-2xl font-bold text-indigo-400">)([\d,]+)(</div>\s*\n\s*<div class="text-xs text-slate-500 mt-0\.5">Citations)'
    new_content, n = re.subn(pattern1, rf'\g<1>{total_citations:,}\3', content)
    if n == 0:
        print("Total-citations pattern not found.", file=sys.stderr)
    elif new_content != content:
        print(f"Updated total citations to {total_citations:,}.")
        changed = True
    content = new_content

    if bayesprism_citations is not None:
        pattern2 = r'(<span class="bayesprism-citations">)([\d,]+)(</span>)'
        new_content, n = re.subn(pattern2, rf'\g<1>{bayesprism_citations:,}\3', content)
        if n == 0:
            print("BayesPrism-citations span not found.", file=sys.stderr)
        elif new_content != content:
            print(f"Updated BayesPrism citations to {bayesprism_citations:,}.")
            changed = True
        content = new_content

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    return changed


if __name__ == "__main__":
    try:
        author = get_author_data()
        total = get_citations(author)
        bp = get_bayesprism_citations(author)
        print(f"Total citations: {total}, BayesPrism: {bp}")
        update_html(total, bp)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(0)
