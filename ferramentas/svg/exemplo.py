# Exemplo mínimo: gera out/exemplo.svg no visual padrão da biblioteca.
#   mkdir -p out && SVG_OUT=out python3 exemplo.py && node prev.js exemplo.svg
from extras import *
d = D(0, 'Laço para: soma de 1 a 3')
y = vstack(d, 56, [('soma <- 0', 'antes do laço', 'xB'),
                   ('para i de 1 ate 3', 'i = 1, 2, 3', 'xP'),
                   ('soma <- soma + i', 'soma = 1, 3, 6', 'xO'),
                   ('escreva(soma)', 'mostra 6', 'xG')], num=True)
codigo(d, 20, y + 10, 440, ['para (i = 1; i <= 3; i++) {',
                            '  soma = soma + i', '}'], k='xB')
d.save('exemplo.svg')
