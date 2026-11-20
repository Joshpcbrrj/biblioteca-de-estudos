#!/usr/bin/env python3
"""Kit tests: the skill's structure, the documentation and the library skeleton.

Usage:  python tests/run.py

Needs PyYAML (`pip install pyyaml`). Prints OK or FAILED for each test and
exits with code 1 if any test fails. The "Kit tests" Action runs the same
on every push and pull request.
"""
import filecmp
import glob
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, 'skill', 'syllabook')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
failures = []


def test(name):
    def run(fn):
        try:
            note = fn()
            print(f'OK      {name}' + (f' ({note})' if note else ''))
        except AssertionError as e:
            failures.append(name)
            print(f'FAILED  {name}: {e}')
        return fn
    return run


def read(path):
    return open(path, encoding='utf-8').read()


def skill_docs():
    return [os.path.join(SKILL, 'SKILL.md')] + sorted(
        glob.glob(os.path.join(SKILL, 'modes', '*.md'))
        + glob.glob(os.path.join(SKILL, 'references', '**', '*.md'), recursive=True))


@test('SKILL.md frontmatter follows the Agent Skills rules')
def _():
    text = read(os.path.join(SKILL, 'SKILL.md'))
    m = re.match(r'---\nname: (.+)\ndescription: (.+?)\n---\n', text, re.S)
    assert m, 'frontmatter with name and description not found'
    name, desc = m.group(1), m.group(2)
    assert name == os.path.basename(SKILL), f'name "{name}" differs from the folder'
    assert re.fullmatch(r'[a-z0-9-]{1,64}', name), 'name must be lowercase letters, digits and hyphens, up to 64'
    assert not re.search(r'anthropic|claude', name), 'name uses a reserved word'
    assert 0 < len(desc) <= 1024, f'description has {len(desc)} characters (max 1024)'
    assert not re.search(r'<[a-zA-Z/]', desc), 'description contains an XML tag'
    lines = len(text.splitlines())
    assert lines <= 500, f'SKILL.md has {lines} lines (max 500)'
    return f'{lines} lines, description {len(desc)} characters'


@test('every path cited in the skill exists')
def _():
    missing = []
    scripts_written = os.path.isdir(os.path.join(SKILL, 'scripts'))
    for path in skill_docs():
        text = read(path)
        for ref in set(re.findall(r'`((?:modes|references|assets)/[\w./-]+)`', text)):
            if not os.path.exists(os.path.join(SKILL, ref)):
                missing.append(f'{os.path.relpath(path, SKILL)} -> {ref}')
        # scripts are checked once the scripts/ folder exists (phase 3 of the rebuild)
        if scripts_written:
            for ref in set(re.findall(r'scripts/([\w-]+\.py)', text)):
                if not os.path.exists(os.path.join(SKILL, 'scripts', ref)):
                    missing.append(f'{os.path.relpath(path, SKILL)} -> scripts/{ref}')
    assert not missing, missing
    return None if scripts_written else 'scripts not written yet: not checked'


@test('every mode and reference file is listed in SKILL.md (one level deep)')
def _():
    skill = read(os.path.join(SKILL, 'SKILL.md'))
    unlisted = []
    for path in skill_docs()[1:]:
        rel = os.path.relpath(path, SKILL).replace(os.sep, '/')
        folder, name = os.path.split(rel)
        # files in areas/ and style/ are listed by name or by the <placeholder> pattern
        if rel in skill or name in skill or f'{folder}/<' in skill:
            continue
        unlisted.append(rel)
    assert not unlisted, unlisted


@test('long skill files start with a table of contents')
def _():
    no_toc = []
    for path in skill_docs()[1:]:
        lines = read(path).splitlines()
        head = '\n'.join(lines[:12])
        if len(lines) > 100 and '## Contents' not in head and '- [ ] 1.' not in head:
            no_toc.append(f'{os.path.relpath(path, SKILL)} ({len(lines)} lines)')
    assert not no_toc, no_toc


@test('hidden answers in the examples use the exact <details> format')
def _():
    bad = []
    for path in skill_docs():
        lines = read(path).splitlines()
        for i, line in enumerate(lines):
            bare = line.lstrip('> ').strip()
            if bare.startswith('<summary>') and i + 1 < len(lines) and lines[i + 1].lstrip('> ').strip():
                bad.append(f'{os.path.relpath(path, SKILL)}:{i + 2} needs a blank line after <summary>')
            if bare == '</details>' and i > 0 and lines[i - 1].lstrip('> ').strip():
                bad.append(f'{os.path.relpath(path, SKILL)}:{i} needs a blank line before </details>')
    assert not bad, bad


@test('Portuguese translations exist and are up to date')
def _():
    import translation
    problems = translation.check()
    assert not problems, problems


@test('every documentation page has the language switcher')
def _():
    import translation
    missing = []
    for rel in translation.english_pages():
        for page in (rel, translation.translation_of(rel)):
            path = os.path.join(ROOT, page)
            # a missing translation is reported by the translation test
            if os.path.exists(path) and 'English' not in read(path)[:600]:
                missing.append(page)
    assert not missing, missing


@test('internal links in the documentation point to existing files')
def _():
    broken = []
    for path in glob.glob(os.path.join(ROOT, '**', '*.md'), recursive=True):
        rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        if rel.startswith(('plano/', 'skill/syllabook/references/')):
            continue
        for target in re.findall(r'\]\(([^)#\s]+)(?:#[^)]*)?\)', read(path)):
            if target.startswith(('http://', 'https://', 'mailto:', '../../')):
                continue
            if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(path), target))):
                broken.append(f'{rel} -> {target}')
    assert not broken, broken


@test('book folders at the root match the library skeleton')
def _():
    lib = os.path.join(SKILL, 'assets', 'library')
    different = []
    for folder in ('created-books', 'improved-materials'):
        for name in ('README.md', 'README.pt-BR.md'):
            a, b = os.path.join(ROOT, folder, name), os.path.join(lib, folder, name)
            if not os.path.exists(b) or not filecmp.cmp(a, b, shallow=False):
                different.append(f'{folder}/{name}')
    assert not different, f'copy the root version into assets/library: {different}'


@test('YAML files are valid and library.yaml has every key')
def _():
    import yaml
    keys = {'author', 'repository', 'branch', 'commit_name', 'commit_email', 'default_language',
            'content_license', 'code_license', 'epub_release', 'notion_page'}
    files = glob.glob(os.path.join(ROOT, '.github', '**', '*.yml'), recursive=True)
    for path in files + [os.path.join(ROOT, 'library.yaml'),
                         os.path.join(SKILL, 'assets', 'library', 'library.yaml')]:
        data = yaml.safe_load(read(path))
        if path.endswith('library.yaml'):
            assert keys <= set(data), f'{os.path.relpath(path, ROOT)} is missing {sorted(keys - set(data))}'
    return f'{len(files) + 2} files'


@test('tools compile')
def _():
    paths = glob.glob(os.path.join(ROOT, 'tools', '*.py')) + glob.glob(os.path.join(SKILL, 'scripts', '**', '*.py'), recursive=True)
    for path in paths:
        compile(read(path), path, 'exec')
    return f'{len(paths)} files'


if __name__ == '__main__':
    print(f'\n{len(failures)} failure(s).' if failures else '\nAll tests passed.')
    sys.exit(1 if failures else 0)
