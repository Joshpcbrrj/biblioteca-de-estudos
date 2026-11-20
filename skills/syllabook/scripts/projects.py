#!/usr/bin/env python3
"""Assembles the book's projects from its code blocks and runs them.

Usage:  python scripts/projects.py [--book B] [--chapter N] [--no-run] [--timeout SECONDS]

How a chapter declares a project (references/TEACHING.md §5):
  <!-- project: todo-api | run: python main.py | expect: Servidor pronto -->
  **app/main.py**
  ```python
  ...
  ```
A file block is a line with the file path in bold, followed by a code block. Blocks after a
`project:` marker belong to that project until the next marker; without a marker they belong
to a project named after the chapter. A later block with the same path replaces the earlier
one, so a project can evolve across chapters. Files go to projects/<name>/.

`run` is executed in the project folder; `expect` is a text its output must contain. A project
without `run` is only assembled ("not run"), e.g. when it needs a service the session lacks.
Prints JSON; exit code 1 when a project fails or a path tries to leave the project folder.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import chapter_numbers, chapter_path, fail, find_book, load_yaml, out

MARKER = re.compile(r'<!--\s*project:\s*(.+?)\s*-->')
# ':' is accepted here only so that a drive path (C:/...) is seen and refused, not silently ignored
FILE_LINE = re.compile(r'^\*\*`?([\w./:-]+\.[\w]+|[\w./:-]*/[\w.-]+)`?\*\*\s*$')
QUOTE = re.compile(r'^(?:>\s?)+')


def parse_marker(text):
    """'todo | run: python main.py | expect: ok' -> {'name': 'todo', 'run': ..., 'expect': ...}"""
    parts = [p.strip() for p in text.split('|')]
    spec = {'name': parts[0]}
    for part in parts[1:]:
        key, _, value = part.partition(':')
        if key.strip() in ('run', 'expect'):
            spec[key.strip()] = value.strip()
    return spec


def safe_path(path):
    """A file path must stay inside the project folder."""
    normal = os.path.normpath(path)
    # since Python 3.13, isabs('/x') is False on Windows: a rooted path without a drive
    return not (os.path.isabs(path) or path.startswith(('/', '\\')) or normal.startswith('..') or ':' in normal)


def collect(text, default_name, projects, errors, chapter):
    """Reads one chapter: markers and file blocks, in order."""
    lines = [QUOTE.sub('', line) for line in text.splitlines()]
    current = default_name
    i = 0
    while i < len(lines):
        marker = MARKER.search(lines[i])
        if marker:
            spec = parse_marker(marker.group(1))
            current = spec['name']
            project = projects.setdefault(current, {'files': {}, 'chapters': []})
            project.update({k: v for k, v in spec.items() if k != 'name'})
        m = FILE_LINE.match(lines[i].strip())
        if m:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip().startswith('```'):
                end = j + 1
                while end < len(lines) and not lines[end].strip().startswith('```'):
                    end += 1
                path = m.group(1)
                if not safe_path(path):
                    errors.append(f'chapter {chapter}: path "{path}" leaves the project folder')
                else:
                    project = projects.setdefault(current, {'files': {}, 'chapters': []})
                    project['files'][path] = '\n'.join(lines[j + 1:end]) + '\n'
                    if chapter not in project['chapters']:
                        project['chapters'].append(chapter)
                i = end
        i += 1


def run_project(folder, spec, timeout):
    try:
        r = subprocess.run(spec['run'], shell=True, cwd=folder, capture_output=True, text=True,
                           encoding='utf-8', errors='replace', timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f'timed out after {timeout} s'
    output = (r.stdout + r.stderr).strip()
    tail = output[-600:]
    if r.returncode != 0:
        return False, f'exit code {r.returncode}: {tail}'
    if spec.get('expect') and spec['expect'] not in output:
        return False, f'output does not contain "{spec["expect"]}": {tail}'
    return True, tail


def main():
    p = argparse.ArgumentParser(description='Assemble the projects from the code blocks and run them.')
    p.add_argument('--book')
    p.add_argument('--chapter', type=int)
    p.add_argument('--no-run', action='store_true')
    p.add_argument('--timeout', type=int, default=120, help='seconds per project run (default 120)')
    args = p.parse_args()
    book_dir, path = find_book(args.book)
    data = load_yaml(path)
    numbers = [args.chapter] if args.chapter else chapter_numbers(data)
    projects, errors = {}, []
    for n in numbers:
        file = chapter_path(book_dir, n)
        if not file:
            if args.chapter:
                fail(f'chapter {n} has no file yet')
            continue
        default = os.path.splitext(os.path.basename(file))[0]
        collect(open(file, encoding='utf-8').read(), default, projects, errors, n)
    results = []
    for name, spec in projects.items():
        if not spec['files']:
            continue
        folder = os.path.join(book_dir, 'projects', name)
        if os.path.isdir(folder):
            shutil.rmtree(folder)  # rebuilt from the book every time, so it never drifts from the text
        for rel, content in spec['files'].items():
            target = os.path.join(folder, rel)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with open(target, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
        result = {'name': name, 'chapters': spec['chapters'], 'files': sorted(spec['files'])}
        if not spec.get('run'):
            result['status'] = 'not run (no run: command in the project marker)'
        elif args.no_run:
            result['status'] = 'not run (--no-run)'
        else:
            ok, output = run_project(folder, spec, args.timeout)
            result.update({'status': 'ok' if ok else 'failed', 'output': output})
        results.append(result)
    failed = [r['name'] for r in results if r['status'] == 'failed']
    out({'projects': results, 'errors': errors, 'ok': not failed and not errors},
        1 if failed or errors else 0)


if __name__ == '__main__':
    main()
