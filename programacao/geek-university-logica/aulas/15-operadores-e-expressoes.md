# Operadores e expressões

> ✨ **Página nova:** as aulas usam operadores desde o início, mas eles só aparecem espalhados. Esta página reúne todos, com as diferenças entre Python, Java e C que mais causam erros.

> 🗺️ **Nesta aula:** operadores aritméticos (com divisão inteira e resto), de atribuição, relacionais e lógicos, a tabela verdade, a ordem de precedência e como montar expressões a partir de frases em português.

## 1. Expressão

Uma **expressão** é uma combinação de valores, variáveis e operadores que produz **um resultado**. `preco * quantidade` é uma expressão aritmética (resulta em número); `idade >= 18` é uma expressão lógica (resulta em verdadeiro ou falso).

## 2. Operadores aritméticos

| Operação | Pseudocódigo | Python | Java / C | Exemplo | Resultado |
| --- | --- | --- | --- | --- | --- |
| Soma | `+` | `+` | `+` | `7 + 2` | 9 |
| Subtração | `-` | `-` | `-` | `7 - 2` | 5 |
| Multiplicação | `*` | `*` | `*` | `7 * 2` | 14 |
| Divisão | `/` | `/` | `/` | `7 / 2` | 3.5 em Python; **3** em Java/C com inteiros |
| Divisão inteira | `div` | `//` | `/` entre inteiros | `7 // 2` | 3 |
| Resto | `mod` ou `%` | `%` | `%` | `7 % 2` | 1 |
| Potência | `^` | `**` | `Math.pow(7, 2)` / `pow(7, 2)` | `7 ** 2` | 49 |

**Onde as linguagens diferem**

```python
print(7 / 2)  # 3.5 → em Python, / sempre dá resultado real
print(7 // 2)  # 3  → divisão inteira
print(7 % 2)  # 1  → resto
print(2 ** 10)  # 1024
```

```java
System.out.println(7 / 2);  // 3  → inteiro / inteiro = inteiro
System.out.println(7.0 / 2);  // 3.5 → basta um operando real
System.out.println(7 % 2);  // 1
System.out.println(Math.pow(2, 10));  // 1024.0
```

```c
printf("%d\n", 7 / 2);  // 3
printf("%.1f\n", 7.0 / 2);  // 3.5
printf("%d\n", 7 % 2);  // 1
// pow(2, 10) exige #include <math.h>
```

> ⚠️ Com números **negativos**, a divisão inteira muda de linguagem para linguagem: em Python `-7 // 2` dá `-4` (arredonda para baixo); em Java e C `-7 / 2` dá `-3` (corta a parte decimal). Teste antes de confiar.

### Para que servem a divisão inteira e o resto

| Problema | Expressão |
| --- | --- |
| O número é par? | `n % 2 == 0` |
| É múltiplo de 5? | `n % 5 == 0` |
| Último dígito de 1234 | `1234 % 10` → 4 |
| Tirar o último dígito de 1234 | `1234 // 10` → 123 |
| 135 minutos em horas e minutos | `135 // 60` → 2 h e `135 % 60` → 15 min |

## 3. Atribuição

| Forma | Equivale a | Python | Java / C |
| --- | --- | --- | --- |
| `x <- x + 1` | somar 1 | `x += 1` | `x += 1` ou `x++` |
| `x <- x - 5` | subtrair 5 | `x -= 5` | `x -= 5` |
| `x <- x * 2` | dobrar | `x *= 2` | `x *= 2` |
| `x <- x / 2` | dividir | `x /= 2` | `x /= 2` |

Python **não tem** `++` nem `--`; use `x += 1`.

## 4. Operadores relacionais

Comparam dois valores e sempre resultam em **verdadeiro** ou **falso**.

| Significado | Pseudocódigo | Python / Java / C |
| --- | --- | --- |
| igual | `=` | `==` |
| diferente | `<>` | `!=` |
| maior / menor | `>` / `<` | `>` / `<` |
| maior ou igual / menor ou igual | `>=` / `<=` | `>=` / `<=` |

> ⚠️ Em Java, compare textos com `.equals()`: `nome.equals("Ana")`. O `==` compara se são o **mesmo objeto** na memória e pode dar `false` mesmo com textos iguais. Em Python, `==` compara o conteúdo normalmente.

## 5. Operadores lógicos e tabela verdade

| Lógico | Pseudocódigo | Python | Java / C | Verdadeiro quando… |
| --- | --- | --- | --- | --- |
| E | `E` | `and` | `&&` | as **duas** condições são verdadeiras |
| OU | `OU` | `or` | `\|\|` | **pelo menos uma** é verdadeira |
| NÃO | `NÃO` | `not` | `!` | a condição é falsa (inverte) |

| A | B | A E B | A OU B | NÃO A |
| --- | --- | --- | --- | --- |
| V | V | **V** | **V** | F |
| V | F | F | **V** | F |
| F | V | F | **V** | **V** |
| F | F | F | F | **V** |

**Para memorizar:** E só é verdadeiro se **tudo** for verdadeiro; OU só é falso se **tudo** for falso.

## 6. Precedência: quem é calculado primeiro

| Ordem | Operadores |
| --- | --- |
| 1º | parênteses `( )` |
| 2º | potência |
| 3º | `*` `/` `//` `%` (da esquerda para a direita) |
| 4º | `+` `-` |
| 5º | relacionais `>` `<` `>=` `<=` `==` `!=` |
| 6º | NÃO (`not` do Python; em Java e C o `!` é unário e vem logo depois dos parênteses, por isso escreva `!(a == b)`) |
| 7º | E |
| 8º | OU |
| 9º | atribuição |

**Resolvendo uma expressão passo a passo**

`3 + 4 * 2 > 10 and not 5 == 6`

1. `4 * 2` → 8, então `3 + 8` → 11.
2. Relacionais: `11 > 10` → V e `5 == 6` → F.
3. `not F` → V.
4. `V and V` → **V**.

```python
print(3 + 4 * 2 > 10 and not 5 == 6)  # True
print((3 + 4) * 2)  # 14 → parênteses mudam a ordem
```

## 7. De frase em português para expressão

| Frase | Expressão (Python) |
| --- | --- |
| idade entre 18 e 65 anos, inclusive | `idade >= 18 and idade <= 65` (ou `18 <= idade <= 65`) |
| menor de 12 **ou** maior de 60 | `idade < 12 or idade > 60` |
| número par e positivo | `n % 2 == 0 and n > 0` |
| nota fora do intervalo de 0 a 10 | `nota < 0 or nota > 10` |
| não é fim de semana | `not (dia == "sábado" or dia == "domingo")` |
| ano bissexto | `(ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0` |

> 💡 Erro clássico: escrever `idade >= 18 and <= 65`. Cada lado do E/OU precisa ser uma comparação completa. A forma encadeada `18 <= idade <= 65` só existe em Python.

## 📌 Resumo da aula

| Grupo | Lembre |
| --- | --- |
| Aritméticos | `/` em Python dá real; em Java/C, inteiro / inteiro = inteiro |
| Divisão inteira e resto | `//` e `%`; resto 0 = divisível (par, múltiplo) |
| Atribuição composta | `x += 1`; Python não tem `++` |
| Relacionais | `==` compara, `=` atribui; textos em Java com `.equals()` |
| Lógicos | E: tudo verdadeiro · OU: pelo menos um · NÃO: inverte |
| Precedência | parênteses → aritméticos → relacionais → NÃO → E → OU |
| Na dúvida | use parênteses |
