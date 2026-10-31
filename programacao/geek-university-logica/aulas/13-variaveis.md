# Variáveis

> 🗺️ **Nesta aula:** o que é uma variável, declaração, atribuição e inicialização nas três linguagens, a diferença entre tipagem estática e dinâmica e as regras para dar bons nomes.

## Definição

Uma **variável** é um espaço na **memória** do computador, identificado por um **nome**, onde o programa guarda um valor que **pode mudar** durante a execução.

Uma analogia comum é uma caixa com etiqueta: a etiqueta é o **nome**, o formato da caixa é o **tipo** (o que cabe nela) e o conteúdo é o **valor**. O conteúdo pode ser trocado, mas a caixa guarda um valor por vez: ao guardar um novo, o anterior é perdido.

Toda variável tem:

| Elemento | Exemplo | Descrição |
| --- | --- | --- |
| Nome | `idade` | Como o programa se refere a ela |
| Tipo | inteiro | Que tipo de valor ela aceita |
| Valor | `30` | O conteúdo atual (pode ser alterado) |

## Declaração e atribuição

- **Declarar** é criar a variável (reservar o espaço e dar o nome).
- **Atribuir** é guardar um valor nela.
- **Inicializar** é a primeira atribuição.

```
// Pseudocódigo
Declare idade: Inteiro
idade <- 30
idade <- idade + 1  // agora vale 31: o valor antigo foi substituído
```

```java
// Java: o tipo é declarado e não muda
public class Variaveis {
  public static void main(String[] args) {
    int idade = 30;
    idade = idade + 1;
    System.out.println(idade); // 31

    // idade = "trinta"; // ❌ erro de compilação: o tipo é int
  }
}
```

```c
// C: o tipo é declarado e não muda
#include <stdio.h>

int main(void) {
  int idade = 30;
  idade = idade + 1;
  printf("%d\n", idade); // 31
  return 0;
}
```

```python
# Python: não se declara o tipo; ele vem do valor
idade = 30
idade = idade + 1
print(idade)  # 31

idade = "trinta"  # permitido: agora a variável guarda um texto
print(type(idade))  # <class 'str'>
```

> ⚠️ Em C, uma variável declarada sem valor inicial (`int x;`) contém "lixo": o que estava antes naquele espaço de memória. Sempre inicialize antes de usar.

## Tipagem estática × dinâmica

|  | Tipagem estática | Tipagem dinâmica |
| --- | --- | --- |
| O tipo pertence a… | À **variável** (definido na declaração) | Ao **valor** guardado no momento |
| Pode trocar de tipo? | Não | Sim |
| Quando o erro de tipo aparece | Na compilação | Durante a execução |
| Linguagens do curso | **Java**, **C** | **Python** (e também JavaScript) |

Mesmo em linguagens dinâmicas, trocar o tipo de uma variável no meio do programa costuma ser má prática: dificulta a leitura e gera bugs. O ideal é que cada variável guarde sempre o mesmo tipo de informação.

## Princípios para nomear variáveis

1. **Use nomes descritivos.** `contadorDeTentativas = 10` em vez de `x = 10`.
2. **Siga a convenção da linguagem:**
  - Java e JavaScript: **camelCase** → `tempoDeEspera`.
  - Python e C: **snake_case** → `tempo_de_espera`.
3. **Seja conciso e descritivo.** `precoTotal` em vez de `p` ou de `oPrecoTotalDaCompraDoCliente`.
4. **Evite nomes genéricos** como `valor`, `dados` ou `temp`, exceto em trechos muito curtos e óbvios.
5. **Use comentários só quando o nome não bastar.** O nome deve explicar a variável; o comentário reforça um detalhe (unidade, origem do valor), não substitui um nome ruim.
6. **Não use palavras reservadas** (`int`, `class`, `if`, `for`…).
7. **Regras obrigatórias** (valem nas três linguagens): começar com letra ou `_`, nunca com número; sem espaços; sem acentos (alguns compiladores aceitam, mas evite). Maiúsculas e minúsculas são diferentes: `idade` e `Idade` são variáveis distintas.

## Exemplos de variáveis por tipo de valor

**Numérica**

```
idadeDoUsuario <- 30
saldoBancario <- 1000.50
```

**Texto**

```
nomeDoCliente <- "João Silva"
mensagemDeBoasVindas <- "Olá, bem-vindo!"
```

**Booleana**

```
ativo <- verdadeiro
pago <- falso
```

**Lista (array)**: uma variável que guarda vários valores, acessados pela posição (índice), que começa em 0.

```python
notas_dos_alunos = [8.5, 7.0, 9.2, 6.5, 8.0]

print(notas_dos_alunos[0])  # 8.5 → primeira nota
print(len(notas_dos_alunos))  # 5  → quantidade de notas
```

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Variável | espaço na memória com nome, tipo e valor que pode mudar |
| Guarda um valor por vez | ao atribuir um novo valor, o anterior se perde |
| Declarar / atribuir / inicializar | criar / guardar um valor / primeira atribuição |
| Tipagem estática (Java, C) | o tipo pertence à variável e não muda; erros aparecem na compilação |
| Tipagem dinâmica (Python) | o tipo vem do valor guardado; pode mudar, mas evite |
| C sem inicializar | a variável contém "lixo" de memória |
| Nomes | camelCase em Java · snake_case em Python e C · nunca começar com número |
