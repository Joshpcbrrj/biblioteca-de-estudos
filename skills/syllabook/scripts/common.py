"""Shared helpers for the Syllabook scripts.

Finding the book: every script accepts `--book <folder or book.yaml>`. Without it,
it uses the SYLLABOOK_BOOK environment variable, then the current folder if it
holds a book.yaml, then the book selected by the last successful
`book.py validate` (saved in ~/.syllabook/current, or SYLLABOOK_STATE).
"""
import glob
import json
import os
import re
import subprocess
import sys
import unicodedata

# JSON output carries emoji and accents; Windows consoles default to another encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATE = os.environ.get('SYLLABOOK_STATE') or os.path.join(os.path.expanduser('~'), '.syllabook', 'current')

# limits per reading profile (references/VISUALS.md §3)
READING = {'large': {'code': 80, 'columns': 6}, 'small': {'code': 60, 'columns': 4}}


def need_yaml():
    try:
        import yaml
    except ImportError:
        # the claude.ai sandbox can install from PyPI; quiet so the output stays short
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pyyaml'], check=True)
        import yaml
    return yaml


def load_yaml(path):
    with open(path, encoding='utf-8') as f:
        return need_yaml().safe_load(f) or {}


def save_yaml(path, data):
    text = need_yaml().safe_dump(data, allow_unicode=True, sort_keys=False, width=100)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def out(obj, code=0):
    print(json.dumps(obj, ensure_ascii=False, indent=1))
    sys.exit(code)


def fail(message):
    out({'ok': False, 'error': message}, 1)


def slugify(text, limit=48):
    ascii_text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode()
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_text.lower()).strip('-')
    if len(slug) > limit:
        # cut at a word boundary so file names stay readable
        slug = slug[:limit].rsplit('-', 1)[0]
    return slug


def labels(language):
    """Fixed labels of a book language, read from references/style/<language>.md."""
    def parse(lang):
        path = os.path.join(SKILL, 'references', 'style', f'{lang}.md')
        if not os.path.exists(path):
            return None
        text = open(path, encoding='utf-8').read().split('## Fixed labels', 1)[-1]
        rows = re.findall(r'^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$', text, re.M)
        return {part: label for part, label in rows if part not in ('Part', '---')}
    found = parse(language) or parse(language.split('-')[0])
    return found or parse('en')


def remember(book_yaml):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, 'w', encoding='utf-8') as f:
        f.write(os.path.abspath(book_yaml))


def find_book(arg=None):
    """Returns (book folder, book.yaml path) or stops with an error."""
    candidates = [arg, os.environ.get('SYLLABOOK_BOOK'), os.getcwd()]
    if os.path.exists(STATE):
        candidates.append(open(STATE, encoding='utf-8').read().strip())
    for c in candidates:
        if not c:
            continue
        path = c if c.endswith('.yaml') else os.path.join(c, 'book.yaml')
        if os.path.exists(path):
            return os.path.dirname(os.path.abspath(path)), os.path.abspath(path)
    fail('book not found: pass --book <folder>, or run "book.py validate <book.yaml>" first')


def chapter_path(book_dir, n):
    found = sorted(glob.glob(os.path.join(book_dir, 'chapters', f'{n:02d}-*.md')))
    return found[0] if found else None


def chapter_numbers(data):
    return [c['n'] for c in data.get('chapters', []) if isinstance(c, dict) and 'n' in c]
