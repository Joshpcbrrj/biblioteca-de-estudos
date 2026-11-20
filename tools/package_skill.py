#!/usr/bin/env python3
"""Packages the skill as a zip ready to upload on Claude's Skills screen.

Usage:
  python tools/package_skill.py --out <folder>

Creates <folder>/syllabook.zip with the `syllabook/` folder at its root,
which is the layout Claude expects for an uploaded skill.
"""
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, 'skill', 'syllabook')
SKIP_DIRS = {'__pycache__', '.pytest_cache'}


def package(out_dir):
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, 'syllabook.zip')
    count = 0
    with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, dirs, files in os.walk(SKILL):
            dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
            for name in sorted(files):
                path = os.path.join(base, name)
                arc = os.path.join('syllabook', os.path.relpath(path, SKILL)).replace(os.sep, '/')
                z.write(path, arc)
                count += 1
    print(f'{target} ({count} files)')
    return target


if __name__ == '__main__':
    if '--out' not in sys.argv or sys.argv.index('--out') + 1 >= len(sys.argv):
        print(__doc__)
        sys.exit(2)
    package(sys.argv[sys.argv.index('--out') + 1])
