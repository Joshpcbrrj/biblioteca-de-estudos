#!/usr/bin/env python3
"""Registro de progresso da remodelagem (para retomar depois de uma
compactação de contexto sem refazer páginas).

O estado fica em /tmp/ss/progresso-<curso>.json (fora do repositório).

Uso:
  progresso.py <curso> init <id> [<id> ...]   cadastra as páginas, em ordem
  progresso.py <curso> nota <id> "<texto>"    anota (ex.: título ou imagens)
  progresso.py <curso> feito <id> [<id> ...]  marca como concluídas
  progresso.py <curso> pendentes              lista o que falta (JSON)
  progresso.py <curso> status                 resumo: total, feitas, próxima

Ids podem ser parciais (os 8 primeiros caracteres bastam se forem únicos).
"""
import json, os, sys

DIR = '/tmp/ss'


def carregar(curso):
    p = os.path.join(DIR, f'progresso-{curso}.json')
    if os.path.exists(p):
        return p, json.load(open(p))
    return p, {'curso': curso, 'paginas': []}


def achar(est, pid):
    pid = pid.replace('-', '')
    cand = [p for p in est['paginas'] if p['id'].startswith(pid)]
    if len(cand) != 1:
        sys.exit(f'id "{pid}" não encontrado ou ambíguo')
    return cand[0]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    curso, cmd, args = sys.argv[1], sys.argv[2], sys.argv[3:]
    os.makedirs(DIR, exist_ok=True)
    caminho, est = carregar(curso)
    if cmd == 'init':
        ja = {p['id'] for p in est['paginas']}
        for a in args:
            a = a.replace('-', '')
            if a not in ja:
                est['paginas'].append({'id': a, 'feito': False, 'nota': ''})
    elif cmd == 'nota':
        achar(est, args[0])['nota'] = ' '.join(args[1:])
    elif cmd == 'feito':
        for a in args:
            achar(est, a)['feito'] = True
    elif cmd == 'pendentes':
        print(json.dumps([p for p in est['paginas'] if not p['feito']],
                         ensure_ascii=False, indent=1))
        return
    elif cmd == 'status':
        pend = [p for p in est['paginas'] if not p['feito']]
        print(json.dumps({'total': len(est['paginas']),
                          'feitas': len(est['paginas']) - len(pend),
                          'proxima': pend[0] if pend else None},
                         ensure_ascii=False))
        return
    else:
        sys.exit(f'comando desconhecido: {cmd}')
    json.dump(est, open(caminho, 'w'), ensure_ascii=False, indent=1)
    print(json.dumps({'ok': True, 'arquivo': caminho}))


if __name__ == '__main__':
    main()
