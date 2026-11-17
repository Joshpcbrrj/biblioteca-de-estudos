# Alguns projetos teste

> 🗺️ **Nesta aula:** quatro mini projetos para praticar seleção de elementos, eventos e manipulação do DOM: formulário de login, troca de cor de fundo, conversor de km para milhas e lista de tarefas.

## De onde paramos

Você já conhece a linguagem e as ferramentas do DOM. Agora é hora de juntar tudo. Tente fazer cada projeto sozinho a partir da descrição antes de abrir o código revisado.

## Projeto 1: formulário de login com boas-vindas

Ao enviar o formulário, mostra uma saudação com o nome digitado e esconde o formulário.

**Código revisado**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Formulário simples de login</title>
  <script src="index.js" defer></script>
</head>
<body>
  <h1 id="t1">Introdução ao JavaScript</h1>
  <h2 id="t2"></h2>

  <!-- sem action: o JavaScript trata o envio -->
  <form id="formularioLogin">
    <label for="nomeUsuario">Usuário</label>
    <input type="text" id="nomeUsuario" required>
    <label for="senha">Senha</label>
    <input type="password" id="senha" required>
    <button type="submit">Entrar</button>
  </form>
</body>
</html>
```

```jsx
document.querySelector("#t1").textContent =
  "JavaScript - Introdução";
document.querySelector("#t2").textContent =
  "Alterando o comportamento de um formulário";

const form = document.querySelector("#formularioLogin");

form.addEventListener("submit", (event) => {
  event.preventDefault();  // não recarrega a página
  const nome = document
    .querySelector("#nomeUsuario").value.trim();
  alert(`Olá, ${nome}! Seja bem-vindo!`);
  form.hidden = true;  // esconde o formulário
});
```

## Projeto 2: trocar a cor de fundo

**Código revisado**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Opções de cor de fundo</title>
  <script src="index.js" defer></script>
</head>
<body>
  <h1>Introdução ao JavaScript</h1>
  <h2>Mexendo com a cor de fundo</h2>

  <label for="coresFundo">Escolha a cor de fundo:</label>
  <!-- value de cada option é uma cor do CSS -->
  <select id="coresFundo">
    <option value="white">Branco</option>
    <option value="lightblue">Azul</option>
    <option value="khaki">Amarelo</option>
    <option value="lightgreen">Verde</option>
    <option value="salmon">Vermelho</option>
  </select>

  <button id="imprimir">Imprimir</button>
</body>
</html>
```

```jsx
const menu = document.querySelector("#coresFundo");

menu.addEventListener("change", () => {
  // value já é a opção selecionada
  document.body.style.backgroundColor = menu.value;
});

document.querySelector("#imprimir")
  .addEventListener("click", () => window.print());
```

## Projeto 3: conversor de quilômetros para milhas

**1 km = 0,621371 milha** (e 1 milha = 1,609 km).

**Código revisado**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Conversor de km para milhas</title>
  <script src="index.js" defer></script>
</head>
<body>
  <h1>Conversão de km para milhas</h1>

  <input type="number" id="valorKm"
    value="1" min="0" step="any">
  <label for="valorKm"><b>km</b></label> =
  <!-- output: elemento próprio para resultados -->
  <output id="resultado">0.621</output> <b>milhas</b>

  <button type="button" id="botaoCalcular">Calcular</button>
</body>
</html>
```

```jsx
const KM_PARA_MILHA = 0.621371;

function calculaKmMilha() {
  const campo = document.querySelector("#valorKm");
  const km = Number(campo.value);
  const milhas = (km * KM_PARA_MILHA).toFixed(3);
  document.querySelector("#resultado").textContent = milhas;
}

document.querySelector("#botaoCalcular")
  .addEventListener("click", calculaKmMilha);

// A variável km existe só DENTRO da função (escopo local).
// Um console.log(km) aqui fora lançaria
// "ReferenceError: km is not defined".
```

## Projeto 4: lista de tarefas

Adicionar, marcar, remover e ações em massa (marcar, desmarcar ou limpar todas).

**Código revisado**

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport"
    content="width=device-width, initial-scale=1.0">
  <title>Lista de tarefas</title>
  <link rel="stylesheet" href="style.css">
  <script src="index.js" defer></script>
</head>
<body>
  <h1>Lista de tarefas</h1>
  <div class="barra">
    <input type="text" id="caixaDeTexto"
      placeholder="Tarefa" aria-label="Nova tarefa">
    <button id="botaoAdicionar"
      aria-label="Adicionar">&#10011;</button>
    <!-- hidden: só aparece quando há tarefas -->
    <select id="listaSuspensa" hidden>
      <option value="">-- Selecione uma opção</option>
      <option value="marcar">
        Marcar todas as tarefas</option>
      <option value="desmarcar">
        Desmarcar todas as tarefas</option>
      <option value="limpar">
        Limpar todas as tarefas</option>
    </select>
  </div>
  <ul id="listaTarefas"></ul>
  <footer>&copy; 2023 - Lista de Tarefas</footer>
</body>
</html>
```

```css
/* fundo escuro e espaço para o footer fixo */
body {
  background: rgb(3, 3, 59);
  color: white;
  font: 14pt Tahoma, sans-serif;
  margin: 0;
  padding: 0 0 60px;  /* espaço para o footer fixo */
}
h1 { text-align: center; }

.barra {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
}
input[type="text"], button, select { padding: 5px; }

ul {
  list-style: none;
  max-width: 600px;
  margin: 0 auto;
  padding: 0;
}
li {
  /* referência para o botão remover */
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 40px 5px 10px;
  cursor: pointer;
}
li.realizada .texto {
  color: darkgray;
  text-decoration: line-through;
}
button.remover {
  position: absolute;
  right: 0;
}

footer {
  background-color: #222;
  text-align: center;
  padding: 10px;
  position: fixed;
  bottom: 0;
  width: 100%;
}
```

```jsx
const listaTarefas =
  document.querySelector("#listaTarefas");
const caixaTexto = document.querySelector("#caixaDeTexto");
const botaoAdicionar =
  document.querySelector("#botaoAdicionar");
const listaSuspensa =
  document.querySelector("#listaSuspensa");

function adicionar() {
  const texto = caixaTexto.value.trim();
  if (!texto) return;  // não aceita tarefa vazia

  listaTarefas.append(criaTarefa(texto));
  caixaTexto.value = "";
  caixaTexto.focus();
  atualizaListaSuspensa();
}

botaoAdicionar.addEventListener("click", adicionar);
caixaTexto.addEventListener("keydown", (e) => {
  // Enter também adiciona
  if (e.key === "Enter") adicionar();
});

function criaTarefa(texto) {
  const li = document.createElement("li");
  const checkbox = document.createElement("input");
  const span = document.createElement("span");
  const remover = document.createElement("button");

  checkbox.type = "checkbox";
  // classe, não id: ids não podem se repetir
  span.className = "texto";
  span.textContent = texto;
  remover.className = "remover";
  remover.textContent = "✕";
  remover.setAttribute("aria-label", "Remover tarefa");

  checkbox.addEventListener("change", () => {
    li.classList.toggle("realizada", checkbox.checked);
  });

  remover.addEventListener("click", () => {
    li.remove();
    atualizaListaSuspensa();
  });

  li.append(checkbox, span, remover);
  return li;
}

function atualizaListaSuspensa() {
  listaSuspensa.hidden = listaTarefas.children.length === 0;
}

listaSuspensa.addEventListener("change", () => {
  const acao = listaSuspensa.value;

  if (acao === "marcar" || acao === "desmarcar") {
    const marcar = acao === "marcar";
    // const: evita criar variável global
    for (const li of listaTarefas.children) {
      li.querySelector("input").checked = marcar;
      li.classList.toggle("realizada", marcar);
    }
  } else if (acao === "limpar") {
    // remove todos os filhos
    listaTarefas.replaceChildren();
    atualizaListaSuspensa();
  }

  listaSuspensa.value = "";  // volta para "Selecione"
});
```

> ⚠️ **Correções:**
>
> - **Conversor: a fórmula estava invertida.** `km * 1.609` converte milhas para km. Para km → milhas, multiplique por **0,621371** (ou divida por 1,609). O valor inicial "1.609" ao lado de 1 km também estava errado.
> - **Conversor:** o `console.log(km)` fora da função não "deixa de aparecer": ele lança um **ReferenceError**.
> - **Lista de tarefas:** todo `span` recebia `id="tarefa"`, mas **ids não podem se repetir**. Troquei por uma classe e simplifiquei a lógica.
> - **Lista de tarefas:** `for (tarefa of ...)` sem `const` criava uma variável global implícita (erro em modo estrito). Também passou a recusar tarefas vazias, aceitar Enter e voltar o select para "Selecione".
> - Os eventos inline (`onsubmit`, `onchange`, `onclick`) foram trocados por `addEventListener`, separando HTML e JS. O submit agora usa `preventDefault()`.
> - Corrigidos os textos "JavaScipt" e "Intrudução", `lang="pt-BR"` e a remoção da meta do Internet Explorer. As cores do projeto 2 ficaram mais suaves para manter o texto legível.

## Desafio extra

Na lista de tarefas, faça as tarefas sobreviverem ao recarregamento da página, salvando-as no `localStorage`.

<details>
<summary>Ver resposta</summary>

```jsx
// grava texto e estado de cada tarefa
function salvar() {
  const tarefas = [...listaTarefas.children].map(li => ({
    texto: li.querySelector(".texto").textContent,
    feita: li.classList.contains("realizada"),
  }));
  localStorage.setItem("tarefas", JSON.stringify(tarefas));
}

// recria as tarefas salvas ao abrir a página
function carregar() {
  const salvas = JSON.parse(
    localStorage.getItem("tarefas") ?? "[]"
  );
  for (const t of salvas) {
    const li = criaTarefa(t.texto);
    li.querySelector("input").checked = t.feita;
    li.classList.toggle("realizada", t.feita);
    listaTarefas.append(li);
  }
  atualizaListaSuspensa();
}

carregar();
```

Chame `salvar()` no fim de `adicionar`, no clique de remover, no `change` do checkbox e nas ações em massa.

</details>

## 🧠 Revisão rápida

**Por que o projeto 1 chama `event.preventDefault()`?**

Para o envio do formulário não recarregar a página.

**Qual a fórmula correta de km para milhas?**

milhas = km × 0,621371.

**Por que cada tarefa usa uma classe `texto` e não um id?**

Porque ids não podem se repetir na página.

> ➡️ **Próximo passo:** um projeto maior, com cálculos de verdade: **Simulador de financiamento**.

## 📌 Resumo

| Projeto | O que pratica |
| --- | --- |
| Login com boas-vindas | evento `submit`, `preventDefault`, `hidden` |
| Cor de fundo | evento `change` em `select`, `style` |
| Conversor km → milhas | leitura de `input`, `Number`, `toFixed`, escopo |
| Lista de tarefas | `createElement`, `classList`, eventos, ações em massa |
