# async/await

> 🗺️ **Nesta aula:** escrever Promises como código sequencial com `async` e `await`, tratar erros com `try/catch`, chamar APIs, rodar operações em paralelo e evitar as armadilhas mais comuns.

## De onde paramos

Com Promises, o callback hell virou uma cadeia de `.then()`. Ainda assim, cada etapa fica dentro de uma função. O `async/await` deixa o mesmo código com cara de passo a passo.

## O que é async/await

`async`**/**`await` **(ES2017) é uma forma de escrever código com Promises que parece sequencial.** Por baixo, continua tudo assíncrono: é só uma sintaxe mais legível para `.then()` e `.catch()`.

- `async` antes de uma função faz com que ela **sempre retorne uma Promise**.
- `await` pausa **aquela função** até a Promise terminar e devolve o valor dela. Se a Promise for rejeitada, o `await` **lança um erro**, que você trata com `try/catch`.

O `await` pausa só a função `async` em que está. O resto do programa (outros eventos, a interface) continua rodando normalmente.

## Exemplo

```jsx
function esperar(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function executarOperacao() {
  console.log("Início da operação");
  try {
    await esperar(2000);
    console.log("Operação assíncrona concluída!");
  } catch (erro) {
    console.error("Ocorreu um erro:", erro);
  }
  console.log("Fim da operação");
}

executarOperacao();
// aparece logo depois de "Início", sem esperar os 2 s
console.log("Enquanto isso...");
```

## Com uma API de verdade

```jsx
async function buscarUsuario(login) {
  try {
    const resposta = await fetch(
      `https://api.github.com/users/${login}`
    );
    // fetch não rejeita em 404!
    if (!resposta.ok) {
      throw new Error(`HTTP ${resposta.status}`);
    }
    const usuario = await resposta.json();
    return usuario.name;
  } catch (erro) {
    console.error("Falha ao buscar:", erro.message);
    return null;
  }
}

// top-level await: só em módulos
const nome = await buscarUsuario("octocat");
```

> ⚠️ O `fetch` só rejeita em **falha de rede**. Uma resposta **404 ou 500 é considerada sucesso** pela Promise. Sempre confira `resposta.ok` (ou `resposta.status`).

## Sequencial × paralelo

```jsx
// ❌ lento: um espera o outro sem necessidade
// (≈ 2 s + 2 s)
const usuarios = await buscar("/usuarios");
const produtos = await buscar("/produtos");

// ✅ rápido: as duas ao mesmo tempo (≈ 2 s)
const [usuarios2, produtos2] = await Promise.all([
  buscar("/usuarios"),
  buscar("/produtos"),
]);
```

Use `await` em sequência só quando uma operação **depende** do resultado da outra.

## Regras rápidas

- `await` só funciona dentro de função `async` ou no topo de um **módulo** (top-level await).
- Uma função `async` sempre retorna Promise: com `async function f() { return 1 }`, `f()` é uma Promise de 1. Para usar o valor, precisa de `await` ou `.then()`.
- `forEach` **não espera** `await`. Para processar itens em sequência, use `for...of`; em paralelo, `Promise.all(array.map(...))`.

```jsx
for (const id of ids) {
  // um de cada vez, em ordem
  await salvar(id);
}
```

## Exercício

Reescreva com `async/await` e `try/catch`:

```jsx
fetch("/api/pedidos/7")
  .then((r) => r.json())
  .then((pedido) => fetch(`/api/clientes/${pedido.clienteId}`))
  .then((r) => r.json())
  .then((cliente) => console.log(cliente.nome))
  .catch((e) => console.error(e));
```

<details>
<summary>Ver resposta</summary>

```jsx
async function mostrarCliente() {
  try {
    const r1 = await fetch("/api/pedidos/7");
    const pedido = await r1.json();
    const r2 = await fetch(
      `/api/clientes/${pedido.clienteId}`
    );
    const cliente = await r2.json();
    console.log(cliente.nome);
  } catch (e) {
    console.error(e);
  }
}

mostrarCliente();
```

Aqui o sequencial é necessário: a segunda requisição depende do `clienteId` da primeira.

</details>

## 🧠 Revisão rápida

**O que uma função `async` sempre retorna?**

Uma Promise.

**O que acontece quando o `await` recebe uma Promise rejeitada?**

Ele lança o erro, que pode ser pego com `try/catch`.

**Como fazer duas requisições independentes ao mesmo tempo?**

`await Promise.all([req1, req2])`.

> ➡️ **Próximo passo:** você já consome APIs. Vamos entender o que é uma API para depois criar a sua: **Introdução API**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `async` | a função passa a retornar Promise |
| `await` | espera a Promise e devolve o valor |
| `try/catch` | trata rejeições |
| Top-level await | `await` fora de função, só em módulos |
| `Promise.all` | várias operações em paralelo |
| `for...of` | espera cada `await`; `forEach` não |
