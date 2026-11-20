#!/usr/bin/env python3
"""Keeps the Portuguese pages in sync with the English ones.

Every `page.pt-BR.md` starts with a line
`<!-- translation-of: page.md sha256:<12 hex digits> -->`
holding the hash of the English page it translates. When the English page
changes, the hash no longer matches and `check` reports the page as outdated.

Usage:
  python tools/translation.py check              # missing, outdated or orphan translations
  python tools/translation.py stamp <file> ...   # after translating, record the current hash

Exit code 1 when `check` finds a problem.
"""
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = re.compile(r'^<!-- translation-of: (\S+) sha256:([0-9a-f]{12}) -->\n')
# English pages that have no Portuguese version on purpose
EXEMPT_FILES = {'CHANGELOG.md', '.github/PULL_REQUEST_TEMPLATE.md',
                'skills/syllabook/assets/library/README.md'}  # a note for Claude, not a page
# folders whose pages are internal or English-only (the skill is written for Claude)
EXEMPT_DIRS = ('plano/', 'skills/syllabook/modes/', 'skills/syllabook/references/', '.github/', 'tests/')
# inside the skill, only the library skeleton is user-facing
SKILL_USER_FACING = 'skills/syllabook/assets/library/'


def digest(path):
    # normalize line endings so Windows and Linux checkouts give the same hash
    data = open(path, 'rb').read().replace(b'\r\n', b'\n')
    return hashlib.sha256(data).hexdigest()[:12]


def english_pages(root=ROOT):
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.') or d == '.github']
        for name in files:
            rel = os.path.relpath(os.path.join(base, name), root).replace(os.sep, '/')
            if not name.endswith('.md') or name.endswith('.pt-BR.md') or rel in EXEMPT_FILES:
                continue
            if rel.startswith(EXEMPT_DIRS):
                continue
            if rel.startswith('skills/') and not rel.startswith(SKILL_USER_FACING):
                continue
            yield rel


def translation_of(rel):
    return rel[:-3] + '.pt-BR.md'


def check(root=ROOT):
    problems = []
    for rel in sorted(english_pages(root)):
        pt = translation_of(rel)
        pt_path = os.path.join(root, pt)
        if not os.path.exists(pt_path):
            problems.append(f'missing: {pt}')
            continue
        m = MARK.match(open(pt_path, encoding='utf-8').read())
        if not m:
            problems.append(f'no translation-of line: {pt}')
        elif m.group(1) != os.path.basename(rel):
            problems.append(f'points to {m.group(1)} instead of {os.path.basename(rel)}: {pt}')
        elif m.group(2) != digest(os.path.join(root, rel)):
            problems.append(f'outdated (English page changed): {pt}')
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for name in files:
            if name.endswith('.pt-BR.md'):
                rel = os.path.relpath(os.path.join(base, name), root).replace(os.sep, '/')
                if not os.path.exists(os.path.join(root, rel.replace('.pt-BR.md', '.md'))):
                    problems.append(f'orphan (no English page): {rel}')
    return problems


def stamp(paths):
    for pt in paths:
        if not pt.endswith('.pt-BR.md'):
            sys.exit(f'not a Portuguese page: {pt}')
        en = pt[:-len('.pt-BR.md')] + '.md'
        if not os.path.exists(en):
            sys.exit(f'English page not found: {en}')
        text = MARK.sub('', open(pt, encoding='utf-8').read(), count=1)
        line = f'<!-- translation-of: {os.path.basename(en)} sha256:{digest(en)} -->\n'
        open(pt, 'w', encoding='utf-8', newline='\n').write(line + text)
        print(f'stamped: {pt}')


if __name__ == '__main__':
    if sys.argv[1:2] == ['check']:
        found = check()
        print('\n'.join(found) if found else 'translations: all up to date')
        sys.exit(1 if found else 0)
    if sys.argv[1:2] == ['stamp'] and sys.argv[2:]:
        stamp(sys.argv[2:])
        sys.exit(0)
    print(__doc__)
    sys.exit(2)
