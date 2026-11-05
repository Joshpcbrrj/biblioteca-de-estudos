# Exercícios 1

> 🗺️ **Nesta lista:** cinco questões de teste de mesa sobre sequência, decisão, repetição e vetores, no estilo da prova de seleção. Tente responder antes de abrir a resolução.

## De onde paramos

Você já viu fluxo sequencial, tipos, decisões e laços. Estas questões usam uma notação um pouco diferente (comandos em maiúsculas, como `ESCREVA` e `LEIA`), comum em provas. A ideia é a mesma: siga o código linha a linha, anotando o valor de cada variável.

> 💡 **Teste de mesa:** faça uma tabela com uma coluna por variável e uma linha por passo. É a forma mais segura de acertar questões assim.

## Questão 1

Sabe-se que:

- `ESCREVA "a", "b"` imprime a mensagem `a b` na tela (os itens saem separados por espaço);
- uma cadeia de caracteres é delimitada por aspas duplas;
- variável é um espaço na memória capaz de guardar e apresentar um valor;
- `REAL x` cria a variável x, que guarda um número real;
- `LEIA z` pede uma informação ao usuário e a guarda em z;
- `*` é o operador de multiplicação.<br />O que o programa mostra na tela, incluindo o que o usuário digitou, se ele digitar 50 e depois 2?

```
REAL a, b

ESCREVA "digite um número: "
LEIA a
ESCREVA "digite um número: "
LEIA b
ESCREVA "a * b = ", a * b
```

<details>
<summary>Ver resposta</summary>

```
digite um número:
50
digite um número:
2
a * b =  100
```

O texto entre aspas sai como está; já `a * b` sem aspas é calculado: 50 × 2 = 100.

</details>

> ⚠️ **Ajuste:** o enunciado original não dizia quais números o usuário digita, mas a resposta usava 50 e 2. Agora o enunciado informa esses valores. O símbolo `*` também tinha sumido da lista de comandos.

## Questão 2

São dados os comandos:

- `INTEIRO x` cria a variável inteira x;
- `ENQUANTO` repete um trecho até a condição ficar falsa;
- `<-` atribui um valor a uma variável;
- `+` é a adição e `!=` significa "diferente de".

```
CADEIA senha
INTEIRO i

ESCREVA "Para continuar, digite sua senha: "
LEIA senha

i <- 0

ENQUANTO senha != "a6b5c4" FAÇA
  ESCREVA "Senha inválida"
  i <- i + 1
  ESCREVA "Para continuar, digite sua senha: "
  LEIA senha
FIM_ENQUANTO

ESCREVA "Seja bem-vindo(a) à área do cliente"
```

Uma cliente usa o programa e, após **7 tentativas** de digitar a senha, vê a mensagem de boas-vindas. Qual o valor de `i` no final?

<details>
<summary>Ver resposta</summary>

**i = 6.** A 7ª tentativa foi a certa, então ela errou 6 vezes. O primeiro `LEIA` fica fora do laço e não conta; `i` só aumenta dentro do laço, uma vez por senha errada.

</details>

> ⚠️ **Ajuste:** o original declarava `CARACTER senha`, mas a senha tem seis símbolos. Um caractere guarda um único símbolo; para texto, o tipo certo é cadeia (string).

## Questão 3

Sabendo que:

- `SE` divide o fluxo em dois: `ENTAO` roda se a condição for verdadeira e `SENAO` se for falsa;
- `/` é a divisão e `>` significa "maior que".

```
INTEIRO x1, x2
REAL res

ESCREVA "digite um número positivo"
LEIA x1
ESCREVA "digite outro número positivo"
LEIA x2

SE (x1 > x2) ENTAO FAÇA
  res <- (x1 - x2) / x1
SENAO FAÇA
  res <- (x2 - x1) / x2
FIM_SE

ESCREVA res
```

Qual a última linha impressa para os pares [x1, x2] = [3, 12], [5, 5] e [10, 8]?

<details>
<summary>Ver resposta</summary>

**0.75, 0.0 e 0.2**, respectivamente.

- [3, 12]: 3 > 12 é falso → (12 − 3) / 12 = 0.75.
- [5, 5]: 5 > 5 é falso → (5 − 5) / 5 = 0.0.
- [10, 8]: 10 > 8 é verdadeiro → (10 − 8) / 10 = 0.2.

</details>

> 💡 A resposta considera que a divisão dá um resultado real. Em Java, C e C++, dividir dois inteiros descarta a parte decimal: `9 / 12` dá 0. Para obter 0.75 seria preciso converter antes, como em `(double) (x2 - x1) / x2`.

## Questão 4

Sabendo que `<` significa "menor que":

```
INTEIRO x, i, t, e
REAL a

ESCREVA "Digite um número: "
LEIA x

i <- 0
t <- 0

ENQUANTO i < x FAÇA
  ESCREVA "Digite um número: "
  LEIA e
  t <- t + e
  i <- i + 1
FIM_ENQUANTO

a <- t / x

ESCREVA i, a
```

Qual a última linha impressa se o usuário digitar, nessa ordem, `5, 3, 4, 5, 4, 5`?

<details>
<summary>Ver resposta</summary>

**5 4.2**<br />O primeiro número (5) vai para x e define quantas vezes o laço roda. Os outros cinco são somados em t: 3 + 4 + 5 + 4 + 5 = 21. No fim, i = 5 e a = 21 / 5 = 4.2 (a média).

</details>

## Questão 5

`PARA` repete um bloco um número definido de vezes, com uma variável (`i`) que conta as iterações. `v(n)` e `u(n)` são vetores de tamanho n que guardam números reais.

```
INTEIRO i, n
REAL v(5), u(5)

v(1) <- 2.0
v(2) <- 3.0
v(3) <- 4.0
v(4) <- 5.0
v(5) <- 6.0

n <- 5

PARA i DE 1 ATÉ n FAÇA
  u(i) <- v(i) * i
FIM_PARA

ESCREVA u(2), u(4)
```

<details>
<summary>Ver resposta</summary>

**6.0 20.0**<br />u(2) = v(2) × 2 = 3.0 × 2 = 6.0; u(4) = v(4) × 4 = 5.0 × 4 = 20.0.

</details>

> 💡 Nesta notação o vetor começa no índice 1. Em Java, C e Python os índices começam em 0.

> ➡️ **Próximo passo:** guardar vários valores numa só variável com listas e arrays.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 | Sequência, entrada e saída |
| 2 | Laço enquanto e contador |
| 3 | Decisão se/senão e divisão |
| 4 | Laço com acumulador e média |
| 5 | Laço para e vetores |
