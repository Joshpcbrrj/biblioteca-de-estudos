#!/usr/bin/env python3
"""Gera os links raw do GitHub (fixados no hash do commit) para subir SVGs
no Notion com notion-create-attachment(source_url=...).

Uso:  python3 -I ferramentas/raw_urls.py programacao/<slug> [arquivo.svg ...]

Sem nomes de arquivo, lista todos os SVGs de img/ (sem a pasta img/epub/).
Saída JSON: {"hash": ..., "publicado": true/false, "urls": {"x.svg": url}}.
"publicado" é false se o commit atual ainda não está em origin/main
(nesse caso faça push antes: o Notion não acha arquivos não publicados).
"""
import json, os, subprocess, sys

REPO = 'Joshpcbrrj/biblioteca-de-estudos'


def git(*a):
    return subprocess.run(['git', *a], capture_output=True, text=True).stdout.strip()


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    curso = sys.argv[1].rstrip('/')
    nomes = sys.argv[2:] or sorted(f for f in os.listdir(f'{curso}/img') if f.endswith('.svg'))
    h = git('rev-parse', 'HEAD')
    git('fetch', '-q', 'origin', 'main')
    remoto = git('rev-parse', 'FETCH_HEAD')
    publicado = remoto == h or subprocess.run(
        ['git', 'merge-base', '--is-ancestor', h, remoto],
        capture_output=True).returncode == 0
    sujos = git('status', '--porcelain', '--', f'{curso}/img')
    urls = {n: f'https://raw.githubusercontent.com/{REPO}/{h}/{curso}/img/{n}' for n in nomes}
    faltando = [n for n in nomes if not os.path.exists(f'{curso}/img/{n}')]
    print(json.dumps({'hash': h, 'publicado': publicado, 'img_nao_commitadas': bool(sujos),
                      'faltando': faltando, 'urls': urls}, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
