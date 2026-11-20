"""diagram.py: every diagram type, every fit problem, the reading profiles and the contact sheet."""
import copy
import xml.etree.ElementTree as ET

import diagram
import pytest
from conftest import load, save

NS = '{http://www.w3.org/2000/svg}'

SPECS = {
    'flow': {'steps': [{'kind': 'start', 'text': 'notas = [7.5, 8.0]'},
                       {'kind': 'decision', 'text': 'Há item?', 'label': 'sim', 'side': 'Mostra a média',
                        'side_label': 'não'},
                       {'kind': 'end', 'text': 'Média: 7.75'}]},
    'timeline': {'events': [{'when': '1947', 'text': 'Mariposa no relé', 'highlight': True},
                            {'when': '1948', 'text': 'Transistor'}]},
    'compare': {'style': 'wrong-right', 'left': {'title': 'Errado'}, 'right': {'title': 'Certo'},
                'rows': [['PI = 3', 'const PI = 3.14']]},
    'boxes': {'name': 'notas', 'cells': [{'value': '7.5', 'label': '0'}, {'value': '8.0', 'label': '1',
                                                                          'highlight': True}]},
    'layers': {'layers': [{'text': 'Código', 'note': 'COPY'}, {'text': 'Python 3.12'}]},
    'tree': {'root': {'text': 'compose.yaml', 'children': [{'text': 'api', 'children': [{'text': 'build'}]}]}},
    'sequence': {'participants': ['api', 'db'], 'messages': [{'from': 'api', 'to': 'db', 'text': 'conecta'},
                                                             {'from': 'db', 'to': 'api', 'text': 'ok',
                                                              'dashed': True}]},
    'bars': {'unit': ' MB', 'bars': [{'label': 'slim', 'value': 130, 'highlight': True},
                                     {'label': 'alpine', 'value': 55}]},
    'cards': {'cards': [{'icon': '[]', 'title': 'Lista', 'items': ['índice começa em 0'], 'code': ['n = [1]']},
                        {'icon': 'for', 'title': 'Laço', 'items': ['um item por volta']}]},
}
TEXTS = {'flow': 'Mostra a média', 'timeline': '1947', 'compare': '✅ Certo', 'boxes': 'notas', 'layers': 'COPY',
         'tree': 'build', 'sequence': '2. ok', 'bars': '130 MB', 'cards': '2. Laço'}


def spec(kind, **extra):
    # a deep copy: tests change the lists inside, and SPECS is shared by every test
    return {'type': kind, 'title': f'Um {kind} de teste', 'caption': 'Legenda.', **copy.deepcopy(SPECS[kind]), **extra}


@pytest.mark.parametrize('kind', sorted(SPECS))
@pytest.mark.parametrize('profile', ['large', 'small'])
def test_each_type_draws_a_valid_svg_in_both_profiles(kind, profile):
    text, height, problems, _ = diagram.render(spec(kind), profile)
    root = ET.fromstring(text)
    assert root.get('width') == str(diagram.PROFILES[profile]['width']) and int(root.get('height')) == height
    assert root.find(f'{NS}title').text == f'Um {kind} de teste'
    assert TEXTS[kind] in ''.join(t.text or '' for t in root.iter(f'{NS}text'))
    assert not problems


def test_alt_text_goes_to_the_description():
    text, *_ = diagram.render(spec('bars', alt='Barras com o tamanho de cada imagem.'))
    assert ET.fromstring(text).find(f'{NS}desc').text == 'Barras com o tamanho de cada imagem.'


@pytest.mark.parametrize('bad, message', [
    ({'type': 'pie', 'title': 'x'}, 'type must be one of'),
    ({'type': 'flow', 'steps': [{'text': 'a'}]}, 'needs "title"'),
    ({'type': 'flow', 'title': 'x'}, 'needs "steps"'),
    ({'type': 'flow', 'title': 'x', 'steps': [{'text': 'a', False: 'lost'}]}, 'yes/no/on/off'),
    ({'type': 'compare', 'title': 'x', 'rows': [['a', 'b', 'c']]}, 'exactly 2 values'),
])
def test_invalid_specs_are_refused(bad, message):
    with pytest.raises(ValueError, match=message):
        diagram.render(bad)


@pytest.mark.parametrize('kind, change, problem', [
    ('layers', lambda s: s['layers'].append({'text': 'x' * 120}), 'does not fit'),
    ('boxes', lambda s: s['cells'].append({'value': '1234567890123'}), 'does not fit in its box'),
    ('sequence', lambda s: s.update(participants=['a', 'b', 'c', 'd', 'e'],
                                     messages=[{'from': 'a', 'to': 'b', 'text': 'oi'}]), 'at most 4'),
    ('sequence', lambda s: s['messages'].append({'from': 'api', 'to': 'db', 'text': 'palavra ' * 30}),
     'longer than the space'),
    ('bars', lambda s: s['bars'].append({'label': 'um rótulo comprido demais para caber', 'value': 1}),
     'too long'),
    ('cards', lambda s: s['cards'].extend([{'title': f'c{i}'} for i in range(12)]), 'at most 12'),
    ('cards', lambda s: s['cards'][0].update(code=['x = "uma linha de código longa demais para o card"']),
     'does not fit in a card'),
])
def test_each_fit_problem_is_reported(kind, change, problem):
    s = spec(kind)
    change(s)
    _, _, problems, _ = diagram.render(s, 'small')
    assert any(problem in p for p in problems), problems


def test_too_many_elements_and_too_tall_for_a_small_screen_are_warnings():
    s = spec('layers')
    s['layers'] = [{'text': f'Camada {i}'} for i in range(12)]
    _, _, problems, warnings = diagram.render(s, 'small')
    assert not problems
    assert any('12 elements' in w for w in warnings) and any('px tall' in w for w in warnings)


def test_command_writes_the_svg_next_to_the_source_folder_with_the_book_profile(cli, book):
    data = load(book / 'book.yaml')
    data['choices']['reading'] = 'small'
    save(book / 'book.yaml', data)
    (book / 'img' / '_source').mkdir()
    save(book / 'img' / '_source' / 'c02-for.yaml', spec('flow'))
    code, r = cli('diagram', book / 'img' / '_source' / 'c02-for.yaml')
    assert code == 0 and r['fits'] and r['profile'] == 'small' and r['width'] == 480
    assert (book / 'img' / 'c02-for.svg').exists()


def test_command_reports_problems_with_exit_code_1(cli, tmp_path):
    s = spec('layers')
    s['layers'].append({'text': 'x' * 200})
    save(tmp_path / 'c.yaml', s)
    code, r = cli('diagram', tmp_path / 'c.yaml', '--reading', 'large', '--out', tmp_path / 'c.svg')
    assert code == 1 and not r['fits'] and (tmp_path / 'c.svg').exists()


@pytest.mark.parametrize('args, message', [
    (['nope.yaml'], 'spec not found'),
])
def test_command_errors(cli, args, message):
    code, r = cli('diagram', *args)
    assert code == 1 and message in r['error']


def test_command_reports_an_invalid_spec(cli, tmp_path):
    save(tmp_path / 'bad.yaml', {'type': 'pie', 'title': 'x'})
    code, r = cli('diagram', tmp_path / 'bad.yaml')
    assert code == 1 and 'invalid spec' in r['error']


def test_help_lists_every_type(capsys, monkeypatch):
    import sys
    monkeypatch.setattr(sys, 'argv', ['diagram.py', '--help'])
    with pytest.raises(SystemExit):
        diagram.main()
    printed = capsys.readouterr().out
    assert all(kind in printed for kind in diagram.TYPES)


def test_contact_sheet_of_a_chapter(cli, book):
    code, r = cli('diagram', '--sheet', 1, '--book', book)
    assert code == 0 and r['images'] == 1 and r['sheet'].endswith('_sheet-c01.svg')
    assert 'png' in r or 'note' in r


def test_contact_sheet_of_a_chapter_without_images(cli, book):
    code, r = cli('diagram', '--sheet', 2, '--book', book)
    assert code == 0 and r['images'] == 0


def test_contact_sheet_of_a_missing_chapter(cli, book):
    code, r = cli('diagram', '--sheet', 9, '--book', book)
    assert code == 1 and 'no file yet' in r['error']


def contrast(a, b):
    """WCAG contrast ratio between two #RRGGBB colors."""
    def lum(c):
        rgb = [int(c[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b_ = (v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in rgb)
        return 0.2126 * r + 0.7152 * g + 0.0722 * b_
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


@pytest.mark.parametrize('color', sorted(diagram.PALETTE))
def test_strong_text_is_readable_on_fill_and_tint(color):
    fill, _, strong, tint = diagram.PALETTE[color]
    assert contrast(strong, fill) >= 4.5 and contrast(strong, tint) >= 4.5


def test_subtitle_and_gradient_underline():
    text, *_ = diagram.render(spec('bars', subtitle='Seção 4 · classes'))
    assert 'Seção 4 · classes' in text and 'url(#underline)' in text and '<linearGradient id="underline"' in text


def test_box_with_note_and_icon_draws_both():
    s = spec('layers')
    s['layers'][0].update(icon='layers', note='COPY . .')
    text, _, problems, _ = diagram.render(s)
    assert 'COPY . .' in text and 'scale(' in text and not problems


def test_icon_takes_width_from_the_text_in_the_small_profile():
    word = 'x' * 51
    assert not diagram.render(dict(spec('layers'), layers=[{'text': word}]), 'small')[2]
    problems = diagram.render(dict(spec('layers'), layers=[{'text': word, 'icon': 'layers'}]), 'small')[2]
    assert any('does not fit' in p for p in problems)


def test_unknown_icon_is_a_problem_with_suggestions():
    s = spec('layers')
    s['layers'][0]['icon'] = 'foldr'
    assert any('unknown icon "foldr"' in p and 'folder' in p for p in diagram.render(s)[2])
