#!/usr/bin/env python3
"""Real images for the book: free-license photos from Wikimedia Commons and screenshots of the book's
application, each one recorded in img/CREDITS.md (references/SOURCES.md §7).

Usage:
  python scripts/images.py search "<what to look for>" [--limit 6]
  python scripts/images.py fetch "File:<title>" --name c03-eniac [--book B]
  python scripts/images.py screenshot <url> --name c05-app [--book B] [--width 1280 --height 800]

search lists only public domain, CC0, CC BY and CC BY-SA images, with author and license.
fetch downloads the 1280 px version to img/<name>.<ext>, records the credit and prints the Markdown
and the caption credit to use. A non-free image is refused.
screenshot opens the application the chapter is running (Playwright) and saves img/<name>.png;
without Playwright it says how to install it, or to ask the user for the screenshot (claude.ai).
"""
import argparse
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import fail, find_book, out

API = 'https://commons.wikimedia.org/w/api.php'
# Wikimedia asks every client to say who it is
AGENT = 'Syllabook/0.3 (https://github.com/Joshpcbrrj/syllabook)'
EXTENSIONS = {'image/jpeg': '.jpg', 'image/png': '.png', 'image/gif': '.gif', 'image/webp': '.webp',
              'image/svg+xml': '.svg'}
FREE = re.compile(r'^(public domain|pd\b|pd-|cc0|cc[ -]by( |-sa |-sa$|$)|cc[ -]by[ -]\d|cc[ -]by-sa[ -]\d)', re.I)


def api(params):
    query = urllib.parse.urlencode({**params, 'format': 'json'})
    request = urllib.request.Request(f'{API}?{query}', headers={'User-Agent': AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def download(url, path):
    request = urllib.request.Request(url, headers={'User-Agent': AGENT})
    with urllib.request.urlopen(request, timeout=60) as response, open(path, 'wb') as f:
        f.write(response.read())


def free_license(name):
    """Public domain, CC0, CC BY or CC BY-SA; NC (non-commercial) and ND (no derivatives) are not free."""
    name = (name or '').strip()
    return bool(FREE.match(name)) and not re.search(r'\b(nc|nd)\b', name, re.I)


def plain(value):
    """Commons metadata comes as HTML: keep the text only."""
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', value or ''))).strip()


def describe(page):
    info = (page.get('imageinfo') or [{}])[0]
    meta = info.get('extmetadata') or {}
    value = lambda key: (meta.get(key) or {}).get('value', '')  # noqa: E731
    return {'title': page.get('title'), 'author': plain(value('Artist')) or 'unknown author',
            'license': plain(value('LicenseShortName')), 'license_url': value('LicenseUrl'),
            'source': info.get('descriptionurl'), 'url': info.get('thumburl') or info.get('url'),
            'mime': info.get('mime'), 'size': f'{info.get("width")}x{info.get("height")}',
            'free': free_license(plain(value('LicenseShortName'))) and value('NonFree') != 'true'}


INFO = {'prop': 'imageinfo', 'iiprop': 'url|mime|size|extmetadata', 'iiurlwidth': 1280}


def search(query, limit):
    data = api({'action': 'query', 'generator': 'search', 'gsrsearch': query, 'gsrnamespace': 6,
                'gsrlimit': max(limit * 3, 10), **INFO})
    found = [describe(p) for p in (data.get('query') or {}).get('pages', {}).values()]
    free = [f for f in found if f['free']]
    for f in free:
        del f['free']
    out({'query': query, 'results': free[:limit], 'left_out': len(found) - len(free),
         'note': 'only public domain, CC0, CC BY and CC BY-SA images; fetch one with images.py fetch'})


def credit(book_dir, filename, line):
    """Adds the image's line to img/CREDITS.md once."""
    path = os.path.join(book_dir, 'img', 'CREDITS.md')
    text = open(path, encoding='utf-8').read() if os.path.exists(path) else '# Image credits\n'
    if not re.search(rf'^- {re.escape(filename)}:', text, re.M):
        # a blank line between the title and the list, then one line per image
        joiner = '\n' if re.search(r'^- ', text, re.M) else '\n\n'
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(text.rstrip('\n') + f'{joiner}- {filename}: {line}\n')


def fetch(title, name, book_dir):
    pages = list((api({'action': 'query', 'titles': title, **INFO}).get('query') or {}).get('pages', {}).values())
    if not pages or 'missing' in pages[0] or not pages[0].get('imageinfo'):
        fail(f'{title} not found on Wikimedia Commons')
    image = describe(pages[0])
    if not image['free']:
        fail(f'{title} has no free license ({image["license"] or "none"}): pick another image')
    filename = name + EXTENSIONS.get(image['mime'], '.jpg')
    os.makedirs(os.path.join(book_dir, 'img'), exist_ok=True)
    download(image['url'], os.path.join(book_dir, 'img', filename))
    license_text = image['license'] + (f' ({image["license_url"]})' if image['license_url'] else '')
    credit(book_dir, filename, f'{image["title"]}, {image["author"]}, {license_text}, {image["source"]}')
    out({'file': f'img/{filename}', 'markdown': f'![<alt text>](../img/{filename})',
         'caption': f'{image["author"]}, {image["license"]}, via Wikimedia Commons',
         'note': 'write the alt text and put the caption credit under the image'})


def screenshot(url, name, book_dir, width, height):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        fail('Playwright is not installed. In Claude Code: pip install playwright && python -m playwright install '
             'chromium. On claude.ai (no browser): ask the user for a screenshot of the running application, '
             'save it in img/ and record it in img/CREDITS.md. Never make up a screenshot.')
    os.makedirs(os.path.join(book_dir, 'img'), exist_ok=True)
    filename = f'{name}.png'
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(url, wait_until='networkidle')
        page.screenshot(path=os.path.join(book_dir, 'img', filename), full_page=False)
        browser.close()
    credit(book_dir, filename, f'screenshot of the book\'s application running at {url}, taken while writing the book')
    out({'file': f'img/{filename}', 'markdown': f'![<alt text>](../img/{filename})'})


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('search')
    s.add_argument('query')
    s.add_argument('--limit', type=int, default=6)
    f = sub.add_parser('fetch')
    f.add_argument('title')
    f.add_argument('--name', required=True)
    f.add_argument('--book')
    c = sub.add_parser('screenshot')
    c.add_argument('url')
    c.add_argument('--name', required=True)
    c.add_argument('--book')
    c.add_argument('--width', type=int, default=1280)
    c.add_argument('--height', type=int, default=800)
    args = p.parse_args()
    if args.cmd == 'search':
        search(args.query, args.limit)
    book_dir, _ = find_book(args.book)
    if args.cmd == 'fetch':
        fetch(args.title, args.name, book_dir)
    screenshot(args.url, args.name, book_dir, args.width, args.height)


if __name__ == '__main__':
    main()
