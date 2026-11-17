# Posicionamento de elementos

> 🗺️ **Nesta aula:** os cinco valores de `position` (static, relative, absolute, fixed e sticky), como `top`/`left` funcionam em cada um e quando usar cada valor.

## De onde paramos

O `display` decide o tipo de caixa, mas a caixa continua no fluxo normal, uma depois da outra. Às vezes é preciso um selo no canto de um card, um menu que não sai do topo ou um cabeçalho que gruda ao rolar. Isso é trabalho do `position`.

## A propriedade `position`

Controla **como** um elemento é posicionado e **em relação a quê** as propriedades `top`, `right`, `bottom` e `left` funcionam.

![static, relative, absolute, fixed e sticky.](../img/position-tipos.svg)

> 💡 **Analogia:** imagine pessoas numa fila. `static` é ficar no seu lugar; `relative` é dar um passo para o lado sem perder o lugar na fila; `absolute` é sair da fila e ficar num ponto exato da sala onde está o "responsável" (o pai posicionado); `fixed` é um aviso colado no vidro da janela, que não se move quando a sala gira; `sticky` é andar com a fila até encostar na parede e parar ali.

### 1. `static` (padrão)

Fluxo normal do documento. **Ignora** `top`, `left`, `right`, `bottom` e `z-index`. Útil para desfazer um posicionamento aplicado antes.

### 2. `relative`

Desloca o elemento **a partir da posição onde ele estaria**. O espaço original **continua reservado**: os vizinhos não se mexem.

```css
/* relative: move em relação ao lugar original */
.elemento {
  position: relative;
  top: 20px;  /* desce 20px */
  left: 10px;  /* vai 10px para a direita */
}
```

Também é muito usado **sem** deslocamento, apenas para servir de referência a filhos com `absolute`.

### 3. `absolute`

**Sai do fluxo**: os vizinhos agem como se ele não existisse. É posicionado em relação ao **ancestral posicionado mais próximo** (qualquer `position` diferente de `static`). Se não houver nenhum, usa a página inteira.

```css
/* referência */
.card { position: relative; }
/* canto superior direito do card */
.selo {
  position: absolute;
  top: 8px;
  right: 8px;
}
```

### 4. `fixed`

Sai do fluxo e fica **preso à janela** do navegador: não se move ao rolar a página. É usado em menus fixos, botões flutuantes e banners de cookies.

```css
/* fixed: fica parado ao rolar a página */
.menu {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}
```

> 💡 Como o elemento fixo sai do fluxo, o conteúdo fica **por baixo** dele. Compense com um `padding-top` no `body` igual à altura do menu.

### 5. `sticky`

Comporta-se como `relative` até a rolagem atingir o limite definido; a partir daí, **gruda** como se fosse `fixed`, mas só enquanto o elemento pai estiver visível. É ideal para cabeçalhos de tabela e menus que grudam no topo.

```css
.cabecalho {
  position: sticky;
  /* obrigatório: sem limite, sticky não faz nada */
  top: 0;
}
```

> ⚠️ **Correções:** o nome do valor é `sticky` (o título dizia "Stick"). O `sticky` **exige** pelo menos um limite (`top`, `bottom`...); no `fixed` e no `absolute` isso é opcional. E o `sticky` não funciona se algum ancestral tiver `overflow: hidden`, `auto` ou `scroll`.

## Comparando

Com cinco valores de `position`, a dúvida mais comum é saber **em relação a quê** cada um se posiciona e se o elemento continua ocupando espaço no fluxo. Resumindo: `static` não aceita deslocamento. `relative` se desloca a partir da própria posição original e **mantém** o espaço que ocupava. `absolute` sai do fluxo e se posiciona em relação ao ancestral mais próximo que tenha `position` diferente de `static`; sem ancestral assim, usa a página. `fixed` sai do fluxo e fica preso à janela. `sticky` se comporta como `relative` até chegar a um limite e, então, “gruda”. O truque mais usado: `relative` no pai e `absolute` no filho, para posicionar algo dentro de um cartão.

| Valor | Sai do fluxo? | Referência de `top`/`left` |
| --- | --- | --- |
| `static` | não | (ignora) |
| `relative` | não | a própria posição original |
| `absolute` | sim | o ancestral posicionado mais próximo |
| `fixed` | sim | a janela do navegador |
| `sticky` | não | a janela, ao atingir o limite |

## `overflow`: rolagem dentro de um elemento

Quando o conteúdo é maior que a caixa, o `overflow` decide o que fazer com a sobra, e já vimos que a escolha mais usada para áreas roláveis é `auto`, que só mostra a barra quando precisa. Esse recurso se une ao posicionamento em um caso clássico: uma lista de mensagens com altura fixa (`height: 300px`) e `overflow-y: auto`, em que o cabeçalho usa `position: sticky` para ficar visível enquanto o conteúdo rola por baixo. Repare que o `overflow` só funciona quando o elemento tem altura ou largura limitada; sem limite, a caixa simplesmente cresce para acomodar o conteúdo.

Quando o conteúdo é maior que a caixa, `overflow` decide o que fazer: `visible` (vaza, o padrão), `hidden` (corta), `scroll` (barras sempre) ou `auto` (barras só quando precisa). Use `overflow-x` e `overflow-y` para cada eixo. Mais detalhes na aula "Ordem de pilha de elementos".

```css
/* auto: barra de rolagem só se precisar */
.caixa {
  height: 200px;
  overflow-y: auto;
}
```

## Projeto de exemplo

**Código revisado (texto de preenchimento resumido)**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Trabalhando com posicionamentos</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="relativo">
    <p>Posição relativa: obedece às coordenadas.</p>
  </div>

  <div id="fixo">
    <p>Div fixa: não sai do lugar ao rolar.</p>
  </div>

  <div id="referencia">
    <div id="absoluto">
      <p>Posição absoluta (em relação à vermelha).</p>
    </div>
  </div>

  <div id="sticky">
    <p>Esta div testa o comportamento sticky.</p>
  </div>

  <!-- vários parágrafos para gerar rolagem -->
  <p>Lorem ipsum dolor sit amet...</p>
</body>
</html>
```

```css
#relativo {
  position: relative;
  left: 30px;
  width: 300px;
  border: 3px solid #73ad21;
}

#fixo {
  position: fixed;
  top: 0;
  right: 0;
  width: 300px;
  border: 5px solid #a3ad21;
  background: white;
}

/* o "pai" que serve de referência ao absoluto */
#referencia {
  position: relative;
  width: 600px;
  height: 200px;
  border: 3px solid red;
}

#absoluto {
  position: absolute;
  top: 50px;
  right: 150px;
  width: 300px;
  height: 70px;
  border: 3px solid blue;
}

#sticky {
  position: sticky;
  /* faltava: sem isso o sticky não gruda */
  top: 0;
  background-color: pink;
  border: 2px solid #4caf50;
  width: 600px;
}

p {
  font-size: 20px;
  text-align: center;
}
```

> ⚠️ **Bugs corrigidos no projeto:** o `#sticky` não tinha `top`, então **nunca grudava**; ele também tinha `overflow-y: scroll` e altura fixa, o que o transformava numa caixa com rolagem própria. O documento terminava com `<body>` em vez de `</body>`. E os IDs foram padronizados em minúsculas, porque IDs diferenciam maiúsculas de minúsculas.

## Exercício

Crie um cartão de produto de 200 px de largura com uma etiqueta "NOVO" fixa no canto superior direito do cartão (não da página).

<details>
<summary>Ver resposta</summary>

```html
<!-- cartão com a etiqueta dentro dele -->
<div class="cartao">
  <span class="etiqueta">NOVO</span>
  <h3>Fone de ouvido</h3>
  <p>R$ 120,00</p>
</div>
```

```css
.cartao {
  /* referência para o filho absoluto */
  position: relative;
  width: 200px;
  padding: 16px;
  border: 1px solid #ccc;
}

.etiqueta {
  position: absolute;
  top: 8px;
  right: 8px;
  background: red;
  color: white;
  padding: 2px 6px;
}
```

Teste: a etiqueta fica no canto do cartão. Se você tirar o `position: relative` do cartão, ela vai para o canto da página.

</details>

## Resumo visual: os valores de position

![Cada valor de position, sua referência e se ocupa espaço.](../img/st-position-valores.svg)

> 💡 **Analogia:** pense em um mural de avisos. O `static` é o aviso na fila normal; o `relative` é o mesmo aviso deslocado um pouco, mantendo seu lugar reservado; o `absolute` é um papel colado em qualquer ponto da moldura; o `fixed` é um adesivo no vidro, que não se mexe quando o mural rola.

## 🧠 Revisão rápida

**Um `.selo` com `position: absolute` foi parar no canto da página, e não no canto do card. Por quê?**

Porque nenhum ancestral está posicionado. Coloque `position: relative` no card.

**Qual a diferença entre `fixed` e `sticky`?**

O `fixed` fica sempre preso à janela; o `sticky` segue o fluxo até atingir o limite e só então gruda.

**O `relative` libera o espaço original do elemento?**

Não: o espaço continua reservado e os vizinhos não se mexem.

> ➡️ **Próximo passo:** posicionar exige saber o tamanho real das caixas, e ele depende de como o padding e a borda são somados: **Tamanho de caixa (mexendo no box)**.

## 📌 Resumo

| Valor | Em uma frase |
| --- | --- |
| `static` | fluxo normal; ignora coordenadas |
| `relative` | desloca da posição original; espaço fica |
| `absolute` | sai do fluxo; ancorado no pai posicionado |
| `fixed` | preso à janela; não rola |
| `sticky` | normal até o limite, depois gruda |
| `overflow` | o que fazer com o conteúdo que não cabe |
