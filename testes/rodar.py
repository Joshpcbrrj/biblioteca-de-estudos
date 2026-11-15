#!/usr/bin/env python3
"""Testes automáticos do kit (skills + scripts). Rode antes de commitar mudanças na
skill ou em ferramentas/; a Action "Testes do kit" roda o mesmo a cada push.

Uso:  python3 testes/rodar.py

Cada teste imprime OK ou FALHOU com o motivo; sai com código 1 se algum falhar.
"""
import glob, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RAIZ, 'skill')
NOMES = ['revisar-curso-biblioteca', 'criar-livro-tecnologia']
falhas = []


def rodar(*cmd):
    return subprocess.run([sys.executable, *cmd], cwd=RAIZ, capture_output=True, text=True)


def teste(nome):
    def deco(f):
        try:
            msg = f()
            print(f'OK      {nome}' + (f' ({msg})' if msg else ''))
        except (AssertionError, SyntaxError, ValueError) as e:
            falhas.append(nome)
            print(f'FALHOU  {nome}: {e}')
        return f
    return deco


@teste('curso de exemplo passa no critério de pronto')
def _():
    r = rodar('-I', 'ferramentas/auditar_curso.py', 'testes/curso-exemplo', '--criterios')
    d = json.loads(r.stdout)
    assert r.returncode == 0 and d['pronto'], d['erros']
    assert not d['avisos'], f"avisos inesperados: {d['avisos']}"


@teste('curso quebrado é recusado, com cada defeito apontado')
def _():
    r = rodar('-I', 'ferramentas/auditar_curso.py', 'testes/curso-quebrado', '--criterios')
    d = json.loads(r.stdout)
    assert r.returncode == 1 and not d['pronto'], 'deveria falhar'
    texto = '\n'.join(d['erros'])
    esperados = ['itens extras', 'título fora do formato', 'não existem', 'codigo_longo',
                 'codigo_sem_comentario', 'sobras_html', 'details_sem_branco',
                 "'revisao'", "'proximo'"]
    faltam = [e for e in esperados if e not in texto]
    assert not faltam, f'defeitos não detectados: {faltam}'
    avisos = '\n'.join(d['avisos'])
    assert 'tabela_larga' in avisos and 'sem_analogia' in avisos, 'avisos não detectados'


@teste('README em dia com a skill')
def _():
    r = rodar('ferramentas/montar_kit.py', '--checar')
    assert r.returncode == 0, r.stdout.strip()


@teste('cabeçalho válido nas duas skills')
def _():
    tamanhos = []
    for nome in NOMES:
        s = open(os.path.join(SKILLS, nome, 'SKILL.md'), encoding='utf-8').read()
        m = re.match(r'---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n', s, re.S)
        assert m, f'{nome}: frontmatter com name e description ausente'
        assert m.group(1) == nome, f'{nome}: name diferente da pasta'
        assert len(m.group(2)) <= 1024, f'{nome}: description acima de 1024 caracteres'
        tamanhos.append(f'{nome}: {len(s.splitlines())} linhas')
    return '; '.join(tamanhos)


@teste('todo caminho citado nas skills existe')
def _():
    quebrados = []
    for arq in glob.glob(os.path.join(SKILLS, '**', '*.md'), recursive=True):
        texto = open(arq, encoding='utf-8').read()
        pasta = os.path.dirname(arq)
        dono = os.path.join(SKILLS, os.path.relpath(pasta, SKILLS).split(os.sep)[0])
        for ref in set(re.findall(r'(?<![\w/])(referencias/[A-Z_]+\.md)', texto)):
            if not os.path.exists(os.path.join(dono, ref)):
                quebrados.append(f'{os.path.relpath(arq, SKILLS)} → {ref}')
        for ref in set(re.findall(r'(?<![\w/])(_comum/[A-Z_]+\.md)', texto)):
            if not os.path.exists(os.path.join(SKILLS, ref)):
                quebrados.append(f'{os.path.relpath(arq, SKILLS)} → {ref}')
        for ref in set(re.findall(r'(ferramentas/[\w/.-]+\.(?:py|js|md))', texto)):
            if not os.path.exists(os.path.join(RAIZ, ref)):
                quebrados.append(f'{os.path.relpath(arq, SKILLS)} → {ref}')
    assert not quebrados, quebrados


@teste('nomes de etapa consistentes (sem "Fase N" antigo)')
def _():
    achados = []
    for arq in glob.glob(os.path.join(SKILLS, '**', '*.md'), recursive=True):
        for i, l in enumerate(open(arq, encoding='utf-8'), 1):
            if re.search(r'\bFases? \d', l):
                achados.append(f'{os.path.basename(arq)}:{i}')
    assert not achados, achados


@teste('mapa das trilhas: só ementa aprovada entra, sobreposição detectada')
def _():
    env = dict(os.environ, LIVROS_DIR=os.path.join(RAIZ, 'testes', 'livros-exemplo'))
    r = subprocess.run([sys.executable, 'ferramentas/mapa_livros.py'], cwd=RAIZ,
                       capture_output=True, text=True, env=env)
    m = json.loads(r.stdout)
    assert [b['slug'] for b in m['trilhas']['docker']] == ['docker-do-zero'], m
    r = subprocess.run([sys.executable, 'ferramentas/mapa_livros.py', '--checar',
                        'testes/livros-exemplo/docker-compose/ementa.yaml'],
                       cwd=RAIZ, capture_output=True, text=True, env=env)
    c = json.loads(r.stdout)
    assert 'volumes' in c['topicos_repetidos'], c
    assert c['pre_requisitos_inexistentes'] == ['livro-que-nao-existe'], c
    assert 'kubernetes' in c['temas_pendentes_da_trilha'], c


@teste('ementa: modelo da skill tem todos os campos que o mapa exige')
def _():
    t = open(os.path.join(SKILLS, 'criar-livro-tecnologia', 'referencias', 'EMENTA.md'),
             encoding='utf-8').read()
    for campo in ['titulo:', 'slug:', 'trilha:', 'nivel:', 'objetivo:', 'capitulos:',
                  'cobre:', 'aprovada_em:', 'fica_para_depois:', 'pre_requisitos:']:
        assert campo in t, f'falta {campo} no modelo'


@teste('briefing do coordenador traz o contrato de resposta')
def _():
    t = open(os.path.join(SKILLS, '_comum', 'COORDENADOR.md'), encoding='utf-8').read()
    for chave in ['"id"', '"ok"', '"imagens"', '"analogias"', '"correcoes"', '"pendencias"']:
        assert chave in t, f'falta {chave} no JSON de resposta'


@teste('scripts compilam')
def _():
    arqs = glob.glob(os.path.join(RAIZ, 'ferramentas', '**', '*.py'), recursive=True)
    for a in arqs:
        # compila o texto em memória, sem gravar .pyc
        compile(open(a, encoding='utf-8').read(), a, 'exec')
    return f'{len(arqs)} arquivos'


@teste('biblioteca.yaml tem as chaves que os scripts usam')
def _():
    r = rodar('ferramentas/config.py')
    for chave in ['autor', 'repositorio', 'branch', 'commit_nome', 'commit_email',
                  'release_epubs', 'release_skill', 'notion_livros']:
        assert chave in r.stdout, f'falta {chave}'


@teste('progresso.py: cadastrar, marcar e retomar')
def _():
    slug = 'teste-automatico'
    caminho = os.path.join(RAIZ, 'progresso', f'{slug}.json')
    try:
        rodar('ferramentas/progresso.py', slug, 'init', 'aaaa1111', 'bbbb2222')
        rodar('ferramentas/progresso.py', slug, 'feito', 'aaaa')
        st = json.loads(rodar('ferramentas/progresso.py', slug, 'status').stdout)
        assert st['total'] == 2 and st['feitas'] == 1, st
        assert st['proxima']['id'].startswith('bbbb'), st
    finally:
        if os.path.exists(caminho):
            os.remove(caminho)


if __name__ == '__main__':
    print(f'\n{len(falhas)} falha(s).' if falhas else '\nTudo certo.')
    sys.exit(1 if falhas else 0)
