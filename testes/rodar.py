#!/usr/bin/env python3
"""Testes automáticos do kit (skill + scripts). Rode antes de commitar mudanças na
skill ou em ferramentas/; a Action "Testes do kit" roda o mesmo a cada push.

Uso:  python3 testes/rodar.py

Cada teste imprime OK ou FALHOU com o motivo; sai com código 1 se algum falhar.
"""
import glob, json, os, re, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, 'skill', 'revisar-curso-biblioteca')
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


@teste('SKILL.md: cabeçalho válido')
def _():
    s = open(os.path.join(SKILL, 'SKILL.md'), encoding='utf-8').read()
    m = re.match(r'---\nname: ([a-z0-9-]+)\ndescription: (.+?)\n---\n', s, re.S)
    assert m, 'frontmatter com name e description ausente'
    assert m.group(1) == 'revisar-curso-biblioteca', 'name diferente da pasta'
    assert len(m.group(2)) <= 1024, 'description acima de 1024 caracteres'
    return f'{len(s.splitlines())} linhas'


@teste('todo caminho citado na skill existe')
def _():
    quebrados = []
    for arq in glob.glob(os.path.join(SKILL, '**', '*.md'), recursive=True):
        texto = open(arq, encoding='utf-8').read()
        for ref in set(re.findall(r'`?(referencias/[A-Z_]+\.md)', texto)):
            if not os.path.exists(os.path.join(SKILL, ref)):
                quebrados.append(f'{os.path.basename(arq)} → {ref}')
        for ref in set(re.findall(r'(ferramentas/[\w/.-]+\.(?:py|js|md))', texto)):
            if not os.path.exists(os.path.join(RAIZ, ref)):
                quebrados.append(f'{os.path.basename(arq)} → {ref}')
    assert not quebrados, quebrados


@teste('nomes de etapa consistentes (sem "Fase N" antigo)')
def _():
    achados = []
    for arq in glob.glob(os.path.join(SKILL, '**', '*.md'), recursive=True):
        for i, l in enumerate(open(arq, encoding='utf-8'), 1):
            if re.search(r'\bFases? \d', l):
                achados.append(f'{os.path.basename(arq)}:{i}')
    assert not achados, achados


@teste('briefing do coordenador traz o contrato de resposta')
def _():
    t = open(os.path.join(SKILL, 'referencias', 'COORDENADOR.md'), encoding='utf-8').read()
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
                  'release_epubs', 'release_skill']:
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
