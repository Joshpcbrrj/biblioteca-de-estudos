"""tools/: the translation checker and the skill packager."""
import os
import zipfile

import package_skill
import pytest
import translation


@pytest.fixture
def repo(tmp_path):
    """A fake repository with one English page and its Portuguese version, in sync."""
    (tmp_path / 'docs').mkdir()
    (tmp_path / 'docs' / 'page.md').write_text('# Page\n', encoding='utf-8')
    (tmp_path / 'docs' / 'page.pt-BR.md').write_text('# Página\n', encoding='utf-8')
    translation.stamp([str(tmp_path / 'docs' / 'page.pt-BR.md')])
    return tmp_path


def test_a_stamped_translation_is_up_to_date(repo):
    assert translation.check(str(repo)) == []
    assert open(repo / 'docs' / 'page.pt-BR.md', encoding='utf-8').read().startswith(
        '<!-- translation-of: page.md sha256:')


def test_line_endings_do_not_change_the_hash(repo):
    (repo / 'docs' / 'page.md').write_bytes(b'# Page\r\n')
    assert translation.check(str(repo)) == []


@pytest.mark.parametrize('setup, problem', [
    (lambda r: (r / 'docs' / 'page.md').write_text('# Page, changed\n', encoding='utf-8'), 'outdated'),
    (lambda r: os.remove(r / 'docs' / 'page.pt-BR.md'), 'missing'),
    (lambda r: (r / 'docs' / 'page.pt-BR.md').write_text('# Página\n', encoding='utf-8'), 'no translation-of line'),
    (lambda r: (r / 'docs' / 'page.pt-BR.md').write_text(
        '<!-- translation-of: other.md sha256:000000000000 -->\n', encoding='utf-8'), 'points to other.md'),
    (lambda r: (r / 'docs' / 'lost.pt-BR.md').write_text('x', encoding='utf-8'), 'orphan'),
])
def test_each_translation_problem(repo, setup, problem):
    setup(repo)
    assert any(problem in p for p in translation.check(str(repo)))


def test_exempt_folders_need_no_translation(repo):
    for folder in ('plano', 'tests', 'skill/syllabook/references'):
        os.makedirs(repo / folder, exist_ok=True)
        (repo / folder / 'internal.md').write_text('x', encoding='utf-8')
    (repo / 'CHANGELOG.md').write_text('x', encoding='utf-8')
    assert translation.check(str(repo)) == []


def test_stamp_refuses_a_page_that_is_not_portuguese_or_has_no_original(repo):
    with pytest.raises(SystemExit):
        translation.stamp([str(repo / 'docs' / 'page.md')])
    (repo / 'docs' / 'alone.pt-BR.md').write_text('x', encoding='utf-8')
    with pytest.raises(SystemExit):
        translation.stamp([str(repo / 'docs' / 'alone.pt-BR.md')])


def test_the_real_repository_translations_are_up_to_date():
    assert translation.check() == []


def run_tool(monkeypatch, capsys, name, *args):
    import runpy
    import sys
    monkeypatch.setattr(sys, 'argv', [f'{name}.py', *map(str, args)])
    with pytest.raises(SystemExit) as e:
        runpy.run_path(os.path.join(os.path.dirname(translation.__file__), f'{name}.py'), run_name='__main__')
    return e.value.code, capsys.readouterr().out


def test_translation_command_line(monkeypatch, capsys, repo):
    code, printed = run_tool(monkeypatch, capsys, 'translation', 'check')
    assert code == 0 and 'all up to date' in printed
    code, printed = run_tool(monkeypatch, capsys, 'translation', 'stamp', repo / 'docs' / 'page.pt-BR.md')
    assert code == 0 and 'stamped' in printed
    code, printed = run_tool(monkeypatch, capsys, 'translation')
    assert code == 2 and 'Usage' in printed


def test_package_skill_command_line(monkeypatch, capsys, tmp_path):
    code, printed = run_tool(monkeypatch, capsys, 'package_skill')
    assert code == 2 and 'Usage' in printed
    import runpy
    import sys
    monkeypatch.setattr(sys, 'argv', ['package_skill.py', '--out', str(tmp_path)])
    runpy.run_path(os.path.join(os.path.dirname(package_skill.__file__), 'package_skill.py'), run_name='__main__')
    assert (tmp_path / 'syllabook.zip').exists()


def test_package_skill_puts_everything_under_one_folder(tmp_path):
    target = package_skill.package(str(tmp_path))
    names = zipfile.ZipFile(target).namelist()
    assert 'syllabook/SKILL.md' in names and 'syllabook/scripts/book.py' in names
    assert all(n.startswith('syllabook/') for n in names)
    assert not any('__pycache__' in n for n in names)
