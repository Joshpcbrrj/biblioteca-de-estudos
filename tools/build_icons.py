#!/usr/bin/env python3
"""Builds skills/syllabook/assets/icons.json from the Lucide icons (https://lucide.dev, ISC license).

Run once when the icon list changes, with the icons folder of the lucide-static package:
  npm pack lucide-static && tar -xzf lucide-static-*.tgz
  python tools/build_icons.py package/icons [--out skills/syllabook/assets/icons.json]

Keeps only the markup inside each <svg> (paths, circles...): diagram.py draws it in its own
<g> with the color and size of the diagram. Names not found are printed, never invented.
"""
import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, 'skills', 'syllabook', 'assets', 'icons.json')

# icons useful in at least two area profiles (programming, math, languages, practical skills, general)
NAMES = [
    'folder', 'folder-open', 'file', 'file-text', 'file-code', 'files', 'code', 'code-xml', 'braces', 'terminal',
    'square-terminal', 'database', 'server', 'cloud', 'cloud-upload', 'cloud-download', 'network', 'globe', 'wifi',
    'link', 'lock', 'lock-open', 'key', 'shield', 'shield-check', 'settings', 'wrench', 'user', 'users',
    'message-circle', 'message-square', 'mail', 'bell', 'book', 'book-open', 'notebook-pen', 'graduation-cap',
    'search', 'lightbulb', 'target', 'brain', 'puzzle', 'chart-bar', 'chart-line', 'chart-pie', 'calculator',
    'sigma', 'percent', 'hash', 'binary', 'variable', 'table', 'clock', 'calendar', 'timer', 'circle-check',
    'circle-x', 'triangle-alert', 'info', 'circle-help', 'play', 'pause', 'repeat', 'refresh-cw', 'rotate-ccw',
    'music', 'mic', 'headphones', 'guitar', 'languages', 'pencil', 'list', 'list-checks', 'list-ordered', 'layers',
    'arrow-right', 'arrow-left-right', 'filter', 'package', 'box', 'container', 'cpu', 'monitor', 'app-window',
    'smartphone', 'git-branch', 'git-merge', 'git-pull-request', 'bug', 'rocket', 'zap', 'flask-conical', 'atom',
    'sparkles', 'star', 'house', 'map', 'compass', 'eye', 'download', 'upload', 'copy', 'save', 'workflow',
]


def inner_markup(svg_text):
    """The elements inside <svg>, on one line, with self-closing tags written as "/>"."""
    body = re.search(r'<svg\b[^>]*>(.*)</svg>', svg_text, re.S).group(1)
    body = re.sub(r'\s*\n\s*', '', body.strip())
    return re.sub(r'\s+/>', '/>', body)


def build(svg_dir, names):
    """Returns ({name: inner markup}, [names not found])."""
    icons, missing = {}, []
    for name in names:
        path = os.path.join(svg_dir, f'{name}.svg')
        if not os.path.exists(path):
            missing.append(name)
            continue
        with open(path, encoding='utf-8') as f:
            icons[name] = inner_markup(f.read())
    return icons, missing


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('svg_dir')
    p.add_argument('--out', default=DEFAULT_OUT)
    args = p.parse_args()
    icons, missing = build(args.svg_dir, NAMES)
    with open(args.out, 'w', encoding='utf-8', newline='\n') as f:
        f.write('{\n' + ',\n'.join(f' {json.dumps(k)}: {json.dumps(icons[k])}' for k in sorted(icons)) + '\n}\n')
    print(f'{len(icons)} icons written to {args.out}')
    if missing:
        print('not found (remove them from NAMES): ' + ', '.join(missing))


if __name__ == '__main__':
    main()
