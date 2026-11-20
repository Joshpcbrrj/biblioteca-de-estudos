"""book.py: every validation rule, the chapter brief and skeleton, progress and status."""
import os

import pytest
from conftest import SAMPLE, edit, load, read, save


def validate_with(cli, tmp_path, change):
    data = load(os.path.join(SAMPLE, 'book.yaml'))
    change(data)
    path = tmp_path / 'draft.yaml'
    save(path, data)
    return cli('book', 'validate', path)


def test_the_sample_book_is_valid_and_gets_selected(cli, book):
    code, r = cli('book', 'validate', book / 'book.yaml')
    assert code == 0 and r['ok'] and not r['warnings'], r
    assert r['book'] == {'title': 'Python do zero (exemplo de teste)', 'chapters': 2, 'concepts': 2, 'approved': True}
    code, r = cli('book', 'status')  # no --book: uses the selection
    assert code == 0 and r['slug'] == 'python-do-zero-teste'


def test_a_missing_file_is_reported(cli, tmp_path):
    code, r = cli('book', 'validate', tmp_path / 'nope.yaml')
    assert code == 1 and 'file not found' in r['error']


ERRORS = [
    ('missing field', lambda d: d.pop('goal'), 'missing field: goal'),
    ('bad slug', lambda d: d.update(slug='Python Zero'), 'slug:'),
    ('bad origin', lambda d: d.update(origin='copied'), 'origin:'),
    ('no profile', lambda d: d.update(profiles=[]), 'profiles:'),
    ('three profiles', lambda d: d.update(profiles=['stem', 'languages', 'skills']), 'profiles:'),
    ('unknown profile', lambda d: d.update(profiles=['cooking']), 'profiles:'),
    ('level without end', lambda d: d.update(level={'start': 'iniciante'}), 'level:'),
    ('bad image choice', lambda d: d['choices'].update(images='photos'), 'choices.images'),
    ('bad reading choice', lambda d: d['choices'].update(reading='tiny'), 'choices.reading'),
    ('source without url', lambda d: d['sources'][0].pop('url'), 'needs title and url'),
    ('source date', lambda d: d['sources'][0].update(checked='ontem'), 'checked must be'),
    ('chapter gap', lambda d: d['chapters'][1].update(n=3), 'n must go 1, 2, 3'),
    ('chapter without goal', lambda d: d['chapters'][0].pop('goal'), 'chapter 1: missing goal'),
    ('concept id', lambda d: d['concepts'][0].update(id='Lista'), 'id must be lowercase'),
    ('concept twice', lambda d: d['concepts'].append(dict(d['concepts'][0])), 'listed twice'),
    ('concept chapter', lambda d: d['concepts'][0].update(chapter=9), 'chapter 9 does not exist'),
    ('unknown dependency', lambda d: d['concepts'][1].update(depends=['dicionario']), 'unknown concept'),
    ('used before taught', lambda d: (d['concepts'][0].update(chapter=2), d['concepts'][1].update(chapter=1)),
     'taught later'),
    ('improved without original', lambda d: d.update(origin='improved', promise={'goal': 1, 'audience': 1,
                                                                                  'level': 1, 'sequence': 1}),
     'missing original'),
    ('improved without promise', lambda d: d.update(origin='improved', original={'title': 'x'}),
     'promise needs'),
    ('translation without glossary', lambda d: d.update(translation_of='python-do-zero'), 'missing glossary'),
    ('approval date', lambda d: d.update(approved_on='ontem'), 'approved_on:'),
]


@pytest.mark.parametrize('case, change, message', ERRORS, ids=[e[0] for e in ERRORS])
def test_each_validation_error(cli, tmp_path, case, change, message):
    code, r = validate_with(cli, tmp_path, change)
    assert code == 1 and any(message in e for e in r['errors']), r['errors']


WARNINGS = [
    ('no sources', lambda d: d.update(sources=[]), 'sources: empty'),
    ('goal that cannot be checked', lambda d: d['chapters'][0].update(goal='Entender listas'), 'cannot be checked'),
    ('no topics', lambda d: d['chapters'][0].pop('topics'), 'no topics'),
    ('no minutes', lambda d: d['chapters'][0].pop('minutes'), 'minutes missing'),
    ('chapter without concepts', lambda d: d['concepts'].pop(), 'teaches no concept'),
    ('improved without mapping', lambda d: d.update(origin='improved', original={'title': 'x'},
                                                   promise={'goal': 1, 'audience': 1, 'level': 1, 'sequence': 1}),
     'sources_original empty'),
    ('too much new content', lambda d: d.update(origin='improved', original={'title': 'x'}, new_content_pct=35,
                                                promise={'goal': 1, 'audience': 1, 'level': 1, 'sequence': 1}),
     'above the ~20% limit'),
]


@pytest.mark.parametrize('case, change, message', WARNINGS, ids=[w[0] for w in WARNINGS])
def test_each_validation_warning(cli, tmp_path, case, change, message):
    code, r = validate_with(cli, tmp_path, change)
    assert code == 0 and any(message in w for w in r['warnings']), r['warnings']


def test_brief_creates_a_skeleton_in_the_book_language(cli, book):
    os.remove(book / 'chapters' / '02-o-laco-for.md')
    code, r = cli('book', 'brief', 2, '--book', book)
    assert code == 0 and r['skeleton_created'] and r['file'] == 'chapters/02-o-laco-for.md'
    assert r['concepts_you_may_use'] == ['lista'] and r['concepts_to_teach'] == ['laço for']
    assert r['previous']['title'] == 'Listas' and r['next'] is None and r['warm_up_from'] == [1]
    text = read(book / r['file'])
    for heading in ('# 2. O laço for', '## De onde paramos', '## O laço for', '## 🏋️ Pratique',
                    '## 🧠 Revisão rápida', '## 📚 Fontes', '🔁 **Revise hoje:** 1'):
        assert heading in text, heading


def test_chapter_one_has_no_warm_up_and_no_where_we_left_off(cli, book):
    os.remove(book / 'chapters' / '01-listas.md')
    code, r = cli('book', 'brief', 1, '--book', book)
    text = read(book / r['file'])
    assert 'De onde paramos' not in text and 'Aquecimento' not in text and r['previous'] is None


def test_brief_never_overwrites_a_chapter(cli, book):
    before = read(book / 'chapters' / '01-listas.md')
    code, r = cli('book', 'brief', 1, '--book', book)
    assert code == 0 and not r['skeleton_created'] and read(book / 'chapters' / '01-listas.md') == before


def test_brief_spaced_review_and_previous_summary(cli, book):
    data = load(book / 'book.yaml')
    data['chapters'] = [{'n': n, 'title': f'Capítulo {n}', 'goal': 'Fazer algo', 'topics': ['t'], 'minutes': 10}
                        for n in range(1, 9)]
    data['concepts'] = [{'id': f'c{n}', 'name': f'c{n}', 'chapter': n, 'depends': []} for n in range(1, 9)]
    data['progress'] = [{'n': 7, 'done': '2026-11-20', 'summary': 'Ensinou c7.'}]
    save(book / 'book.yaml', data)
    code, r = cli('book', 'brief', 8, '--book', book)
    assert r['review_today'] == [1, 5, 7] and r['previous']['summary'] == 'Ensinou c7.'


def test_brief_for_an_improved_book_lists_the_original_sections(cli, book):
    data = load(book / 'book.yaml')
    data['chapters'][0]['sources_original'] = ['aula-01', 'aula-02']
    save(book / 'book.yaml', data)
    code, r = cli('book', 'brief', 1, '--book', book)
    assert r['original_sections'] == ['aula-01', 'aula-02']


def test_brief_for_a_translation_points_to_the_original_chapter(cli, book, tmp_path):
    import shutil
    shutil.copytree(book, tmp_path / 'python-do-zero')
    data = load(book / 'book.yaml')
    data.update(translation_of='python-do-zero', glossary=[{'source': 'lista', 'target': 'list'}])
    save(book / 'book.yaml', data)
    code, r = cli('book', 'brief', 1, '--book', book)
    assert r['original_chapter'].endswith('python-do-zero/chapters/01-listas.md') and r['glossary']


def test_brief_for_a_chapter_not_in_the_syllabus(cli, book):
    code, r = cli('book', 'brief', 9, '--book', book)
    assert code == 1 and 'chapter 9 is not in book.yaml' in r['error']


def test_done_records_progress_and_points_to_the_next_step(cli, book):
    code, r = cli('book', 'done', 1, '--summary', 'Listas e len.', '--book', book)
    assert code == 0 and r == {'saved': True, 'progress': '1/2', 'next': 'book.py brief 2'}
    code, r = cli('book', 'done', 1, '--summary', 'Listas, len e índices.', '--book', book)
    assert [p['summary'] for p in load(book / 'book.yaml')['progress']] == ['Listas, len e índices.']
    code, r = cli('book', 'done', 2, '--summary', 'Laço for.', '--book', book)
    assert r['progress'] == '2/2' and 'fixed parts' in r['next']


@pytest.mark.parametrize('setup, message', [
    (lambda b: os.remove(b / 'chapters' / '01-listas.md'), 'has no file yet'),
    (lambda b: edit(b / 'chapters' / '01-listas.md', '## Listas', '## Listas\n\n<!-- TODO: x -->'), 'TODO'),
])
def test_done_refuses_an_unfinished_chapter(cli, book, setup, message):
    setup(book)
    code, r = cli('book', 'done', 1, '--summary', 'x', '--book', book)
    assert code == 1 and message in r['error']


def test_done_requires_a_summary(cli, book):
    code, r = cli('book', 'done', 1, '--book', book)
    assert code == 1 and '--summary is required' in r['error']


@pytest.mark.parametrize('change, step', [
    (lambda d, b: d.update(approved_on=''), 'syllabus not approved yet'),
    (lambda d, b: d.pop('choices'), 'ask the choices'),
    (lambda d, b: None, 'book.py brief 1'),
    (lambda d, b: (d.update(progress=[{'n': 1, 'summary': 'a'}, {'n': 2, 'summary': 'b'}]),
                   os.remove(b / 'chapters' / 'glossario.md')), 'write the fixed parts: glossary'),
    (lambda d, b: d.update(progress=[{'n': 1, 'summary': 'a'}, {'n': 2, 'summary': 'b'}]), 'audit.py'),
])
def test_status_next_step(cli, book, change, step):
    data = load(book / 'book.yaml')
    change(data, book)
    save(book / 'book.yaml', data)
    code, r = cli('book', 'status', '--book', book)
    assert step in r['next_step'], r
