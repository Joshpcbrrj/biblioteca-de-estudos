# Mais sobre arrays: find, some, every, sort e desestruturação

> ✨ **Página nova:** complementa a página Arrays com métodos de busca, ordenação e a sintaxe moderna de desestruturação, spread e rest, que aparecem em todo código JavaScript atual.

> 🗺️ **Nesta aula:** buscar elementos (`find`, `findIndex`, `some`, `every`), recortar sem estragar o original (`slice`), ordenar corretamente (`sort` e `toSorted`), matrizes, desestruturação, spread e parâmetros rest.

## 1. Buscando elementos

| Método | Pergunta que responde | Retorna |
| --- | --- | --- |
| `includes(x)` | o valor `x` está no array? | `true` / `false` |
| `find(fn)` | qual o **primeiro** elemento que passa no teste? | o elemento ou `undefined` |
| `findIndex(fn)` | em que posição está esse elemento? | índice ou `-1` |
| `some(fn)` | **algum** elemento passa no teste? | `true` / `false` |
| `every(fn)` | **todos** passam no teste? | `true` / `false` |

**Código exemplo**

```jsx
const alunos = [
  { nome: "Ana", nota: 8 },
  { nome: "Bruno", nota: 5 },
  { nome: "Carla", nota: 9.5 },
];

alunos.find(a => a.nota < 7);  // { nome: "Bruno", nota: 5 }
alunos.findIndex(a => a.nome === "Carla");  // 2
alunos.some(a => a.nota === 10);  // false → ninguém tirou 10
alunos.every(a => a.nota >= 5);  // true  → todos com 5 ou mais
```

## 2. `slice` × `splice`

|  | `slice(ini, fim)` | `splice(ini, qtd, ...novos)` |
| --- | --- | --- |
| Altera o array original? | ❌ não | ✅ sim |
| Para que serve | copiar um pedaço | remover, inserir ou substituir itens |

**Código exemplo**

```jsx
const letras = ["a", "b", "c", "d", "e"];

const meio = letras.slice(1, 4);  // ["b", "c", "d"]; letras continua igual
const ultimos = letras.slice(-2);  // ["d", "e"]

letras.splice(1, 2, "X");  // remove "b" e "c" e insere "X" no lugar
console.log(letras);  // ["a", "X", "d", "e"]
```

## 3. Ordenando com `sort`

- Sem argumentos, `sort()` ordena como **texto**. Para números, isso dá resultado errado.
- Passe uma função de comparação: `(a, b) => a - b` (crescente) ou `(a, b) => b - a` (decrescente).
- `sort` **altera** o array original. Desde o ES2023 existe `toSorted()`, que devolve uma cópia ordenada.

**Código exemplo**

```jsx
const nums = [10, 9, 1, 25];

console.log([...nums].sort());  // [1, 10, 25, 9] ← ordem de texto!
console.log([...nums].sort((a, b) => a - b)); // [1, 9, 10, 25]
console.log(nums.toSorted((a, b) => b - a));  // [25, 10, 9, 1]; nums não muda

const nomes = ["Érica", "bruno", "Ana"];
nomes.sort((a, b) => a.localeCompare(b, "pt-BR"));  // ordem alfabética correta com acentos
console.log(nomes);  // ["Ana", "bruno", "Érica"]

const alunos = [{ nome: "Ana", nota: 8 }, { nome: "Bia", nota: 9.5 }];
alunos.sort((a, b) => b.nota - a.nota);  // maior nota primeiro
```

## 4. Matrizes (arrays de arrays)

- Um array pode conter outros arrays, formando linhas e colunas: `matriz[linha][coluna]`.

**Código exemplo**

```jsx
const tabuleiro = [
  ["X", "O", "X"],
  [" ", "X", "O"],
  ["O", " ", "X"],
];

console.log(tabuleiro[1][2]);  // "O" (linha 1, coluna 2)

for (const linha of tabuleiro) {
  console.log(linha.join(" | "));
}
```

## 5. Desestruturação

- Extrai valores de arrays e objetos direto para variáveis, em uma linha.

**Código exemplo: arrays**

```jsx
const cores = ["vermelho", "verde", "azul"];
const [primeira, segunda] = cores;  // "vermelho", "verde"
const [, , terceira] = cores;  // pula posições: "azul"

let a = 1, b = 2;
[a, b] = [b, a];  // troca de valores (desafio de Dados)
```

**Código exemplo: objetos**

```jsx
const usuario = { nome: "Ana", idade: 30, cidade: "Recife" };

const { nome, idade } = usuario;  // variáveis com o nome das chaves
const { cidade: local } = usuario;  // renomeando: local = "Recife"
const { pais = "Brasil" } = usuario;  // valor padrão se a chave não existir

// Muito usado nos parâmetros de funções
function apresentar({ nome, idade }) {
  return `${nome} tem ${idade} anos`;
}
apresentar(usuario);  // "Ana tem 30 anos"
```

## 6. Spread e rest (`...`)

- **Spread** (espalhar): abre um array ou objeto em elementos soltos. Serve para copiar e juntar.
- **Rest** (resto): junta vários valores em um array. Aparece em parâmetros e na desestruturação.

**Código exemplo**

```jsx
// Spread
const frutas = ["maçã", "banana"];
const todas = [...frutas, "uva"];  // ["maçã", "banana", "uva"]
console.log(Math.max(...[3, 9, 4]));  // 9
const atualizado = { ...{ nome: "Ana", idade: 30 }, idade: 31 };  // { nome: "Ana", idade: 31 }

// Rest em parâmetros: quantidade livre de argumentos
function somar(...numeros) {
  return numeros.reduce((total, n) => total + n, 0);
}
somar(1, 2, 3, 4);  // 10

// Rest na desestruturação
const [primeiro, ...resto] = [10, 20, 30];  // primeiro = 10, resto = [20, 30]
```

## 📌 Resumo da aula

| Tema | Lembre |
| --- | --- |
| Buscar | `find` (elemento), `findIndex` (posição), `some` (algum?), `every` (todos?) |
| Recortar | `slice` copia; `splice` altera o original |
| Ordenar números | sempre `sort((a, b) => a - b)`; `toSorted` não altera o original |
| Matriz | `matriz[linha][coluna]` |
| Desestruturação | `const [a, b] = array` · `const { nome } = objeto` |
| `...` | spread espalha (copiar/juntar); rest junta (parâmetros variados) |
