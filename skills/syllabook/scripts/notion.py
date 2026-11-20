#!/usr/bin/env python3
"""Converts the book to Notion's Markdown, for the copy in Notion (modes/PUBLISH.md §4).

Usage:
  python scripts/notion.py <n> [--book B]      one chapter (0 = chapter 0; the mock exam has the next number)
  python scripts/notion.py <file.md> [--book B]  a file in chapters/ without a number, such as the glossary
  python scripts/notion.py index [--book B]    the book's index page

Prints JSON with `content` (ready for the Notion page tools) and `uploads`: the images to
upload first. Each upload has a `placeholder` that appears in the content as
<image source="PLACEHOLDER">; replace it with what the Notion upload tool returns.

What changes on the way:
  <details> answers      -> <toggle> (Notion saves <details> as plain text)
  > quotes and notes     -> <callout> with the note's emoji as the icon
  SVG diagrams           -> uploads
  real photos (no spec)  -> uploads
  illustrations (PNG/JPG with a spec in img/_source/) -> left out: Notion gets the diagrams only
  links to other chapters -> plain text (the chapters are subpages in Notion)
  <!-- comments -->, navigation and the generated map -> removed
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chapter_path, fail, find_book, first_h1, labels, load_yaml, out

IMAGE = re.compile(r'^!\[([^\]]*)\]\(\.\./img/([^)\s]+)\)\s*$')
CHAPTER_LINK = re.compile(r'\[([^\]]+)\]\((?!https?:)[^)\s]+\.md(#[^)\s]*)?\)')
COMMENT = re.compile(r'<!--.*?-->', re.S)
# the emoji a note starts with picks the callout's color
CALLOUT_COLORS = {'⚠️': 'yellow_bg', '💡': 'blue_bg', '🛠️': 'green_bg', '🔥': 'orange_bg', '❌': 'red_bg',
                  '✅': 'green_bg', '🔎': 'purple_bg', '🧪': 'blue_bg', '🎯': 'purple_bg'}
EMOJI = re.compile(r'^\s*(?:\*\*)?\s*([\U0001F300-\U0001FAFF☀-➿][️‍\U0001F300-\U0001FAFF]*)')


def strip_generated(text):
    for block in ('nav', 'map', 'index', 'list'):
        text = re.sub(rf'<!-- {block}:start -->.*?<!-- {block}:end -->', '', text, flags=re.S)
    return COMMENT.sub('', text)


def kind_of_image(book_dir, name):
    """svg | photo | illustration"""
    stem, ext = os.path.splitext(name)
    if ext.lower() == '.svg':
        return 'svg'
    has_spec = glob.glob(os.path.join(book_dir, 'img', '_source', f'{os.path.basename(stem)}.*'))
    return 'illustration' if has_spec else 'photo'


def callout(lines):
    """A Markdown quote becomes a callout; its first emoji becomes the icon."""
    text = '\n'.join(re.sub(r'^>\s?', '', line) for line in lines).strip()
    m = EMOJI.match(text)
    icon = m.group(1) if m else '💬'
    if m:
        text = (text[:m.start(1)] + text[m.end(1):]).lstrip()
        text = re.sub(r'^\*\*\s+', '**', text)
    color = CALLOUT_COLORS.get(icon, 'gray_bg')
    return [f'<callout icon="{icon}" color="{color}">', text, '</callout>']


def convert(text, book_dir):
    """Returns (content, uploads, left_out)."""
    lines = strip_generated(text).splitlines()
    result, uploads, left_out = [], [], []
    i, fence = 0, None
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        # code blocks pass through untouched, whatever they contain
        if fence:
            result.append(line)
            if stripped.startswith(fence):
                fence = None
            i += 1
            continue
        m = re.match(r'^(`{3,}|~{3,})', stripped)
        if m:
            fence = m.group(1)
            result.append(line)
            i += 1
            continue
        if stripped == '<details>':
            j, summary, body = i + 1, '', []
            while j < len(lines) and lines[j].strip() != '</details>':
                s = re.match(r'^\s*<summary>(.*?)</summary>\s*$', lines[j])
                if s and not summary:
                    summary = s.group(1).strip()
                else:
                    body.append(lines[j])
                j += 1
            inner, more_uploads, more_left = convert('\n'.join(body), book_dir)
            uploads += more_uploads
            left_out += more_left
            # an answer starting with "4." would become a numbered list item
            inner = re.sub(r'^(\d+)\.(\s|$)', r'\1\\.\2', inner.strip())
            result += ['<toggle>', summary, '', inner, '</toggle>']
            i = j + 1
            continue
        if stripped.startswith('>'):
            j = i
            while j < len(lines) and lines[j].strip().startswith('>'):
                j += 1
            quoted = lines[i:j]
            # a quote holding an answer: keep the answer as a toggle after the callout
            if any('<details>' in q for q in quoted):
                plain = [re.sub(r'^\s*>\s?', '', q) for q in quoted]
                k = next(n for n, q in enumerate(plain) if q.strip() == '<details>')
                result += callout(['> ' + q for q in plain[:k] if q.strip()])
                inner, more_uploads, more_left = convert('\n'.join(plain[k:]), book_dir)
                uploads += more_uploads
                left_out += more_left
                result.append(inner.strip())
            else:
                result += callout(quoted)
            i = j
            continue
        img = IMAGE.match(stripped)
        if img:
            alt, name = img.groups()
            kind = kind_of_image(book_dir, name)
            if kind == 'illustration':
                left_out.append(name)
            else:
                placeholder = f'UPLOAD:{name}'
                uploads.append({'placeholder': placeholder, 'file': os.path.join(book_dir, 'img', name),
                                'kind': kind})
                result.append(f'<image source="{placeholder}">{alt}</image>')
            i += 1
            continue
        result.append(CHAPTER_LINK.sub(r'\1', line))
        i += 1
    content = re.sub(r'\n{3,}', '\n\n', '\n'.join(result)).strip() + '\n'
    return content, uploads, left_out


def title_of(text):
    return first_h1(text)


def site_url(repository):
    if not repository or '/' not in repository:
        return ''
    owner, name = repository.split('/', 1)
    return f'https://{owner.lower()}.github.io/{name}/'


def index_page(book_dir, data):
    """The book's index page in Notion: what it is, the links, and the chapter list."""
    from build import COLLECTIONS, epub_url, library_settings
    settings, _ = library_settings(book_dir)
    lab = labels(data.get('language', 'en'))
    repo = settings.get('repository', '')
    folder = COLLECTIONS.get(data.get('origin'), 'created-books')
    links = []
    if repo:
        site = site_url(repo)
        tree = f'https://github.com/{repo}/tree/{settings.get("branch", "main")}'
        links += [f'🌐 [{lab["Book map"]}]({site}{folder}/{data["slug"]}/)',
                  f'📂 [GitHub]({tree}/{folder}/{data["slug"]})',
                  f'📥 [{lab["Download EPUB"]}]({epub_url(settings, data["slug"])})']
    parts = []
    if data.get('subtitle'):
        parts.append(data['subtitle'])
    if links:
        parts += ['<callout icon="📚" color="blue_bg">', '\n'.join(links), '</callout>']
    parts += [f'## {lab["Chapters"]}', '']
    chapters = [f'0. {lab["How to study this book"]}'] + [f'{c["n"]}. {c["title"]}' for c in data['chapters']]
    parts += [f'- {c}' for c in chapters + [lab['Final mock exam'], lab['Glossary']]]
    return {'title': data['title'], 'content': '\n'.join(parts) + '\n', 'uploads': [], 'left_out': []}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('target', help='a chapter number, or "index"')
    p.add_argument('--book')
    args = p.parse_args()
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    if args.target == 'index':
        out(index_page(book_dir, data))
    if args.target.endswith('.md'):
        file = os.path.join(book_dir, 'chapters', os.path.basename(args.target))
        if not os.path.exists(file):
            fail(f'not found: chapters/{os.path.basename(args.target)}')
    elif args.target.isdigit():
        file = chapter_path(book_dir, int(args.target))
        if not file:
            fail(f'chapter {args.target} has no file yet')
    else:
        fail('give a chapter number, a file in chapters/ or "index"')
    text = open(file, encoding='utf-8').read()
    content, uploads, left_out = convert(text, book_dir)
    # the title becomes the Notion page title, not a heading inside the page
    title = title_of(text)
    if title and content.startswith(f'# {title}'):
        content = content[len(f'# {title}'):].lstrip('\n')
    out({'title': title_of(text), 'content': content, 'uploads': uploads, 'left_out': left_out})


if __name__ == '__main__':
    main()
