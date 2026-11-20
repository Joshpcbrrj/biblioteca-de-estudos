"""Shared fixtures: an isolated environment per test, sample books and a way to run scripts.

Scripts run in-process (their main() with a patched argv), so coverage sees them and a
failure shows a normal Python traceback.
"""
import importlib
import json
import os
import shutil
import sys

import pytest
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, 'skills', 'syllabook')
SCRIPTS = os.path.join(SKILL, 'scripts')
SAMPLE = os.path.join(ROOT, 'tests', 'fixtures', 'sample-book')
sys.path[:0] = [SCRIPTS, os.path.join(ROOT, 'tools')]


@pytest.fixture(autouse=True)
def isolated(tmp_path, monkeypatch):
    """No test touches the user's home folder, the real repository or another test's book."""
    import common
    monkeypatch.setattr(common, 'STATE', str(tmp_path / 'state' / 'current'))
    monkeypatch.delenv('SYLLABOOK_BOOK', raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def book(tmp_path):
    """A copy of the sample book (2 chapters, fixed parts, one image)."""
    dest = tmp_path / 'book'
    shutil.copytree(SAMPLE, dest)
    return dest


@pytest.fixture
def library(tmp_path):
    """A user library: the skeleton from assets/library with the sample book inside."""
    lib = tmp_path / 'lib'
    shutil.copytree(os.path.join(SKILL, 'assets', 'library'), lib)
    shutil.copytree(SAMPLE, lib / 'created-books' / 'python-do-zero-teste')
    settings = load(lib / 'library.yaml')
    settings.update(author='Teste', repository='exemplo/minha-biblioteca', default_language='pt-BR')
    save(lib / 'library.yaml', settings)
    return lib


@pytest.fixture
def cli(monkeypatch, capsys):
    """Runs a script's main() like the command line does; returns (exit code, JSON output)."""
    def run(script, *args):
        module = importlib.import_module(script)
        monkeypatch.setattr(sys, 'argv', [f'{script}.py', *map(str, args)])
        code = 0
        try:
            module.main()
        except SystemExit as e:
            code = e.code or 0
        printed = capsys.readouterr().out
        try:
            return code, json.loads(printed)
        except json.JSONDecodeError:
            pytest.fail(f'{script} {" ".join(map(str, args))} did not print JSON:\n{printed}')
    return run


def load(path):
    return yaml.safe_load(open(path, encoding='utf-8'))


def save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(data, f, allow_unicode=True, sort_keys=False)


def edit(path, old, new):
    """Replaces text in a file, failing loudly if the text is not there (keeps tests honest)."""
    text = open(path, encoding='utf-8').read()
    assert old in text, f'"{old}" not found in {path}'
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.replace(old, new))


def read(path):
    return open(path, encoding='utf-8').read()
