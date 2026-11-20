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


def test_chapter_path(book):
    assert common.chapter_path(str(book), 1).endswith('01-listas.md')
    assert common.chapter_path(str(book), 9) is None


def test_need_yaml_returns_the_module():
    assert hasattr(common.need_yaml(), 'safe_load')
