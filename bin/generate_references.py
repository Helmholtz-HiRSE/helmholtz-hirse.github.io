#!/usr/bin/env python3
"""
Generate _data/references.yml from _bibliography/rse_publications.bib.

Usage:
    python bin/generate_references.py

The script reads the BibTeX file, parses all entries, and writes a YAML file
that Jekyll can consume via site.data.references.

Entries are sorted by year (descending), then by first author (ascending).
"""

import os
import re
import sys

import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import yaml


BIB_FILE = os.path.join(os.path.dirname(__file__), '..', '_bibliography', 'rse_publications.bib')
YAML_FILE = os.path.join(os.path.dirname(__file__), '..', '_data', 'references.yml')
ASSETS_BIB_COPY = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data', 'rse_publications.bib')


def clean_latex(text):
    """Convert LaTeX markup to HTML for web rendering."""
    if not text:
        return text

    # Step 1: Handle LaTeX commands WITH braced arguments (before brace stripping).
    # \textsuperscript{x} -> <sup>x</sup>
    text = re.sub(r'\\textsuperscript\{([^}]*)\}', r'<sup>\1</sup>', text)
    # \emph{x}, \textit{x}, \textsl{x} -> <em>x</em>
    text = re.sub(r'\\(?:emph|textit|textsl)\{([^}]*)\}', r'<em>\1</em>', text)
    # \textbf{x} -> <strong>x</strong>
    text = re.sub(r'\\textbf\{([^}]*)\}', r'<strong>\1</strong>', text)

    # Step 2: Strip remaining braces used for case protection (e.g. {Germany} -> Germany).
    text = re.sub(r'\{([^}]*)\}', r'\1', text)

    # Step 3: Handle malformed ordinal patterns that lost their braces.
    # e.g. N{\textbackslash}textbackslashtextsuperscriptth -> N\textbackslashtextsuperscriptth
    text = re.sub(
        r'\\textbackslashtextsuperscript(st|nd|rd|th)\b',
        r'<sup>\1</sup>', text, flags=re.IGNORECASE,
    )
    # e.g. N{\textbackslash}textsuperscriptth -> N\textsuperscriptth
    text = re.sub(
        r'\\textsuperscript(st|nd|rd|th)\b',
        r'<sup>\1</sup>', text, flags=re.IGNORECASE,
    )

    # Step 4: Handle display commands without a braced argument (malformed BibTeX).
    # \emphWORD -> <em>WORD</em>  (e.g. \emphnpm, \emphThe)
    text = re.sub(r'\\(?:emph|textit|textsl)(\w+)', r'<em>\1</em>', text)
    # \textbfWORD -> <strong>WORD</strong>
    text = re.sub(r'\\textbf(\w+)', r'<strong>\1</strong>', text)

    # Step 5: Remove remaining LaTeX commands.
    text = re.sub(r'\\textbackslash\b', '', text)
    # \command{text} -> text (any remaining braced command)
    text = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', text)
    # \command -> remove (standalone commands without argument)
    text = re.sub(r'\\[a-zA-Z@]+\b', '', text)
    # Stray backslash sequences (e.g. \\ or \160)
    text = re.sub(r'\\+\S*', '', text)

    # Step 6: Normalize whitespace.
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_authors(author_field):
    """Split an author field into a list of author name strings."""
    if not author_field:
        return []
    # Authors are separated by ' and '
    authors = [a.strip() for a in re.split(r'\s+and\s+', author_field)]
    cleaned = []
    for author in authors:
        # Handle "Last, First" → "First Last"
        if ',' in author:
            parts = [p.strip() for p in author.split(',', 1)]
            author = f"{parts[1]} {parts[0]}"
        cleaned.append(clean_latex(author))
    return cleaned


def entry_to_dict(entry):
    """Convert a bibtexparser entry dict to a clean dict for YAML output."""
    def get(field):
        return clean_latex(entry.get(field, '').strip())

    authors = parse_authors(get('author'))
    year_str = get('year')
    try:
        year = int(year_str)
    except ValueError:
        year = 0

    result = {
        'id': entry.get('ID', ''),
        'type': entry.get('ENTRYTYPE', 'misc'),
        'authors': authors,
        'title': get('title'),
        'year': year,
    }

    # Venue: journal for articles, booktitle for inproceedings/incollection
    journal = get('journal')
    booktitle = get('booktitle')
    if journal:
        result['journal'] = journal
    if booktitle:
        result['booktitle'] = booktitle

    # Optional fields
    for field in ('volume', 'number', 'pages', 'doi', 'url', 'abstract', 'publisher', 'address'):
        value = get(field)
        if value:
            result[field] = value

    return result


def main():
    bib_path = os.path.abspath(BIB_FILE)
    yaml_path = os.path.abspath(YAML_FILE)

    if not os.path.exists(bib_path):
        print(f"ERROR: BibTeX file not found: {bib_path}", file=sys.stderr)
        sys.exit(1)

    parser = BibTexParser(common_strings=True)
    parser.customization = convert_to_unicode

    with open(bib_path, encoding='utf-8') as f:
        bib_database = bibtexparser.load(f, parser=parser)

    entries = [entry_to_dict(e) for e in bib_database.entries]

    # Sort: descending year, then ascending first author
    entries.sort(key=lambda e: (-e['year'], (e['authors'][0] if e['authors'] else '')))

    os.makedirs(os.path.dirname(yaml_path), exist_ok=True)
    with open(yaml_path, 'w', encoding='utf-8') as f:
        f.write("# Auto-generated by bin/generate_references.py — do not edit manually.\n")
        f.write("# Run: python bin/generate_references.py\n")
        yaml.dump(entries, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"Written {len(entries)} entries to {yaml_path}")

    # Keep the publicly served copy in sync so the download link works
    import shutil
    assets_bib_path = os.path.abspath(ASSETS_BIB_COPY)
    os.makedirs(os.path.dirname(assets_bib_path), exist_ok=True)
    shutil.copy2(bib_path, assets_bib_path)
    print(f"Copied bib file to {assets_bib_path}")


if __name__ == '__main__':
    main()
