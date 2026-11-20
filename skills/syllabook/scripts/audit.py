#!/usr/bin/env python3
"""Ready criteria for a chapter or the whole book.

Usage:
  python scripts/audit.py <n> [--book B]   one chapter
  python scripts/audit.py [--book B]       the whole book (chapters, fixed parts, images)

Errors block (`ready: false`, exit code 1). Warnings are allowed, but go to the
final summary with the reason. Limits follow the reading profile in book.yaml.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import READING, chapter_numbers, chapter_path, find_book, labels, load_yaml, out, slugify

# blocks that hold program output or data, not code: no comment required
NO_COMMENT_LANGS = {'', 'text', 'txt', 'output', 'console', 'plaintext', 'json', 'csv', 'markdown', 'md', 'diff'}
COMMENT = re.compile(r'^\s*(#|//|--|/\*|\*|<!--|;|%|\'|rem\b)', re.I)
FILLER = {
    'en': r'\b(?:simply|just|obviously|basically)\b',
    'pt': r'\b(?:simplesmente|obviamente|basicamente|é só)\b',
    'es': r'\b(?:simplemente|obviamente|básicamente)\b',
}
IMAGE = re.compile(r'!\[([^\]]*)\]\(([^)\s]+)\)')
LINK = re.compile(r'(?<!!)\[[^\]]*\]\(([^)\s#]+\.md)(#[^)]*)?\)')


def audit_chapter(path, n, lab, limits, language, errors, warnings):
    name = os.path.basename(path)
    text = open(path, encoding='utf-8').read()
    lines = text.splitlines()

    def where(i):
        return f'{name}:{i}'

    if '<!-- TODO' in text:
        errors.append(f'{name}: {text.count("<!-- TODO")} TODO placeholder(s) left')
    required = ['In this chapter', 'Practice', 'Quick review', 'Summary', 'Sources']
    if n > 1:
        required.append('Where we left off')
    for part in required:
        if lab[part] not in text:
            errors.append(f'{name}: missing section "{lab[part]}"')

    in_code, lang, start, commented = False, '', 0, False
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith('```'):
            if not in_code:
                in_code, lang, start, commented = True, stripped[3:].strip().lower(), i, False
            else:
                size = i - start - 1
                if lang not in NO_COMMENT_LANGS and size >= 4 and not commented:
                    errors.append(f'{where(start)}: {lang} block with {size} lines and no comment explaining why')
                in_code = False
            continue
        if in_code:
            if COMMENT.match(line) or re.search(r'\s(#|//|--)\s', line):
                commented = True
            if len(line) > limits['code']:
                # real output, URLs and long unbreakable tokens cannot be wrapped honestly
                unbreakable = lang in NO_COMMENT_LANGS or '://' in line or max(map(len, line.split() or [''])) >= 40
                (warnings if unbreakable else errors).append(
                    f'{where(i)}: line with {len(line)} characters (limit {limits["code"]})')
            continue
        if stripped.startswith('<summary>') or stripped.lstrip('> ').startswith('<summary>'):
            if i < len(lines) and lines[i].lstrip('> ').strip():
                errors.append(f'{where(i)}: blank line needed after <summary>')
        if stripped.lstrip('> ') == '</details>' and i > 1 and lines[i - 2].lstrip('> ').strip():
            errors.append(f'{where(i)}: blank line needed before </details>')
        if stripped.startswith('|') and i < len(lines) and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i]):
            cols = len(re.findall(r'(?<!\\)\|', stripped)) - 1
            if cols > limits['columns']:
                warnings.append(f'{where(i)}: table with {cols} columns (limit {limits["columns"]})')
        for alt, target in IMAGE.findall(line):
            if not alt.strip():
                errors.append(f'{where(i)}: image without alt text ({target})')
            if not target.startswith('http') and not os.path.exists(os.path.join(os.path.dirname(path), target)):
                errors.append(f'{where(i)}: image not found ({target})')
        for target, _ in LINK.findall(line):
            if not target.startswith('http') and not os.path.exists(os.path.join(os.path.dirname(path), target)):
                errors.append(f'{where(i)}: link to a missing file ({target})')
        filler = FILLER.get(language.split('-')[0])
        if filler:
            prose = re.sub(r'`[^`]*`', '', line)
            for word in re.findall(filler, prose, re.I):
                warnings.append(f'{where(i)}: filler word "{word}"')
    if in_code:
        errors.append(f'{where(start)}: code block never closed')

    heading = re.search(rf'^##\s.*{re.escape(lab["Sources"])}.*$', text, re.M)
    sources = text[heading.end():].split('\n## ', 1)[0] if heading else ''
    if heading and 'http' not in sources:
        warnings.append(f'{name}: "{lab["Sources"]}" has no link')
    return re.findall(r'\]\(\.\./img/([^)\s]+)\)', text)


def main():
    p = argparse.ArgumentParser(description='Ready criteria for a chapter or the whole book.')
    p.add_argument('n', type=int, nargs='?')
    p.add_argument('--book')
    args = p.parse_args()
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    language = data.get('language', 'en')
    lab = labels(language)
    limits = READING[(data.get('choices') or {}).get('reading', 'large')]
    errors, warnings, used = [], [], set()

    numbers = [args.n] if args.n else chapter_numbers(data)
    for n in numbers:
        file = chapter_path(book_dir, n)
        if not file:
            errors.append(f'chapter {n}: file missing')
            continue
        used.update(audit_chapter(file, n, lab, limits, language, errors, warnings))
        ch = next((c for c in data['chapters'] if c['n'] == n), {})
        if data.get('origin') == 'improved' and not ch.get('sources_original'):
            errors.append(f'chapter {n}: does not say where it comes from in the original (sources_original)')

    if not args.n:
        files = [os.path.basename(f) for f in glob.glob(os.path.join(book_dir, 'chapters', '*.md'))]
        fixed = {'chapter 0': [f for f in files if f.startswith('00-')],
                 lab['Final mock exam']: [f for f in files if slugify(lab['Final mock exam']) in f],
                 lab['Glossary']: [f for f in files if slugify(lab['Glossary']) in f]}
        for part, found in fixed.items():
            if not found:
                errors.append(f'fixed part missing: {part}')
            else:
                text = open(os.path.join(book_dir, 'chapters', found[0]), encoding='utf-8').read()
                if '<!-- TODO' in text:
                    errors.append(f'{found[0]}: TODO placeholder(s) left')
                used.update(re.findall(r'\]\(\.\./img/([^)\s]+)\)', text))
        if not os.path.exists(os.path.join(book_dir, 'README.md')):
            errors.append('README.md missing (the book front page)')
        img = os.path.join(book_dir, 'img')
        if os.path.isdir(img):
            existing = {os.path.relpath(f, img).replace(os.sep, '/')
                        for f in glob.glob(os.path.join(img, '**', '*'), recursive=True)
                        if os.path.isfile(f) and '_source' not in f and not f.endswith('CREDITS.md')}
            for orphan in sorted(existing - used):
                warnings.append(f'image not used in any chapter: img/{orphan}')

    out({'scope': f'chapter {args.n}' if args.n else 'whole book', 'ready': not errors,
         'errors': errors, 'warnings': warnings}, 0 if not errors else 1)


if __name__ == '__main__':
    main()
