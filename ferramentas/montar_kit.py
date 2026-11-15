#!/usr/bin/env python3
"""Mantém o kit das skills: README sempre igual aos arquivos e zip para instalar.

Uso:
  python3 ferramentas/montar_kit.py            # reescreve a seção da skill no README.md
  python3 ferramentas/montar_kit.py --checar   # sai com erro se o README estiver desatualizado
  python3 ferramentas/montar_kit.py --zip <pasta>     # um zip por skill (com _comum/) para upload no Claude

A seção do README fica entre <!-- kit:inicio --> e <!-- kit:fim -->: não edite
à mão, edite os arquivos em skill/ e rode este script.
"""
import os, sys, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RAIZ, 'skill')
COMUM = os.path.join(SKILLS, '_comum')
README = os.path.join(RAIZ, 'README.md')
INI, FIM = '<!-- kit:inicio -->', '<!-- kit:fim -->'

# skill -> (título, [(arquivo relativo à pasta da skill, rótulo)])
KIT = {
    'revisar-curso-biblioteca': ('Reformular um curso anotado no Notion', [
        ('SKILL.md', 'Skill completa: revisar-curso-biblioteca'),
    ]),
    'criar-livro-tecnologia': ('Criar um livro de tecnologia do zero', [
        ('SKILL.md', 'Skill completa: criar-livro-tecnologia'),
        ('referencias/EMENTA.md', 'Apoio: ementa (propor, ajustar, aprovar)'),
        ('referencias/PESQUISA.md', 'Apoio: pesquisa, fontes e verificação'),
    ]),
}
# arquivos comuns às duas skills (em skill/_comum/)
COMUNS = [
    ('PADRAO_AULA.md', 'Padrão de aula, imagens e armadilhas'),
    ('EXEMPLOS.md', 'Aula e cheat sheet modelo (antes e depois)'),
    ('COORDENADOR.md', 'Modo coordenador (um agente por página)'),
    ('DIDATICA_VISUAL.md', 'Imagens, didática visual e design system'),
    ('NOTION.md', 'Notas técnicas do Notion'),
    ('PDFS.md', 'PDFs do curso com o Docling (opcional)'),
    ('PUBLICACAO.md', 'Exportação, conversão e publicação'),
    ('CAPA.md', 'Capa do livro'),
]


def bloco(caminho, rotulo, mostrar):
    texto = open(caminho, encoding='utf-8').read().rstrip('\n')
    cerca = '~~~~'
    while cerca in texto:
        cerca += '~'
    return (f'<details>\n<summary><b>{rotulo}</b> · <code>{mostrar}</code></summary>\n\n'
            f'{cerca}markdown\n{texto}\n{cerca}\n\n</details>')


def secao():
    partes = []
    for nome, (titulo, arqs) in KIT.items():
        blocos = '\n\n'.join(bloco(os.path.join(SKILLS, nome, r), t, f'{nome}/{r}') for r, t in arqs)
        partes.append(f'### {titulo}\n\nZip para instalar: [`{nome}.zip`](../../releases/download/skill/{nome}.zip)\n\n{blocos}')
    comuns = '\n\n'.join(bloco(os.path.join(COMUM, r), t, f'_comum/{r}') for r, t in COMUNS)
    partes.append(f'### Arquivos comuns às duas skills\n\nPadrão de aula, design, Notion e publicação: as duas skills leem daqui, e os dois zips já os incluem.\n\n{comuns}')
    corpo = '\n\n'.join(partes)
    return f'''{INI}
## 🤖 Kit de reformulação e criação (skills + arquivos de apoio)

Todos os livros daqui foram feitos com as skills abaixo. Qualquer pessoa pode refazer o processo do zero num chat novo do Claude: veja o passo a passo em **[COMO-USAR.md](COMO-USAR.md)**.

- **`revisar-curso-biblioteca`:** transforma as anotações de um curso no Notion num livro revisado.
- **`criar-livro-tecnologia`:** cria um livro do zero sobre um tema, com ementa aprovada por você, e livros complementares na mesma trilha.
- **Instalar:** baixe o zip da skill (links abaixo, na release **skill**) e envie na tela de Skills do Claude. Sem instalar: copie o bloco "Skill completa" e cole na primeira mensagem.
- Scripts em [`ferramentas/`](ferramentas/), configuração em [`biblioteca.yaml`](biblioteca.yaml), andamento em [`ESTADO.md`](ESTADO.md), mapa das trilhas em [`livros/`](livros/).

> Esta seção é gerada por `ferramentas/montar_kit.py` a partir de [`skill/`](skill/). Edite os arquivos de lá, não este README.

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


def zipar(pasta_saida):
    os.makedirs(pasta_saida, exist_ok=True)
    for nome in KIT:
        saida = os.path.join(pasta_saida, f'{nome}.zip')
        with zipfile.ZipFile(saida, 'w', zipfile.ZIP_DEFLATED) as z:
            for origem, destino in [(os.path.join(SKILLS, nome), nome), (COMUM, f'{nome}/_comum')]:
                for base, _, nomes in os.walk(origem):
                    for n in sorted(nomes):
                        c = os.path.join(base, n)
                        z.write(c, os.path.join(destino, os.path.relpath(c, origem)))
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
