# Instruções lógicas

> 🗺️ **Nesta aula:** o que é uma instrução, os seis tipos de instrução (entrada, atribuição, cálculo, saída, decisão e repetição) e as instruções lógicas: condições com operadores relacionais, `se/senão` e operadores E, OU e NÃO.

## O que é uma instrução

Uma **instrução** é um comando que indica ao computador **uma ação elementar** a executar: guardar um valor, fazer uma conta, mostrar uma mensagem, testar uma condição.

Uma instrução sozinha raramente resolve um problema. É a **sequência** de instruções, na ordem certa, que forma um algoritmo. Por exemplo, para fritar um ovo:

1. Colocar óleo na frigideira.
2. Acender o fogo.
3. Quebrar o ovo na frigideira.
4. Esperar o ovo fritar.
5. Desligar o fogo.

Cada linha é uma instrução. Fora de ordem (quebrar o ovo antes de colocar a frigideira, por exemplo), o resultado não sai.

> Lembrando: as instruções sempre são executadas de cima para baixo, a menos que uma estrutura de decisão ou repetição mude esse fluxo.

## Tipos de instruções

| Tipo | O que faz | Pseudocódigo | Python |
| --- | --- | --- | --- |
| Entrada | Recebe um dado de fora | `Leia idade` | `idade = int(input())` |
| Atribuição | Guarda um valor em uma variável | `total <- 0` | `total = 0` |
| Cálculo | Faz uma operação | `total <- preco * qtd` | `total = preco * qtd` |
| Saída | Mostra um resultado | `Escreva total` | `print(total)` |
| Decisão | Escolhe um caminho | `Se ... então` | `if ...:` |
| Repetição | Repete um bloco | `Enquanto ... faça` | `while ...:` |

As três primeiras mudam dados. As duas últimas são as **instruções lógicas**, que controlam o fluxo do programa.

## Instruções lógicas

São instruções que **avaliam condições** (expressões que resultam em verdadeiro ou falso) e, com base nesse resultado, decidem o que executar.

### 1. Avaliação de condições

Uma condição compara valores usando **operadores relacionais**:

| Operador | Significado | Exemplo | Resultado |
| --- | --- | --- | --- |
| `==` | igual a | `5 == 5` | verdadeiro |
| `!=` | diferente de | `5 != 3` | verdadeiro |
| `>` | maior que | `2 > 7` | falso |
| `<` | menor que | `2 < 7` | verdadeiro |
| `>=` | maior ou igual | `18 >= 18` | verdadeiro |
| `<=` | menor ou igual | `20 <= 18` | falso |

Atenção: `=` é **atribuição** (guarda um valor) e `==` é **comparação** (pergunta se são iguais).

```python
idade = 20

if idade >= 18:
  # Executa este bloco somente se a idade for maior ou igual a 18
  print("Você é maior de idade.")
```

### 2. Tomada de decisão

Com `se ... senão` (`if ... else`), o programa escolhe **um entre dois caminhos**:

```python
saldo = 750
valor_compra = 1000

if saldo >= valor_compra:
  print("Compra realizada.")
else:
  print("Saldo insuficiente.")  # ← este bloco é executado
```

### 3. Operações lógicas combinadas

Para avaliar várias condições ao mesmo tempo, usamos **operadores lógicos**. Cada linguagem os escreve de um jeito:

| Operador | Pseudocódigo | Python | Java / C / JavaScript | Verdadeiro quando… |
| --- | --- | --- | --- | --- |
| E | `E` | `and` | `&&` | **as duas** condições são verdadeiras |
| OU | `OU` | `or` | `\|\|` | **pelo menos uma** é verdadeira |
| NÃO | `NÃO` | `not` | `!` | a condição é falsa (inverte o valor) |

```python
idade = 25
possui_carteira = True

if idade >= 18 and possui_carteira:
  # Executa somente se as DUAS condições forem verdadeiras
  print("Pode dirigir.")
else:
  print("Não pode dirigir.")
```

O mesmo teste em Java:

```java
public class Direcao {
  public static void main(String[] args) {
    int idade = 25;
    boolean possuiCarteira = true;

    if (idade >= 18 && possuiCarteira) {
      System.out.println("Pode dirigir.");
    } else {
      System.out.println("Não pode dirigir.");
    }
  }
}
```

A lógica é idêntica nas duas linguagens; só a escrita (sintaxe) muda.

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Instrução | uma ação elementar; a sequência de instruções forma o algoritmo |
| Tipos de instrução | entrada, atribuição, cálculo e saída mudam dados; decisão e repetição controlam o fluxo |
| Condição | expressão que resulta em verdadeiro ou falso (`>`, `<`, `>=`, `<=`, `==`, `!=`) |
| `=` × `==` | `=` guarda um valor; `==` compara |
| `se / senão` | escolhe um entre dois caminhos |
| E / OU / NÃO | `and` `or` `not` em Python; `&&` `\|\|` `!` em Java e C |

Os operadores são aprofundados (com tabela verdade e precedência) na página **Operadores e expressões**.
