"""The icons diagram.py draws: Lucide icons (ISC license) kept in assets/icons.json.

Each icon is the markup of a 24×24, stroke-only drawing; draw() places it at any size and color.
`python scripts/diagram.py --icons` lists the names.
"""
import difflib
import json
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'icons.json')
_icons = None


def _library():
    global _icons
    if _icons is None:
        with open(PATH, encoding='utf-8') as f:
            _icons = json.load(f)
    return _icons


def names():
    return sorted(_library())


def known(name):
    return name in _library()


def suggest(name):
    """Up to 3 names close to a misspelled one."""
    return difflib.get_close_matches(str(name), names(), n=3, cutoff=0.6)


def draw(name, x, y, size, color, width=2):
    """The icon as an SVG group with its top-left corner at (x, y); KeyError for an unknown name."""
    markup = _library()[name]
    return (f'<g transform="translate({x:g},{y:g}) scale({size / 24:g})" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{markup}</g>')
