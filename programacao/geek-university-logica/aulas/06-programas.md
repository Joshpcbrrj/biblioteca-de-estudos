# Programas

> 🗺️ **Nesta aula:** a diferença entre algoritmo e programa, como o código-fonte vira algo executável (compilação × interpretação) e os elementos de um programa: instruções, linguagem, objetivo, dados, execução, depuração e manutenção.

## Definição

Um **programa** é um algoritmo escrito em uma **linguagem de programação**, de forma que o computador consiga executá-lo.

- **Algoritmo** → a ideia da solução, em passos (pode estar no papel, em português).
- **Programa** → essa ideia traduzida para uma linguagem com regras rígidas de escrita (sintaxe), pronta para rodar.

Programas vão de uma calculadora de média até sistemas operacionais e jogos.

## Do código-fonte à execução

O código que escrevemos (o **código-fonte**) é texto. O processador só entende **código de máquina** (instruções binárias). Alguém precisa fazer essa tradução, e há duas formas principais:

|  | Compilação | Interpretação |
| --- | --- | --- |
| Como funciona | Um **compilador** traduz todo o código de uma vez e gera um arquivo executável | Um **interpretador** lê e executa o código aos poucos, a cada execução |
| Quando os erros de sintaxe aparecem | Na compilação, antes de rodar | Quando o interpretador chega no trecho com erro |
| Exemplo no curso | **C** (gera `.exe` com o GCC) | **Python** |

O **Java** usa um modelo misto: o `javac` compila o código para *bytecode* (arquivo `.class`), e a **JVM** executa esse bytecode em qualquer sistema operacional.

## Elementos que definem um programa

### Instruções

O programa é formado por uma sequência de instruções que dizem ao computador exatamente o que fazer: ler dados, calcular, decidir, repetir e mostrar resultados.

### Linguagem de programação

As instruções são escritas em uma linguagem com sintaxe própria (Python, Java, C, JavaScript…). A mesma lógica pode ser escrita em qualquer uma delas:

```python
print("Olá!")
```

```java
public class Ola {
  public static void main(String[] args) {
    System.out.println("Olá!");
  }
}
```

```c
#include <stdio.h>

int main(void) {
  printf("Olá!\n");
  return 0;
}
```

### Objetivo

Todo programa é feito para resolver um problema específico: um jogo, um aplicativo de cadastro, um site, um sistema operacional.

### Dados

Os programas manipulam dados: informações digitadas pelo usuário, lidas de arquivos, de bancos de dados ou de sensores. Esses dados ficam guardados em **variáveis** enquanto o programa roda.

### Execução

O computador segue as instruções passo a passo. A execução pode ser:

- **Interativa**: o usuário participa em tempo real (um aplicativo, um jogo).
- **Em lote** (*batch*): o programa roda sozinho, sem intervenção (um backup agendado, um relatório gerado à noite).

### Depuração

Durante o desenvolvimento, quase todo programa tem erros (*bugs*). **Depurar** (*debug*) é encontrar e corrigir esses erros. Há três tipos principais:

| Tipo de erro | O que é | Exemplo |
| --- | --- | --- |
| **De sintaxe** | O código quebra as regras da linguagem e nem chega a rodar | Esquecer um parêntese |
| **De execução** | O programa começa, mas para no meio | Dividir por zero, usar variável inexistente |
| **De lógica** | O programa roda, mas dá o resultado errado | Somar quando deveria multiplicar |

Os erros de lógica são os mais difíceis, porque não geram mensagem nenhuma: só aparecem testando o programa e conferindo os resultados.

### Manutenção

Depois de pronto, o programa continua mudando: corrigir bugs encontrados pelos usuários, adicionar recursos, melhorar o desempenho. Código claro e organizado é o que torna essa manutenção viável.

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Programa | algoritmo escrito em uma linguagem de programação, pronto para executar |
| Compilação | traduz tudo antes de rodar e gera um executável (C) |
| Interpretação | lê e executa o código a cada execução (Python) |
| Modelo misto | Java compila para bytecode e a JVM executa |
| Erro de sintaxe | quebra as regras da linguagem; nem roda |
| Erro de execução | começa a rodar e para no meio (divisão por zero, variável inexistente) |
| Erro de lógica | roda, mas dá resultado errado; só aparece testando |
