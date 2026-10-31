# Textos e números: métodos essenciais

> ✨ **Página nova:** a página Dados apresenta os tipos; esta reúne as ferramentas para trabalhar com eles no dia a dia, muito usadas nos desafios e na lista final.

> 🗺️ **Nesta aula:** métodos de string (tamanho, maiúsculas, busca, recorte, troca, divisão) e de número (arredondamento, `Math`, sorteio, validação e formatação em reais).

## 1. Strings

- Uma string se comporta como uma lista de caracteres: tem `length` e cada caractere tem um índice começando em 0.
- Strings são **imutáveis**: os métodos não alteram a original, sempre devolvem uma **nova** string.

| Método | O que faz | Exemplo | Resultado |
| --- | --- | --- | --- |
| `length` | quantidade de caracteres | `"Brasil".length` | `6` |
| `[i]` / `at(i)` | caractere na posição (`at(-1)` = último) | `"Brasil".at(-1)` | `"l"` |
| `toUpperCase()` / `toLowerCase()` | maiúsculas / minúsculas | `"js".toUpperCase()` | `"JS"` |
| `trim()` | remove espaços das pontas | `"  oi  ".trim()` | `"oi"` |
| `includes(t)` | contém o trecho? | `"banana".includes("nan")` | `true` |
| `startsWith(t)` / `endsWith(t)` | começa / termina com? | `"foto.png".endsWith(".png")` | `true` |
| `indexOf(t)` | posição da primeira ocorrência (-1 se não achar) | `"banana".indexOf("n")` | `2` |
| `slice(ini, fim)` | recorta do índice `ini` até antes de `fim` | `"JavaScript".slice(0, 4)` | `"Java"` |
| `replace(a, b)` / `replaceAll(a, b)` | troca a primeira / todas as ocorrências | `"a-b-c".replaceAll("-", "/")` | `"a/b/c"` |
| `split(sep)` | divide em array | `"a,b,c".split(",")` | `["a", "b", "c"]` |
| `repeat(n)` | repete n vezes | `"#".repeat(3)` | `"###"` |
| `padStart(n, c)` | completa à esquerda até n caracteres | `"7".padStart(2, "0")` | `"07"` |

**Código exemplo: tratando um nome digitado**

```jsx
const entrada = "   maria DA silva  ";

const nome = entrada.trim().toLowerCase();  // "maria da silva"
const primeiroNome = nome.split(" ")[0];  // "maria"
const capitalizado = primeiroNome[0].toUpperCase() + primeiroNome.slice(1);
console.log(capitalizado);  // "Maria"

console.log(nome.includes("silva"));  // true
console.log(nome.length);  // 14
```

**Código exemplo: inverter e contar letras**

```jsx
const palavra = "arara";

const invertida = palavra.split("").reverse().join("");  // string → array → inverte → string
console.log(invertida === palavra ? "É palíndromo" : "Não é");  // É palíndromo

let vogais = 0;
for (const letra of palavra) {
  if ("aeiou".includes(letra)) vogais++;
}
console.log(`${vogais} vogais`);  // 3 vogais
```

> ⚠️ `replace` com texto troca **só a primeira** ocorrência. Para trocar todas, use `replaceAll`.

## 2. Números e o objeto `Math`

| Recurso | O que faz | Exemplo | Resultado |
| --- | --- | --- | --- |
| `toFixed(n)` | fixa n casas decimais (devolve **string**) | `(2.567).toFixed(2)` | `"2.57"` |
| `Math.round(x)` | arredonda para o inteiro mais próximo | `Math.round(2.5)` | `3` |
| `Math.floor(x)` | arredonda para baixo | `Math.floor(2.9)` | `2` |
| `Math.ceil(x)` | arredonda para cima | `Math.ceil(2.1)` | `3` |
| `Math.trunc(x)` | corta a parte decimal | `Math.trunc(-2.7)` | `-2` |
| `Math.max(...)` / `Math.min(...)` | maior / menor valor | `Math.max(3, 9, 4)` | `9` |
| `Math.abs(x)` | valor absoluto | `Math.abs(-5)` | `5` |
| `Math.sqrt(x)` / `x ** y` | raiz quadrada / potência | `Math.sqrt(16)` | `4` |
| `Math.PI` | π | `Math.PI` | `3.14159…` |
| `Math.random()` | sorteia número entre 0 (incluso) e 1 (excluso) | `Math.random()` | ex.: `0.42…` |

**Código exemplo: sorteando um inteiro entre mín e máx**

```jsx
function sortear(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min;  // inclui os dois extremos
}

console.log(sortear(1, 6));  // dado: 1 a 6
console.log(sortear(1, 60));  // número da Mega-Sena
```

## 3. Validando números

- `Number("abc")` resulta em `NaN` (*Not a Number*). Teste com `Number.isNaN(valor)`. Comparar com `=== NaN` **nunca** funciona, porque `NaN` não é igual nem a si mesmo.
- `Number.isInteger(5)` → `true`; `Number.isInteger(5.5)` → `false`.

**Código exemplo**

```jsx
const entrada = "12a";
const numero = Number(entrada);

if (Number.isNaN(numero)) {
  console.log("Digite apenas números!");
} else {
  console.log(`O dobro é ${numero * 2}`);
}

console.log(NaN === NaN);  // false (!)
```

## 4. Formatando valores em reais

- `toLocaleString` formata números no padrão de cada país: separador de milhar, vírgula decimal e símbolo da moeda.

**Código exemplo**

```jsx
const preco = 1234.5;

console.log(preco.toLocaleString("pt-BR", { style: "currency", currency: "BRL" }));
// R$ 1.234,50

console.log((0.157).toLocaleString("pt-BR", { style: "percent", minimumFractionDigits: 1 }));
// 15,7%
```

> 💡 Lembre: `0.1 + 0.2` dá `0.30000000000000004`. Para dinheiro, arredonde só na hora de **mostrar** (`toFixed(2)` ou `toLocaleString`), ou faça as contas em centavos (inteiros).

## 📌 Resumo da aula

| Tema | Lembre |
| --- | --- |
| Strings | imutáveis; índice começa em 0; `length` dá o tamanho |
| Métodos de texto mais usados | `trim`, `toUpperCase`, `includes`, `slice`, `split`, `replaceAll` |
| Arredondar | `round` (mais próximo), `floor` (baixo), `ceil` (cima), `toFixed` (texto) |
| Sorteio | `Math.floor(Math.random() * (max - min + 1)) + min` |
| Validação | `Number.isNaN()` e `Number.isInteger()` |
| Moeda | `toLocaleString("pt-BR", { style: "currency", currency: "BRL" })` |
