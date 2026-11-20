#!/usr/bin/env python3
"""Draws an SVG diagram from a short YAML spec, in the books' visual theme.

Usage:
  python scripts/diagram.py <spec.yaml> [--reading large|small] [--out FILE]
  python scripts/diagram.py --sheet <chapter> [--book B]    one contact sheet with the chapter's images
  python scripts/diagram.py --help

Every spec has: type, title (the idea in one sentence), and optionally caption (a closing
line in italics). The width follows the book's reading profile (large 960, small 480).
A spec in img/_source/<name>.yaml is drawn to img/<name>.svg.

Types and their fields:
  flow      steps: [{text, kind: start|step|decision|end, color, label, side, side_label}]
            a decision's `side` is drawn as a box to the right (the other way out, e.g. "não");
            `label` names the arrow to the next step (e.g. "sim")
  timeline  events: [{when, text, highlight}]
  compare   left: {title, color}, right: {title, color}, rows: [[left, right], ...]
            style: wrong-right marks the left column ❌ (red) and the right one ✅ (green)
  boxes     cells: [{value, label, highlight}], name (above the boxes, e.g. a variable)
  layers    layers: [{text, note, color}]   (top to bottom)
  tree      root: {text, color, children: [...]}
  sequence  participants: [names, at most 4], messages: [{from, to, text, dashed}]
  bars      bars: [{label, value, highlight}], unit
  cards     cards: [{icon, title, items: [...], code: [...]}]   (the cheat sheet, up to 12)

Colors: blue (input, structure), green (right, output, end), orange (decision, attention),
red (error), purple (central idea), teal, gray (neutral). Prints JSON with the file written,
its size and any text that does not fit; exit code 1 when something does not fit.
"""
import argparse
import base64
import os
import re
import shutil
import subprocess
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chapter_path, fail, find_book, load_yaml, out

BG = '#FAF9F6'
INK, SOFT = '#2B2B33', '#55555F'
# fill, border, strong (text and arrows on that color)
PALETTE = {
    'blue': ('#E3EEFF', '#9DBEF5', '#2F5DA8'),
    'green': ('#DDF5EA', '#94D8B8', '#1F7A52'),
    'orange': ('#FFF4CC', '#EBCF6E', '#8A6A00'),
    'red': ('#FFE7E0', '#F5AE9B', '#A8402A'),
    'purple': ('#EEE6FB', '#C3ADEE', '#5B3E9E'),
    'teal': ('#DDF3F3', '#93D2D2', '#1F6E6E'),
    'gray': ('#F1EFEA', '#C9C4BA', '#55555F'),
}
KIND_COLOR = {'start': 'gray', 'step': 'blue', 'decision': 'orange', 'end': 'green'}
# sizes per reading profile: width, body, title, small text; a 6" screen needs bigger letters
PROFILES = {'large': {'width': 960, 'body': 20, 'title': 26, 'small': 16},
            'small': {'width': 480, 'body': 14, 'title': 17, 'small': 12.5}}
MAX_ELEMENTS = 7  # references/VISUALS.md: more than ~7 main elements overloads the reader
TYPES = ('flow', 'timeline', 'compare', 'boxes', 'layers', 'tree', 'sequence', 'bars', 'cards')


class Canvas:
    def __init__(self, profile):
        self.p = PROFILES[profile]
        self.w = self.p['width']
        self.pad = round(self.w * 0.04)
        self.parts, self.problems, self.y = [], [], 0

    # text measures: an average sans-serif letter is ~0.56 em wide, a monospace one 0.6 em
    def width_of(self, text, size, mono=False):
        return len(text) * size * (0.6 if mono else 0.56)

    def wrap(self, text, size, width, mono=False):
        """Splits text into lines that fit the width; reports a word that cannot fit at all."""
        text = str(text)
        limit = max(1, int(width / (size * (0.6 if mono else 0.56))))
        lines, line = [], ''
        for word in text.split():
            if len(word) > limit:
                self.problems.append(f'"{word}" does not fit in {round(width)} px: shorten it or widen the box')
            candidate = f'{line} {word}'.strip()
            if len(candidate) <= limit or not line:
                line = candidate
            else:
                lines.append(line)
                line = word
        return lines + [line] if line or not lines else lines

    def rect(self, x, y, w, h, color='gray', rx=12, dashed=False, shadow=True):
        fill, border, _ = PALETTE[color]
        if shadow:
            self.parts.append(f'<rect x="{x}" y="{y + 4}" width="{w}" height="{h}" rx="{rx}" '
                              f'fill="#3A3226" opacity="0.07"/>')
        dash = ' stroke-dasharray="9 6"' if dashed else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                          f'stroke="{border}" stroke-width="2"{dash}/>')

    def diamond(self, cx, y, w, h, color='orange'):
        fill, border, _ = PALETTE[color]
        pts = f'{cx},{y} {cx + w / 2},{y + h / 2} {cx},{y + h} {cx - w / 2},{y + h / 2}'
        self.parts.append(f'<polygon points="{pts}" fill="{fill}" stroke="{border}" stroke-width="2"/>')

    def text(self, x, y, value, size=None, weight=400, anchor='middle', fill=INK, mono=False, italic=False):
        size = size or self.p['body']
        family = "'Courier New', Menlo, monospace" if mono else 'system-ui, -apple-system, sans-serif'
        style = ' font-style="italic"' if italic else ''
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
                          f'font-weight="{weight}" text-anchor="{anchor}" fill="{fill}"{style}>'
                          f'{escape(str(value))}</text>')

    def lines(self, x, y, lines, size=None, **kw):
        size = size or self.p['body']
        for i, line in enumerate(lines):
            self.text(x, y + size + i * size * 1.3, line, size=size, **kw)
        return len(lines) * size * 1.3

    def arrow(self, x1, y1, x2, y2, label='', color='gray', dashed=False):
        strong = PALETTE[color][2]
        dash = ' stroke-dasharray="9 6"' if dashed else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{strong}" stroke-width="2.5"'
                          f'{dash} marker-end="url(#arrow-{color})"/>')
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            side = 10 if x1 == x2 else 0
            self.text(mx + side, my - (6 if y1 == y2 else -5), label, size=self.p['small'],
                      anchor='start' if x1 == x2 else 'middle', fill=strong, weight=600)

    def svg(self, title, caption, alt):
        height = round(self.y + self.pad)
        markers = ''.join(f'<marker id="arrow-{c}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
                          f'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
                          f'fill="{v[2]}"/></marker>' for c, v in PALETTE.items())
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{height}" '
                f'viewBox="0 0 {self.w} {height}" role="img">'
                f'<title>{escape(title)}</title><desc>{escape(alt or caption or title)}</desc>'
                f'<defs>{markers}</defs><rect width="100%" height="100%" fill="{BG}"/>'
                + ''.join(self.parts) + '</svg>\n'), height


# ---------- layouts ----------

def header(c, spec):
    lines = c.wrap(spec['title'], c.p['title'], c.w - 2 * c.pad)
    c.y = c.pad
    c.y += c.lines(c.w / 2, c.y, lines, size=c.p['title'], weight=800)
    # the underline in the theme's gradient colors marks the title
    c.parts.append(f'<rect x="{c.w / 2 - c.w * 0.12}" y="{c.y + 8}" width="{c.w * 0.24}" height="4" rx="2" '
                   f'fill="{PALETTE["purple"][1]}"/>')
    c.y += c.pad


def footer(c, spec):
    if spec.get('caption'):
        lines = c.wrap(spec['caption'], c.p['small'], c.w - 2 * c.pad)
        c.y += c.lines(c.w / 2, c.y, lines, size=c.p['small'], fill=SOFT, italic=True)


def box_with_text(c, x, y, w, text, color, size=None, weight=500, dashed=False):
    size = size or c.p['body']
    lines = c.wrap(text, size, w - 2 * 14)
    h = len(lines) * size * 1.3 + 2 * 14
    c.rect(x, y, w, h, color, dashed=dashed)
    c.lines(x + w / 2, y + 14 - size * 0.2, lines, size=size, weight=weight, fill=PALETTE[color][2]
            if color != 'gray' else INK)
    return h


def flow(c, spec):
    steps = spec['steps']
    has_side = any(s.get('side') for s in steps)
    col = c.w * (0.56 if has_side else 0.8)
    x = c.pad if has_side else (c.w - col) / 2
    side_x = x + col + c.pad * 1.5
    side_w = c.w - side_x - c.pad
    gap = c.p['body'] * 2.4
    for i, s in enumerate(steps):
        kind = s.get('kind', 'step')
        color = s.get('color') or KIND_COLOR.get(kind, 'blue')
        top = c.y
        if kind == 'decision':
            # a diamond narrower than the boxes, so the decision stands out without dominating
            dw = col * 0.78
            lines = c.wrap(s['text'], c.p['body'], dw * 0.6)
            h = len(lines) * c.p['body'] * 1.3 + c.p['body'] * 2.6
            c.diamond(x + col / 2, top, dw, h, color)
            c.lines(x + col / 2, top + h / 2 - len(lines) * c.p['body'] * 0.65 - c.p['body'] * 0.2, lines,
                    weight=600, fill=PALETTE[color][2])
            right_edge = x + col / 2 + dw / 2
        else:
            h = box_with_text(c, x, top, col, s['text'], color, weight=600 if kind != 'step' else 500)
            right_edge = x + col
        if s.get('side'):
            side_h = box_with_text(c, side_x, top + h / 2 - c.p['body'] * 1.15, side_w, s['side'], 'red')
            c.arrow(right_edge, top + h / 2, side_x, top + h / 2, s.get('side_label', ''), 'red')
            h = max(h, side_h)
        c.y = top + h
        if i + 1 < len(steps):
            c.arrow(x + col / 2, c.y, x + col / 2, c.y + gap, s.get('label', ''), 'gray')
            c.y += gap
    c.y += c.pad
    return len(steps)


def timeline(c, spec):
    events = spec['events']
    line_x = c.pad + c.p['body'] * 0.6
    text_x = line_x + c.p['body'] * 1.6
    start = c.y
    for e in events:
        color = 'purple' if e.get('highlight') else 'blue'
        c.parts.append(f'<circle cx="{line_x}" cy="{c.y + c.p["body"] * 0.7}" r="{c.p["body"] * 0.45}" '
                       f'fill="{PALETTE[color][0]}" stroke="{PALETTE[color][2]}" stroke-width="2.5"/>')
        # the date on its own line, the event below it
        c.text(text_x, c.y + c.p['body'], e['when'], weight=800, anchor='start', fill=PALETTE[color][2])
        lines = c.wrap(e['text'], c.p['body'], c.w - text_x - c.pad)
        c.y += c.p['body'] * 1.45
        c.y += c.lines(text_x, c.y, lines, anchor='start') + c.p['body'] * 1.1
    c.parts.insert(0, f'<line x1="{line_x}" y1="{start}" x2="{line_x}" y2="{c.y - c.p["body"]}" '
                      f'stroke="{PALETTE["gray"][1]}" stroke-width="3"/>')
    c.y += c.pad / 2
    return len(events)


def compare(c, spec):
    wrong_right = spec.get('style') == 'wrong-right'
    sides = []
    for key, mark, default in (('left', '❌ ', 'red'), ('right', '✅ ', 'green')):
        side = spec.get(key) or {}
        color = side.get('color') or (default if wrong_right else ('blue' if key == 'left' else 'purple'))
        sides.append(((mark if wrong_right else '') + str(side.get('title', '')), color))
    col = (c.w - 3 * c.pad) / 2
    xs = (c.pad, 2 * c.pad + col)
    for i, row in enumerate(spec['rows'], 1):
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError(f'compare row {i} must have exactly 2 values, left and right')
    heights = []
    for (title, color), x in zip(sides, xs, strict=True):
        heights.append(box_with_text(c, x, c.y, col, title, color, weight=800))
    c.y += max(heights) + c.p['body'] * 0.6
    for row in spec['rows']:
        h = max(len(c.wrap(value, c.p['body'], col - 28)) * c.p['body'] * 1.3 + 22 for value in row)
        for (_, color), x, value in zip(sides, xs, row, strict=True):
            c.rect(x, c.y, col, h, color, rx=10, shadow=False)
            c.lines(x + col / 2, c.y + 11 - c.p['body'] * 0.2, c.wrap(value, c.p['body'], col - 28))
        c.y += h + c.p['body'] * 0.5
    c.y += c.pad / 2
    return len(spec['rows'])


def boxes(c, spec):
    cells = spec['cells']
    size = min((c.w - 2 * c.pad) / max(len(cells), 1), c.p['body'] * 5)
    x0 = (c.w - size * len(cells)) / 2
    if spec.get('name'):
        c.text(x0, c.y + c.p['body'], spec['name'], weight=700, anchor='start', mono=True, fill=PALETTE['blue'][2])
        c.y += c.p['body'] * 1.8
    for i, cell in enumerate(cells):
        color = 'purple' if cell.get('highlight') else 'blue'
        c.rect(x0 + i * size, c.y, size, size, color, rx=6, shadow=False)
        value = str(cell['value'])
        if c.width_of(value, c.p['body'], mono=True) > size - 8:
            c.problems.append(f'value "{value}" does not fit in its box ({round(size)} px)')
        c.text(x0 + i * size + size / 2, c.y + size / 2 + c.p['body'] * 0.35, value, mono=True, weight=700)
        if 'label' in cell:
            c.text(x0 + i * size + size / 2, c.y + size + c.p['small'] * 1.4, cell['label'], size=c.p['small'],
                   fill=SOFT)
    c.y += size + c.p['small'] * 2.4 + c.pad / 2
    return 1


def layers(c, spec):
    for i, layer in enumerate(spec['layers']):
        color = layer.get('color') or ('purple', 'blue', 'teal', 'green', 'orange', 'gray')[i % 6]
        text = layer['text'] + (f'  ·  {layer["note"]}' if layer.get('note') else '')
        c.y += box_with_text(c, c.pad, c.y, c.w - 2 * c.pad, text, color, weight=600) + c.p['body'] * 0.5
    c.y += c.pad / 2
    return len(spec['layers'])


def tree(c, spec):
    count = [0]
    indent = c.p['body'] * 1.8

    def node(n, depth, parent_mid):
        count[0] += 1
        x = c.pad + depth * indent
        w = c.w - x - c.pad
        top = c.y
        color = n.get('color') or ('purple' if depth == 0 else ('blue', 'teal', 'green', 'orange')[(depth - 1) % 4])
        h = box_with_text(c, x, top, w, n['text'], color, weight=700 if depth == 0 else 500)
        if parent_mid is not None:
            px = x - indent / 2
            c.parts.append(f'<path d="M{px},{parent_mid} V{top + h / 2} H{x}" fill="none" '
                           f'stroke="{PALETTE["gray"][1]}" stroke-width="2"/>')
        c.y = top + h + c.p['body'] * 0.5
        for child in n.get('children') or []:
            node(child, depth + 1, top + h)
    node(spec['root'], 0, None)
    c.y += c.pad / 2
    return count[0]


def sequence(c, spec):
    names = spec['participants']
    if len(names) > 4:
        c.problems.append(f'{len(names)} participants: at most 4 fit side by side')
    col = (c.w - 2 * c.pad) / len(names)
    centers = {name: c.pad + col * i + col / 2 for i, name in enumerate(names)}
    head_h = max(box_with_text(c, c.pad + col * i + 6, c.y, col - 12, name, 'purple', weight=700)
                 for i, name in enumerate(names))
    c.y += head_h
    top = c.y
    c.y += c.p['body'] * 1.6
    for i, m in enumerate(spec['messages'], 1):
        x1, x2 = centers[m['from']], centers[m['to']]
        label = f'{i}. {m["text"]}'
        if c.width_of(label, c.p['small']) > abs(x2 - x1) + col * 0.8:
            c.problems.append(f'message "{m["text"]}" is longer than the space between {m["from"]} and {m["to"]}')
        c.text((x1 + x2) / 2, c.y - 8, label, size=c.p['small'], fill=INK, weight=600)
        c.arrow(x1, c.y, x2, c.y, '', 'gray', dashed=m.get('dashed', False))
        c.y += c.p['body'] * 2.2
    for x in centers.values():
        c.parts.insert(0, f'<line x1="{x}" y1="{top}" x2="{x}" y2="{c.y}" stroke="{PALETTE["gray"][1]}" '
                          f'stroke-width="2" stroke-dasharray="6 6"/>')
    c.y += c.pad / 2
    return len(spec['messages'])


def bars(c, spec):
    items = spec['bars']
    top = max(float(b['value']) for b in items) or 1
    label_w = (c.w - 2 * c.pad) * 0.3
    bar_w = c.w - 2 * c.pad - label_w - c.p['body'] * 4
    for b in items:
        color = 'purple' if b.get('highlight') else 'blue'
        h = c.p['body'] * 1.6
        c.text(c.pad + label_w - 10, c.y + h * 0.7, b['label'], anchor='end')
        if c.width_of(str(b['label']), c.p['body']) > label_w - 10:
            c.problems.append(f'bar label "{b["label"]}" is too long')
        length = max(2, bar_w * float(b['value']) / top)
        c.rect(c.pad + label_w, c.y, length, h, color, rx=6, shadow=False)
        c.text(c.pad + label_w + length + 8, c.y + h * 0.7, f'{b["value"]}{spec.get("unit", "")}', anchor='start',
               weight=700, fill=PALETTE[color][2])
        c.y += h + c.p['body'] * 0.6
    c.y += c.pad / 2
    return len(items)


def cards(c, spec, profile):
    items = spec['cards']
    columns = 3 if profile == 'large' else 2
    gap = c.pad / 2
    w = (c.w - 2 * c.pad - (columns - 1) * gap) / columns
    size, small = c.p['body'] * 0.85, c.p['small'] * 0.95
    colors = ('blue', 'purple', 'teal', 'green', 'orange', 'red')
    rows = [items[i:i + columns] for i in range(0, len(items), columns)]
    for r, row in enumerate(rows):
        heights = []
        for k, card in enumerate(row):
            title = c.wrap(f'{r * columns + k + 1}. {card["title"]}', size, w - 2 * 14)
            body = [line for item in card.get('items', []) for line in c.wrap(f'✓ {item}', small, w - 2 * 14)]
            code = [line for line in card.get('code', [])]
            for line in code:
                if c.width_of(line, small, mono=True) > w - 2 * 20:
                    c.problems.append(f'code "{line}" does not fit in a card')
            heights.append((len(title) * size + len(body) * small + len(code) * small) * 1.3 + 3.2 * size)
        h = max(heights)
        for k, card in enumerate(row):
            x = c.pad + k * (w + gap)
            color = colors[(r * columns + k) % len(colors)]
            c.rect(x, c.y, w, h, color, rx=14)
            icon = str(card.get('icon', ''))[:4]
            c.text(x + w - 14, c.y + size * 1.4, icon, size=small, mono=True, anchor='end', weight=700,
                   fill=PALETTE[color][2])
            y = c.y + 10
            y += c.lines(x + 14, y, c.wrap(f'{r * columns + k + 1}. {card["title"]}', size, w - 2 * 14),
                         size=size, anchor='start', weight=800, fill=PALETTE[color][2])
            for item in card.get('items', []):
                y += c.lines(x + 14, y, c.wrap(f'✓ {item}', small, w - 2 * 14), size=small, anchor='start')
            if card.get('code'):
                code_h = len(card['code']) * small * 1.3 + 8
                c.parts.append(f'<rect x="{x + 12}" y="{y + 6}" width="{w - 24}" height="{code_h}" rx="6" '
                               f'fill="#F0F0F0"/>')
                c.lines(x + 20, y + 6, card['code'], size=small, anchor='start', mono=True)
        c.y += h + gap
    c.y += c.pad / 2
    if len(items) > 12:
        c.problems.append(f'{len(items)} cards: a cheat sheet holds at most 12')
    return 0  # cards are a reference sheet, not a diagram to take in at a glance


LAYOUTS = {'flow': flow, 'timeline': timeline, 'compare': compare, 'boxes': boxes, 'layers': layers,
           'tree': tree, 'sequence': sequence, 'bars': bars}
REQUIRED = {'flow': 'steps', 'timeline': 'events', 'compare': 'rows', 'boxes': 'cells', 'layers': 'layers',
            'tree': 'root', 'sequence': 'messages', 'bars': 'bars', 'cards': 'cards'}


def boolean_keys(value, path='spec'):
    """YAML reads keys such as no, yes, on and off as booleans: the field would vanish silently."""
    if isinstance(value, dict):
        for k, v in value.items():
            if isinstance(k, bool):
                raise ValueError(f'{path} has a key read as {k} (a key named yes/no/on/off): rename it or quote it')
            boolean_keys(v, f'{path}.{k}')
    elif isinstance(value, list):
        for i, v in enumerate(value):
            boolean_keys(v, f'{path}[{i}]')


def render(spec, profile='large'):
    """Returns (svg text, height, problems, warnings)."""
    boolean_keys(spec)
    kind = spec.get('type')
    if kind not in TYPES:
        raise ValueError(f'type must be one of {", ".join(TYPES)}')
    for key in ('title', REQUIRED[kind]):
        if not spec.get(key):
            raise ValueError(f'a {kind} spec needs "{key}"')
    c = Canvas(profile)
    header(c, spec)
    elements = cards(c, spec, profile) if kind == 'cards' else LAYOUTS[kind](c, spec)
    footer(c, spec)
    text, height = c.svg(spec['title'], spec.get('caption', ''), spec.get('alt', ''))
    warnings = []
    if elements > MAX_ELEMENTS:
        warnings.append(f'{elements} elements: more than ~{MAX_ELEMENTS} overloads the reader; split in two')
    if profile == 'small' and kind != 'cards' and height > 640:
        warnings.append(f'{height} px tall: on a 6-inch screen it will be split across pages; split it')
    return text, height, c.problems, warnings


def book_profile(path):
    """The reading profile of the book a spec belongs to, or None."""
    d = os.path.dirname(os.path.abspath(path))
    for _ in range(4):
        if os.path.exists(os.path.join(d, 'book.yaml')):
            return (load_yaml(os.path.join(d, 'book.yaml')).get('choices') or {}).get('reading')
        d = os.path.dirname(d)
    return None


def target_for(spec_path):
    folder, name = os.path.split(os.path.abspath(spec_path))
    stem = os.path.splitext(name)[0]
    if os.path.basename(folder) == '_source':
        folder = os.path.dirname(folder)
    return os.path.join(folder, stem + '.svg')


def contact_sheet(book_dir, n):
    path = chapter_path(book_dir, n)
    if not path:
        fail(f'chapter {n} has no file yet')
    names = re.findall(r'\]\(\.\./img/([^)\s]+\.svg)\)', open(path, encoding='utf-8').read())
    if not names:
        out({'chapter': n, 'images': 0, 'note': 'the chapter has no SVG images'})
    tile, gap, cols = 480, 24, 2
    rows = (len(names) + cols - 1) // cols
    parts = []
    for i, name in enumerate(names):
        data = base64.b64encode(open(os.path.join(book_dir, 'img', name), 'rb').read()).decode()
        x, y = gap + (i % cols) * (tile + gap), gap + (i // cols) * (tile + 2 * gap)
        parts.append(f'<image x="{x}" y="{y}" width="{tile}" height="{tile}" href="data:image/svg+xml;base64,{data}"/>'
                     f'<text x="{x}" y="{y + tile + 18}" font-family="sans-serif" font-size="14">{escape(name)}</text>')
    w, h = cols * (tile + gap) + gap, rows * (tile + 2 * gap) + gap
    sheet = os.path.join(book_dir, 'img', '_source', f'_sheet-c{n:02d}.svg')
    os.makedirs(os.path.dirname(sheet), exist_ok=True)
    with open(sheet, 'w', encoding='utf-8') as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">'
                f'<rect width="100%" height="100%" fill="white"/>{"".join(parts)}</svg>')
    result = {'chapter': n, 'images': len(names), 'sheet': sheet}
    png = sheet[:-4] + '.png'
    if to_png(sheet, png):
        result['png'] = png
    else:
        result['note'] = 'no SVG to PNG converter available: open the SVG sheet instead'
    out(result)


def to_png(svg, png):
    """Renders an SVG to PNG so Claude can look at it; resvg works on every system, without native libraries."""
    try:
        import resvg_py
    except ImportError:
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet', 'resvg-py'], check=True,
                           capture_output=True)
            import resvg_py
        except (subprocess.CalledProcessError, ImportError):
            resvg_py = None
    if resvg_py:
        with open(png, 'wb') as f:
            f.write(bytes(resvg_py.svg_to_bytes(svg_path=svg)))
        return True
    if shutil.which('rsvg-convert'):
        subprocess.run(['rsvg-convert', '-o', png, svg], check=True)
        return True
    return False


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('spec', nargs='?')
    p.add_argument('--reading', choices=sorted(PROFILES))
    p.add_argument('--out')
    p.add_argument('--sheet', type=int, metavar='CHAPTER')
    p.add_argument('--book')
    args = p.parse_args()
    if args.sheet:
        book_dir, _ = find_book(args.book)
        contact_sheet(book_dir, args.sheet)
    if not args.spec:
        p.error('give a spec file, or --sheet <chapter>')
    if not os.path.exists(args.spec):
        fail(f'spec not found: {args.spec}')
    profile = args.reading or book_profile(args.spec) or 'large'
    try:
        text, height, problems, warnings = render(load_yaml(args.spec), profile)
    except (ValueError, KeyError, TypeError) as e:
        fail(f'invalid spec: {e}')
    target = args.out or target_for(args.spec)
    os.makedirs(os.path.dirname(target) or '.', exist_ok=True)
    with open(target, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
    out({'svg': target, 'profile': profile, 'width': PROFILES[profile]['width'], 'height': height,
         'fits': not problems, 'problems': problems, 'warnings': warnings}, 1 if problems else 0)


if __name__ == '__main__':
    main()
