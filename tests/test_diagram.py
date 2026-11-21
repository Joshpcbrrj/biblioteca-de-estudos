"""diagram.py: every diagram type, every fit problem, the reading profiles and the contact sheet."""
import copy
import re
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
    'scene': {'steps': [['user'], ['list'], ['sparkles']], 'ops': ['+', '='], 'label': 'Melhor saída'},
    'chord': {'chords': [{'name': 'Em', 'frets': '022000', 'fingers': '023000'},
                         {'name': 'F', 'frets': '133211', 'fingers': '134211',
                          'barre': {'fret': 1, 'from': 6, 'to': 1}},
                         {'name': 'D7', 'frets': ['x', 'x', 0, 2, 1, 2]}]},
    'fretboard': {'frets': [5, 8], 'notes': [{'string': 6, 'fret': 5, 'label': 'A', 'root': True},
                                              {'string': 6, 'fret': 8, 'label': 'C'},
                                              {'string': 1, 'fret': 5, 'label': 'A',
                                               'root': True}]},
    'tab': {'steps': ['6:0', '4:2', '3:0', '|', '6:0 3:0']},
}
TEXTS = {'flow': 'Mostra a média', 'timeline': '1947', 'compare': 'Certo', 'boxes': 'notas', 'layers': 'COPY',
         'tree': 'build', 'sequence': '2. ok', 'bars': '130 MB', 'cards': '2. Laço', 'scene': 'Melhor saída',
         'chord': 'Em', 'fretboard': 'A', 'tab': '2'}


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
    (book / 'img' / '_source').mkdir(exist_ok=True)
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


@pytest.mark.parametrize('kind, change, expect', [
    ('flow', lambda s: s['steps'][0].update(icon='play', note='lê as notas'), 'lê as notas'),
    ('flow', lambda s: s['steps'][1].update(side_note='nada a fazer', side_color='teal', side_icon='info'),
     'nada a fazer'),
    ('flow', lambda s: s['steps'][1].update(note='a lista pode estar vazia'), 'a lista pode estar vazia'),
    ('tree', lambda s: s['root'].update(icon='file-code'), 'scale('),
    ('timeline', lambda s: s['events'][0].update(icon='bug'), 'scale('),
    ('sequence', lambda s: s.update(participants=[{'name': 'api', 'icon': 'server'}, 'db']), 'scale('),
    ('compare', lambda s: s['right'].update(icon='rocket'), 'scale('),
    ('boxes', lambda s: None, 'stroke-width="3"'),
])
def test_new_optional_fields(kind, change, expect):
    s = spec(kind)
    change(s)
    text, _, problems, _ = diagram.render(s)
    assert expect in text and not problems


def test_compare_wrong_right_uses_drawn_icons_not_emoji():
    text, *_ = diagram.render(spec('compare'))
    assert '✅' not in text and '❌' not in text and 'scale(' in text


@pytest.mark.parametrize('kind', sorted(SPECS))
def test_no_emoji_left_in_any_type(kind):
    text, *_ = diagram.render(spec(kind))
    assert not re.search('[✀-➿\U0001F300-\U0001FAFF]', text), kind


def test_scene_type_draws_steps_ops_and_label():
    s = {'type': 'scene', 'title': 'Prompt', 'steps': [['user'], ['list'], ['sparkles']],
         'ops': ['+', '='], 'label': 'Melhor saída'}
    text, _, problems, _ = diagram.render(s)
    assert 'Melhor saída' in text and '>+<' in text and '>=<' in text and not problems


@pytest.mark.parametrize('scene, problem', [
    ({'steps': [['file']] * 5}, 'at most 4 steps'),
    ({'steps': [[]]}, '1 to 3 icons'),
    ({'steps': [['file'] * 4]}, '1 to 3 icons'),
    ({'steps': [['file'], ['file']], 'ops': ['*']}, 'must be one of'),
    ({'steps': [['file'], ['foldr']]}, 'unknown icon "foldr"'),
])
def test_scene_limits(scene, problem):
    assert any(problem in p for p in diagram.render({'type': 'scene', 'title': 'x', **scene})[2])


def test_card_with_icon_name_items_with_icons_and_a_scene():
    s = spec('cards')
    s['cards'][0].update(icon='folder', items=[{'text': 'juntos', 'icon': 'files'}, 'instruções'],
                         scene={'steps': [['folder'], ['file', 'file']], 'label': 'Memória'})
    for profile in ('large', 'small'):
        text, _, problems, _ = diagram.render(s, profile)
        assert 'Memória' in text and 'instruções' in text and not problems


def test_card_ascii_icon_still_works():
    text, _, problems, _ = diagram.render(spec('cards'))
    assert '>for<' in text and not problems


def test_card_icon_named_like_a_lucide_icon_draws_it():
    s = spec('cards')
    s['cards'][1]['icon'] = 'code'
    text, _, problems, _ = diagram.render(s)
    assert '>code<' not in text and not problems


def test_a_long_scene_label_wraps_inside_the_card():
    s = spec('cards')
    s['cards'][0]['scene'] = {'steps': [['folder'], ['file']], 'label': 'Memória compartilhada entre as conversas'}
    text, _, problems, _ = diagram.render(s, 'small')
    assert 'Memória compartilhada entre as conversas' not in text and 'compartilhada' in text and not problems


def test_a_misspelled_card_icon_is_a_problem_not_a_text_badge():
    s = spec('cards')
    s['cards'][0]['icon'] = 'databse'
    problems = diagram.render(s)[2]
    assert any('unknown icon "databse"' in p and 'database' in p for p in problems)


def test_a_card_scene_may_be_a_list_of_steps():
    s = spec('cards')
    s['cards'][0]['scene'] = [['folder'], ['file']]
    _, _, problems, _ = diagram.render(s)
    assert not problems


def test_a_card_scene_in_another_shape_is_an_invalid_spec():
    s = spec('cards')
    s['cards'][0]['scene'] = 'folder'
    with pytest.raises(ValueError, match='scene must be'):
        diagram.render(s)


@pytest.mark.parametrize('change, problem', [
    (lambda s: s['chords'][0].update(frets='02200'), 'one position per string'),
    (lambda s: s['chords'][0].update(frets='0220z0'), 'one position per string'),
    (lambda s: s['chords'][0].update(fingers='025000'), 'fingers go from 1 to 4'),
    (lambda s: s['chords'][1].update(barre={'fret': 0, 'from': 6, 'to': 1}), 'barre'),
    (lambda s: s['chords'][1].update(barre={'fret': 1, 'from': 7, 'to': 1}), 'barre'),
    (lambda s: s['chords'].extend([{'name': 'E', 'frets': '022100'}] * 5), 'at most 6 chords'),
])
def test_chord_problems(change, problem):
    s = spec('chord')
    change(s)
    assert any(problem in p for p in diagram.render(s)[2]), diagram.render(s)[2]


@pytest.mark.parametrize('change, problem', [
    (lambda s: s['notes'].append({'string': 6, 'fret': 12, 'label': 'E'}), 'outside frets 5-8'),
    (lambda s: s['notes'].append({'string': 7, 'fret': 5, 'label': 'x'}), 'no string 7'),
])
def test_fretboard_problems(change, problem):
    s = spec('fretboard')
    change(s)
    assert any(problem in p for p in diagram.render(s)[2])


@pytest.mark.parametrize('steps', [['6-0'], ['9:0'], ['6:x']])
def test_tab_problems(steps):
    assert any('tab step' in p for p in diagram.render(spec('tab', steps=steps))[2])


def test_a_four_string_tuning_draws_four_strings():
    s = spec('chord', tuning=['G', 'C', 'E', 'A'], chords=[{'name': 'C', 'frets': '0003', 'fingers': '0003'}])
    text, _, problems, _ = diagram.render(s)
    assert not problems and text.count('class="string"') == 4


def test_high_chords_start_at_their_lowest_fret():
    s = spec('chord', chords=[{'name': 'A', 'frets': ['x', 0, 7, 6, 5, 5], 'fingers': 'x04312'}])
    text, _, problems, _ = diagram.render(s)
    assert not problems and '>5fr<' in text


def test_text_version_of_each_music_type():
    chords = diagram.text_version(spec('chord')).splitlines()
    # one line per string, highest first, with the finger after it: the format a reader copies
    assert chords[:3] == ['Em', 'e |--0--|', 'B |--0--|'] and 'A |--2--|  2' in chords
    assert 'A |--x--|' in chords and 'E |--1--|  1' in chords
    tab = diagram.text_version(spec('tab')).splitlines()
    assert tab[0].startswith('e|') and tab[-1].startswith('E|') and '|' in tab[-1][3:]
    assert '6:5 A*' in diagram.text_version(spec('fretboard'))
    assert diagram.text_version(spec('flow')) is None


def test_command_prints_the_text_version(cli, tmp_path):
    path = tmp_path / 'acordes.yaml'
    save(path, spec('chord'))
    code, r = cli('diagram', path, '--out', tmp_path / 'acordes.svg')
    assert code == 0 and r['text'].startswith('Em' + chr(10) + 'e |--0--|')
