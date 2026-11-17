# Grid

> 🗺️ **Nesta aula:** referência do CSS Grid: colunas e linhas com `fr`, `repeat()` e `minmax()`, posicionamento pelas linhas da grade, áreas nomeadas e quando usar Grid ou Flexbox.

## De onde paramos

O Flexbox organiza itens em uma direção. Para o esqueleto de uma página, com cabeçalho, conteúdo, barra lateral e rodapé, é mais natural controlar linhas **e** colunas ao mesmo tempo.

## O que é CSS Grid

Imagine desenhar a página num papel quadriculado: você risca linhas e colunas, e depois diz em que quadradinhos cada bloco fica. É isso o Grid. O Flexbox pensa numa direção por vez, e o Grid pensa nas duas ao mesmo tempo, o que o torna a escolha natural para o esqueleto de uma página, galerias de fotos e painéis.

**CSS Grid é um sistema de layout bidimensional: você divide o contêiner em linhas e colunas e posiciona os itens nessa grade.**

```css
.container {
  /* ou inline-grid */
  display: grid;
}
```

## Principais propriedades

| Propriedade | Onde | Para que serve |
| --- | --- | --- |
| `grid-template-columns` | contêiner | quantidade e largura das colunas |
| `grid-template-rows` | contêiner | quantidade e altura das linhas |
| `gap` | contêiner | espaço entre as células |
| `grid-template-areas` | contêiner | "desenhar" o layout com nomes |
| `justify-items` / `align-items` | contêiner | alinhar o conteúdo nas células |
| `grid-column` / `grid-row` | item | linhas onde o item começa e termina |
| `grid-area` | item | área nomeada onde o item fica |

## Colunas e linhas

Veja o exemplo com números. Num contêiner de 800 px e `200px 1fr 2fr`, a primeira coluna pega 200 px. Sobram 600 px, que são divididos em três partes: 1fr fica com 200 px e 2fr com 400 px. Se a janela encolhe para 500 px, as frações encolhem junto (100 e 200), e a coluna fixa continua com 200. O `repeat(auto-fit, minmax(220px, 1fr))` vai além: cria quantas colunas de pelo menos 220 px couberem, e reorganiza sozinho conforme a tela, sem media query.

![fr divide o espaço que sobra depois das medidas fixas.](../img/grid-template-2.svg)

> 💡 **Analogia:** o `fr` é como dividir uma pizza depois de separar os pedaços reservados. Em `200px 1fr 2fr`, primeiro sai a fatia fixa de 200px; o que sobra é dividido em 3 partes iguais, e uma pessoa leva 1 parte enquanto a outra leva 2.

```css
/* 3 colunas: uma fixa e duas proporcionais */
.container {
  display: grid;
  grid-template-columns: 200px 1fr 2fr;
  grid-template-rows: auto 1fr;
  gap: 16px;
}
```

A unidade `fr` ("fração") divide o espaço **livre**. Num contêiner de 800px com `200px 1fr 2fr`, sobram 600px: a 2ª coluna fica com 200px e a 3ª com 400px (sem contar o gap).

```css
/* 4 colunas iguais */
grid-template-columns: repeat(4, 1fr);
/* responsivo sem media query: quantas
   colunas de no mínimo 220px couberem */
grid-template-columns:
  repeat(auto-fit, minmax(220px, 1fr));
```

## Posicionando itens

Cada item pode ser posicionado pelas linhas da grade. O que confunde é que há uma linha a mais que colunas: uma grade com 3 colunas tem 4 linhas, numeradas de 1 a 4. `grid-column: 1 / 3` diz "comece na linha 1 e termine na linha 3", ocupando duas colunas. O valor `-1` é a última linha, o que torna `1 / -1` um atalho para "largura total", mesmo sem saber quantas colunas existem.

![Itens são posicionados pelas linhas da grade, não pelas células.](../img/grid-linhas-2.svg)

> 💡 **Analogia:** as linhas da grade são como as ruas numeradas de um bairro planejado. Um terreno "da rua 1 à rua 3" ocupa dois quarteirões: você informa as ruas, não os quarteirões.

```css
/* da linha 1 à 3 = 2 colunas */
.destaque { grid-column: 1 / 3; }
/* 2 linhas */
.lateral { grid-row: 1 / 3; }
/* largura total */
.banner { grid-column: 1 / -1; }
/* 2 colunas a partir de onde estiver */
.card { grid-column: span 2; }
```

## Áreas nomeadas

As áreas nomeadas são a parte mais legível do Grid: o próprio CSS parece um desenho. Cada linha de texto entre aspas é uma linha da grade, e cada palavra é um quadradinho; repetir o nome (`header header`) faz o item ocupar os dois. Cada elemento escolhe seu lugar com `grid-area`. Para mudar o layout no celular, você só reescreve o desenho.

```css
/* areas: desenha o layout com nomes */
.pagina {
  display: grid;
  grid-template-columns: 3fr 1fr;
  grid-template-areas:
    "header   header"
    "conteudo lateral"
    "footer   footer";
  gap: 10px;
}
header { grid-area: header; }
main   { grid-area: conteudo; }
aside  { grid-area: lateral; }
footer { grid-area: footer; }
```

Para o celular, basta redesenhar as áreas numa media query:

```css
/* no celular: uma coluna, áreas empilhadas */
@media (max-width: 600px) {
  .pagina {
    grid-template-columns: 1fr;
    grid-template-areas:
      "header" "conteudo" "lateral" "footer";
  }
}
```

## Flexbox ou Grid?

- **Grid** para o esqueleto da página e para galerias e dashboards, ou seja, tudo que tem linhas **e** colunas.
- **Flexbox** para componentes em uma direção: menus, barras de botões, alinhar ícone e texto.
- Eles se combinam muito bem: Grid na página e Flexbox dentro de cada bloco.

> 💡 No DevTools (Chrome/Firefox), clique no selo **grid** ao lado do elemento na aba Elements: o navegador desenha as linhas e os números da grade por cima da página.

> ⚠️ **Correções:** `grid-gap` é o nome antigo; hoje a propriedade se chama `gap`. No exemplo original, o seletor `container` estava sem o ponto (`.container`).

## Exercício

Crie uma galeria de fotos que mostre quantas colunas couberem (cada uma com no mínimo 150px), com 8px de espaço, e faça a primeira foto ocupar 2 colunas e 2 linhas.

<details>
<summary>Ver resposta</summary>

```css
/* auto-fill: cria colunas enquanto couber */
.galeria {
  display: grid;
  grid-template-columns:
    repeat(auto-fill, minmax(150px, 1fr));
  grid-auto-rows: 150px;
  gap: 8px;
}
.galeria img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.galeria img:first-child {
  grid-column: span 2;
  grid-row: span 2;
}
```

`grid-auto-rows` define a altura das linhas criadas automaticamente; `object-fit: cover` evita fotos distorcidas.

</details>

## 🧠 Revisão rápida

**O que `1fr` significa?**

Uma fração do espaço livre do contêiner.

**Como fazer um item ocupar a largura toda?**

`grid-column: 1 / -1`.

**Quando preferir Grid a Flexbox?**

Quando o layout tem linhas e colunas ao mesmo tempo.

> ➡️ **Próximo passo:** e se o grid e os componentes já viessem prontos? Conheça o **Bootstrap**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `display: grid` | cria a grade |
| `grid-template-columns` | define as colunas |
| `fr` | fração do espaço livre |
| `repeat(auto-fit, minmax())` | colunas responsivas sem media query |
| `grid-column: 1 / 3` | posiciona pelas linhas da grade |
| `span` | ocupa N trilhas |
| `grid-template-areas` | desenha o layout com nomes |
