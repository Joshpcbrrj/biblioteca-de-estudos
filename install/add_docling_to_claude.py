#!/usr/bin/env python3
"""Adds the Docling MCP server to the Claude desktop app's settings, keeping everything else.

Usage:  python add_docling_to_claude.py [--config PATH] [--uvx PATH]

Finds claude_desktop_config.json (Windows, including the Microsoft Store install; macOS;
Linux), saves a backup next to it (.bak), and puts the "docling" entry under "mcpServers"
at the top level of the file, never inside "preferences". Running it again only updates
the entry. Restart the Claude app afterwards. See docs/integrations/docling.md.
"""
import argparse
import glob
import json
import os
import shutil
import sys

# versions that work together (docs/integrations/docling.md, "Common problems")
SERVER = {
    'args': ['--from', 'docling-mcp[local]==2.1.0', '--with', 'mcp<2', 'docling-mcp-server', '--transport', 'stdio'],
    'env': {'DOCLING_CONVERSION_MODE': 'local', 'DOCLING_MCP_CONVERSION_MODE': 'local'},
}


def candidates():
    home = os.path.expanduser('~')
    if sys.platform == 'win32':
        appdata, local = os.environ.get('APPDATA', ''), os.environ.get('LOCALAPPDATA', '')
        found = [os.path.join(appdata, 'Claude', 'claude_desktop_config.json')]
        # the Microsoft Store install and newer app versions keep it under LOCALAPPDATA
        found += glob.glob(os.path.join(local, 'Packages', 'Claude_*', 'LocalCache', 'Roaming', 'Claude',
                                        'claude_desktop_config.json'))
        found += glob.glob(os.path.join(local, 'Claude-Data', '*', 'claude_desktop_config.json'))
        return found
    if sys.platform == 'darwin':
        return [os.path.join(home, 'Library', 'Application Support', 'Claude', 'claude_desktop_config.json')]
    return [os.path.join(home, '.config', 'Claude', 'claude_desktop_config.json')]


def find_config():
    existing = [p for p in candidates() if os.path.exists(p)]
    return existing[0] if existing else candidates()[0]


def add(config_path, uvx):
    settings = {}
    if os.path.exists(config_path):
        text = open(config_path, encoding='utf-8').read()
        try:
            settings = json.loads(text) if text.strip() else {}
        except json.JSONDecodeError as e:
            sys.exit(f'{config_path} is not valid JSON ({e}); fix it or remove it, then run this again. '
                     'Nothing was changed.')
        shutil.copyfile(config_path, config_path + '.bak')
    settings.setdefault('mcpServers', {})['docling'] = {'command': uvx, **SERVER}
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return config_path


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--config', help='path to claude_desktop_config.json (found automatically if left out)')
    p.add_argument('--uvx', help='path to uvx (found on the PATH if left out)')
    args = p.parse_args()
    uvx = args.uvx or shutil.which('uvx')
    if not uvx:
        sys.exit('uvx not found: install uv first (docs/integrations/docling.md, step 1).')
    path = add(args.config or find_config(), os.path.abspath(uvx))
    print(f'Docling added to {path}')
    print('Quit the Claude app completely (also from the system tray) and open it again.')


if __name__ == '__main__':
    main()
