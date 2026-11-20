"""tools/sync_template.py: the library template repository mirrors the skill's library skeleton."""
import os

import pytest
import sync_template
from conftest import SKILL

SKELETON = os.path.join(SKILL, 'assets', 'library')


def files_under(root):
    found = set()
    for folder, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d != '.git']
        found |= {os.path.relpath(os.path.join(folder, n), root).replace(os.sep, '/') for n in names}
    return found


def test_sync_copies_the_skeleton_without_its_note(tmp_path):
    changed = sync_template.sync(str(tmp_path))
    expected = files_under(SKELETON) - {'SKELETON.md'}
    assert files_under(tmp_path) == expected and set(changed) == expected
    assert '.github/workflows/epub.yml' in expected and 'library.yaml' in expected


def test_sync_removes_stale_files_but_keeps_git(tmp_path):
    (tmp_path / '.git').mkdir()
    (tmp_path / '.git' / 'HEAD').write_text('ref', encoding='utf-8')
    (tmp_path / 'old.md').write_text('stale', encoding='utf-8')
    sync_template.sync(str(tmp_path))
    assert not (tmp_path / 'old.md').exists() and (tmp_path / '.git' / 'HEAD').exists()


def test_a_second_sync_changes_nothing(tmp_path):
    sync_template.sync(str(tmp_path))
    assert sync_template.sync(str(tmp_path)) == []


def test_command_needs_an_existing_folder(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['sync_template.py', str(tmp_path / 'nope')])
    with pytest.raises(SystemExit):
        sync_template.main()


def test_command_reports_the_changes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['sync_template.py', str(tmp_path)])
    sync_template.main()
    assert 'library.yaml' in capsys.readouterr().out
