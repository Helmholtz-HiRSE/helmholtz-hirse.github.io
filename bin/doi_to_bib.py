#!/usr/bin/env python3
"""
Add new entries to _bibliography/rse_publications.bib from DOIs or arXiv IDs.

Usage:
    python bin/doi_to_bib.py --input "10.1145/3194747.3194749 2301.12345"

Supported identifier formats:
    - Bare DOI:       10.1145/3194747.3194749
    - DOI URL:        https://doi.org/10.1145/3194747.3194749
    - arXiv new-style: 2301.12345  or  2301.12345v2
    - arXiv old-style: cs.LG/0601001
    - arXiv URL:      https://arxiv.org/abs/2301.12345

The script appends new BibTeX entries to the bibliography file and prints a
summary suitable for posting as a GitHub issue comment.
"""

import argparse
import os
import re
import sys

import bibtexparser
import requests
from bibtexparser.bibdatabase import BibDatabase
from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import BibTexWriter


BIB_FILE = os.path.join(
    os.path.dirname(__file__), '..', '_bibliography', 'rse_publications.bib'
)

# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------
# A DOI always starts with "10." followed by a registrant code and a suffix.
_DOI_BARE = re.compile(
    r'(?<!\w)(10\.\d{4,}(?:\.\d+)*/[^\s,;?&#>\])"\']+)',
)
_DOI_URL = re.compile(
    r'https?://(?:dx\.)?doi\.org/(10\.\d{4,}(?:\.\d+)*/[^\s,;?&#>\])"\']+)',
)

# arXiv identifiers
_ARXIV_URL = re.compile(
    r'https?://(?:www\.)?arxiv\.org/(?:abs|pdf)/([^\s,;>\])"\']+)',
)
_ARXIV_NEW = re.compile(r'(?<![:/\w])(\d{4}\.\d{4,5}(?:v\d+)?)(?!\d)')
_ARXIV_OLD = re.compile(r'(?<![:/\w])([a-zA-Z-]+(?:\.[A-Z]{2})?/\d{7})(?!\d)')


# ---------------------------------------------------------------------------
# Identifier extraction
# ---------------------------------------------------------------------------

def _strip_arxiv_version(arxiv_id: str) -> str:
    return re.sub(r'v\d+$', '', arxiv_id.strip())


def extract_identifiers(text: str) -> list:
    """
    Return a list of (kind, identifier) tuples found in *text*.

    *kind* is either ``'doi'`` or ``'arxiv'``.  Duplicates are removed.
    DOI URLs and arXiv URLs are processed first so that the "10." pattern
    inside a doi.org URL is not double-counted.
    """
    seen: set = set()
    result: list = []

    def _add(kind, value):
        value = value.rstrip('.,;)')
        if value not in seen:
            seen.add(value)
            result.append((kind, value))

    # 1. DOI URLs: https://doi.org/10.xxx/yyy
    for m in _DOI_URL.finditer(text):
        _add('doi', m.group(1))

    # 2. arXiv URLs: https://arxiv.org/abs/XXXXXXX
    for m in _ARXIV_URL.finditer(text):
        _add('arxiv', _strip_arxiv_version(m.group(1)))

    # 3. Bare DOIs (not already matched as part of a doi.org URL)
    for m in _DOI_BARE.finditer(text):
        doi = m.group(1)
        # Skip if this DOI was already captured via a doi.org URL
        if doi not in seen:
            _add('doi', doi)

    # 4. Bare new-style arXiv IDs: YYMM.NNNNN[vN]
    for m in _ARXIV_NEW.finditer(text):
        _add('arxiv', _strip_arxiv_version(m.group(1)))

    # 5. Bare old-style arXiv IDs: category/NNNNNNN
    for m in _ARXIV_OLD.finditer(text):
        _add('arxiv', m.group(1))

    return result


# ---------------------------------------------------------------------------
# BibTeX key generation
# ---------------------------------------------------------------------------

def _sanitize_name(name: str) -> str:
    """Keep only ASCII letters from a surname."""
    return re.sub(r'[^A-Za-z]', '', name)


def make_unique_key(last_name: str, year: str, existing: dict) -> str:
    """Return a BibTeX key not yet present in *existing*."""
    base = f"{_sanitize_name(last_name)}_{year}"
    if base not in existing:
        return base
    for letter in 'bcdefghijklmnopqrstuvwxyz':
        candidate = base + letter
        if candidate not in existing:
            return candidate
    # Very unlikely fallback
    return base + '_new'


# ---------------------------------------------------------------------------
# Duplicate detection helpers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lower-case, remove non-alphanumeric chars for fuzzy comparison."""
    return re.sub(r'[^a-z0-9]', '', text.lower())


def _doi_exists(doi: str, db: bibtexparser.bibdatabase.BibDatabase) -> bool:
    doi_norm = _normalize(doi)
    for entry in db.entries:
        if _normalize(entry.get('doi', '')) == doi_norm:
            return True
    return False


def _arxiv_exists(arxiv_id: str, db: bibtexparser.bibdatabase.BibDatabase) -> bool:
    arxiv_norm = _normalize(arxiv_id)
    for entry in db.entries:
        eprint = _normalize(entry.get('eprint', ''))
        url = _normalize(entry.get('url', ''))
        if arxiv_norm and (arxiv_norm == eprint or arxiv_norm in url):
            return True
    return False


# ---------------------------------------------------------------------------
# Fetchers
# ---------------------------------------------------------------------------

def fetch_doi(doi: str, db: bibtexparser.bibdatabase.BibDatabase) -> tuple:
    """
    Fetch a BibTeX entry for *doi* via doi.org content negotiation.

    Returns ``(entry_dict, message)`` where *entry_dict* is ``None`` if
    the entry could not be fetched or is a duplicate.
    """
    if _doi_exists(doi, db):
        return None, f"⚠️ **{doi}** — already in the bibliography (duplicate DOI), skipped."

    url = f"https://doi.org/{doi}"
    try:
        resp = requests.get(
            url,
            headers={'Accept': 'application/x-bibtex'},
            timeout=30,
            allow_redirects=True,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        return None, f"❌ **{doi}** — could not fetch from doi.org: {exc}"

    raw_bib = resp.text.strip()
    if not raw_bib or not raw_bib.startswith('@'):
        return None, f"❌ **{doi}** — doi.org did not return valid BibTeX."

    try:
        parsed = bibtexparser.loads(raw_bib)
    except Exception as exc:
        return None, f"❌ **{doi}** — failed to parse the returned BibTeX: {exc}"

    if not parsed.entries:
        return None, f"❌ **{doi}** — BibTeX parsed but contained no entries."

    entry = parsed.entries[0]

    # Always set the DOI field (doi.org sometimes omits it)
    entry.setdefault('doi', doi)

    # Generate a key
    authors_raw = entry.get('author', '')
    first_author_last = _first_author_last(authors_raw)
    year = entry.get('year', '0000')
    entry['ID'] = make_unique_key(first_author_last, year, db.get_entry_dict())

    title = entry.get('title', doi)
    return entry, f"✅ **{doi}** — added as `{entry['ID']}`: _{title}_"


def fetch_arxiv(arxiv_id: str, db: bibtexparser.bibdatabase.BibDatabase) -> tuple:
    """
    Fetch metadata for *arxiv_id* using the arxiv Python library.

    Returns ``(entry_dict, message)``.
    """
    if _arxiv_exists(arxiv_id, db):
        return None, f"⚠️ **{arxiv_id}** — already in the bibliography (duplicate arXiv ID), skipped."

    try:
        import arxiv  # noqa: PLC0415 — optional dependency
    except ImportError:
        return None, "❌ The `arxiv` Python package is not installed. Run: pip install arxiv"

    client = arxiv.Client()
    search = arxiv.Search(id_list=[arxiv_id])
    try:
        results = list(client.results(search))
    except Exception as exc:
        return None, f"❌ **{arxiv_id}** — arXiv API error: {exc}"

    if not results:
        return None, f"❌ **{arxiv_id}** — not found on arXiv."

    paper = results[0]
    authors = paper.authors
    year = str(paper.published.year)

    if len(authors) > 1:
        first_author_last = authors[0].name.split()[-1]
        author_str = " and ".join(a.name for a in authors)
    else:
        first_author_last = authors[0].name.split()[-1]
        author_str = authors[0].name

    # Canonical arXiv ID without version
    canonical_id = _strip_arxiv_version(paper.entry_id.split('/')[-1])

    existing = db.get_entry_dict()
    bib_key = make_unique_key(first_author_last, year, existing)

    entry = {
        'ENTRYTYPE': 'misc',
        'ID': bib_key,
        'author': author_str,
        'title': paper.title.replace('\n', ' ').strip(),
        'year': year,
        'eprint': canonical_id,
        'archivePrefix': 'arXiv',
        'primaryClass': paper.primary_category,
        'url': f"https://arxiv.org/abs/{canonical_id}",
        'abstract': paper.summary.replace('\n', ' ').strip(),
    }

    title = entry['title']
    return entry, f"✅ **arXiv:{arxiv_id}** — added as `{bib_key}`: _{title}_"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _first_author_last(authors_raw: str) -> str:
    """Extract the last name of the first author from a BibTeX author string."""
    if not authors_raw:
        return 'Unknown'
    first = re.split(r'\s+and\s+', authors_raw, maxsplit=1)[0].strip()
    if ',' in first:
        # "Last, First" format
        return first.split(',', 1)[0].strip()
    # "First Last" format — take the last token
    parts = first.split()
    return parts[-1] if parts else 'Unknown'


def load_bib(bib_path: str) -> bibtexparser.bibdatabase.BibDatabase:
    parser = BibTexParser(common_strings=True)
    with open(bib_path, encoding='utf-8') as f:
        return bibtexparser.load(f, parser=parser)


def write_bib(new_entries: list, bib_path: str) -> None:
    """Append *new_entries* to the BibTeX file without touching existing content."""
    mini_db = BibDatabase()
    mini_db.entries = new_entries
    writer = BibTexWriter()
    writer.indent = '  '
    writer.add_trailing_comma = True
    writer.order_entries_by = None
    new_text = writer.write(mini_db)
    with open(bib_path, 'a', encoding='utf-8') as f:
        f.write(new_text)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Add bibliography entries from DOIs or arXiv IDs.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Free-form text containing DOIs and/or arXiv IDs.',
    )
    parser.add_argument(
        '--bib', '-b',
        default=os.path.abspath(BIB_FILE),
        help='Path to the BibTeX file (default: _bibliography/rse_publications.bib).',
    )
    args = parser.parse_args()

    bib_path = os.path.abspath(args.bib)
    if not os.path.exists(bib_path):
        print(f"ERROR: BibTeX file not found: {bib_path}", file=sys.stderr)
        sys.exit(1)

    identifiers = extract_identifiers(args.input)
    if not identifiers:
        print(
            "I could not find any DOIs or arXiv IDs in the text you provided.\n\n"
            "Supported formats:\n"
            "  - DOI (bare):    10.1145/3194747.3194749\n"
            "  - DOI (URL):     https://doi.org/10.1145/3194747.3194749\n"
            "  - arXiv (bare):  2301.12345  or  2301.12345v2\n"
            "  - arXiv (URL):   https://arxiv.org/abs/2301.12345\n"
        )
        return

    db = load_bib(bib_path)
    messages = []
    new_entries = []

    for kind, identifier in identifiers:
        print(f"Processing {kind}: {identifier} …", file=sys.stderr)
        if kind == 'doi':
            entry, msg = fetch_doi(identifier, db)
        else:
            entry, msg = fetch_arxiv(identifier, db)

        messages.append(msg)

        if entry is not None:
            db.entries.append(entry)
            new_entries.append(entry)

    if new_entries:
        write_bib(new_entries, bib_path)
        print(f"Added {len(new_entries)} new entry/entries to {bib_path}", file=sys.stderr)

    # Print the summary (captured by the workflow as the issue comment)
    summary_lines = [
        f"### 🤖 bibbot summary\n",
        f"Processed {len(identifiers)} identifier(s), added {len(new_entries)} new entry/entries.\n",
    ]
    summary_lines.extend(f"- {msg}" for msg in messages)
    print('\n'.join(summary_lines))


if __name__ == '__main__':
    main()
