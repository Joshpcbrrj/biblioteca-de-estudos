# 8 exemplos de Associatividade e Precedência de Operadores em Programação

**Referência (Boson Treinamentos)**

🔗 [Resumo Básico de Operadores em Programação - Bóson Treinamentos em Ciência e Tecnologia](http://www.bosontreinamentos.com.br/logica-de-programacao/resumo-basico-de-operadores-em-programacao/)

> 🗺️ **Nesta aula:** a diferença entre precedência e associatividade, exemplos de cada uma e a tabela completa de operadores da família C, com os equivalentes no Portugol.

## De onde paramos

Ao longo do curso apareceram operadores aritméticos, relacionais, lógicos e de atribuição, muitas vezes na mesma expressão. Esta aula reúne as regras que decidem em que ordem todos eles são resolvidos.

Quando uma expressão tem vários operadores, duas regras decidem a ordem em que eles são resolvidos.

## Precedência

Decide qual operador é resolvido primeiro quando operadores **diferentes** aparecem lado a lado. Os de maior precedência vão antes, como na matemática da escola: multiplicação antes de soma.

```c
// * primeiro: b * c, depois a soma
a + b * c
// parênteses primeiro: a + b
(a + b) * c
```

## Associatividade

Decide a ordem quando operadores de **mesma precedência** aparecem lado a lado:

- **ED (esquerda para a direita)**: o da esquerda é resolvido primeiro. É o caso de `+` e `-`, e de `*`, `/` e `%`.
- **DE (direita para a esquerda)**: o da direita é resolvido primeiro. É o caso das atribuições e da exponenciação.

```c
// ED: (a + b) - c
a + b - c
// (10 - 4) - 3 = 3, e não 9
10 - 4 - 3
// DE: primeiro b = 5, depois a = b
a = b = 5
```

![Três expressões e a ordem de avaliação](../img/pr-arvores.svg)

> 💡 **Analogia:** precedência é a hierarquia de uma fila de embarque (prioridades passam na frente, não importa onde estejam). Associatividade é o critério de desempate dentro do mesmo grupo: entre dois passageiros comuns, vale a ordem de chegada, da esquerda para a direita.

## Tabela de precedência

Da maior para a menor precedência. A tabela é a referência geral das linguagens da família C; nem todos os operadores existem no Portugol (os bit a bit e o condicional, por exemplo), e lá os lógicos se escrevem `e`, `ou` e `nao`.

| Tipo de operador | Operadores | Associatividade |
| --- | --- | --- |
| Parênteses | `( )` | ED |
| Exponenciação (em linguagens que têm o operador) | `**` ou `^` | DE |
| Incremento/decremento pós-fixo | `x++`, `x--` | ED |
| Unários | `-x`, `!` (não), `~`, `++x`, `--x` | DE |
| Multiplicação, divisão e resto | `*`, `/`, `%` | ED |
| Adição e subtração | `+`, `-` | ED |
| Deslocamento de bits | `<<`, `>>` | ED |
| Relacionais | `<`, `<=`, `>`, `>=` | ED |
| Igualdade | `==`, `!=` | ED |
| E bit a bit | `&` | ED |
| OU-exclusivo bit a bit | `^` | ED |
| OU bit a bit | <code>&#124;</code> | ED |
| E lógico | `&&` (no Portugol, `e`) | ED |
| OU lógico | <code>&#124;&#124;</code> (no Portugol, `ou`) | ED |
| Condicional (ternário) | `? :` | DE |
| Atribuição | `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `<<=`, `>>=`, `&=`, `^=`, <code>&#124;=</code> | DE |

> 💡 Na dúvida, use parênteses. Eles não mudam o resultado quando a ordem já está certa e deixam a intenção clara para quem lê: `(a * b) + c` é mais fácil de ler que `a * b + c`.

## 🧠 Revisão rápida

**Quanto vale `2 + 3 * 4 - 1`?**

13: primeiro 3 * 4 = 12; depois, da esquerda, 2 + 12 = 14 e 14 − 1 = 13.

**Quanto vale `20 / 4 / 5`?**

1: ED, então (20 / 4) / 5 = 5 / 5.

**Num `se (a > 5 e b < 3 ou c == 0)`, o que é avaliado primeiro?**

As comparações (`>`, `<`, `==`), depois o `e` e por último o `ou`. Fica: `(a > 5 e b < 3) ou c == 0`.

> ➡️ **Próximo passo:** funções, recursão e expressões juntas na última lista do curso: **5ª Lista de exercícios**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Precedência | Decide qual operador diferente é resolvido primeiro |
| Associatividade | Decide a ordem entre operadores de mesma precedência |
| ED | Da esquerda para a direita: aritméticos, relacionais, lógicos |
| DE | Da direita para a esquerda: atribuições, unários, exponenciação |
| Exemplo | `10 - 4 - 3` vale 3, porque é `(10 - 4) - 3` |
| Na dúvida | Use parênteses |
