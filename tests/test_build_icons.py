"""tools/build_icons.py: picks the Lucide icons the diagrams use and keeps their inner markup."""
import json

import build_icons

LUCIDE = '''<!-- @license lucide-static v1.77.0 - ISC -->
<svg
  class="lucide lucide-folder"
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
>
  <path d="M1 1h2" />
  <circle cx="5" cy="5" r="1" />
</svg>
'''


def test_build_keeps_the_inner_markup_and_reports_missing(tmp_path):
    (tmp_path / 'folder.svg').write_text(LUCIDE, encoding='utf-8')
    icons, missing = build_icons.build(str(tmp_path), ['folder', 'nope'])
    assert icons == {'folder': '<path d="M1 1h2"/><circle cx="5" cy="5" r="1"/>'} and missing == ['nope']


def test_command_writes_sorted_json_and_lists_what_is_missing(tmp_path, monkeypatch, capsys):
    (tmp_path / 'folder.svg').write_text(LUCIDE, encoding='utf-8')
    (tmp_path / 'atom.svg').write_text(LUCIDE, encoding='utf-8')
    monkeypatch.setattr(build_icons, 'NAMES', ['folder', 'atom', 'nope'])
    out = tmp_path / 'icons.json'
    monkeypatch.setattr('sys.argv', ['build_icons.py', str(tmp_path), '--out', str(out)])
    build_icons.main()
    data = json.loads(out.read_text(encoding='utf-8'))
    assert list(data) == ['atom', 'folder']
    assert 'nope' in capsys.readouterr().out
