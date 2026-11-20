"""notion.py: the conversion to Notion's Markdown, the uploads and the index page."""
import notion
import pytest
from conftest import edit, load, save


def convert(text, book):
    return notion.convert(text, str(book))


def test_a_chapter_becomes_a_notion_page(cli, book):
    code, r = cli('notion', 1, '--book', book)
    assert code == 0 and r['title'] == '1. Listas'
    content = r['content']
    assert not content.startswith('# '), 'the title is the page title, not a heading in the page'
    assert '<callout icon="🗺️" color="gray_bg">\n**Neste capítulo:**' in content
    assert '<callout icon="⚠️" color="yellow_bg">' in content
    assert '<toggle>\nVer resposta\n\n4\\. `len` conta os itens' in content
    assert '<details>' not in content and '<summary>' not in content and '\n>' not in content
    assert '<image source="UPLOAD:c01-lista.svg">A lista notas' in content
    assert r['uploads'][0]['placeholder'] == 'UPLOAD:c01-lista.svg' and r['uploads'][0]['kind'] == 'svg'


def test_code_passes_through_untouched(book):
    text = '````markdown\n> não é callout\n<details>\n```python\nx = 1\n```\n````\n'
    content, uploads, _ = convert(text, book)
    assert content == text and uploads == []


def test_a_quote_with_an_answer_keeps_the_answer_as_a_toggle(book):
    text = ('> 🔥 **Aquecimento:** quanto é 2 + 2?\n>\n> <details>\n> <summary>Ver resposta</summary>\n>\n> 4\n>\n'
            '> </details>\n')
    content, _, _ = convert(text, book)
    assert content.startswith('<callout icon="🔥" color="orange_bg">\n**Aquecimento:** quanto é 2 + 2?\n</callout>')
    assert '<toggle>\nVer resposta\n\n4\n</toggle>' in content


@pytest.mark.parametrize('quote, icon, color', [
    ('> 💡 **Analogia:** um quadro branco.', '💡', 'blue_bg'),
    ('> ➡️ **Próximo passo:** laços.', '➡️', 'gray_bg'),
    ('> Uma nota sem emoji.', '💬', 'gray_bg'),
])
def test_each_note_becomes_a_callout_with_its_emoji(book, quote, icon, color):
    content, _, _ = convert(quote, book)
    assert content.startswith(f'<callout icon="{icon}" color="{color}">')


def test_illustrations_are_left_out_and_real_photos_uploaded(book):
    (book / 'img' / '_source').mkdir(exist_ok=True)
    (book / 'img' / '_source' / 'c01-cena.yaml').write_text('type: x\n')
    text = '![Uma cena](../img/c01-cena.png)\n\n![O Mark II](../img/c01-mark2.jpg)\n'
    content, uploads, left_out = convert(text, book)
    assert left_out == ['c01-cena.png'] and 'c01-cena' not in content
    assert uploads[0]['kind'] == 'photo' and '<image source="UPLOAD:c01-mark2.jpg">O Mark II</image>' in content


def test_links_comments_and_generated_blocks_are_removed(book):
    text = ('Veja o [capítulo 2](02-o-laco-for.md#o-laco-for) e a [doc](https://docs.python.org).\n\n'
            '<!-- project: x | run: y -->\n\n<!-- nav:start -->\n---\n[◀ anterior](00.md)\n<!-- nav:end -->\n')
    content, _, _ = convert(text, book)
    assert 'Veja o capítulo 2 e a [doc](https://docs.python.org).' in content
    assert '<!--' not in content and 'anterior' not in content


def test_the_glossary_by_file_name_and_chapter_zero_by_number(cli, book):
    code, r = cli('notion', 'glossario.md', '--book', book)
    assert code == 0 and r['title'] == 'Glossário'
    code, r = cli('notion', 0, '--book', book)
    assert code == 0 and r['title'] == '0. Como estudar este livro'


@pytest.mark.parametrize('target, message', [
    (9, 'has no file yet'),
    ('nada.md', 'not found'),
    ('capitulo', 'give a chapter number'),
])
def test_targets_that_do_not_exist(cli, book, target, message):
    code, r = cli('notion', target, '--book', book)
    assert code == 1 and message in r['error']


def test_index_page_with_links_from_the_library(cli, library):
    code, r = cli('notion', 'index', '--book', library / 'created-books' / 'python-do-zero-teste')
    assert code == 0 and r['title'] == 'Python do zero (exemplo de teste)'
    content = r['content']
    assert '<callout icon="📚" color="blue_bg">' in content
    assert 'https://exemplo.github.io/minha-biblioteca/created-books/python-do-zero-teste/' in content
    assert 'https://github.com/exemplo/minha-biblioteca/tree/main/created-books/python-do-zero-teste' in content
    assert 'releases/download/epubs/python-do-zero-teste.epub' in content
    # "- 0. x" would be a numbered list inside the bullet, renumbered from 1 by Notion
    assert '- 0\\. Como estudar este livro' in content and '- 2\\. O laço for' in content and '- Glossário' in content
    # Notion's Markdown wants a blank line between blocks
    assert '</callout>\n\n## ' in content


def test_index_page_without_a_library_has_no_links(cli, book):
    data = load(book / 'book.yaml')
    data['subtitle'] = 'Um subtítulo'
    save(book / 'book.yaml', data)
    code, r = cli('notion', 'index', '--book', book)
    assert r['content'].startswith('Um subtítulo') and '📚' not in r['content']


def test_site_url():
    assert notion.site_url('Joshpcbrrj/syllabook-demo') == 'https://joshpcbrrj.github.io/syllabook-demo/'
    assert notion.site_url('') == ''


def test_a_chapter_without_a_title(book):
    edit(book / 'chapters' / '01-listas.md', '# 1. Listas', 'Listas')
    assert notion.title_of(open(book / 'chapters' / '01-listas.md', encoding='utf-8').read()) == ''
