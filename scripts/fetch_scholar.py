#!/usr/bin/env python3
"""
Google Scholar sync for the resume site.

Fetches the publication list for the configured Scholar author ID and merges
new papers into data/publications.js. Rules:

  - Entries with "source": "manual" are NEVER modified or removed.
  - Scholar entries are matched by normalized title; existing entries get
    missing year/venue filled in, nothing else is overwritten.
  - New Scholar papers are appended with "source": "scholar".

If Google Scholar rate-limits or captchas the runner (this happens often on
cloud IPs), the script exits non-zero and the GitHub Action simply keeps the
current data — the site never breaks. You can always add papers manually to
data/publications.js instead.

Run locally:
    pip install scholarly
    python3 scripts/fetch_scholar.py
"""

import json
import re
import sys
from pathlib import Path

SCHOLAR_AUTHOR_ID = "JNqveLcAAAAJ"

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "publications.js"

BEGIN = "window.PUBLICATIONS = "
END = ";"


def norm(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def load_entries() -> list[dict]:
    text = DATA_FILE.read_text(encoding="utf-8")
    m = re.search(re.escape(BEGIN) + r"(\[.*\])" + re.escape(END), text, re.S)
    if not m:
        raise SystemExit(f"Could not find PUBLICATIONS array in {DATA_FILE}")
    return json.loads(m.group(1))


def save_entries(entries: list[dict]) -> None:
    header = """// ============================================================================
// PUBLICATIONS DATA — this is the ONLY file you edit to update publications.
// Manual entries ("source": "manual") are never touched by the Scholar sync.
// ============================================================================

"""
    body = json.dumps(entries, indent=2, ensure_ascii=False)
    DATA_FILE.write_text(f"{header}{BEGIN}{body}{END}\n", encoding="utf-8")


def fetch_scholar() -> list[dict]:
    from scholarly import scholarly  # imported here so --help works without it

    author = scholarly.search_author_id(SCHOLAR_AUTHOR_ID)
    author = scholarly.fill(author, sections=["publications"])
    results = []
    for pub in author.get("publications", []):
        bib = pub.get("bib", {})
        title = bib.get("title", "").strip()
        if not title:
            continue
        year = bib.get("pub_year")
        venue = bib.get("venue") or bib.get("journal") or bib.get("conference") or ""
        url = pub.get("pub_url") or (
            f"https://scholar.google.com/citations?view_op=view_citation&hl=en"
            f"&user={SCHOLAR_AUTHOR_ID}&citation_for_view={pub.get('author_pub_id', '')}"
        )
        results.append({
            "title": title,
            "year": int(year) if str(year or "").isdigit() else None,
            "venue": venue,
            "url": url,
            "source": "scholar",
        })
    return results


def merge(existing: list[dict], fetched: list[dict]) -> tuple[list[dict], int]:
    by_title = {norm(e["title"]): e for e in existing}
    added = 0
    for item in fetched:
        key = norm(item["title"])
        if key in by_title:
            cur = by_title[key]
            if cur.get("year") is None and item.get("year") is not None:
                cur["year"] = item["year"]
            if not cur.get("venue") and item.get("venue"):
                cur["venue"] = item["venue"]
        else:
            existing.append(item)
            by_title[key] = item
            added += 1
    return existing, added


def main() -> int:
    try:
        fetched = fetch_scholar()
    except Exception as exc:  # Scholar blocked / network error — keep current data
        print(f"Scholar fetch failed ({type(exc).__name__}: {exc}).")
        print("Keeping existing publications.js unchanged.")
        return 1

    if not fetched:
        print("Scholar returned no publications — keeping existing data unchanged.")
        return 1

    entries = load_entries()
    entries, added = merge(entries, fetched)
    save_entries(entries)
    print(f"Done. {len(fetched)} Scholar papers checked, {added} new added, "
          f"{len(entries)} total in publications.js.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
