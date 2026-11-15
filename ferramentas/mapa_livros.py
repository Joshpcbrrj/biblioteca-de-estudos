#!/usr/bin/env python3
"""Mapa das trilhas de livros: o que cada livro cobre e em que ordem ler.

Lê livros/*/ementa.yaml (a ementa aprovada de cada livro) e:

  python3 ferramentas/mapa_livros.py                 # JSON com trilhas e tópicos cobertos
  python3 ferramentas/mapa_livros.py --md            # reescreve livros/README.md (mapa legível)
  python3 ferramentas/mapa_livros.py --checar <ementa.yaml>
        # compara uma ementa nova (rascunho) com os livros existentes: tópicos
        # repetidos, pré-requisitos que não existem, posição na trilha

A skill criar-livro-tecnologia usa este script antes de propor uma ementa,
para não repetir o que outro livro já ensina e para ligar o livro novo aos
anteriores. Só as ementas com "aprovada_em" preenchido entram no mapa.
"""
import glob, json, os, sys

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit('Falta o PyYAML: pip install pyyaml')

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIVROS = os.environ.get('LIVROS_DIR', os.path.join(RAIZ, 'livros'))
NIVEIS = {'iniciante': 1, 'intermediário': 2, 'intermediario': 2, 'avançado': 3, 'avancado': 3}
OBRIGATORIOS = ['titulo', 'slug', 'trilha', 'nivel', 'objetivo', 'capitulos', 'cobre']


def carregar(caminho):
    with open(caminho, encoding='utf-8') as f:
        e = yaml.safe_load(f) or {}
    faltam = [k for k in OBRIGATORIOS if not e.get(k)]
    if faltam:
        raise ValueError(f'{caminho}: faltam os campos {faltam}')
    e['cobre'] = [str(t).strip().lower() for t in e['cobre']]
    e.setdefault('pre_requisitos', [])
    e.setdefault('fica_para_depois', [])
    return e


def ementas(somente_aprovadas=True):
    lista = []
    for c in sorted(glob.glob(os.path.join(LIVROS, '*', 'ementa.yaml'))):
        e = carregar(c)
        if somente_aprovadas and not e.get('aprovada_em'):
            continue
        lista.append(e)
    return lista


def mapa():
    trilhas, topicos = {}, {}
    for e in ementas():
        trilhas.setdefault(e['trilha'], []).append({
            'slug': e['slug'], 'titulo': e['titulo'], 'nivel': e['nivel'],
            'ordem': e.get('ordem_na_trilha', 99), 'pre_requisitos': e['pre_requisitos'],
            'capitulos': len(e['capitulos']), 'fica_para_depois': e['fica_para_depois']})
        for t in e['cobre']:
            topicos.setdefault(t, []).append(e['slug'])
    for t in trilhas.values():
        t.sort(key=lambda x: (x['ordem'], NIVEIS.get(x['nivel'], 9)))
    return {'trilhas': trilhas, 'topicos': topicos}


def checar(caminho):
    novo = carregar(caminho)
    m = mapa()
    existentes = {b['slug'] for t in m['trilhas'].values() for b in t}
    repetidos = {t: m['topicos'][t] for t in novo['cobre'] if t in m['topicos']
                 and novo['slug'] not in m['topicos'][t]}
    pre_inexistentes = [p for p in novo['pre_requisitos'] if p not in existentes]
    trilha = m['trilhas'].get(novo['trilha'], [])
    sugeridos = sorted({x for b in trilha for x in b['fica_para_depois']} - set(novo['cobre']))
    total = len(novo['cobre']) or 1
    return {
        'livro': novo['slug'],
        'trilha': novo['trilha'],
        'livros_na_trilha': [f"{b['ordem']}. {b['titulo']} ({b['nivel']})" for b in trilha],
        'topicos_repetidos': repetidos,
        'sobreposicao': f'{round(100 * len(repetidos) / total)}%',
        'pre_requisitos_inexistentes': pre_inexistentes,
        'temas_pendentes_da_trilha': sugeridos,
        'alerta': len(repetidos) / total > 0.4,
    }


def markdown():
    m = mapa()
    linhas = ['# 🗺️ Mapa dos livros', '',
              'Gerado por `ferramentas/mapa_livros.py --md` a partir das ementas aprovadas. '
              'Não edite à mão.', '']
    if not m['trilhas']:
        linhas += ['Ainda não há livros. Para criar o primeiro, veja o [COMO-USAR.md](../COMO-USAR.md).']
    for nome, livros in sorted(m['trilhas'].items()):
        linhas += [f'## Trilha: {nome}', '', '| Ordem | Livro | Nível | Pré-requisitos |',
                   '| --- | --- | --- | --- |']
        for b in livros:
            pre = ', '.join(b['pre_requisitos']) or '—'
            linhas.append(f"| {b['ordem']} | [{b['titulo']}]({b['slug']}/) | {b['nivel']} | {pre} |")
        pend = sorted({x for b in livros for x in b['fica_para_depois']})
        if pend:
            linhas += ['', f"**Próximos temas sugeridos:** {', '.join(pend)}."]
        linhas.append('')
    os.makedirs(LIVROS, exist_ok=True)
    with open(os.path.join(LIVROS, 'README.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas).rstrip() + '\n')
    print('livros/README.md atualizado.')


if __name__ == '__main__':
    a = sys.argv[1:]
    if '--md' in a:
        markdown()
    elif '--checar' in a:
        print(json.dumps(checar(a[a.index('--checar') + 1]), ensure_ascii=False, indent=1))
    else:
        print(json.dumps(mapa(), ensure_ascii=False, indent=1))
