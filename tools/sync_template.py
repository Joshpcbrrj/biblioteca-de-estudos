#!/usr/bin/env python3
"""Mirrors the skill's library skeleton into a clone of the library template repository.

Every user creates their own library from Joshpcbrrj/syllabook-library ("Use this template"), so that
repository must hold exactly skills/syllabook/assets/library/, minus SKELETON.md (a note for the skill).
Run at each release, then commit and push the clone:

  git clone https://github.com/Joshpcbrrj/syllabook-library ../syllabook-library
  python tools/sync_template.py ../syllabook-library

Files that are no longer in the skeleton are removed; .git is left alone. Prints the changed files.
"""
import argparse
import filecmp
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKELETON = os.path.join(ROOT, 'skills', 'syllabook', 'assets', 'library')
LEFT_OUT = {'SKELETON.md'}


def _files(root):
    found = set()
    for folder, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != '.git']
        found |= {os.path.relpath(os.path.join(folder, n), root).replace(os.sep, '/') for n in names}
    return found


def sync(dest):
    """Makes dest match the skeleton; returns the files added, changed or removed (sorted)."""
    wanted = _files(SKELETON) - LEFT_OUT
    changed = []
    for rel in sorted(_files(dest) - wanted):
        os.remove(os.path.join(dest, rel))
        changed.append(rel)
    for rel in sorted(wanted):
        src, dst = os.path.join(SKELETON, rel), os.path.join(dest, rel)
        if os.path.exists(dst) and filecmp.cmp(src, dst, shallow=False):
            continue
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        changed.append(rel)
    # folders emptied by removals go too (git does not keep empty folders)
    for folder, _dirs, _names in os.walk(dest, topdown=False):
        if '.git' not in folder.split(os.sep) and folder != dest and not os.listdir(folder):
            os.rmdir(folder)
    return sorted(changed)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('dest', help='a clone of the library template repository')
    args = p.parse_args()
    if not os.path.isdir(args.dest):
        sys.exit(f'not a folder: {args.dest}')
    changed = sync(args.dest)
    print('\n'.join(changed) if changed else 'already in sync')


if __name__ == '__main__':
    main()
