"""install/: the Docling installers and the helper that edits the Claude app's settings."""
import json
import os
import shutil
import subprocess
import sys

import pytest
from conftest import ROOT

sys.path.insert(0, os.path.join(ROOT, 'install'))
import add_docling_to_claude as helper  # noqa: E402


def test_adds_docling_at_the_top_level_and_keeps_everything_else(tmp_path):
    config = tmp_path / 'claude_desktop_config.json'
    config.write_text(json.dumps({'preferences': {'sidebarMode': 'chat'},
                                  'mcpServers': {'other': {'command': 'x'}}}), encoding='utf-8')
    helper.add(str(config), '/home/me/.local/bin/uvx')
    data = json.loads(config.read_text(encoding='utf-8'))
    assert data['preferences'] == {'sidebarMode': 'chat'} and data['mcpServers']['other'] == {'command': 'x'}
    docling = data['mcpServers']['docling']
    assert docling['command'] == '/home/me/.local/bin/uvx' and 'mcp<2' in docling['args']
    assert docling['args'][-2:] == ['--transport', 'stdio'] and docling['env']['DOCLING_MCP_CONVERSION_MODE'] == 'local'
    assert 'mcpServers' not in data['preferences']
    assert (tmp_path / 'claude_desktop_config.json.bak').exists()


def test_running_twice_only_updates_the_entry(tmp_path):
    config = tmp_path / 'c.json'
    helper.add(str(config), 'uvx-1')
    helper.add(str(config), 'uvx-2')
    data = json.loads(config.read_text(encoding='utf-8'))
    assert list(data['mcpServers']) == ['docling'] and data['mcpServers']['docling']['command'] == 'uvx-2'


def test_creates_the_file_when_there_is_none(tmp_path):
    config = tmp_path / 'Claude' / 'claude_desktop_config.json'
    helper.add(str(config), 'uvx')
    assert json.loads(config.read_text(encoding='utf-8'))['mcpServers']['docling']['command'] == 'uvx'


def test_an_invalid_file_is_left_untouched(tmp_path):
    config = tmp_path / 'c.json'
    config.write_text('{"preferences": {', encoding='utf-8')
    with pytest.raises(SystemExit, match='not valid JSON'):
        helper.add(str(config), 'uvx')
    assert config.read_text(encoding='utf-8') == '{"preferences": {'


def test_finds_an_existing_config_among_the_candidates(tmp_path, monkeypatch):
    real = tmp_path / 'b' / 'claude_desktop_config.json'
    real.parent.mkdir()
    real.write_text('{}')
    monkeypatch.setattr(helper, 'candidates', lambda: [str(tmp_path / 'a' / 'x.json'), str(real)])
    assert helper.find_config() == str(real)
    monkeypatch.setattr(helper, 'candidates', lambda: [str(tmp_path / 'a' / 'x.json')])
    assert helper.find_config() == str(tmp_path / 'a' / 'x.json')


def test_each_system_has_a_candidate():
    assert all(p.endswith('claude_desktop_config.json') for p in helper.candidates())


def test_command_line(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['x', '--config', str(tmp_path / 'c.json'), '--uvx', 'uvx'])
    helper.main()
    assert 'Docling added' in capsys.readouterr().out
    monkeypatch.setattr(sys, 'argv', ['x', '--config', str(tmp_path / 'c.json')])
    monkeypatch.setattr(helper.shutil, 'which', lambda name: None)
    with pytest.raises(SystemExit, match='uvx not found'):
        helper.main()


@pytest.mark.skipif(not shutil.which('shellcheck'), reason='shellcheck not installed')
def test_the_shell_installer_passes_shellcheck():
    r = subprocess.run(['shellcheck', os.path.join(ROOT, 'install', 'install-docling.sh')],
                       capture_output=True, text=True)
    assert r.returncode == 0, r.stdout


@pytest.mark.skipif(not shutil.which('powershell') and not shutil.which('pwsh'), reason='PowerShell not available')
def test_the_powershell_installer_parses():
    shell = shutil.which('pwsh') or shutil.which('powershell')
    path = os.path.join(ROOT, 'install', 'install-docling.ps1')
    command = ('$e = $null; [System.Management.Automation.Language.Parser]::ParseFile('
               f"'{path}', [ref]$null, [ref]$e) | Out-Null; if ($e.Count) {{ $e; exit 1 }}")
    r = subprocess.run([shell, '-NoProfile', '-Command', command], capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
