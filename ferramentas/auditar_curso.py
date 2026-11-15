#!/usr/bin/env python3
"""Auditoria mecânica de um curso já convertido para Markdown.

Uso:  python3 -I ferramentas/auditar_curso.py programacao/<slug> [--resumo | --criterios]

Saída: JSON em stdout com tudo o que a skill manda conferir "à mão":
- estrutura da pasta do curso (só README.md, metadata.yaml, capa.*, aulas/, img/);
- título do metadata.yaml no formato "<Plataforma(s)>: <Nome> - <Criador>";
- por aula: nº de imagens, imagens sem callout de Analogia logo abaixo,
  linhas de código > 60 caracteres, tabelas com mais de 4 colunas,
  blocos de código sem nenhum comentário, sobras de HTML do Notion,
  <details> sem as linhas em branco obrigatórias, seções obrigatórias ausentes;
- imagens referenciadas que não existem em img/ e imagens órfãs.
Com --resumo, mostra só os totais e as aulas com problema.
Com --criterios, aplica o critério de pronto da skill: lista ERROS (impedem
publicar) e AVISOS (aceitáveis se registrados no ESTADO.md) e sai com código 1
se houver algum erro. É o que a Action de testes usa.
Não altera nenhum arquivo.
"""
import json, os, re, sys

PERMITIDOS = {'README.md', 'metadata.yaml', 'capa.png', 'capa.svg', 'aulas', 'img'}
SOBRAS = ['<callout', '<toggle', '<aside', '<page ', 'notion-file-block', '&lt;', '<unknown']
SECOES = {'nesta_aula': r'Nesta (aula|lista)', 'de_onde': r'De onde paramos', 'revisao': r'Revisão rápida',
          'resumo': r'📌 Resumo', 'proximo': r'Próximo passo'}
COMENT = re.compile(r'^\s*(//|#|--|/\*|\*|<!--|;|%)')
TITULO = re.compile(r'^[^:]+: .+ - .+$')


def auditar_aula(caminho, primeira=False):
    linhas = open(caminho, encoding='utf-8').read().split('\n')
    texto = '\n'.join(linhas)
    r = {'imagens': [], 'sem_analogia': [], 'codigo_longo': [], 'tabela_larga': [],
         'codigo_sem_comentario': [], 'sobras_html': [], 'details_sem_branco': [],
         'secoes_ausentes': []}
    em_codigo, ini, tem_coment, lang = False, 0, False, ''
    for i, l in enumerate(linhas, 1):
        if l.lstrip().startswith('```'):
            if not em_codigo:
                em_codigo, ini, tem_coment, lang = True, i, False, l.strip()[3:]
            else:
                tamanho = i - ini - 1
                if not tem_coment and tamanho >= 4 and lang not in ('json', 'txt', 'text', ''):
                    r['codigo_sem_comentario'].append(ini)
                em_codigo = False
            continue
        if em_codigo:
            if len(l) > 60:
                r['codigo_longo'].append(i)
            if COMENT.match(l) or re.search(r'\s(//|#|--)\s', l):
                tem_coment = True
            continue
        m = re.search(r'!\[[^\]]*\]\(\.\./img/([^)]+)\)', l)
        if m:
            r['imagens'].append(m.group(1))
            seguinte = '\n'.join(linhas[i:i + 3])
            if 'Analogia' not in seguinte and 'mapa' not in m.group(1):
                r['sem_analogia'].append(m.group(1))
        if l.startswith('|') and l.count('|') - 1 > 4 and not re.match(r'^\|[\s:|-]+\|$', l):
            r['tabela_larga'].append(i)
        for s in SOBRAS:
            if s in l:
                r['sobras_html'].append(i)
                break
        if l.strip().startswith('<summary>') and i < len(linhas) and linhas[i].strip() != '':
            r['details_sem_branco'].append(i)
        if l.strip() == '</details>' and i >= 2 and linhas[i - 2].strip() != '':
            r['details_sem_branco'].append(i)
    nome = os.path.basename(caminho)
    if not nome.startswith('00-'):
        for k, rx in SECOES.items():
            # a primeira aula não tem aula anterior para retomar
            if k == 'de_onde' and primeira:
                continue
            if not re.search(rx, texto):
                r['secoes_ausentes'].append(k)
    r['tabela_larga'] = sorted(set(r['tabela_larga']))
    return r


ERROS = ['codigo_longo', 'codigo_sem_comentario', 'sobras_html', 'details_sem_branco', 'secoes_ausentes']
AVISOS = ['sem_analogia', 'tabela_larga']


def criterios(out):
    erros, avisos = [], []
    if out['estrutura_extra']:
        erros.append(f"pasta do curso com itens extras: {out['estrutura_extra']}")
    if out['titulo_ok'] is False:
        erros.append(f"título fora do formato '<Plataforma>: <Nome> - <Criador>': {out.get('titulo')}")
    if out['img_faltando']:
        erros.append(f"imagens citadas que não existem: {out['img_faltando']}")
    for f, a in out['aulas'].items():
        for k in ERROS:
            if a[k]:
                erros.append(f'{f}: {k} {a[k]}')
        for k in AVISOS:
            if a[k]:
                avisos.append(f'{f}: {k} {a[k]}')
    return erros, avisos


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    base = sys.argv[1].rstrip('/')
    so_resumo = '--resumo' in sys.argv
    out = {'curso': base, 'estrutura_extra': [], 'titulo_ok': None, 'aulas': {},
           'img_faltando': [], 'img_orfas': [], 'totais': {}}
    out['estrutura_extra'] = sorted(set(os.listdir(base)) - PERMITIDOS)
    meta = os.path.join(base, 'metadata.yaml')
    if os.path.exists(meta):
        m = re.search(r'^title:\s*"?(.+?)"?\s*$', open(meta, encoding='utf-8').read(), re.M)
        out['titulo'] = m.group(1) if m else None
        out['titulo_ok'] = bool(m and TITULO.match(m.group(1)))
    aulas_dir = os.path.join(base, 'aulas')
    usadas = set()
    nomes = [f for f in sorted(os.listdir(aulas_dir)) if f.endswith('.md')]
    primeira = next((f for f in nomes if not f.startswith('00-')), None)
    for f in nomes:
        if f.endswith('.md'):
            r = auditar_aula(os.path.join(aulas_dir, f), f == primeira)
            usadas.update(r['imagens'])
            out['aulas'][f] = r
    img_dir = os.path.join(base, 'img')
    existentes = {f for f in os.listdir(img_dir) if os.path.isfile(os.path.join(img_dir, f))} \
        if os.path.isdir(img_dir) else set()
    out['img_faltando'] = sorted(usadas - existentes)
    out['img_orfas'] = sorted(existentes - usadas)
    chaves = ['sem_analogia', 'codigo_longo', 'tabela_larga', 'codigo_sem_comentario',
              'sobras_html', 'details_sem_branco']
    out['totais'] = {k: sum(len(a[k]) for a in out['aulas'].values()) for k in chaves}
    out['totais']['aulas'] = len(out['aulas'])
    out['totais']['imagens'] = sum(len(a['imagens']) for a in out['aulas'].values())
    out['totais']['aulas_sem_imagem'] = [f for f, a in out['aulas'].items()
                                         if not a['imagens'] and not f.startswith('00-')]
    if '--criterios' in sys.argv:
        erros, avisos = criterios(out)
        print(json.dumps({'curso': base, 'pronto': not erros, 'erros': erros, 'avisos': avisos},
                         ensure_ascii=False, indent=1))
        sys.exit(1 if erros else 0)
    if so_resumo:
        problemas = {f: {k: v for k, v in a.items() if v and k != 'imagens'}
                     for f, a in out['aulas'].items()}
        out['aulas'] = {f: p for f, p in problemas.items() if p}
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
