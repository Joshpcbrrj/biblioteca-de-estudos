#!/usr/bin/env python3
"""Lê o biblioteca.yaml da raiz (chave: "valor" por linha, sem dependências).

Uso em script:  from config import CFG   (ou python3 ferramentas/config.py [chave])
"""
import os, re, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ler(caminho=os.path.join(RAIZ, 'biblioteca.yaml')):
    cfg = {}
    for linha in open(caminho, encoding='utf-8'):
        m = re.match(r'\s*([a-z_]+)\s*:\s*"([^"]*)"', linha)
        if m:
            cfg[m.group(1)] = m.group(2)
    return cfg


CFG = ler()

if __name__ == '__main__':
    print(CFG[sys.argv[1]] if len(sys.argv) > 1 else CFG)
