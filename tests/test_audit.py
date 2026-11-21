"""audit.py: every check, per chapter and for the whole book, in both reading profiles."""
import os
import shutil

import pytest
from conftest import edit, load, save

CHAPTER = os.path.join('chapters', '01-listas.md')
BLOCK = ('```python\nnotas = [7.5, 8.0, 6.5]\nmaior = max(notas)\nmenor = min(notas)\n'
         'print(maior, menor)\n```\n\n## 🏋️ Pratique')


def audit(cli, book, *args):
    return cli('audit', *args, '--book', book)


def test_the_sample_book_is_ready(cli, book):
    code, r = audit(cli, book)
    assert code == 0 and r['ready'] and not r['errors'] and not r['warnings'], r
    code, r = audit(cli, book, 1)
    assert code == 0 and r['scope'] == 'chapter 1'


ERRORS = [
    ('placeholder', '## Listas', '## Listas\n\n<!-- TODO: explain -->', 'TODO placeholder'),
    ('missing section', '## 🧠 Revisão rápida', '## Revisão', 'missing section "Revisão rápida"'),
    ('code without comment', '## 🏋️ Pratique', BLOCK, 'no comment explaining why'),
    ('long code line', 'quantidade = len(notas)', 'quantidade = len(notas)' + ' + 0' * 25, 'limit 80'),
    ('image without alt', '![A lista notas com os índices 0, 1 e 2 e os valores 7,5, 8,0 e 6,5]', '![]',
     'image without alt text'),
    ('missing image', '../img/c01-lista.svg', '../img/nao-existe.svg', 'image not found'),
    ('broken link', '## 📚 Fontes', 'Veja o [capítulo 5](05-nao-existe.md).\n\n## 📚 Fontes', 'missing file'),
    ('no blank line after summary', '<summary>Ver resposta</summary>\n\n4.', '<summary>Ver resposta</summary>\n4.',
     'after <summary>'),
    ('no blank line before /details', 'maior valor.\n\n</details>', 'maior valor.\n</details>', 'before </details>'),
    ('unclosed code block', '```text\n3\n```', '```text\n3\n', 'never closed'),
]


@pytest.mark.parametrize('case, old, new, message', ERRORS, ids=[e[0] for e in ERRORS])
def test_each_chapter_error(cli, book, case, old, new, message):
    edit(book / CHAPTER, old, new)
    code, r = audit(cli, book, 1)
    assert code == 1 and not r['ready'] and any(message in e for e in r['errors']), r['errors']


WARNINGS = [
    ('long output line', '```text\n3\n```', '```text\n' + 'x ' * 50 + '\n```', 'characters (limit 80)'),
    ('long URL in code', 'quantidade = len(notas)',
     'quantidade = len(notas)  # https://docs.python.org/3/tutorial/datastructures.html#more-on-lists', 'limit 80'),
    ('wide table', '| Item | Em uma frase |\n| --- | --- |',
     '| a | b | c | d | e | f | g |\n| --- | --- | --- | --- | --- | --- | --- |', 'table with 7 columns'),
    ('filler word', 'Guardar 40 notas', 'Basicamente, guardar 40 notas', 'filler word'),
    ('sources without link', '- [The Python Tutorial](https://docs.python.org/3/tutorial/), conferido em 2026-11-20.',
     '- The Python Tutorial', 'has no link'),
]


@pytest.mark.parametrize('case, old, new, message', WARNINGS, ids=[w[0] for w in WARNINGS])
def test_each_chapter_warning(cli, book, case, old, new, message):
    edit(book / CHAPTER, old, new)
    code, r = audit(cli, book, 1)
    assert code == 0 and r['ready'] and any(message in w for w in r['warnings']), r


def test_small_reading_profile_has_stricter_limits(cli, book):
    data = load(book / 'book.yaml')
    data['choices']['reading'] = 'small'
    save(book / 'book.yaml', data)
    # 70 characters: fine on large screens, too long on a 6-inch e-reader
    edit(book / CHAPTER, 'quantidade = len(notas)', 'quantidade = len(notas)' + ' + 0' * 12)
    code, r = audit(cli, book, 1)
    assert code == 1 and any('limit 60' in e for e in r['errors'])


def test_where_we_left_off_is_required_from_chapter_two(cli, book):
    edit(book / 'chapters' / '02-o-laco-for.md', '## De onde paramos', '## Antes')
    code, r = audit(cli, book, 2)
    assert code == 1 and any('De onde paramos' in e for e in r['errors'])


@pytest.mark.parametrize('setup, message', [
    (lambda b: os.remove(b / 'chapters' / 'glossario.md'), 'fixed part missing: Glossário'),
    (lambda b: os.remove(b / 'chapters' / '03-simulado-final.md'), 'fixed part missing: Simulado final'),
    (lambda b: os.remove(b / 'chapters' / '00-como-estudar-este-livro.md'), 'fixed part missing: chapter 0'),
    (lambda b: os.remove(b / 'README.md'), 'README.md missing'),
    (lambda b: os.remove(b / 'chapters' / '02-o-laco-for.md'), 'chapter 2: file missing'),
    (lambda b: edit(b / 'chapters' / 'glossario.md', '# Glossário', '# Glossário\n\n<!-- TODO -->'), 'TODO'),
])
def test_whole_book_errors(cli, book, setup, message):
    setup(book)
    code, r = audit(cli, book)
    assert code == 1 and any(message in e for e in r['errors']), r['errors']


def test_whole_book_warns_about_unused_images_but_ignores_sources_and_credits(cli, book):
    shutil.copy(book / 'img' / 'c01-lista.svg', book / 'img' / 'sobrando.svg')
    os.makedirs(book / 'img' / '_source', exist_ok=True)
    (book / 'img' / '_source' / 'c01-lista.yaml').write_text('type: blocks\n')
    (book / 'img' / 'CREDITS.md').write_text('# Credits\n')
    code, r = audit(cli, book)
    assert code == 0 and r['warnings'] == ['image not used in any chapter: img/sobrando.svg']


def test_improved_book_chapters_must_say_where_they_come_from(cli, book):
    data = load(book / 'book.yaml')
    data['origin'] = 'improved'
    save(book / 'book.yaml', data)
    code, r = audit(cli, book, 1)
    assert code == 1 and any('sources_original' in e for e in r['errors'])


def test_a_chapter_without_its_research_dossier_is_a_warning(cli, book):
    os.remove(book / 'research' / 'c01.md')
    code, r = audit(cli, book, 1)
    assert code == 0 and any('research/c01.md' in w for w in r['warnings']), r


def test_a_translation_needs_no_research_dossier(cli, book):
    os.remove(book / 'research' / 'c01.md')
    data = load(book / 'book.yaml')
    data['translation_of'] = 'python-do-zero-en'
    save(book / 'book.yaml', data)
    code, r = audit(cli, book, 1)
    assert not any('research/' in w for w in r['warnings']), r


def test_a_photo_without_credit_is_an_error(cli, book):
    (book / 'img' / 'c01-foto.jpg').write_bytes(b'fake')
    edit(book / CHAPTER, 'Guardar 40 notas', '![Uma foto](../img/c01-foto.jpg)\n\nGuardar 40 notas')
    code, r = audit(cli, book, 1)
    assert code == 1 and any('c01-foto.jpg' in e and 'CREDITS.md' in e for e in r['errors']), r
    (book / 'img' / 'CREDITS.md').write_text('# Créditos\n\n- c01-foto.jpg: foto, domínio público\n',
                                             encoding='utf-8')
    code, r = audit(cli, book, 1)
    assert code == 0, r
