# Tipos de dados

> 🗺️ **Nesta aula:** o que um tipo de dado define, a tabela de equivalência entre pseudocódigo, Java, C e Python, e cada tipo em detalhe: inteiros (e overflow), reais (e imprecisão), caracteres, strings, booleanos, enums, classes, arrays e referências/ponteiros.

## O que é um tipo de dado

O **tipo de dado** define:

- **que valores** uma variável pode guardar (números inteiros, texto, verdadeiro/falso…);
- **que operações** podem ser feitas com eles (somar números faz sentido; somar dois booleanos, não);
- em linguagens como Java e C, **quanta memória** a variável ocupa.

Os tipos básicos (inteiro, real, caractere, lógico) existem em praticamente todas as linguagens, com nomes diferentes. Cada linguagem também tem tipos próprios.

## Resumo: os tipos nas linguagens do curso

| Conceito | Pseudocódigo | Java | C | Python |
| --- | --- | --- | --- | --- |
| Inteiro | `Inteiro` | `int`, `long` | `int`, `long` | `int` |
| Real (decimal) | `Real` | `double`, `float` | `double`, `float` | `float` |
| Caractere | `Caractere` | `char` | `char` | (não existe: usa string de 1 letra) |
| Texto | `Caractere`/`Literal` | `String` | `char[]` (vetor de caracteres) | `str` |
| Lógico | `Lógico` | `boolean` | `bool` (com `stdbool.h`) ou `int` | `bool` |

## Tipos de dados mais comuns (exemplos em Java)

### Inteiros

Números sem casas decimais, positivos ou negativos. Java tem quatro tamanhos:

| Tipo | Tamanho | Faixa aproximada |
| --- | --- | --- |
| `byte` | 1 byte | -128 a 127 |
| `short` | 2 bytes | -32 mil a 32 mil |
| `int` | 4 bytes | -2,1 bilhões a 2,1 bilhões |
| `long` | 8 bytes | ± 9,2 quintilhões |

```java
int numeroInteiro = 42;
long populacaoMundial = 8_100_000_000L; // não cabe em int; o L indica long
```

Se uma conta ultrapassa o limite do tipo, ocorre **overflow**: o valor "dá a volta" e vira negativo, sem aviso.

```java
int maximo = Integer.MAX_VALUE; // 2147483647
System.out.println(maximo + 1); // -2147483648
```

**Divisão entre inteiros descarta a parte decimal:** `7 / 2` resulta em `3`, não em `3.5`.

### Ponto flutuante (reais)

Números com casas decimais. Use `double` (8 bytes, cerca de 15 dígitos de precisão) por padrão; `float` (4 bytes) tem menos precisão e exige o sufixo `f`.

```java
double numeroReal = 3.14159;
float outroReal = 3.14f;

System.out.println(7 / 2);  // 3  → divisão de inteiros
System.out.println(7.0 / 2);  // 3.5 → um dos operandos é real
System.out.println(0.1 + 0.2); // 0.30000000000000004
```

O último resultado não é bug do Java: números reais são guardados em binário e alguns decimais (como 0,1) não têm representação exata. Por isso, valores em dinheiro em sistemas reais costumam usar tipos próprios, como `BigDecimal` em Java.

### Caracteres

O tipo `char` guarda **um único caractere**, entre **aspas simples**. Internamente, é um número (o código do caractere na tabela Unicode).

```java
char letra = 'A';
System.out.println((int) letra); // 65 → código do 'A'
```

### Cadeias de caracteres (strings)

Texto com zero ou mais caracteres, entre **aspas duplas**. Em Java, `String` não é um tipo primitivo: é uma **classe**, por isso começa com letra maiúscula e tem métodos.

```java
String nome = "João Silva";
System.out.println(nome.length());  // 10 → quantidade de caracteres
System.out.println(nome.toUpperCase()); // JOÃO SILVA
```

`'A'` (char) e `"A"` (String) são tipos diferentes.

### Booleanos

Apenas dois valores possíveis: `true` (verdadeiro) ou `false` (falso). São o resultado de toda comparação e o que controla `if` e laços.

```java
boolean estaChovendo = true;
boolean maiorDeIdade = 20 >= 18; // true
```

### Enumerados

Um `enum` define um tipo com um **conjunto fixo de valores** possíveis, evitando erros de digitação e valores inválidos.

```java
enum DiaDaSemana {
  SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO, DOMINGO
}

DiaDaSemana diaAtual = DiaDaSemana.TERCA;
```

### Estruturas de dados complexas (classes)

Quando os tipos básicos não bastam, é possível criar um tipo próprio agrupando vários dados. Em Java, isso é feito com uma **classe**:

```java
class Pessoa {
  String nome;
  int idade;

  Pessoa(String nome, int idade) {
    this.nome = nome;
    this.idade = idade;
  }
}

Pessoa pessoa1 = new Pessoa("Maria", 30);
System.out.println(pessoa1.nome + " tem " + pessoa1.idade + " anos.");
```

(Em C, o equivalente é a `struct`; em Python, também se usa `class`.)

### Arrays (vetores)

Um array guarda **vários valores do mesmo tipo** em sequência, acessados pelo **índice**, que começa em 0. Em Java e C, o tamanho é fixo depois de criado.

```java
int[] numeros = {1, 2, 3, 4, 5};

System.out.println(numeros[0]);  // 1 → primeiro elemento
System.out.println(numeros.length);  // 5 → tamanho
// numeros[5] → ❌ ArrayIndexOutOfBoundsException (o último índice é 4)
```

### Apontadores (referências em Java)

Em Java, existem dois grupos de tipos:

- **Primitivos** (`int`, `double`, `char`, `boolean`…): a variável guarda **o próprio valor**.
- **Referência** (objetos, `String`, arrays): a variável guarda **o endereço** de onde o objeto está na memória.

Na prática, isso muda o que acontece ao copiar uma variável:

```java
int a = 10;
int b = a;  // copia o VALOR
b = 20;
System.out.println(a); // 10 → a não mudou

int[] lista1 = {1, 2, 3};
int[] lista2 = lista1;  // copia o ENDEREÇO: as duas apontam para o mesmo array
lista2[0] = 99;
System.out.println(lista1[0]); // 99 → lista1 também "mudou"
```

Em **C**, esse conceito é explícito: um **ponteiro** é uma variável que guarda um endereço de memória.

```c
#include <stdio.h>

int main(void) {
  int idade = 30;
  int *ponteiro = &idade; // & obtém o endereço de "idade"

  *ponteiro = 31;  // * acessa o valor no endereço apontado
  printf("%d\n", idade);  // 31 → alterado através do ponteiro
  return 0;
}
```

> Esses são os tipos mais usados, mas cada linguagem tem outros (por exemplo, `None` em Python e `null` em Java para "ausência de valor").

## 📌 Resumo da aula

| Tipo | Guarda | Armadilha |
| --- | --- | --- |
| Inteiro (`int`, `long`) | números sem casas decimais | overflow: passou do limite, "dá a volta"; `7 / 2` entre inteiros dá `3` |
| Real (`double`, `float`) | números com casas decimais | `0.1 + 0.2` ≠ `0.3` exato; para dinheiro, use tipos próprios |
| Caractere (`char`) | um caractere, aspas simples | `'A'` é diferente de `"A"` |
| Texto (`String`, `str`) | sequência de caracteres, aspas duplas | em Java é classe, não primitivo |
| Lógico (`boolean`, `bool`) | verdadeiro ou falso | resultado de toda comparação |
| Enum | um valor de uma lista fixa | só aceita os valores declarados |
| Array | vários valores do mesmo tipo, por índice | índice começa em 0; último é `tamanho - 1` |
| Referência / ponteiro | endereço de memória | copiar a variável copia o endereço, não o objeto |
