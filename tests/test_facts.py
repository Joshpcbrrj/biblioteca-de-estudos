"""facts.py: which sentences need a fact check, and which do not."""
import facts
import pytest


def kinds(line):
    found = [s for _, s in facts.sentences(line)]
    assert found, f'no sentence extracted from: {line}'
    return {k for k, rx in facts.PATTERNS.items() if rx.search(found[0])}


@pytest.mark.parametrize('line, kind', [
    ('A mariposa foi encontrada em setembro de 1947 no relé.', 'date'),
    ('O prazo vence em 15/03/2027 para todos.', 'date'),
    ('O circuito usa uma fonte de 5 V e consome pouco.', 'number'),
    ('A taxa de acerto subiu para 30% no segundo teste.', 'number'),
    ('A anotação dizia “primeiro caso real de bug encontrado” no caderno.', 'quote'),
    ('A linguagem foi criada por Guido na Holanda.', 'name'),
])
def test_each_kind_of_fact_is_detected(line, kind):
    assert kind in kinds(line)


@pytest.mark.parametrize('text', [
    '```python\nprint("Lançado em 1991 por Guido")\n```',
    '## O que aconteceu em 1947',
    '| --- | --- |',
    '- [The Python Tutorial](https://docs.python.org/3/tutorial/), conferido em 2026-11-20.',
    'Curto.',
])
def test_code_headings_separators_source_lists_and_short_lines_are_skipped(text):
    assert list(facts.sentences(text)) == []


def test_a_table_cell_is_not_taken_for_a_name():
    assert all('name' not in kinds(c) for c in ['| Item | Em uma frase longa aqui |'])


def test_the_command_lists_the_dated_sentence(cli, book):
    code, r = cli('facts', 2, '--book', book)
    assert code == 0 and r['to_check'] >= 1
    assert any('1991' in s['sentence'] and 'date' in s['kinds'] for s in r['sentences'])


def test_the_command_reports_a_chapter_without_a_file(cli, book):
    code, r = cli('facts', 9, '--book', book)
    assert code == 1 and 'no file yet' in r['error']
