# Formatação de listas

> 🗺️ **Nesta aula:** mudar o tipo e a posição dos marcadores de listas, usar imagens e emojis como marcadores e zerar o estilo para fazer menus.

## De onde paramos

As aulas de fonte e alinhamento trataram do texto corrido. As listas têm um elemento a mais: o marcador. Ele pode virar número romano, ícone, emoji ou sumir de vez, como nos menus de navegação.

## Estilizando listas

Menus de navegação, índices, passos de receita e listas de recursos de um produto são listas por baixo. Por isso saber estilizá-las é útil: a lista de links de um menu é uma `<ul>` sem marcadores e sem recuo, disposta na horizontal. As regras desta aula servem tanto para o caso simples (trocar a bolinha por um quadrado) quanto para essa transformação completa.

As listas `<ul>` (não ordenada) e `<ol>` (ordenada) vêm com marcadores, recuo e margens padrão. O CSS permite mudar o tipo de marcador, a posição dele ou trocar por uma imagem.

## `list-style-type`: o tipo de marcador

A escolha do marcador comunica algo. Numeração (`decimal`, `lower-alpha`, `upper-roman`) diz que a ordem importa, como nos passos de uma instalação. Bolinhas e quadrados dizem que os itens são equivalentes. `none` remove o marcador e é o primeiro passo para transformar uma lista em menu. Lembre que o tipo é só visual: se a ordem importa, a tag certa continua sendo `<ol>`, mesmo que você esconda os números.

| Valor | Marcador | Normalmente em |
| --- | --- | --- |
| `disc` | ● círculo cheio (padrão do `ul`) | `ul` |
| `circle` | ○ círculo vazado | `ul` |
| `square` | ■ quadrado **cheio** | `ul` |
| `decimal` | 1, 2, 3 (padrão do `ol`) | `ol` |
| `decimal-leading-zero` | 01, 02, 03 | `ol` |
| `lower-alpha` / `upper-alpha` | a, b, c / A, B, C | `ol` |
| `lower-roman` / `upper-roman` | i, ii, iii / I, II, III | `ol` |
| `none` | sem marcador | menus de navegação |

## `list-style-position`: onde fica o marcador

![outside deixa o marcador fora da caixa do item; inside coloca dentro do texto.](../img/list-position.svg)

> 💡 **Analogia:** pense numa lista de compras escrita num caderno com margem vermelha. Com `outside`, os marcadores ficam na margem, e o texto de cada item começa sempre na mesma linha vertical. Com `inside`, o marcador entra no espaço do texto, como se fosse a primeira letra da frase.

Com `outside`, as linhas quebradas ficam alinhadas com o texto, o que é melhor para leitura. Use `inside` quando o item tiver fundo ou borda e você quiser o marcador dentro deles.

## `list-style-image` e o atalho

```css
ul { list-style-image: url("icone-check.svg"); }

/* atalho: tipo posição imagem */
ul { list-style: square inside; }

/* zerar tudo, muito usado em menus */
nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
```

## `::marker`: estilizando só o marcador

Antes do `::marker`, mudar a cor do marcador sem mudar a cor do texto exigia truques com imagens e pseudoelementos. Agora basta uma regra. O exemplo com `content: "✅ "` cria uma lista de tarefas sem uma única linha de HTML extra. A limitação é que só algumas propriedades funcionam no `::marker`: cor, fonte e `content`. Para algo mais elaborado, como um ícone com tamanho próprio, ainda se usa `list-style: none` junto com um `::before`.

```css
li::marker {
  color: #2563eb;
  font-weight: bold;
}

/* marcador com qualquer texto ou emoji */
.tarefas li::marker { content: "✅ "; }
```

`::marker` aceita poucas propriedades (cor, fonte, `content`), mas resolve a maior parte dos casos sem gambiarras.

## Projeto

No projeto, a lista usa `list-style: square inside` e um fundo azul claro nos itens. Perceba o efeito de `inside`: com o marcador dentro da caixa, o fundo azul o envolve, e o item parece uma etiqueta. Troque para `outside` e o marcador sai da área colorida. Essa diferença só aparece quando o item tem fundo ou borda, e é por isso que o projeto usa os dois.

**Código revisado**

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Formatação de listas</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h2>Lista não ordenada</h2>
  <ul class="quadrado">
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
  </ul>

  <h2>Lista ordenada com romanos</h2>
  <ol class="romanos">
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
  </ol>

  <h2>Marcador personalizado</h2>
  <ul class="tarefas">
    <li>Estudar CSS</li>
    <li>Fazer o projeto</li>
  </ul>
</body>
</html>
```

```css
/* style.css */
.quadrado { list-style: square inside; }
.quadrado li {
  background: #dbeafe;
  margin-bottom: 4px;
}

.romanos { list-style-type: upper-roman; }
.romanos li::marker {
  color: #7c3aed;
  font-weight: bold;
}

.tarefas { list-style: none; padding-left: 0; }
.tarefas li::before { content: "✅ "; }
```

> ⚠️ **Correções:** `square` é um quadrado **cheio**, não "vazado" (o vazado é o `circle`). O `lang="en"` do projeto virou `pt-BR`.

## 🧠 Revisão rápida

**Como tirar os marcadores e o recuo de uma lista de menu?**

`list-style: none; margin: 0; padding: 0;`

**Qual a diferença entre `outside` e `inside`?**

No `outside` o marcador fica fora da caixa do item; no `inside`, dentro, junto do texto.

**Como deixar só os números de uma lista ordenada em roxo?**

Com `li::marker { color: purple; }`.

> ➡️ **Próximo passo:** para fechar o módulo, um projeto que junta HTML e CSS num formulário estilizado: **Projeto exemplo de criação de formulários**.

## 📌 Resumo

| Propriedade | Em uma frase |
| --- | --- |
| `list-style-type` | tipo do marcador (disc, square, decimal, roman...) |
| `list-style-position` | marcador fora (outside) ou dentro (inside) |
| `list-style-image` | imagem como marcador |
| `list-style: none` | sem marcador, comum em menus |
| `::marker` | estiliza só o marcador |
