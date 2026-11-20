#!/usr/bin/env python3
"""Draws an SVG diagram from a short YAML spec, in the books' visual theme.

Usage:
  python scripts/diagram.py <spec.yaml> [--reading large|small] [--out FILE]
  python scripts/diagram.py --sheet <chapter> [--book B]    one contact sheet with the chapter's images
  python scripts/diagram.py --icons    lists the icon names for the "icon" fields
  python scripts/diagram.py --help

Every spec has: type, title (the idea in one sentence), and optionally subtitle (a short line under the
title) and caption (a closing line in italics). The width follows the book's reading profile (large 960,
small 480). A spec in img/_source/<name>.yaml is drawn to img/<name>.svg.

Boxes take `text` (bold) and an optional `note` (a smaller line below) and `icon` (a name from --icons):
the icon anchors each idea at a glance and still reads on a grayscale screen.

Types and their fields:
  flow      steps: [{text, note, icon, kind: start|step|decision|end, color, label,
                     side, side_note, side_icon, side_color, side_label}]
            a decision's `side` is drawn as a box to the right (the other way out; red unless side_color);
            `label` names the arrow to the next step (e.g. "não")
  timeline  events: [{when, text, icon, highlight}]
  compare   left: {title, icon, color}, right: {title, icon, color}, rows: [[left, right], ...]
            style: wrong-right marks the left column with a red x icon and the right one with a green check
  boxes     cells: [{value, label, highlight}], name (above the boxes, e.g. a variable)
  layers    layers: [{text, note, icon, color}]   (top to bottom)
  tree      root: {text, note, icon, color, children: [...]}
  sequence  participants: [name or {name, icon}, at most 4], messages: [{from, to, text, dashed}]
  bars      bars: [{label, value, highlight}], unit
  cards     cards: [{icon, title, items: [text or {text, icon}], code: [...], scene}]   (the cheat sheet,
            up to 12; icon = a name from --icons, or up to 4 characters such as "for")
  scene     steps: [[icon, ...], ...] (up to 4 steps of 1-3 icons), ops: [→ + = ↔], label
            a scene shows a relation with icons (folder → files, A + B = C); in a card, `scene` is
            {steps, ops, label} or just the list of steps, and goes under the items. It demonstrates the
            idea, never decorates.

Colors: blue (input, structure), green (right, output, end), orange (decision, attention),
red (error), purple (central idea), teal, gray (neutral). Prints JSON with the file written,
its size and any text that does not fit or icon name that does not exist; exit code 1 then.
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
import icons
from common import chapter_path, fail, find_book, load_yaml, out

BG = '#FAF9F6'
INK, SOFT = '#2B2B33', '#55555F'
# fill (inner boxes), border, strong (text, icons and arrows on that color), tint (the box itself, stronger)
PALETTE = {
    'blue': ('#EAF1FF', '#7FA8F0', '#1F4E9C', '#D3E2FF'),
    'green': ('#E4F6EC', '#6FC39C', '#17694A', '#C9ECD9'),
    'orange': ('#FFF5D9', '#E2B84A', '#6E4D00', '#FFE7A6'),
    'red': ('#FFEBE4', '#EE9478', '#963019', '#FFD3C5'),
    'purple': ('#F2EBFC', '#A989E6', '#4F2F8C', '#E0D1F8'),
    'teal': ('#E2F5F5', '#74C2C2', '#125B5B', '#C6E9E9'),
    'gray': ('#F4F2ED', '#B9B2A5', '#45454F', '#E4E0D6'),
}
# the title underline: the theme colors left to right
GRADIENT = ('blue', 'purple', 'red', 'orange')
KIND_COLOR = {'start': 'gray', 'step': 'blue', 'decision': 'orange', 'end': 'green'}
# sizes per reading profile: width, body, title, small text; a 6" screen needs bigger letters
PROFILES = {'large': {'width': 960, 'body': 20, 'title': 26, 'small': 16},
            'small': {'width': 480, 'body': 14, 'title': 17, 'small': 12.5}}
MAX_ELEMENTS = 7  # references/VISUALS.md: more than ~7 main elements overloads the reader
TYPES = ('flow', 'timeline', 'compare', 'boxes', 'layers', 'tree', 'sequence', 'bars', 'cards', 'scene')
SCENE_OPS = ('→', '+', '=', '↔')


class Canvas:
    def __init__(self, profile):
        self.p = PROFILES[profile]
        self.w = self.p['width']
        self.pad = round(self.w * 0.04)
        self.parts, self.problems, self.y = [], [], 0

    # text measures: an average sans-serif letter is ~0.56 em wide, a monospace one 0.6 em
    def width_of(self, text, size, mono=False):
        return len(text) * size * (0.6 if mono else 0.56)

    def wrap(self, text, size, width, mono=False, report=True):
        """Splits text into lines that fit the width; reports a word that cannot fit at all (unless report=False,
        for measuring before drawing)."""
        text = str(text)
        limit = max(1, int(width / (size * (0.6 if mono else 0.56))))
        lines, line = [], ''
        for word in text.split():
            if len(word) > limit and report:
                self.problems.append(f'"{word}" does not fit in {round(width)} px: shorten it or widen the box')
            candidate = f'{line} {word}'.strip()
            if len(candidate) <= limit or not line:
                line = candidate
            else:
                lines.append(line)
                line = word
        return lines + [line] if line or not lines else lines

    def rect(self, x, y, w, h, color='gray', rx=12, dashed=False, shadow=True, tint=False):
        fill, border, _, strong_fill = PALETTE[color]
        fill = strong_fill if tint else fill
        if shadow:
            self.parts.append(f'<rect x="{x}" y="{y + 4}" width="{w}" height="{h}" rx="{rx}" '
                              f'fill="#3A3226" opacity="0.07"/>')
        dash = ' stroke-dasharray="9 6"' if dashed else ''
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" '
                          f'stroke="{border}" stroke-width="2"{dash}/>')

    def diamond(self, cx, y, w, h, color='orange'):
        _, border, _, fill = PALETTE[color]
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

    def shift(self, start, dy):
        """Moves everything drawn since parts[start] down by dy (up when negative)."""
        if dy:
            self.parts[start:] = [f'<g transform="translate(0,{dy:g})">' + ''.join(self.parts[start:]) + '</g>']

    def unknown_icon(self, name):
        near = icons.suggest(name)
        self.problems.append(f'unknown icon "{name}"' + (f' (did you mean {", ".join(near)}?)' if near else ''))

    def icon(self, name, x, y, size, color):
        """Draws a named icon in the color's strong tone; an unknown name is reported, with suggestions."""
        if not icons.known(name):
            self.unknown_icon(name)
            return False
        self.parts.append(icons.draw(name, x, y, size, PALETTE[color][2]))
        return True

    def arrow(self, x1, y1, x2, y2, label='', color='gray', dashed=False, both=False):
        strong = PALETTE[color][2]
        dash = ' stroke-dasharray="9 6"' if dashed else ''
        start = f' marker-start="url(#arrow-{color})"' if both else ''
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{strong}" stroke-width="2.5"'
                          f'{dash}{start} marker-end="url(#arrow-{color})"/>')
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
        stops = ''.join(f'<stop offset="{i / (len(GRADIENT) - 1):g}" stop-color="{PALETTE[c][1]}"/>'
                        for i, c in enumerate(GRADIENT))
        gradient = f'<linearGradient id="underline" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>'
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{height}" '
                f'viewBox="0 0 {self.w} {height}" role="img">'
                f'<title>{escape(title)}</title><desc>{escape(alt or caption or title)}</desc>'
                f'<defs>{markers}{gradient}</defs><rect width="100%" height="100%" fill="{BG}"/>'
                + ''.join(self.parts) + '</svg>\n'), height


# ---------- layouts ----------

def header(c, spec):
    lines = c.wrap(spec['title'], c.p['title'], c.w - 2 * c.pad)
    c.y = c.pad
    c.y += c.lines(c.w / 2, c.y, lines, size=c.p['title'], weight=800)
    if spec.get('subtitle'):
        sub = c.wrap(spec['subtitle'], c.p['small'], c.w - 2 * c.pad)
        c.y += c.p['small'] * 0.3 + c.lines(c.w / 2, c.y, sub, size=c.p['small'], fill=SOFT)
    # the underline in the theme's gradient colors marks the title
    c.parts.append(f'<rect x="{c.w / 2 - c.w * 0.12}" y="{c.y + 8}" width="{c.w * 0.24}" height="5" rx="2.5" '
                   f'fill="url(#underline)"/>')
    c.y += c.pad


def footer(c, spec):
    if spec.get('caption'):
        lines = c.wrap(spec['caption'], c.p['small'], c.w - 2 * c.pad)
        c.y += c.lines(c.w / 2, c.y, lines, size=c.p['small'], fill=SOFT, italic=True)


def box_with_text(c, x, y, w, text, color, size=None, weight=500, dashed=False, note=None, icon=None):
    """A box with its text in bold tone, an optional smaller note below and an optional icon on the left.
    Returns the height. With an icon the text is left-aligned after it; otherwise it is centered."""
    size = size or c.p['body']
    small = c.p['small']
    icon_w = size * 1.3 + 10 if icon else 0
    inner = w - 2 * 14 - icon_w
    lines = c.wrap(text, size, inner)
    notes = c.wrap(note, small, inner) if note else []
    text_h = len(lines) * size * 1.3 + (len(notes) * small * 1.3 + small * 0.2 if notes else 0)
    h = max(text_h, size * 1.3 if icon else 0) + 2 * 14
    c.rect(x, y, w, h, color, dashed=dashed, tint=True)
    ink = PALETTE[color][2] if color != 'gray' else INK
    if icon:
        c.icon(icon, x + 14, y + h / 2 - size * 0.65, size * 1.3, color)
        tx, anchor = x + 14 + icon_w, 'start'
    else:
        tx, anchor = x + w / 2, 'middle'
    top = y + h / 2 - text_h / 2 - size * 0.2
    used = c.lines(tx, top, lines, size=size, weight=weight, fill=ink, anchor=anchor)
    if notes:
        c.lines(tx, top + used + small * 0.2, notes, size=small, fill=SOFT, anchor=anchor)
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
            size = c.p['body']
            # the question on one line when it fits, at the body size or a little smaller, before wrapping
            if c.width_of(s['text'], size) > dw * 0.75 and c.width_of(s['text'], c.p['small']) <= dw * 0.75:
                size = c.p['small']
            one_line = c.width_of(s['text'], size) <= dw * 0.75
            lines = c.wrap(s['text'], size, dw * 0.75 if one_line else dw * 0.6)
            notes = c.wrap(s['note'], c.p['small'], dw * 0.72) if s.get('note') else []
            text_h = len(lines) * size * 1.3 + len(notes) * c.p['small'] * 1.3
            h = text_h + c.p['body'] * 2.6
            c.diamond(x + col / 2, top, dw, h, color)
            y0 = top + h / 2 - text_h / 2 - size * 0.2
            used = c.lines(x + col / 2, y0, lines, size=size, weight=700, fill=PALETTE[color][2])
            if notes:
                c.lines(x + col / 2, y0 + used, notes, size=c.p['small'], fill=SOFT)
            right_edge = x + col / 2 + dw / 2
        else:
            h = box_with_text(c, x, top, col, s['text'], color, weight=700 if kind != 'step' else 600,
                              note=s.get('note'), icon=s.get('icon'))
            right_edge = x + col
        if s.get('side'):
            side_color = s.get('side_color', 'red')
            start = len(c.parts)
            side_h = box_with_text(c, side_x, top, side_w, s['side'], side_color, weight=700,
                                   note=s.get('side_note'), icon=s.get('side_icon'))
            # drawn at the top, then moved so it is centered on the decision
            c.shift(start, h / 2 - side_h / 2)
            c.arrow(right_edge, top + h / 2, side_x, top + h / 2, s.get('side_label', ''), side_color)
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
        r = c.p['body'] * (0.75 if e.get('icon') else 0.45)
        cy = c.y + c.p['body'] * 0.7
        c.parts.append(f'<circle cx="{line_x}" cy="{cy}" r="{r}" '
                       f'fill="{PALETTE[color][3]}" stroke="{PALETTE[color][2]}" stroke-width="2.5"/>')
        if e.get('icon'):
            c.icon(e['icon'], line_x - r * 0.65, cy - r * 0.65, r * 1.3, color)
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
    for key, mark, default in (('left', 'circle-x', 'red'), ('right', 'circle-check', 'green')):
        side = spec.get(key) or {}
        color = side.get('color') or (default if wrong_right else ('blue' if key == 'left' else 'purple'))
        # wrong-right marks each side with a drawn icon (an emoji depends on the reader's fonts)
        sides.append((str(side.get('title', '')), color, side.get('icon') or (mark if wrong_right else None)))
    col = (c.w - 3 * c.pad) / 2
    xs = (c.pad, 2 * c.pad + col)
    for i, row in enumerate(spec['rows'], 1):
        if not isinstance(row, list) or len(row) != 2:
            raise ValueError(f'compare row {i} must have exactly 2 values, left and right')
    heights = []
    for (title, color, icon), x in zip(sides, xs, strict=True):
        heights.append(box_with_text(c, x, c.y, col, title, color, weight=800, icon=icon))
    c.y += max(heights) + c.p['body'] * 0.6
    for row in spec['rows']:
        h = max(len(c.wrap(value, c.p['body'], col - 28)) * c.p['body'] * 1.3 + 22 for value in row)
        for (_, color, _), x, value in zip(sides, xs, row, strict=True):
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
        c.rect(x0 + i * size, c.y, size, size, color, rx=6, shadow=False, tint=True)
        if cell.get('highlight'):
            # the focus: a thicker border in the strong tone
            c.parts.append(f'<rect x="{x0 + i * size + 1.5}" y="{c.y + 1.5}" width="{size - 3}" height="{size - 3}" '
                           f'rx="5" fill="none" stroke="{PALETTE[color][2]}" stroke-width="3"/>')
        value = str(cell['value'])
        if c.width_of(value, c.p['body'], mono=True) > size - 8:
            c.problems.append(f'value "{value}" does not fit in its box ({round(size)} px)')
        c.text(x0 + i * size + size / 2, c.y + size / 2 + c.p['body'] * 0.35, value, mono=True, weight=700)
        if 'label' in cell:
            # the index in a small gray badge under its box
            label = str(cell['label'])
            bw = max(c.width_of(label, c.p['small']) + 14, c.p['small'] * 1.8)
            cx = x0 + i * size + size / 2
            c.parts.append(f'<rect x="{cx - bw / 2}" y="{c.y + size + 6}" width="{bw}" height="{c.p["small"] * 1.5}" '
                           f'rx="{c.p["small"] * 0.75}" fill="{PALETTE["gray"][3]}"/>')
            c.text(cx, c.y + size + 6 + c.p['small'] * 1.1, label, size=c.p['small'], fill=INK, weight=600)
    c.y += size + c.p['small'] * 2.4 + c.pad / 2
    return 1


def layers(c, spec):
    for i, layer in enumerate(spec['layers']):
        color = layer.get('color') or ('purple', 'blue', 'teal', 'green', 'orange', 'gray')[i % 6]
        c.y += box_with_text(c, c.pad, c.y, c.w - 2 * c.pad, layer['text'], color, weight=700,
                             note=layer.get('note'), icon=layer.get('icon')) + c.p['body'] * 0.5
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
        h = box_with_text(c, x, top, w, n['text'], color, weight=700 if depth == 0 else 600, note=n.get('note'),
                          icon=n.get('icon'))
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
    # a participant is a name, or {name, icon}
    people = [p if isinstance(p, dict) else {'name': p} for p in spec['participants']]
    names = [p['name'] for p in people]
    if len(names) > 4:
        c.problems.append(f'{len(names)} participants: at most 4 fit side by side')
    col = (c.w - 2 * c.pad) / len(names)
    centers = {name: c.pad + col * i + col / 2 for i, name in enumerate(names)}
    head_h = max(box_with_text(c, c.pad + col * i + 6, c.y, col - 12, p['name'], 'purple', weight=700,
                               icon=p.get('icon')) for i, p in enumerate(people))
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


def scene_size(c, w, scene):
    """(tile size, gap between tiles, total height) of a scene drawn in width w."""
    n = max(len(scene.get('steps') or []), 1)
    tile = min(w / (n + (n - 1) * 0.7), c.p['body'] * 4)
    label = 0
    if scene.get('label'):
        label = len(c.wrap(scene['label'], c.p['small'], w, report=False)) * c.p['small'] * 1.3 + c.p['small'] * 0.7
    return tile, tile * 0.7, tile + label


def scene_block(c, x, y, w, scene, color=None):
    """A short row of icons joined by arrows or by + and =, which shows an idea (folder -> files, A + B = C).
    Each step is a list of 1 to 3 icons stacked in one tile. Returns the height."""
    steps = scene.get('steps') or []
    ops = scene.get('ops') or ['→'] * (len(steps) - 1)
    if len(steps) > 4:
        c.problems.append(f'{len(steps)} steps: a scene holds at most 4 steps')
    for op in ops:
        if op not in SCENE_OPS:
            c.problems.append(f'scene op "{op}" must be one of {" ".join(SCENE_OPS)}')
    tile, gap, height = scene_size(c, w, scene)
    x0 = x + (w - (len(steps) * tile + (len(steps) - 1) * gap)) / 2
    cycle = ('blue', 'purple', 'teal', 'green')
    for i, step in enumerate(steps):
        names = step if isinstance(step, list) else [step]
        if not 1 <= len(names) <= 3:
            c.problems.append(f'step {i + 1} has {len(names)} icons: a scene step holds 1 to 3 icons')
        tone = color or cycle[i % len(cycle)]
        tx = x0 + i * (tile + gap)
        c.rect(tx, y, tile, tile, tone, rx=tile * 0.18, shadow=False, tint=color is None)
        shown = names[:3]
        size = min(tile * 0.58, tile * 0.84 / max(len(shown), 1))
        top = y + tile / 2 - size * len(shown) / 2
        for k, name in enumerate(shown):
            c.icon(name, tx + tile / 2 - size * 0.46, top + k * size + size * 0.04, size * 0.92, tone)
        if i + 1 < len(steps):
            op = ops[i] if i < len(ops) else '→'
            mid, left, right = y + tile / 2, tx + tile + gap * 0.18, tx + tile + gap * 0.82
            if op in ('+', '='):
                c.text((left + right) / 2, mid + c.p['title'] * 0.36, op, size=c.p['title'] * 1.1, weight=800,
                       fill=PALETTE[color or 'gray'][2])
            else:
                c.arrow(left, mid, right, mid, color=color or 'gray', both=op == '↔')
    if scene.get('label'):
        c.lines(x + w / 2, y + tile + c.p['small'] * 0.4, c.wrap(scene['label'], c.p['small'], w), size=c.p['small'],
                fill=SOFT, weight=600)
    return height


def scene(c, spec):
    c.y += scene_block(c, c.pad, c.y, c.w - 2 * c.pad, spec) + c.pad / 2
    return len(spec['steps'])


def card_layout(c, card, number, w, size, small):
    """Measures one cheat-sheet card once (wrapping reports problems, so it must run only once).
    A scene goes below the items, across the card: beside them it squeezes the text in a 3-column sheet."""
    icon = str(card.get('icon', '') or '')
    if len(icon) > 4 and not icons.known(icon):
        # up to 4 characters is a text mark ("for", "[ ]"); longer is meant as an icon name, so a typo is reported
        c.unknown_icon(icon)
    scene = card.get('scene')
    if isinstance(scene, list):
        scene = {'steps': scene}
    elif scene is not None and not isinstance(scene, dict):
        raise ValueError(f'card {number} scene must be {{steps, ops, label}} or a list of steps')
    badge = size * 2.1 if icon else 0
    inner = w - 2 * 14
    title = c.wrap(f'{number}. {card["title"]}', size, inner - (badge + 10 if badge else 0))
    items = []
    for item in card.get('items', []):
        text, mark = (item.get('text', ''), item.get('icon')) if isinstance(item, dict) else (item, None)
        items.append((mark or 'circle-check', c.wrap(text, small, inner - small * 1.7)))
    code = list(card.get('code', []))
    for line in code:
        if c.width_of(line, small, mono=True) > inner - 12:
            c.problems.append(f'code "{line}" does not fit in a card')
    head = max(badge, len(title) * size * 1.3)
    body = sum(len(lines) for _, lines in items) * small * 1.45 + (len(code) * small * 1.3 + 14 if code else 0)
    scene_h = scene_size(c, inner, scene)[2] + small if scene else 0
    h = 14 + head + small * 0.6 + body + scene_h + 14
    return {'icon': icon, 'badge': badge, 'inner': inner, 'title': title, 'items': items,
            'code': code, 'head': head, 'h': h, 'scene': scene}


def draw_card(c, card, lay, x, y, w, h, color, size, small):
    c.rect(x, y, w, h, color, rx=14, tint=True)
    strong = PALETTE[color][2]
    if lay['badge']:
        b = lay['badge']
        c.parts.append(f'<rect x="{x + 14}" y="{y + 14}" width="{b}" height="{b}" rx="{b * 0.22}" '
                       f'fill="{PALETTE[color][0]}" stroke="{PALETTE[color][1]}" stroke-width="1.5"/>')
        if icons.known(lay['icon']):
            c.icon(lay['icon'], x + 14 + b * 0.2, y + 14 + b * 0.2, b * 0.6, color)
        else:
            # a short text mark (e.g. "for", "[ ]"), as in specs written before the icon library
            c.text(x + 14 + b / 2, y + 14 + b / 2 + small * 0.36, lay['icon'][:4], size=small, mono=True,
                   weight=700, fill=strong)
    tx = x + 14 + (lay['badge'] + 10 if lay['badge'] else 0)
    title_h = len(lay['title']) * size * 1.3
    c.lines(tx, y + 14 + lay['head'] / 2 - title_h / 2 - size * 0.2, lay['title'], size=size, anchor='start',
            weight=800, fill=strong)
    cy = y + 14 + lay['head'] + small * 0.6
    for mark, lines in lay['items']:
        c.icon(mark, x + 14, cy + small * 0.12, small * 1.15, color)
        for k, line in enumerate(lines):
            c.text(x + 14 + small * 1.7, cy + small * (1.0 + k * 1.45), line, size=small, anchor='start')
        cy += len(lines) * small * 1.45
    if lay['code']:
        code_h = len(lay['code']) * small * 1.3 + 8
        c.parts.append(f'<rect x="{x + 12}" y="{cy + 4}" width="{lay["inner"] + 4}" height="{code_h}" rx="6" '
                       f'fill="#FFFFFF" opacity="0.75"/>')
        c.lines(x + 20, cy + 4, lay['code'], size=small, anchor='start', mono=True)
        cy += code_h + 10
    if lay['scene']:
        scene_block(c, x + 14, cy + small * 0.6, lay['inner'], lay['scene'], color)


def cards(c, spec, profile):
    items = spec['cards']
    columns = 3 if profile == 'large' else 2
    gap = c.pad / 2
    w = (c.w - 2 * c.pad - (columns - 1) * gap) / columns
    size, small = c.p['body'] * 0.85, c.p['small'] * 0.95
    colors = ('blue', 'purple', 'teal', 'green', 'orange', 'red')
    rows = [items[i:i + columns] for i in range(0, len(items), columns)]
    for r, row in enumerate(rows):
        layouts = [card_layout(c, card, r * columns + k + 1, w, size, small)
                   for k, card in enumerate(row)]
        h = max(lay['h'] for lay in layouts)
        for k, (card, lay) in enumerate(zip(row, layouts, strict=True)):
            color = colors[(r * columns + k) % len(colors)]
            draw_card(c, card, lay, c.pad + k * (w + gap), c.y, w, h, color, size, small)
        c.y += h + gap
    c.y += c.pad / 2
    if len(items) > 12:
        c.problems.append(f'{len(items)} cards: a cheat sheet holds at most 12')
    return 0  # cards are a reference sheet, not a diagram to take in at a glance


LAYOUTS = {'flow': flow, 'timeline': timeline, 'compare': compare, 'boxes': boxes, 'layers': layers,
           'tree': tree, 'sequence': sequence, 'bars': bars, 'scene': scene}
REQUIRED = {'flow': 'steps', 'timeline': 'events', 'compare': 'rows', 'boxes': 'cells', 'layers': 'layers',
            'tree': 'root', 'sequence': 'messages', 'bars': 'bars', 'cards': 'cards', 'scene': 'steps'}


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
    p.add_argument('--icons', action='store_true')
    args = p.parse_args()
    if args.icons:
        out({'icons': icons.names()})
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
