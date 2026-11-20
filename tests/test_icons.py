"""icons.py: the embedded Lucide icons used by diagram.py."""
import xml.etree.ElementTree as ET

import icons
import pytest


def test_every_icon_is_valid_svg_markup():
    for name in icons.names():
        ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{icons.draw(name, 0, 0, 24, "#000")}</svg>')


def test_suggestions_for_a_typo():
    assert 'folder' in icons.suggest('foldr')


def test_known_names():
    assert icons.known('folder') and not icons.known('nope')


def test_draw_scales_to_the_size_and_colors_the_stroke():
    g = icons.draw('folder', 10, 20, 48, '#123456')
    assert 'translate(10,20) scale(2' in g and 'stroke="#123456"' in g


def test_unknown_icon_raises_key_error():
    with pytest.raises(KeyError):
        icons.draw('nope', 0, 0, 24, '#000')


def test_the_library_has_the_planned_size():
    assert 70 <= len(icons.names()) <= 110


def test_command_lists_icons(cli):
    code, result = cli('diagram', '--icons')
    assert code == 0 and 'folder' in result['icons']
