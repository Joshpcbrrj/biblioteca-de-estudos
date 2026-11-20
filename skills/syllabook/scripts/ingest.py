#!/usr/bin/env python3
"""Turns a study material into Markdown sections plus an outline, so Claude reads only what it needs.

Usage:
  python scripts/ingest.py <file | folder | url> --out DIR [--level 2] [--engine auto|docling|basic]

Inputs:
  .md .txt              as they are
  a folder              every .md/.txt in it, in name order (e.g. Notion pages saved one per file)
  .html, a web address  converted to Markdown
  .epub                 its chapters in reading order
  .docx .odt .rtf       through pandoc
  .pdf .pptx images     through Docling when available; a PDF falls back to plain text per page

--engine auto uses Docling where it helps (PDF, PPTX, images) and the built-in converters
elsewhere; docling forces it; basic never uses it. Writes DIR/NN-<slug>.md, one per section
(split at headings up to --level), and DIR/outline.json, and prints the outline: read it
first and open only the sections a step needs.
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fail, out, pandoc_path, slugify

DOCLING_GUIDE = 'https://github.com/Joshpcbrrj/syllabook/blob/main/docs/integrations/docling.md'
TEXT = ('.md', '.markdown', '.txt')
PANDOC = ('.docx', '.odt', '.rtf')
DOCLING_ONLY = ('.pptx', '.xlsx', '.png', '.jpg', '.jpeg', '.tiff')
BIG_SECTION = 5000  # words: more than this is better read in parts


# ---------- HTML ----------

class Markdown(HTMLParser):
    """A small HTML to Markdown converter: headings, paragraphs, lists, code, emphasis and links."""
    BLOCKS = {'p', 'div', 'section', 'article', 'br', 'tr', 'blockquote'}
    SKIP = {'script', 'style', 'head', 'nav', 'footer', 'noscript'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts, self.skip, self.pre, self.href = [], 0, False, None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n' + '#' * int(tag[1]) + ' ')
        elif tag == 'li':
            self.parts.append('\n- ')
        elif tag == 'pre':
            self.pre = True
            self.parts.append('\n\n```\n')
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag in ('strong', 'b'):
            self.parts.append('**')
        elif tag in ('em', 'i'):
            self.parts.append('*')
        elif tag == 'a':
            self.href = dict(attrs).get('href')
            self.parts.append('[' if self.href and self.href.startswith('http') else '')
        elif tag in self.BLOCKS:
            self.parts.append('\n\n')

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif re.fullmatch(r'h[1-6]', tag):
            self.parts.append('\n\n')
        elif tag == 'pre':
            self.pre = False
            self.parts.append('\n```\n\n')
        elif tag == 'code' and not self.pre:
            self.parts.append('`')
        elif tag in ('strong', 'b'):
            self.parts.append('**')
        elif tag in ('em', 'i'):
            self.parts.append('*')
        elif tag == 'a':
            if self.href and self.href.startswith('http'):
                self.parts.append(f']({self.href})')
            self.href = None

    def handle_data(self, data):
        if self.skip:
            return
        self.parts.append(data if self.pre else re.sub(r'\s+', ' ', data))

    def markdown(self):
        text = ''.join(self.parts)
        text = re.sub(r'[ \t]+\n', '\n', text)
        return re.sub(r'\n{3,}', '\n\n', text).strip() + '\n'


def html_to_md(html):
    parser = Markdown()
    parser.feed(html)
    return parser.markdown()


# ---------- converters ----------

def epub_to_md(path):
    with zipfile.ZipFile(path) as z:
        container = ET.fromstring(z.read('META-INF/container.xml'))
        opf_path = container.find('.//{*}rootfile').get('full-path')
        opf = ET.fromstring(z.read(opf_path))
        base = os.path.dirname(opf_path)
        # findall, not iter: only find/findall accept the {*} namespace wildcard
        manifest = {item.get('id'): item.get('href') for item in opf.findall('.//{*}item')}
        chapters = []
        for ref in opf.findall('.//{*}itemref'):
            href = manifest.get(ref.get('idref'))
            if href:
                name = f'{base}/{href}' if base else href
                chapters.append(html_to_md(z.read(name).decode('utf-8', errors='replace')))
    return '\n\n'.join(chapters)


def folder_to_md(path):
    files = sorted(f for f in glob.glob(os.path.join(path, '*')) if f.lower().endswith(TEXT))
    if not files:
        fail(f'no .md or .txt files in {path}')
    parts = []
    for f in files:
        text = open(f, encoding='utf-8', errors='replace').read().strip()
        if not text.startswith('#'):
            # each file becomes a section titled by its name
            text = f'# {os.path.splitext(os.path.basename(f))[0]}\n\n{text}'
        parts.append(text)
    return '\n\n'.join(parts) + '\n'


def pandoc_to_md(path):
    r = subprocess.run([pandoc_path(), path, '-t', 'gfm', '--wrap=none'], capture_output=True, text=True,
                       encoding='utf-8')
    if r.returncode != 0:
        fail(f'pandoc could not read {os.path.basename(path)}: {r.stderr.strip()[-300:]}')
    return r.stdout


def docling_command():
    """The Docling command line, or None. Docling is heavy: usually on the user's computer, not in a sandbox."""
    found = shutil.which('docling')
    return [found] if found else None


def docling_to_md(path):
    command = docling_command()
    with tempfile.TemporaryDirectory() as tmp:
        r = subprocess.run(command + [path, '--to', 'md', '--output', tmp], capture_output=True, text=True,
                           encoding='utf-8', errors='replace')
        produced = glob.glob(os.path.join(tmp, '**', '*.md'), recursive=True)
        if r.returncode != 0 or not produced:
            fail(f'Docling could not convert {os.path.basename(path)}: {(r.stderr or r.stdout).strip()[-300:]}')
        return open(produced[0], encoding='utf-8').read()


def pdf_basic(path, warnings):
    try:
        from pypdf import PdfReader
    except ImportError:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'pypdf'], check=True)
        from pypdf import PdfReader
    pages = [page.extract_text() or '' for page in PdfReader(path).pages]
    words = sum(len(p.split()) for p in pages)
    if words < 20 * len(pages):
        warnings.append('very little text: the PDF may be scanned images; Docling (with OCR) reads it better: '
                        + DOCLING_GUIDE)
    warnings.append('plain-text extraction: tables and headings are lost; Docling keeps them: ' + DOCLING_GUIDE)
    return '\n\n'.join(f'## p. {i}\n\n{text.strip()}' for i, text in enumerate(pages, 1))


def fetch(url):
    request = urllib.request.Request(url, headers={'User-Agent': 'Syllabook ingest'})
    with urllib.request.urlopen(request, timeout=30) as r:
        return r.read(), r.headers.get('Content-Type', '')


def convert(source, engine, warnings):
    """Returns (markdown, engine used)."""
    if re.match(r'https?://', source):
        data, kind = fetch(source)
        if 'pdf' in kind:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
                f.write(data)
            try:
                return convert(f.name, engine, warnings)
            finally:
                os.remove(f.name)
        return html_to_md(data.decode('utf-8', errors='replace')), 'html'
    if not os.path.exists(source):
        fail(f'not found: {source}')
    if os.path.isdir(source):
        return folder_to_md(source), 'folder'
    ext = os.path.splitext(source)[1].lower()
    docling = docling_command() if engine != 'basic' else None
    if engine == 'docling' and not docling:
        fail(f'Docling is not installed here. Install it on your computer: {DOCLING_GUIDE}')
    if ext in TEXT:
        return open(source, encoding='utf-8', errors='replace').read(), 'text'
    if ext in ('.html', '.htm'):
        return html_to_md(open(source, encoding='utf-8', errors='replace').read()), 'html'
    if ext == '.epub':
        return epub_to_md(source), 'epub'
    if docling and (engine == 'docling' or ext in ('.pdf',) + DOCLING_ONLY):
        return docling_to_md(source), 'docling'
    if ext in PANDOC:
        return pandoc_to_md(source), 'pandoc'
    if ext == '.pdf':
        return pdf_basic(source, warnings), 'pdf-text'
    if ext in DOCLING_ONLY:
        fail(f'{ext} files need Docling: {DOCLING_GUIDE}')
    fail(f'unsupported file type: {ext}')


# ---------- sections ----------

def split(markdown, level):
    """Sections start at headings of level <= `level`; headings inside code blocks do not count."""
    sections, current, in_code = [], {'title': '(intro)', 'level': 0, 'lines': []}, False
    for line in markdown.splitlines():
        if line.lstrip().startswith(('```', '~~~')):
            in_code = not in_code
        m = None if in_code else re.match(r'^(#{1,6})\s+(.+?)\s*#*\s*$', line)
        if m and len(m.group(1)) <= level:
            if any(x.strip() for x in current['lines']):
                sections.append(current)
            current = {'title': m.group(2).strip(), 'level': len(m.group(1)), 'lines': []}
        current['lines'].append(line)
    if any(x.strip() for x in current['lines']):
        sections.append(current)
    return sections


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('source')
    p.add_argument('--out', required=True)
    p.add_argument('--level', type=int, default=2, help='split at headings up to this level (default 2)')
    p.add_argument('--engine', choices=['auto', 'docling', 'basic'], default='auto')
    args = p.parse_args()
    warnings = []
    markdown, engine = convert(args.source, args.engine, warnings)
    sections = split(markdown, args.level)
    if not sections:
        fail('the material has no text')
    os.makedirs(args.out, exist_ok=True)
    for old in glob.glob(os.path.join(args.out, '[0-9][0-9]-*.md')):
        os.remove(old)  # a previous run of the same material would leave stale sections
    outline = []
    for i, s in enumerate(sections, 1):
        name = f'{i:02d}-{slugify(s["title"], 40) or "section"}.md'
        text = '\n'.join(s['lines']).strip() + '\n'
        with open(os.path.join(args.out, name), 'w', encoding='utf-8', newline='\n') as f:
            f.write(text)
        words = len(re.findall(r'\w+', text))
        outline.append({'id': f's{i:02d}', 'title': s['title'], 'level': s['level'], 'words': words, 'file': name})
        if words > BIG_SECTION:
            warnings.append(f'{name} has {words} words: read it in parts')
    result = {'source': args.source, 'engine': engine, 'sections': outline,
              'total_words': sum(s['words'] for s in outline), 'warnings': warnings}
    with open(os.path.join(args.out, 'outline.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    out(result)


if __name__ == '__main__':
    main()
