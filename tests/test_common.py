"""common.py: slugs, labels, finding the book."""
import os

import common
import pytest
from conftest import SKILL


@pytest.mark.parametrize('text, expected', [
    ('Ação Rápida!', 'acao-rapida'),
    ('  O laço  for  ', 'o-laco-for'),
    ('C++ & Python 3', 'c-python-3'),
    ('Simulado final', 'simulado-final'),
])
def test_slugify(text, expected):
    assert common.slugify(text) == expected


def test_slugify_cuts_long_text_at_a_word_boundary():
    slug = common.slugify('palavra ' * 20, limit=30)
    assert len(slug) <= 30 and not slug.endswith('-') and slug.endswith('palavra')


def test_labels_in_the_book_language():
    assert common.labels('pt-BR')['See answer'] == 'Ver resposta'
    assert common.labels('en')['See answer'] == 'See answer'


def test_labels_fall_back_to_english_for_a_language_without_a_style_file():
    assert common.labels('xx-YY') == common.labels('en')


def test_every_style_file_has_every_label_the_scripts_use():
    """Contract: a style file missing a label would crash a script at the user's desk."""
    import ast
    known = set(common.labels('en'))
    used = set()
    for name in os.listdir(os.path.join(SKILL, 'scripts')):
        if name.endswith('.py'):
            tree = ast.parse(open(os.path.join(SKILL, 'scripts', name), encoding='utf-8').read())
            # any string literal that is a label key, however the script reaches it
            used |= {n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and n.value in known}
    assert len(used) > 15, f'only {len(used)} labels found: is the English style file complete?'
    for style in os.listdir(os.path.join(SKILL, 'references', 'style')):
        lang = style[:-3]
        missing = used - set(common.labels(lang))
        assert not missing, f'style/{style} is missing labels: {sorted(missing)}'


def test_find_book_by_folder_by_yaml_by_env_by_cwd_and_by_the_last_selection(book, tmp_path, monkeypatch):
    expected = (str(book), str(book / 'book.yaml'))
    assert common.find_book(str(book)) == expected
    assert common.find_book(str(book / 'book.yaml')) == expected
    monkeypatch.setenv('SYLLABOOK_BOOK', str(book))
    assert common.find_book() == expected
    monkeypatch.delenv('SYLLABOOK_BOOK')
    monkeypatch.chdir(book)
    assert common.find_book() == expected
    monkeypatch.chdir(tmp_path)
    common.remember(str(book / 'book.yaml'))
    assert common.find_book() == expected


def test_find_book_stops_with_a_clear_error_when_there_is_no_book(capsys):
    with pytest.raises(SystemExit) as e:
        common.find_book()
    assert e.value.code == 1 and 'book not found' in capsys.readouterr().out


@pytest.mark.parametrize('text, title', [
    ('# 1. Listas\n\ntexto', '1. Listas'),
    ('```python\n# um comentário\n```\n\n# O título', 'O título'),
    ('````md\n```\n# dentro\n```\n````\n# Fora', 'Fora'),
    ('Sem título\n\n## Seção', ''),
])
def test_first_h1_ignores_comments_inside_code(text, title):
    assert common.first_h1(text) == title


def test_chapter_path(book):
    assert common.chapter_path(str(book), 1).endswith('01-listas.md')
    assert common.chapter_path(str(book), 9) is None


def test_need_yaml_returns_the_module():
    assert hasattr(common.need_yaml(), 'safe_load')


def test_load_yaml_reports_the_line_of_a_syntax_error(tmp_path, capsys):
    p = tmp_path / 'spec.yaml'
    p.write_text('steps:\n  - {text: Precisa isolar?, kind: decision}\n', encoding='utf-8')
    with pytest.raises(SystemExit) as e:
        common.load_yaml(str(p))
    assert e.value.code == 1
    assert 'spec.yaml line 2' in capsys.readouterr().out


def test_load_yaml_reports_an_error_without_a_line(tmp_path, capsys):
    p = tmp_path / 'spec.yaml'
    p.write_text('title: a\x07b\n', encoding='utf-8')
    with pytest.raises(SystemExit):
        common.load_yaml(str(p))
    assert '"error": "spec.yaml: ' in capsys.readouterr().out


def test_remember_does_not_fail_when_the_state_folder_cannot_be_written(tmp_path, monkeypatch):
    # a read-only home (a sandbox, a locked-down account): remembering the book is a convenience, never an error
    blocker = tmp_path / 'not-a-folder'
    blocker.write_text('x', encoding='utf-8')
    monkeypatch.setattr(common, 'STATE', str(blocker / 'current'))
    common.remember(str(tmp_path / 'book.yaml'))
