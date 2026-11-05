# Testando as propriedades de estilização com um teste prático

> 🗺️ **Nesta aula:** um projeto com três páginas que compartilham o mesmo CSS externo, para ver na prática como o inline e o interno sobrescrevem o externo.

## De onde paramos

A aula anterior explicou as três formas de aplicar CSS e a regra de desempate. Aqui você vai ver cada uma vencendo (ou perdendo) em páginas de verdade.

## Objetivo

Três páginas que usam o **mesmo** arquivo CSS externo, cada uma testando uma forma diferente de aplicar estilo:

| Página | O que testa |
| --- | --- |
| `index.html` | só o CSS externo |
| `pagina2.html` | CSS externo e **inline** em alguns elementos |
| `pagina3.html` | CSS externo e **interno** (`<style>`), que sobrescreve o externo |

## CSS externo (`estilo.css`)

```css
body {
  background-color: aquamarine;
  font-size: 16px;
}

h1 {
  font-size: 120px;
  background-color: aqua;
  color: rgba(4, 4, 70, 0.71);
}

p {
  font-size: 35px;
  background-color: white;
  color: rgb(97, 9, 109);
}
```

## `index.html`: só o externo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Teste de CSS externo</title>
  <link rel="stylesheet" href="estilo.css">
</head>
<body>
  <h1>Teste de CSS externo</h1>
  <p>Esta página testa o CSS externo.</p>
  <a href="pagina2.html">Ir para a página 2</a><br>
  <a href="pagina3.html">Ir para a página 3</a>
</body>
</html>
```

## `pagina2.html`: inline vence o externo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Teste de CSS no elemento</title>
  <link rel="stylesheet" href="estilo.css">
</head>
<body>
  <!-- só o tamanho deste h1 muda; cor e fundo
       continuam vindo do externo -->
  <h1 style="font-size: 100px;">
    Teste de CSS no elemento
  </h1>
  <p>Esta página testa o estilo no elemento.</p>
  <h3>Próximas aulas</h3>
  <p style="color: rgb(72, 95, 7);">
    Aguardem os próximos capítulos!
  </p>
  <a href="index.html">Voltar para o início</a><br>
  <a href="pagina3.html">Ir para a página 3</a>
</body>
</html>
```

## `pagina3.html`: interno depois do externo

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Teste de CSS na página</title>
  <link rel="stylesheet" href="estilo.css">
  <!-- vem DEPOIS do link: com a mesma
       especificidade, estas regras vencem -->
  <style>
    body { background-color: green; }
    p {
      color: rgb(214, 178, 125);
      background-color: black;
      font-size: 25px;
    }
    a {
      font-size: 30px;
      background-color: rgb(200, 159, 238);
      text-decoration: none;
      border: 4px solid rgb(93, 93, 202);
    }
  </style>
</head>
<body>
  <h1>Teste de CSS direto na página</h1>
  <p>Vamos testar a formatação nesta página.</p>
  <a href="index.html">Voltar para o início</a><br>
  <a href="pagina2.html">Ir para a página 2</a>
</body>
</html>
```

> ⚠️ Cuidados com este projeto: o link de volta deve apontar para `index.html` (não para um `pagina1.html` que não existe), e o nome no `<link>` precisa ser exatamente o do arquivo na pasta (`estilo.css`). O `font-size` do `body` chega, sim, ao `h1`; ele só não aparece aqui porque o `estilo.css` define `font-size: 120px` diretamente no `h1`.

> 💡 **Para experimentar:** abra o DevTools (F12) → aba **Elements** → selecione um elemento. O painel **Styles** mostra todas as regras aplicadas, e as que perderam o conflito aparecem **riscadas**. É a melhor forma de entender a cascata na prática.

## Desafio

Na `pagina3.html`, faça só o primeiro parágrafo voltar ao estilo do `estilo.css`, sem apagar o `<style>`.

<details>
<summary>Ver resposta</summary>

Dê uma classe ao parágrafo e repita o estilo externo numa regra mais específica dentro do `<style>`:

```css
p.normal {
  color: rgb(97, 9, 109);
  background-color: white;
  font-size: 35px;
}
```

`p.normal` (0-1-1) vence `p` (0-0-1), independentemente da ordem.

</details>

## 🧠 Revisão rápida

**Na `pagina2.html`, por que o `h1` mantém a cor do arquivo externo?**

Porque o `style` inline só redefine o `font-size`; as outras propriedades continuam vindo do externo.

**O que aconteceria na `pagina3.html` se o `<style>` viesse antes do `<link>`?**

O arquivo externo venceria, porque com a mesma especificidade a última regra ganha.

> ➡️ **Próximo passo:** para mirar exatamente os elementos certos, você precisa dos **Seletores e especificidade do CSS**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Externo compartilhado | um arquivo estiliza as três páginas |
| Inline | sobrescreve só as propriedades que define |
| Interno depois do link | vence o externo pela ordem |
| DevTools → Styles | mostra regras vencedoras e riscadas |
