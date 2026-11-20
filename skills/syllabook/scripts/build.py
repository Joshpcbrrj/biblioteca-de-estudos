#!/usr/bin/env python3
"""Builds a book (navigation, map, index, EPUB, zip) and the library (lists, website source).

Usage:
  python scripts/build.py [--book B] [--out DIR] [--partial] [--no-epub] [--no-zip]
      navigation between chapters, the map in the book's README, the concept index
      in the glossary, the EPUB (answers moved to an appendix) and the zip(s)
  python scripts/build.py lists --library ROOT
      the book lists in the READMEs of created-books/ and improved-materials/
  python scripts/build.py site --library ROOT --out DIR
      the website source for Zensical (mkdocs.yml + docs/), answers as collapsible blocks

--out defaults to ./dist (on claude.ai, use /mnt/user-data/outputs).
--partial packs what exists so far, without the EPUB: a checkpoint when GitHub is not connected.
Zips above 100 files are split into parts: GitHub's website uploads at most 100 files at a time.
"""
import argparse
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (SKILL, chapter_numbers, chapter_path, fail, find_book, labels, load_yaml, need_yaml,
                    out, slugify)

COLLECTIONS = {'created': 'created-books', 'improved': 'improved-materials'}
GITHUB_UPLOAD_LIMIT = 100  # files per upload on GitHub's website
LINK_MD = re.compile(r'\]\((?!https?:)([^)#\s]+\.md)(#[^)\s]+)?\)')
DETAILS_OPEN = re.compile(r'^\s*<details>\s*$')
SUMMARY = re.compile(r'^\s*<summary>(.*?)</summary>\s*$')


# ---------- small helpers ----------

def read(path):
    return open(path, encoding='utf-8').read()


def write(path, text):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def set_block(text, name, content):
    """Replaces the text between <!-- name:start --> and <!-- name:end -->, or appends it."""
    block = f'<!-- {name}:start -->\n{content.strip()}\n<!-- {name}:end -->'
    pattern = re.compile(rf'<!-- {name}:start -->.*?<!-- {name}:end -->', re.S)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text)
    return text.rstrip('\n') + '\n\n' + block + '\n'


def drop_block(text, name):
    return re.sub(rf'\n*<!-- {name}:start -->.*?<!-- {name}:end -->\n?', '\n', text, flags=re.S)


def h1(path):
    for line in read(path).splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    return os.path.basename(path)


def library_settings(start):
    """library.yaml of the repository the book lives in, if any."""
    d = os.path.abspath(start)
    while True:
        if os.path.exists(os.path.join(d, 'library.yaml')):
            return load_yaml(os.path.join(d, 'library.yaml')), d
        parent = os.path.dirname(d)
        if parent == d:
            return {}, None
        d = parent


def book_files(book_dir, data, lab):
    """The book's reading order: chapter 0, chapters, mock exam, glossary."""
    folder = os.path.join(book_dir, 'chapters')
    names = sorted(os.listdir(folder)) if os.path.isdir(folder) else []
    order = [os.path.join(folder, n) for n in names if n.startswith('00-')]
    order += [p for p in (chapter_path(book_dir, n) for n in chapter_numbers(data)) if p]
    for label in ('Final mock exam', 'Glossary'):
        order += [os.path.join(folder, n) for n in names
                  if slugify(lab[label]) in n and os.path.join(folder, n) not in order]
    return order


# ---------- book: navigation, map, index ----------

def update_navigation(files, lab):
    for i, path in enumerate(files):
        parts = []
        if i > 0:
            parts.append(f'[◀ {lab["Previous chapter"]}]({os.path.basename(files[i - 1])})')
        parts.append(f'[{lab["Book map"]}](../README.md)')
        if i + 1 < len(files):
            parts.append(f'[{lab["Next chapter"]} ▶]({os.path.basename(files[i + 1])})')
        write(path, set_block(read(path), 'nav', '---\n\n' + ' · '.join(parts)))


def update_map(book_dir, data, files, lab):
    minutes = {c['n']: c.get('minutes') for c in data['chapters']}
    lines = [f'## 🗺️ {lab["Book map"]}', '']
    for path in files:
        m = re.match(r'(\d+)-', os.path.basename(path))
        n = int(m.group(1)) if m else None
        extra = f' · ⏱️ ~{minutes[n]} min' if n in minutes and minutes[n] else ''
        lines.append(f'- [{h1(path)}](chapters/{os.path.basename(path)}){extra}')
    readme = os.path.join(book_dir, 'README.md')
    text = read(readme) if os.path.exists(readme) else f'# {data["title"]}\n\n{data.get("subtitle", "")}\n'
    write(readme, set_block(text, 'map', '\n'.join(lines)))


def update_index(book_dir, data, files, lab):
    glossary = [p for p in files if slugify(lab['Glossary']) in os.path.basename(p)]
    if not glossary:
        return
    by_chapter = {c['n']: chapter_path(book_dir, c['n']) for c in data['chapters']}
    rows = [f'## {lab["Index"]}', '']
    for c in sorted(data.get('concepts') or [], key=lambda c: c['name'].lower()):
        target = by_chapter.get(c.get('chapter'))
        if target:
            rows.append(f'- {c["name"]}: [{h1(target)}]({os.path.basename(target)})')
    write(glossary[0], set_block(read(glossary[0]), 'index', '\n'.join(rows)))


# ---------- book: EPUB ----------

def split_answers(text, first_number):
    """Moves every <details> answer out of the text. Returns (text, answers)."""
    lines, kept, answers = text.splitlines(), [], []
    i = 0
    while i < len(lines):
        prefix = re.match(r'^((?:>\s?)*)', lines[i]).group(1)
        if DETAILS_OPEN.match(lines[i][len(prefix):]):
            j, summary, body = i + 1, '', []
            while j < len(lines) and lines[j][len(prefix):].strip() != '</details>':
                inner = lines[j][len(prefix):]
                m = SUMMARY.match(inner)
                if m and not summary:
                    summary = m.group(1).strip()
                else:
                    body.append(inner)
                j += 1
            k = first_number + len(answers)
            answers.append((k, summary, '\n'.join(body).strip()))
            kept.append(f'{prefix}[{summary} ↓](#ans-{k}){{#q-{k} .answer-link}}')
            i = j + 1
            continue
        kept.append(lines[i])
        i += 1
    return '\n'.join(kept), answers


def file_id(path):
    return 'f-' + slugify(os.path.splitext(os.path.basename(path))[0], 60)


def epub_markdown(files, lab):
    parts, answers = [], []
    for path in files:
        text = drop_block(read(path), 'nav')
        # explicit ids on the chapter titles, so links between chapters survive the merge
        anchor = file_id(path)
        text = re.sub(r'^# (.+)$', lambda m, a=anchor: f'# {m.group(1)} {{#{a}}}', text, count=1, flags=re.M)
        text = LINK_MD.sub(lambda m: f']({m.group(2) or "#" + file_id(m.group(1))})', text)
        text, found = split_answers(text, len(answers) + 1)
        answers += [(k, h1(path), s, b) for k, s, b in found]
        parts.append(text)
    if answers:
        lines = [f'# {lab["Answers"]} {{#answers}}', '']
        current = None
        for k, chapter, _summary, body in answers:
            if chapter != current:
                lines += [f'## {chapter}', '']
                current = chapter
            if '\n' not in body:
                # a one-line answer such as "0." would be read as an empty numbered list
                body = re.sub(r'^(\d+)\.', r'\1\\.', body)
            lines += [f'[]{{#ans-{k}}}**{k}.**', '', body, '', f'[↩ {lab["Back to the exercise"]}](#q-{k})', '']
        parts.append('\n'.join(lines))
    return '\n\n'.join(parts), len(answers)


def pandoc_path():
    found = shutil.which('pandoc')
    if found:
        return found
    try:
        import pypandoc
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pypandoc_binary'], check=True)
        import pypandoc
    return pypandoc.get_pandoc_path()


def build_epub(book_dir, data, files, lab, out_dir, library):
    text, answers = epub_markdown(files, lab)
    with tempfile.TemporaryDirectory() as tmp:
        source = os.path.join(tmp, 'book.md')
        write(source, text)
        target = os.path.join(out_dir, f'{data["slug"]}.epub')
        os.makedirs(out_dir, exist_ok=True)
        meta = {'title': data['title'], 'lang': data.get('language', 'en'),
                'author': library.get('author') or data.get('author') or '',
                'rights': library.get('content_license', '')}
        if data.get('subtitle'):
            meta['subtitle'] = data['subtitle']
        cmd = [pandoc_path(), source, '-f', 'markdown', '-t', 'epub3', '-o', target, '--toc', '--toc-depth=2',
               '--split-level=1', '--mathml', '--css', os.path.join(SKILL, 'assets', 'epub.css'),
               '--resource-path', os.pathsep.join([os.path.join(book_dir, 'chapters'), book_dir])]
        for key, value in meta.items():
            if value:
                cmd += ['--metadata', f'{key}={value}']
        cover = os.path.join(book_dir, 'cover.png')
        if os.path.exists(cover):
            cmd += ['--epub-cover-image', cover]
        r = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if r.returncode != 0:
            fail(f'pandoc failed: {r.stderr.strip()[-600:]}')
    return target, answers, [w for w in r.stderr.splitlines() if w.strip()][:5]


# ---------- book: zip ----------

def pack(book_dir, data, out_dir, suffix=''):
    collection = COLLECTIONS.get(data.get('origin'), 'created-books')
    files = sorted(p for p in glob.glob(os.path.join(book_dir, '**', '*'), recursive=True) if os.path.isfile(p))
    chunks = [files[i:i + GITHUB_UPLOAD_LIMIT] for i in range(0, len(files), GITHUB_UPLOAD_LIMIT)] or [[]]
    made = []
    for i, chunk in enumerate(chunks, 1):
        name = data['slug'] + suffix + (f'-part{i}-of-{len(chunks)}' if len(chunks) > 1 else '') + '.zip'
        target = os.path.join(out_dir, name)
        with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
            for path in chunk:
                rel = os.path.relpath(path, book_dir).replace(os.sep, '/')
                z.write(path, f'{collection}/{data["slug"]}/{rel}')
        made.append({'zip': target, 'files': len(chunk)})
    return made


def cmd_book(args):
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    lab = labels(data.get('language', 'en'))
    library, _ = library_settings(book_dir)
    out_dir = os.path.abspath(args.out)
    os.makedirs(out_dir, exist_ok=True)
    files = book_files(book_dir, data, lab)
    result = {'book': data['title']}
    if files:
        update_navigation(files, lab)
        update_map(book_dir, data, files, lab)
        update_index(book_dir, data, files, lab)
    if args.partial:
        result['zips'] = pack(book_dir, data, out_dir, '-partial')
        result['note'] = 'partial checkpoint: no EPUB'
        out(result)
    if not args.no_epub:
        epub, answers, warnings = build_epub(book_dir, data, files, lab, out_dir, library)
        result.update({'epub': epub, 'answers_in_appendix': answers})
        if warnings:
            result['pandoc_warnings'] = warnings
    if args.no_zip:
        out(result)
    result['zips'] = pack(book_dir, data, out_dir)
    if len(result['zips']) > 1:
        result['note'] = (f'{len(result["zips"])} zips: GitHub\'s website takes at most {GITHUB_UPLOAD_LIMIT} '
                          'files per upload; upload them in order')
    out(result)


# ---------- library: lists and website ----------

def library_books(root):
    books = []
    for folder in COLLECTIONS.values():
        for path in sorted(glob.glob(os.path.join(root, folder, '*', 'book.yaml'))):
            data = load_yaml(path)
            books.append({'folder': folder, 'dir': os.path.dirname(path), 'data': data})
    return books


def epub_url(settings, slug):
    repo, tag = settings.get('repository'), settings.get('epub_release', 'epubs')
    return f'https://github.com/{repo}/releases/download/{tag}/{slug}.epub' if repo else ''


def book_rows(books, settings, lab, link):
    rows = [f'| {lab["Book"]} | {lab["Level"]} | {lab["Chapters"]} | EPUB |', '| --- | --- | --- | --- |']
    for b in books:
        d = b['data']
        level = d.get('level') or {}
        url = epub_url(settings, d['slug'])
        rows.append(f'| [{d["title"]}]({link(b)}) ({d.get("language", "")}) | {level.get("start", "")} → '
                    f'{level.get("end", "")} | {len(d.get("chapters") or [])} | '
                    + (f'[{lab["Download EPUB"]}]({url})' if url else '') + ' |')
    return '\n'.join(rows)


def cmd_lists(args):
    root = os.path.abspath(args.library)
    settings, _ = library_settings(root)
    books = library_books(root)
    updated = []
    for folder in COLLECTIONS.values():
        group = [b for b in books if b['folder'] == folder]
        if not group:
            continue
        for readme, lang in (('README.md', 'en'), ('README.pt-BR.md', 'pt-BR')):
            path = os.path.join(root, folder, readme)
            if os.path.exists(path):
                table = book_rows(group, settings, labels(lang), lambda b: os.path.basename(b['dir']) + '/')
                write(path, set_block(read(path), 'list', table))
                updated.append(os.path.relpath(path, root).replace(os.sep, '/'))
    out({'books': len(books), 'updated': updated})


def collapsible(text):
    """<details> answers become Zensical collapsible blocks, which keep Markdown inside them."""
    lines, kept, i = text.splitlines(), [], 0
    while i < len(lines):
        prefix = re.match(r'^((?:>\s?)*)', lines[i]).group(1)
        if DETAILS_OPEN.match(lines[i][len(prefix):]):
            j, summary, body = i + 1, '', []
            while j < len(lines) and lines[j][len(prefix):].strip() != '</details>':
                inner = lines[j][len(prefix):]
                m = SUMMARY.match(inner)
                if m and not summary:
                    summary = m.group(1).strip()
                else:
                    body.append(inner)
                j += 1
            title = summary.replace('"', "'")
            # a block inside a quote is moved out of it: collapsible blocks do not nest in quotes
            kept += ['', f'??? success "{title}"', ''] + [('    ' + b) if b.strip() else '' for b in body] + ['']
            i = j + 1
            continue
        kept.append(lines[i])
        i += 1
    return '\n'.join(kept) + '\n'


def cmd_site(args):
    yaml = need_yaml()
    root = os.path.abspath(args.library)
    settings, _ = library_settings(root)
    lang = settings.get('default_language') or 'en'
    lang = 'en' if lang == 'auto' else lang
    lab = labels(lang)
    out_dir = os.path.abspath(args.out)
    docs = os.path.join(out_dir, 'docs')
    if os.path.exists(docs):
        shutil.rmtree(docs)
    books = library_books(root)
    nav = [{'Home': 'index.md'}]
    home = [f'# 📚 {settings.get("site_title") or (settings.get("repository") or "Library").split("/")[-1]}', '']
    for origin, folder in COLLECTIONS.items():
        group = [b for b in books if b['folder'] == folder]
        title = lab['Created books' if origin == 'created' else 'Improved materials']
        home += [f'## {title}', '']
        if group:
            home += [book_rows(group, settings, lab,
                               lambda b, f=folder: f'{f}/{os.path.basename(b["dir"])}/README.md'), '']
        else:
            home += ['—', '']
        section = []
        for b in group:
            d, src = b['data'], b['dir']
            dest = os.path.join(docs, folder, os.path.basename(src))
            shutil.copytree(src, dest, ignore=shutil.ignore_patterns('_source', 'book.yaml', 'cover.svg'))
            for md in glob.glob(os.path.join(dest, '**', '*.md'), recursive=True):
                write(md, collapsible(read(md)))
            blab = labels(d.get('language', lang))
            rel = f'{folder}/{os.path.basename(src)}'
            entries = [{blab['Book map']: f'{rel}/README.md'}]
            entries += [{h1(p): f'{rel}/chapters/{os.path.basename(p)}'}
                        for p in book_files(dest, d, blab)]
            section.append({d['title']: entries})
        if section:
            nav.append({title: section})
    write(os.path.join(docs, 'index.md'), '\n'.join(home))
    config = {
        'site_name': home[0][5:],
        'docs_dir': 'docs',
        'site_dir': 'site',
        'theme': {'name': 'material', 'language': lang.split('-')[0] if lang != 'pt-BR' else 'pt-BR',
                  'features': ['navigation.sections', 'navigation.footer', 'navigation.top', 'search.highlight',
                               'search.suggest', 'content.code.copy'],
                  'palette': [{'scheme': 'default', 'toggle': {'icon': 'material/weather-night', 'name': 'Dark mode'}},
                              {'scheme': 'slate', 'toggle': {'icon': 'material/weather-sunny', 'name': 'Light mode'}}]},
        'markdown_extensions': ['admonition', 'pymdownx.details', 'pymdownx.superfences', 'pymdownx.highlight',
                                'tables', 'attr_list', 'md_in_html', {'pymdownx.arithmatex': {'generic': True}}],
        'extra_javascript': ['https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'],
        'nav': nav,
    }
    if settings.get('repository'):
        owner, name = settings['repository'].split('/', 1)
        config['site_url'] = f'https://{owner.lower()}.github.io/{name}/'
        config['repo_url'] = f'https://github.com/{settings["repository"]}'
    write(os.path.join(out_dir, 'mkdocs.yml'),
          yaml.safe_dump(config, allow_unicode=True, sort_keys=False, width=100))
    out({'books': len(books), 'source': out_dir, 'build': f'cd "{out_dir}" && zensical build --clean'})


def main():
    if sys.argv[1:2] in (['lists'], ['site']):
        p = argparse.ArgumentParser(description='Library lists and website source.')
        p.add_argument('cmd')
        p.add_argument('--library', default='.')
        p.add_argument('--out', default='_site')
        args = p.parse_args()
        (cmd_lists if args.cmd == 'lists' else cmd_site)(args)
        return
    p = argparse.ArgumentParser(description='Build a book: navigation, map, index, EPUB and zip.')
    p.add_argument('--book')
    p.add_argument('--out', default='dist')
    p.add_argument('--partial', action='store_true')
    p.add_argument('--no-epub', action='store_true')
    p.add_argument('--no-zip', action='store_true', help='only the EPUB (used by the EPUB workflow)')
    cmd_book(p.parse_args())


if __name__ == '__main__':
    main()
