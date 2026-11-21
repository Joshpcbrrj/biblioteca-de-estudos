# Design: diagramas de música no diagram.py (acorde, braço, tablatura)

Aprovado pelo usuário em 2026-11-20, depois do piloto de violão (o VISUALS.md promete diagramas de acorde, mas o `diagram.py` não tinha o tipo; o capítulo saiu só com cifra em texto).

## Intenção

Quem aprende violão (ou guitarra, baixo, ukulele, cavaquinho) lê acordes, escalas e trechos em três desenhos que todo material da área usa: o **diagrama de acorde**, o **braço com as notas** e a **tablatura**. O livro precisa desses desenhos com a mesma qualidade dos outros diagramas, e sempre com a versão em texto ao lado (o que o leitor reproduz é texto: `references/areas/skills.md`).

## Tipos novos

**`chord`**: um ou mais acordes lado a lado (até 6; 3 por linha no `small`).

```yaml
type: chord
title: Os dois primeiros acordes
chords:
  - {name: Em, frets: "022000", fingers: "023000"}
  - {name: Am, frets: "x02210", fingers: "x03210"}
  - {name: F, frets: "133211", fingers: "134211", barre: {fret: 1, from: 6, to: 1}}
```

- `frets`: uma posição por corda, da mais grave para a mais aguda; `x` = não tocar, `0` = solta, número = casa. Casas acima de 9 em lista: `[x, 10, 12, 12, 11, 10]`.
- `fingers` (opcional): o dedo em cada corda (1 a 4; `0`/`x` sem dedo).
- `barre` (opcional): a pestana, de uma corda a outra.
- `tuning` (opcional, todo o diagrama): padrão `[E, A, D, G, B, E]`; o número de cordas vem dela (4 para baixo e ukulele).
- Desenho: cordas na vertical, casas na horizontal, pestana (nut) grossa no alto quando o desenho começa na casa 1; senão, o número da primeira casa ao lado. `x` e `o` acima das cordas, dedos dentro das bolinhas, nomes das cordas embaixo.

**`fretboard`**: o braço com notas marcadas (escalas, intervalos, onde fica cada nota).

```yaml
type: fretboard
title: Pentatônica de Lá menor na 5ª casa
frets: [5, 8]
notes:
  - {string: 6, fret: 5, label: A, root: true}
  - {string: 6, fret: 8, label: C}
```

- Horizontal, como na tablatura: a corda mais aguda em cima; números das casas embaixo; marcações de casa (3, 5, 7, 9, 12) quando estiverem no trecho.
- `root: true` destaca a tônica com a cor de foco; as outras notas em azul. `label` é o texto da bolinha (nota, grau ou dedo).

**`tab`**: tablatura desenhada.

```yaml
type: tab
title: Arpejo de Em
steps: ["6:0", "4:2", "3:0", "2:0", "|", "6:0 3:0"]
```

- Cada passo é um tempo: `corda:casa`, vários juntos separados por espaço (tocados juntos); `|` é a barra de compasso.

## Texto ao lado, sempre

O JSON que o `diagram.py` imprime ganha `text`: a mesma informação em texto copiável (`Em = 022000 (dedos 023000)`; a tablatura em ASCII). A skill põe esse texto no capítulo, logo abaixo da imagem.

## Checagens

- `frets`/`fingers` com uma posição por corda; só `x`, `0`–`9` (ou números na lista); dedos de 1 a 4; pestana dentro das cordas e com casa > 0.
- Até 6 acordes por diagrama; no braço, nota fora do trecho de casas ou de corda inexistente; na tablatura, passo mal escrito.
- Tudo vira `problem` (saída 1), como o texto que não cabe.

## Fora do escopo

Partitura (pentagrama), diagramas de circuito e de pinos: ficam para quando um piloto pedir.
