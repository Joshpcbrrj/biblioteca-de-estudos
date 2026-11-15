#!/usr/bin/env python3
"""Mantém o kit da skill: README sempre igual aos arquivos e zip para instalar.

Uso:
  python3 ferramentas/montar_kit.py            # reescreve a seção da skill no README.md
  python3 ferramentas/montar_kit.py --checar   # sai com erro se o README estiver desatualizado
  python3 ferramentas/montar_kit.py --zip saida.zip   # empacota a skill para upload no Claude

A seção do README fica entre <!-- kit:inicio --> e <!-- kit:fim -->: não edite
à mão, edite os arquivos em skill/revisar-curso-biblioteca/ e rode este script.
"""
import os, sys, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(RAIZ, 'skill', 'revisar-curso-biblioteca')
README = os.path.join(RAIZ, 'README.md')
INI, FIM = '<!-- kit:inicio -->', '<!-- kit:fim -->'

# (arquivo relativo à pasta da skill, rótulo do bloco recolhido)
ARQUIVOS = [
    ('SKILL.md', 'Skill completa (SKILL.md)'),
    ('referencias/EXEMPLOS.md', 'Apoio: aula e cheat sheet modelo (antes e depois)'),
    ('referencias/COORDENADOR.md', 'Apoio: modo coordenador (um agente por página)'),
    ('referencias/DIDATICA_VISUAL.md', 'Apoio: imagens, didática visual e design system'),
    ('referencias/NOTION.md', 'Apoio: notas técnicas do Notion'),
    ('referencias/PDFS.md', 'Apoio: PDFs do curso com o Docling (opcional)'),
    ('referencias/PUBLICACAO.md', 'Apoio: exportação, conversão e publicação'),
    ('referencias/CAPA.md', 'Apoio: capa do livro'),
]


def ler(rel):
    return open(os.path.join(SKILL, rel), encoding='utf-8').read().rstrip('\n')


def bloco(rel, rotulo):
    texto = ler(rel)
    cerca = '~~~~'
    while cerca in texto:
        cerca += '~'
    return (f'<details>\n<summary><b>{rotulo}</b> · <code>{rel}</code></summary>\n\n'
            f'{cerca}markdown\n{texto}\n{cerca}\n\n</details>')


def secao():
    corpo = '\n\n'.join(bloco(r, t) for r, t in ARQUIVOS)
    return f'''{INI}
## 🤖 Kit de reformulação (skill + arquivos de apoio)

Todos os cursos daqui foram reformulados com a skill abaixo. Qualquer pessoa pode refazer o processo do zero num chat novo do Claude: veja o passo a passo em **[COMO-USAR.md](COMO-USAR.md)**.

- **Instalar (recomendado):** baixe o [`revisar-curso-biblioteca.zip`](../../releases/download/skill/revisar-curso-biblioteca.zip) e envie na tela de Skills do Claude.
- **Sem instalar:** abra o primeiro bloco, copie e cole na primeira mensagem do chat.
- Os scripts que a skill usa ficam em [`ferramentas/`](ferramentas/); a configuração da biblioteca, em [`biblioteca.yaml`](biblioteca.yaml); o andamento de cada curso, em [`ESTADO.md`](ESTADO.md).

> Esta seção é gerada por `ferramentas/montar_kit.py` a partir de [`skill/revisar-curso-biblioteca/`](skill/revisar-curso-biblioteca/). Edite os arquivos de lá, não este README.

{corpo}
{FIM}'''


def readme_novo():
    r = open(README, encoding='utf-8').read()
    if INI in r and FIM in r:
        a, resto = r.split(INI, 1)
        _, b = resto.split(FIM, 1)
        return a + secao() + b
    marca = '\n> Estes são resumos pessoais'
    i = r.find(marca)
    return (r[:i] + '\n' + secao() + '\n' + r[i:]) if i >= 0 else r.rstrip('\n') + '\n\n' + secao() + '\n'


def zipar(saida):
    with zipfile.ZipFile(saida, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, nomes in os.walk(SKILL):
            for n in sorted(nomes):
                caminho = os.path.join(base, n)
                z.write(caminho, os.path.join('revisar-curso-biblioteca', os.path.relpath(caminho, SKILL)))
    print(f'zip: {saida}')


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--zip' in args:
        zipar(args[args.index('--zip') + 1])
    elif '--checar' in args:
        if open(README, encoding='utf-8').read() != readme_novo():
            print('README desatualizado: rode python3 ferramentas/montar_kit.py e faça commit.')
            sys.exit(1)
        print('README em dia com a skill.')
    else:
        novo = readme_novo()
        open(README, 'w', encoding='utf-8').write(novo)
        print('README atualizado.')
