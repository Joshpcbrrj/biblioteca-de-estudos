#!/usr/bin/env python3
"""Move o cheat sheet de cada seção para o início da primeira aula da seção.

Uso: python3 -I ferramentas/mover_cheatsheet.py <area>/<slug> [--dry]

Lê as seções do README do curso (`## Seção` + links numerados), procura o
bloco `## 🧭 Cheat sheet da seção` (título + imagem) em qualquer aula da
seção e o recoloca logo depois do callout "Nesta aula" da primeira aula.
Se o bloco já está na primeira aula, não faz nada. Pode rodar de novo.
"""
import re
import sys
from pathlib import Path

TITULO = "## 🧭 Cheat sheet da seção"
INTRO = ("Antes de começar, veja o mapa da seção: é o que as próximas "
         "aulas vão explicar. Volte a ele no fim para revisar.")


def secoes(readme):
    """Devolve [(titulo, [arquivos])] na ordem do README."""
    out, atual = [], None
    for linha in readme.read_text(encoding="utf-8").split("\n"):
        if linha.startswith("## "):
            atual = (linha[3:].strip(), [])
            out.append(atual)
            continue
        m = re.match(r"(?:\d+\.|-) \[.+\]\(aulas/(.+\.md)\)$", linha)
        if m and atual:
            atual[1].append(m.group(1))
    return [s for s in out if s[1]]


def extrair(texto):
    """Separa o bloco do cheat sheet. Devolve (texto_sem_bloco, bloco)."""
    linhas = texto.split("\n")
    for i, l in enumerate(linhas):
        if l.strip() == TITULO:
            j = i + 1
            while j < len(linhas) and not linhas[j].startswith("## "):
                j += 1
            bloco = [x for x in linhas[i + 1:j]]
            imagens = [x for x in bloco if x.startswith("![")]
            resto = linhas[:i] + linhas[j:]
            while resto and resto[-1] == "":
                resto.pop()
            return "\n".join(resto) + "\n", imagens
    return texto, None


def inserir(texto, imagens):
    linhas = texto.split("\n")
    pos = None
    for i, l in enumerate(linhas):
        if l.startswith("> 🗺️"):
            pos = i
            while pos < len(linhas) and linhas[pos].startswith(">"):
                pos += 1
            break
    if pos is None:  # sem callout: logo depois do H1
        pos = 1
    bloco = ["", TITULO, "", INTRO, ""] + [x for im in imagens
                                          for x in (im, "")]
    bloco.pop()  # sem linha em branco sobrando no fim
    novo = linhas[:pos] + bloco + linhas[pos:]
    return "\n".join(novo)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    curso = Path(sys.argv[1])
    dry = "--dry" in sys.argv
    aulas = curso / "aulas"
    for titulo, arquivos in secoes(curso / "README.md"):
        primeira = aulas / arquivos[0]
        achado = None
        for nome in arquivos:
            _, imgs = extrair((aulas / nome).read_text(encoding="utf-8"))
            if imgs is not None:
                achado = nome
                break
        if achado is None:
            print(f"sem cheat sheet: {titulo}")
            continue
        if achado == arquivos[0]:
            print(f"ok (já no início): {titulo}")
            continue
        sem, imgs = extrair((aulas / achado).read_text(encoding="utf-8"))
        novo = inserir(primeira.read_text(encoding="utf-8").rstrip("\n"),
                       imgs) + "\n"
        print(f"movido: {titulo}: {achado} -> {arquivos[0]}")
        if not dry:
            (aulas / achado).write_text(sem, encoding="utf-8")
            primeira.write_text(novo, encoding="utf-8")


if __name__ == "__main__":
    main()
