# Kit de diagramas SVG da biblioteca

Gera os diagramas dos cursos no visual padrão: 480 px de largura (legível em
e-reader), caixas com degradê suave e sombra, título com sublinhado colorido,
etapas numeradas em círculos coloridos e tabelas com cabeçalho em destaque.

| Arquivo | Para quê |
| --- | --- |
| `lib.py` | paleta, estilos, classe `D` (texto, caixas, setas, ajuste de altura) |
| `kit.py` | `tabela`, `vstack`, `dia` (losango), `codigo`, `lado`, `nota` |
| `extras.py` | diagrama de sequência (`seq`), `uml`, `pilha`, `tab` (tabela de banco) |
| `prev.js` | renderiza os SVGs a 380 px numa folha `prev.png` para conferir |
| `restyle.py` | converte SVGs do visual antigo (mesmas classes) para o novo |
| `exemplo.py` | ponto de partida |

```bash
mkdir -p out
SVG_OUT=out python3 exemplo.py
node prev.js exemplo.svg   # depois abra prev.png
```

Classes de cor (`k`): `xB` azul, `xG` verde, `xO` laranja, `xP` roxo,
`xR` vermelho, `xT` verde-água, `xK` rosa, `xY` cinza, `xW` branco.
`hB`, `hG`... são as versões sólidas (use com texto `w`, branco).
