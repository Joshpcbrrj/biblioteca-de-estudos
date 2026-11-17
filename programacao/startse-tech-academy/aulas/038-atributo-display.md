# Atributo Display

> 🗺️ **Nesta aula:** os valores de `display` (block, inline, inline-block, none, flex, grid) e as três formas de esconder um elemento.

## De onde paramos

A aula de media queries mostrou como mudar estilos conforme a tela. Muitas dessas mudanças são justamente trocar o `display`: esconder o menu no celular, transformar uma lista em linha, ligar o Flexbox. Esta é a propriedade que decide como cada caixa entra no layout.

## O que é `display`?

Todo elemento da página é uma caixa, e antes de qualquer outra coisa o navegador precisa decidir como essa caixa se comporta: ela pega a linha toda e empurra o vizinho para baixo, ou fica ao lado dele como uma palavra numa frase? Quem responde é o `display`. Quando um layout "não obedece" você, em geral o problema é um `display` diferente do que você imaginava. É a propriedade que mais explica o comportamento das caixas.

**A propriedade** `display` **define como uma caixa participa do layout**: se ocupa a linha inteira, se fica no fluxo do texto, se some, ou se vira um contêiner flex ou grid para os filhos.

![Como cada valor afeta o elemento e os vizinhos.](../img/display-valores.svg)

> 💡 **Analogia:** pense numa estante. Um elemento `block` é uma prateleira inteira: o próximo item vai para a prateleira de baixo. Um `inline` é um livro em pé, ao lado dos outros, com a altura que o próprio livro tem. Um `inline-block` é uma caixa que você coloca ao lado dos livros, mas com o tamanho que escolher. E `none` é tirar o item da estante.

| Valor | Comportamento |
| --- | --- |
| `block` | nova linha, largura total, aceita `width`/`height` |
| `inline` | no fluxo do texto; **ignora** `width`/`height` e margens verticais |
| `inline-block` | no fluxo do texto, mas aceita `width`, `height` e margens |
| `none` | não aparece e não ocupa espaço |
| `flex` | vira um contêiner Flexbox (layout em uma dimensão) |
| `grid` | vira um contêiner Grid (layout em duas dimensões) |
| `inline-flex` / `inline-grid` | contêiner flex/grid que fica em linha |

Cada tag já nasce com um `display` padrão: `div`, `p`, `h1` e `ul` são `block`; `span`, `a`, `strong` e `img` são `inline`. O CSS pode trocar isso:

```css
/* inline: o tamanho do texto; block: a linha toda */
span   { display: inline; }
div    { display: block; }
button { display: inline-block;
         width: 100px; height: 40px; }
.hidden-element { display: none; }
```

## Esconder elementos: `display` × `visibility` × `opacity`

Os três escondem, mas por caminhos diferentes, e a escolha muda o resultado. Num menu que abre e fecha, `display: none` faz o menu sumir e libera o espaço, e o leitor de tela o ignora: é o certo. Já `visibility: hidden` mantém o buraco do tamanho do elemento, útil quando você não quer que o layout se mexa. E `opacity: 0` deixa o elemento invisível mas ainda clicável, o que costuma ser um bug, a não ser que você esteja fazendo uma animação de aparecer. Uma regra prática: se o conteúdo não deve existir para ninguém naquele momento, `display: none`.

| Propriedade | Ocupa espaço? | Clicável? | Leitor de tela lê? |
| --- | --- | --- | --- |
| `display: none` | não | não | não |
| `visibility: hidden` | sim | não | não |
| `opacity: 0` | sim | sim | sim |

Nos três casos o elemento não aparece; a diferença está no espaço, no clique e na acessibilidade.

```css
/* some de vez */
.a { display: none; }
/* fica um "buraco" do tamanho dele */
.b { visibility: hidden; }
/* valor padrão */
.c { visibility: visible; }
```

> 💡 Para esconder algo **só visualmente**, mantendo para leitores de tela (ex.: um texto "Pular para o conteúdo"), use uma classe utilitária de leitura de tela: `.sr-only` no Tailwind e `.visually-hidden` no Bootstrap 5, em vez de `display: none`.

## Projeto de exemplo

O projeto coloca parágrafos com borda e fundo colorido para você enxergar a caixa de cada um. Repare como cada `p` ocupa a largura inteira, mesmo com pouco texto: é o `display: block` padrão. Depois mude os parágrafos para `inline-block` ou `inline` e observe: as caixas encolhem ao tamanho do conteúdo e passam a dividir a linha. Uma experiência de dois minutos vale mais que decorar a tabela.

**Código revisado**

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Exemplos de uso de display</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <p class="ex1">Parágrafo 1</p>
  <p class="ex2">Parágrafo 2</p>
  <p class="ex3">Parágrafo 3</p>
  <p class="ex4">Parágrafo 4</p>
  <p class="ex5">Parágrafo 5</p>
  <p class="ex6">Teste</p>
</body>
</html>
```

```css
/* style.css */
p {
  border: 1px solid red;
  background-color: pink;
  margin: 10px;
}

/* some e não ocupa espaço */
p.ex1 { display: none; }

/* some, mas o espaço continua reservado */
p.ex2 { visibility: hidden; }

/* em linha: outros elementos ficam ao lado */
p.ex3 { display: inline; }

/* bloco (já é o padrão do <p>) */
p.ex4 { display: block; }

/* em linha, mas aceita largura e altura */
p.ex5, p.ex6 {
  display: inline-block;
  width: 200px;
  height: 200px;
  border: 2px solid black;
}
```

> ⚠️ **Bugs corrigidos:** `maring: 10px` virou `margin` (com o erro de digitação, a propriedade era ignorada). O comentário aninhado `/*/* ... */*/` sobre o `.ex2` não é suportado pelo CSS: fechava no primeiro `*/` e o resto estragava o seletor, descartando a regra `visibility: hidden`. As regras idênticas de `.ex5` e `.ex6` foram agrupadas, e a meta `X-UA-Compatible` (para o Internet Explorer, descontinuado) foi removida. Nas anotações, os exemplos de CSS também estavam marcados como HTML.

## 🧠 Revisão rápida

**Por que `width: 200px` não funciona num `span`?**

Porque o `span` é `inline`, e elementos inline ignoram largura e altura. Use `inline-block` ou `block`.

**Qual a diferença entre `display: none` e `visibility: hidden`?**

O primeiro some e libera o espaço; o segundo some, mas o espaço continua reservado.

**Qual o `display` padrão de uma `div`?**

`block`.

> ➡️ **Próximo passo:** além de decidir o tipo de caixa, dá para tirá-la do fluxo e colocá-la em um ponto exato: **Posicionamento de elementos**.

## 📌 Resumo

| Valor | Em uma frase |
| --- | --- |
| `block` | ocupa a linha inteira |
| `inline` | flui no texto, ignora largura e altura |
| `inline-block` | em linha, mas aceita tamanho |
| `none` | some sem ocupar espaço |
| `flex` / `grid` | transforma em contêiner de layout |
| `visibility: hidden` | some, mas o espaço fica |
