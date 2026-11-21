"""build.py: the pure transformations first, then the book, the library lists and the website."""
import os
import re
import shutil
import subprocess
import sys
import zipfile

import build
import pytest
from conftest import ROOT, edit, load, read, save

BOOK_IN_LIB = os.path.join('created-books', 'python-do-zero-teste')


def has_pandoc():
    if shutil.which('pandoc'):
        return True
    try:
        import pypandoc  # noqa: F401
        return True
    except ImportError:
        return False


needs_pandoc = pytest.mark.skipif(not has_pandoc(), reason='pandoc not available')


# ---------- pure transformations ----------

def test_set_block_appends_then_replaces():
    once = build.set_block('texto\n', 'nav', 'A')
    assert once == 'texto\n\n<!-- nav:start -->\nA\n<!-- nav:end -->\n'
    twice = build.set_block(once, 'nav', 'B')
    assert 'B' in twice and 'A' not in twice and twice.count('nav:start') == 1
    assert build.drop_block(twice, 'nav').strip() == 'texto'


def test_split_answers_keeps_quote_prefixes_and_numbers_from_a_start():
    text = ('Pergunta?\n\n> <details>\n> <summary>Ver resposta</summary>\n>\n> **3**\n>\n> </details>\n\n'
            '<details>\n<summary>Ver resposta</summary>\n\nQuatro.\n\n</details>\n')
    kept, answers = build.split_answers(text, 5)
    assert '<details>' not in kept
    assert '> [Ver resposta ↓](#ans-5){#q-5 .answer-link}' in kept
    assert '[Ver resposta ↓](#ans-6){#q-6 .answer-link}' in kept
    assert [(k, s, b) for k, s, b in answers] == [(5, 'Ver resposta', '**3**'), (6, 'Ver resposta', 'Quatro.')]


def test_collapsible_turns_answers_into_zensical_blocks_and_moves_them_out_of_quotes():
    text = '> <details>\n> <summary>Ver "resposta"</summary>\n>\n> `3`: três.\n>\n> </details>\n'
    out = build.collapsible(text)
    assert '??? success "Ver \'resposta\'"' in out and '    `3`: três.' in out and '<details>' not in out


def test_epub_markdown_gives_chapters_ids_and_resolves_links(book):
    files = [str(book / 'chapters' / n) for n in ('01-listas.md', '03-simulado-final.md')]
    text, answers = build.epub_markdown(files, build.labels('pt-BR'))
    assert '# 1. Listas {#f-01-listas}' in text
    assert '](#f-02-o-laco-for)' in text  # the mock exam's link to chapter 2
    assert '# Respostas {#answers}' in text and answers == 3


def test_a_one_line_answer_that_looks_like_a_list_is_escaped(book):
    text, _ = build.epub_markdown([str(book / 'chapters' / '01-listas.md')], build.labels('pt-BR'))
    assert '\n0\\.\n' in text


def test_pack_splits_in_parts_by_the_upload_limit(book, tmp_path, monkeypatch):
    monkeypatch.setattr(build, 'GITHUB_UPLOAD_LIMIT', 3)
    zips = build.pack(str(book), load(book / 'book.yaml'), str(tmp_path))
    total = sum(len(files) for _, _, files in os.walk(book))
    # every file goes in exactly one part, and no part goes over the limit
    assert sum(z['files'] for z in zips) == total and all(z['files'] <= 3 for z in zips) and len(zips) >= 2
    assert zips[0]['zip'].endswith(f'python-do-zero-teste-part1-of-{len(zips)}.zip')
    names = zipfile.ZipFile(zips[0]['zip']).namelist()
    assert all(n.startswith('created-books/python-do-zero-teste/') for n in names)


def test_pack_uses_the_improved_folder_for_improved_books(book, tmp_path):
    data = load(book / 'book.yaml')
    data['origin'] = 'improved'
    names = zipfile.ZipFile(build.pack(str(book), data, str(tmp_path))[0]['zip']).namelist()
    assert all(n.startswith('improved-materials/') for n in names)


def test_library_settings_found_upwards_or_empty(library, tmp_path):
    settings, root = build.library_settings(str(library / BOOK_IN_LIB / 'chapters'))
    assert settings['author'] == 'Teste' and root == str(library)
    assert build.library_settings(str(tmp_path / 'book')) == ({}, None)


# ---------- the book ----------

@needs_pandoc
@pytest.mark.slow
def test_build_a_book_end_to_end(cli, library):
    book = library / BOOK_IN_LIB
    code, r = cli('build', '--book', book, '--out', library / 'dist')
    assert code == 0 and r['answers_in_appendix'] == 6 and len(r['zips']) == 1, r
    epub = zipfile.ZipFile(r['epub'])
    pages = '\n'.join(epub.read(n).decode('utf-8') for n in epub.namelist() if n.endswith('.xhtml'))
    assert '<details' not in pages
    assert len(re.findall(r'#ans-\d+"', pages)) == 6 and len(re.findall(r'#q-\d+"', pages)) == 6
    assert 'Respostas' in pages and 'Voltar ao exercício' in pages
    assert re.search(r'href="[^"]*#f-02-o-laco-for"', pages)
    assert 'Teste' in epub.read('EPUB/content.opf').decode('utf-8')  # author from library.yaml
    chapter = read(book / 'chapters' / '01-listas.md')
    assert '[◀ Capítulo anterior](00-como-estudar-este-livro.md)' in chapter
    assert '[Próximo capítulo ▶](02-o-laco-for.md)' in chapter
    assert '- [2. O laço for](chapters/02-o-laco-for.md) · ⏱️ ~30 min' in read(book / 'README.md')
    assert '- laço for: [2. O laço for](02-o-laco-for.md)' in read(book / 'chapters' / 'glossario.md')


@needs_pandoc
@pytest.mark.slow
def test_build_with_a_cover_and_only_the_epub(cli, library):
    book = library / BOOK_IN_LIB
    # any PNG works for pandoc's cover option
    shutil.copy(os.path.join(ROOT, 'tests', 'fixtures', 'cover.png'), book / 'cover.png')
    code, r = cli('build', '--book', book, '--out', library / 'dist', '--no-zip')
    assert code == 0 and 'zips' not in r
    assert any('cover' in n for n in zipfile.ZipFile(r['epub']).namelist())


def test_partial_build_has_no_epub(cli, book, tmp_path):
    code, r = cli('build', '--book', book, '--out', tmp_path / 'p', '--partial')
    assert code == 0 and 'epub' not in r and r['zips'][0]['zip'].endswith('python-do-zero-teste-partial.zip')


def test_a_split_build_says_how_to_upload(cli, book, tmp_path, monkeypatch):
    monkeypatch.setattr(build, 'GITHUB_UPLOAD_LIMIT', 4)
    code, r = cli('build', '--book', book, '--out', tmp_path / 's', '--no-epub')
    assert len(r['zips']) >= 2 and 'upload them in order' in r['note']


def test_the_map_creates_a_readme_when_there_is_none(cli, book, tmp_path):
    os.remove(book / 'README.md')
    cli('build', '--book', book, '--out', tmp_path / 'd', '--no-epub', '--no-zip')
    readme = read(book / 'README.md')
    assert readme.startswith('# Python do zero (exemplo de teste)') and 'Mapa do livro' in readme


def test_a_pandoc_failure_is_reported(cli, book, tmp_path, monkeypatch):
    # python as "pandoc": it rejects pandoc's arguments and exits with an error
    monkeypatch.setattr(build, 'pandoc_path', lambda: sys.executable)
    code, r = cli('build', '--book', book, '--out', tmp_path / 'd')
    assert code == 1 and 'pandoc failed' in r['error']


# ---------- library lists and website ----------

def test_lists_in_both_languages_for_both_collections(cli, library):
    improved = library / 'improved-materials' / 'notas-de-aula'
    shutil.copytree(library / BOOK_IN_LIB, improved)
    data = load(improved / 'book.yaml')
    data.update(origin='improved', slug='notas-de-aula', title='Notas de aula')
    save(improved / 'book.yaml', data)
    code, r = cli('build', 'lists', '--library', library)
    assert code == 0 and r['books'] == 2 and len(r['updated']) == 4
    assert '| Livro | Nível | Capítulos | EPUB |' in read(library / 'created-books' / 'README.pt-BR.md')
    english = read(library / 'improved-materials' / 'README.md')
    assert '| Book | Level | Chapters | EPUB |' in english and '[Notas de aula](notas-de-aula/)' in english
    assert 'releases/download/epubs/notas-de-aula.epub' in english


def test_lists_leave_empty_collections_untouched(cli, library):
    before = read(library / 'improved-materials' / 'README.md')
    cli('build', 'lists', '--library', library)
    assert read(library / 'improved-materials' / 'README.md') == before


def test_site_source(cli, library):
    import yaml
    code, r = cli('build', 'site', '--library', library, '--out', library / '_site')
    assert code == 0 and r['books'] == 1
    config = yaml.safe_load(read(library / '_site' / 'mkdocs.yml'))
    assert config['theme']['language'] == 'pt-BR' and config['site_url'] == 'https://exemplo.github.io/minha-biblioteca/'
    assert config['nav'][1] == {'Livros criados': [{'Python do zero (exemplo de teste)': [
        {'Mapa do livro': 'created-books/python-do-zero-teste/README.md'},
        {'0. Como estudar este livro': 'created-books/python-do-zero-teste/chapters/00-como-estudar-este-livro.md'},
        {'1. Listas': 'created-books/python-do-zero-teste/chapters/01-listas.md'},
        {'2. O laço for': 'created-books/python-do-zero-teste/chapters/02-o-laco-for.md'},
        {'Simulado final': 'created-books/python-do-zero-teste/chapters/03-simulado-final.md'},
        {'Glossário': 'created-books/python-do-zero-teste/chapters/glossario.md'}]}]}
    docs = library / '_site' / 'docs'
    assert not (docs / BOOK_IN_LIB / 'book.yaml').exists()
    assert '??? success "Ver resposta"' in read(docs / BOOK_IN_LIB / 'chapters' / '01-listas.md')
    home = read(docs / 'index.md')
    assert '## Livros criados' in home and '## Materiais aprimorados' in home


def test_site_language_auto_falls_back_to_english(cli, library):
    import yaml
    settings = load(library / 'library.yaml')
    settings.update(default_language='auto', repository='')
    save(library / 'library.yaml', settings)
    cli('build', 'site', '--library', library, '--out', library / '_site')
    config = yaml.safe_load(read(library / '_site' / 'mkdocs.yml'))
    assert config['theme']['language'] == 'en' and 'site_url' not in config


@pytest.mark.slow
@pytest.mark.skipif(not shutil.which('zensical'), reason='zensical not installed')
def test_zensical_builds_the_site(cli, library):
    cli('build', 'site', '--library', library, '--out', library / '_site')
    built = subprocess.run(['zensical', 'build', '--clean'], cwd=library / '_site', capture_output=True, text=True)
    assert built.returncode == 0, built.stderr[-800:]
    html = read(library / '_site' / 'site' / BOOK_IN_LIB / 'chapters' / '01-listas' / 'index.html')
    assert '<details class="success"' in html and '<summary>Ver resposta</summary>' in html
    assert 'Guido van Rossum' in read(library / '_site' / 'site' / 'search.json')


def test_index_is_skipped_when_there_is_no_glossary(cli, book, tmp_path):
    os.remove(book / 'chapters' / 'glossario.md')
    code, r = cli('build', '--book', book, '--out', tmp_path / 'd', '--no-epub', '--no-zip')
    assert code == 0


def test_a_chapter_title_without_h1_uses_the_file_name(book):
    edit(book / 'chapters' / '03-simulado-final.md', '# Simulado final', 'Simulado final')
    assert build.h1(str(book / 'chapters' / '03-simulado-final.md')) == '03-simulado-final.md'
