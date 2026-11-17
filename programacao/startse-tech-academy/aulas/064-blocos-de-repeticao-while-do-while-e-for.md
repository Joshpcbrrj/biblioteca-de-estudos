# Blocos de repetição (While, do while e for)

> 🗺️ **Nesta aula:** repetir código com `while`, `do...while` e `for`, percorrer coleções com `for...of` e `for...in`, e controlar laços com `break` e `continue`.

## De onde paramos

Com condicionais o programa escolhe um caminho. Mas muitas tarefas são repetitivas: mostrar cada produto de uma lista, somar várias notas, pedir uma senha até ela estar certa. Para isso servem os laços.

## O que são laços de repetição

Imagine mostrar na tela cem produtos. Sem laços, você escreveria cem linhas quase iguais, e se aparecesse o produto 101, teria de escrever mais uma. Com um laço, escreve a instrução uma vez e diz "repita para cada produto": funciona para 10 itens ou para 10 mil, sem mudar o código. É por isso que, depois das condicionais, os laços são a segunda ferramenta mais usada de toda a programação.

**Laços repetem um bloco de código enquanto uma condição for verdadeira, ou uma vez para cada item de uma coleção.** Cada repetição é chamada de **iteração**.

A condição precisa, em algum momento, ficar falsa. Caso contrário, temos um **loop infinito**, que trava a aba do navegador.

## `while`

Leia o exemplo como o programa lê: "enquanto o contador for menor ou igual a 5, mostre-o e some 1". Acompanhe os valores: começa em 1, mostra 1, vira 2; mostra 2, vira 3; e assim até mostrar 5 e virar 6, quando a condição fica falsa e o laço termina. A linha `contador++` é a que impede o laço infinito: se você a apagar, o contador nunca passa de 1 e a página trava.

Testa a condição **antes** de cada repetição. Se ela já começar falsa, o bloco não roda nenhuma vez.

```jsx
let contador = 1;

while (contador <= 5) {
  console.log(`Contador: ${contador}`);
  // sem esta linha, o loop seria infinito
  contador++;
}
```

## `do...while`

Executa o bloco **primeiro** e testa depois: roda **pelo menos uma vez**.

```jsx
// do...while: executa o bloco antes de testar a condição
let contador = 1;

do {
  console.log(`Contador: ${contador}`);
  contador++;
} while (contador <= 5);
```

![A diferença está em quando a condição é testada.](../img/loops.svg)

> 💡 **Analogia:** o `while` é o porteiro que confere o convite **antes** de você entrar na festa: sem convite, você nem entra. O `do...while` é a degustação no supermercado: você prova primeiro e só depois decide se quer mais. O `for` é a série de abdominais do treino: você já sabe que são 20 e vai contando.

## `for`

O `for` junta, numa única linha, as três partes que o `while` espalha: onde começa (`let i = 1`), até quando continua (`i <= 5`) e como avança (`i++`). Por isso é o preferido quando você sabe o número de repetições: o risco de esquecer o passo e criar um laço infinito diminui, porque o passo está à vista, ao lado da condição.

Junta início, condição e passo em uma linha. Ideal quando você sabe **quantas vezes** quer repetir.

```jsx
// início; condição; passo
for (let i = 1; i <= 5; i++) {
  console.log(`Contador: ${i}`);
}
```

A ordem de execução é: início (uma vez) → testa a condição → executa o bloco → passo → testa a condição de novo, e assim por diante.

## `for...of`: percorrer os valores

A forma mais legível de percorrer arrays, strings, Map e Set.

```jsx
// for...of percorre os valores de um array
const frutas = ["maçã", "uva", "kiwi"];

for (const fruta of frutas) {
  console.log(fruta);
}
```

## `for...in`: percorrer as chaves de um objeto

```jsx
// for...in percorre as chaves de um objeto
const pessoa = { nome: "Ana", idade: 28 };

for (const chave in pessoa) {
  console.log(`${chave}: ${pessoa[chave]}`);
}
```

> ⚠️ Evite `for...in` em arrays: ele percorre as chaves como texto (`"0"`, `"1"`…) e pode incluir propriedades herdadas. Para arrays, use `for...of`.

## `break` e `continue`

As duas palavras mudam o ritmo do laço. O `continue` diz "pule o resto desta volta e vá para a próxima", como ignorar um item inválido da lista. O `break` diz "pare o laço agora", útil quando você já achou o que procurava e não precisa olhar o resto. No exemplo, os números pares são pulados e o laço para depois do 7, por isso a saída é 1, 3, 5, 7.

```jsx
for (let i = 1; i <= 10; i++) {
  // pula para a próxima iteração
  if (i % 2 === 0) continue;
  // encerra o laço
  if (i > 7) break;
  console.log(i);  // 1, 3, 5, 7
}
```

## Qual usar?

| Situação | Laço |
| --- | --- |
| Número de repetições conhecido | `for` |
| Repetir até algo acontecer | `while` |
| Rodar pelo menos uma vez (ex.: menu) | `do...while` |
| Percorrer os itens de um array | `for...of` (ou `forEach`) |
| Percorrer as propriedades de um objeto | `for...in` ou `Object.entries()` |

## Exercício

Usando um laço, calcule a soma dos números pares de 1 a 100 e mostre o resultado no console.

<details>
<summary>Ver resposta</summary>

```jsx
let soma = 0;
for (let i = 2; i <= 100; i += 2) {
  soma += i;
}
console.log(soma);  // 2550
```

Começar em 2 e andar de 2 em 2 dispensa o teste `i % 2 === 0`.

</details>

## 🧠 Revisão rápida

**Qual laço sempre executa pelo menos uma vez?**

O `do...while`.

**Qual a diferença entre `break` e `continue`?**

`break` encerra o laço; `continue` pula só a iteração atual.

**Qual laço usar para percorrer os itens de um array?**

`for...of` (ou métodos como `forEach` e `map`).

> ➡️ **Próximo passo:** laços brilham quando há uma lista de valores para percorrer. Conheça o **Array**.

## 📌 Resumo

| Laço | Em uma frase |
| --- | --- |
| `while` | testa antes; pode rodar 0 vezes |
| `do...while` | testa depois; roda no mínimo 1 vez |
| `for` | início, condição e passo em uma linha |
| `for...of` | percorre os valores de um array ou string |
| `for...in` | percorre as chaves de um objeto |
| `break` / `continue` | encerra o laço / pula a iteração |
