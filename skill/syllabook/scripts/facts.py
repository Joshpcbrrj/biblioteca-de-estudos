#!/usr/bin/env python3
"""Lists the sentences of a chapter that state checkable facts.

Usage:  python scripts/facts.py <n> [--book B]

A sentence is listed when it has a year or date, a number with a unit or a
percentage, a quotation, or a proper name in the middle of the sentence.
Code blocks are skipped (code is verified by running it). Check each
sentence against the sources (references/SOURCES.md §5).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chapter_path, fail, find_book, out

PATTERNS = {
    'date': re.compile(r'\b(1[0-9]{3}|20[0-9]{2})\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b'),
    # (?!\w) instead of \b: "%" is not a word character, so \b would never match after it
    'number': re.compile(r'\b\d+([.,]\d+)?\s?'
                         r'(%|por cento|percent|km|kg|mb|gb|tb|mhz|ghz|hz|v|w|ms|s|min|h|bpm|x)(?!\w)', re.I),
    'quote': re.compile(r'[“"«][^”"»]{12,}[”"»]'),
    # a capitalized word that does not start the sentence: likely a person, place or product
    'name': re.compile(r'(?<=[a-zà-ÿ,;:)] )[A-ZÀ-Ý][\w-]+'),
}
MARKUP = re.compile(r'`[^`]*`|!\[[^\]]*\]\([^)]*\)|\]\([^)]*\)|<[^>]+>|[*_#>|]')


def sentences(text):
    """Yields (line number, sentence) outside code blocks."""
    in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith('```') or line.lstrip().startswith('~~~'):
            in_code = not in_code
            continue
        # headings and table separators state no facts
        if in_code or not line.strip() or line.lstrip().startswith('#') or re.match(r'^\s*\|?[\s:|-]+\|?\s*$', line):
            continue
        # entries of the Sources list are the references themselves, not claims
        if re.match(r'^\s*[-*]\s*\[[^\]]+\]\(https?://', line):
            continue
        # each table cell starts a new sentence, so its first word is not taken for a name
        clean = MARKUP.sub(' ', line.replace('|', '. '))
        for s in re.split(r'(?<=[.!?])\s+', clean):
            s = ' '.join(s.split())
            if len(s) > 15:
                yield i, s


def main():
    p = argparse.ArgumentParser(description='List the sentences with facts to check.')
    p.add_argument('n', type=int)
    p.add_argument('--book')
    args = p.parse_args()
    book_dir, _ = find_book(args.book)
    path = chapter_path(book_dir, args.n)
    if not path:
        fail(f'chapter {args.n} has no file yet')
    found = []
    for line, s in sentences(open(path, encoding='utf-8').read()):
        kinds = [k for k, rx in PATTERNS.items() if rx.search(s)]
        if kinds:
            found.append({'line': line, 'kinds': kinds, 'sentence': s[:220]})
    out({'chapter': args.n, 'to_check': len(found), 'sentences': found})


if __name__ == '__main__':
    main()
