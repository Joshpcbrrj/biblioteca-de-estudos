# Introdução à Lógica de Programação com Portugol Studio

**Ranking de linguagens (índice TIOBE)**

🔗 [https://www.tiobe.com/tiobe-index/](https://www.tiobe.com/tiobe-index/)

> 🗺️ **Nesta aula:** o que é lógica e lógica de programação, hardware e software, programa, linguagem (compilada e interpretada), algoritmo, o ciclo entrada → processamento → saída e os níveis de linguagem.

## O que é lógica?

É a ciência do raciocínio correto: organizar pensamentos numa sequência coerente, em que cada passo faz sentido a partir do anterior.

## O que é lógica de programação?

É a técnica de organizar instruções numa **sequência lógica** que leva a um objetivo e que depois pode ser escrita numa linguagem de programação. Aprender lógica vem antes de aprender uma linguagem: a linguagem muda, o raciocínio continua o mesmo.

## Hardware e software

- **Hardware** é a parte física do computador: CPU, memória RAM, HD/SSD, teclado, monitor.
- **Software** é a parte lógica: os programas, incluindo o sistema operacional. É aqui que a programação acontece.

O programador não manipula o hardware diretamente. O código que escrevemos é traduzido em instruções que o sistema operacional leva até o hardware.

![Usuário, software e hardware em camadas](img/i-hw-sw.svg)

## O que é um programa?

É um conjunto de instruções, escritas numa linguagem de programação, que o computador executa numa ordem definida para resolver um problema.

## O que é uma linguagem de programação?

É um conjunto de regras (vocabulário e sintaxe) para escrever algoritmos de forma precisa, sem as ambiguidades da língua falada. Depois de escrito, o código precisa virar código de máquina, o que acontece de duas formas:

- **Compilação**: um compilador traduz o programa inteiro antes de executar, gerando um arquivo executável.
- **Interpretação**: um interpretador traduz e executa uma instrução por vez, no momento da execução.

Qual das duas é usada depende da linguagem.

![Linguagem compilada x interpretada](img/i-compila.svg)

## O que é um algoritmo?

É o passo a passo lógico para resolver um problema: uma sequência de instruções ordenada, finita e sem ambiguidade. Quando escrito numa linguagem de programação, o algoritmo vira o **código-fonte** do programa.

A ordem das instruções é tão importante quanto as instruções em si. No exemplo abaixo os passos são praticamente os mesmos, mas só a sequência da esquerda funciona. A da direita está fora de ordem e tem passos ambíguos ("retire a lâmpada": qual delas?).

![Sequência lógica x sequência desordenada e ambígua](img/i-sequencia.svg)

## Modelo de processamento de dados

Todo programa segue o mesmo ciclo: recebe dados (**entrada**), trabalha sobre eles (**processamento**) e devolve um resultado (**saída**). Os dados também podem ser guardados para uso posterior (**armazenamento**).

![Entrada, processamento e saída](img/i-fluxo-dados.svg)

## Níveis de linguagem

![Do alto nível à linguagem de máquina](img/i-niveis.svg)

| Nível | Características | Exemplos |
| --- | --- | --- |
| Linguagem de máquina | A única que o processador entende diretamente: instruções em binário (0 e 1) | `10110000 01100001` |
| Baixo nível | Instruções próximas da máquina, com nomes curtos legíveis por humanos | Assembly |
| Alto nível | Instruções próximas da linguagem humana; precisam ser compiladas ou interpretadas | C#, Python, Java, PHP, Visual Basic, Lisp |

## 📌 Resumo

| Conceito | Em uma frase |
| --- | --- |
| Lógica de programação | Organizar instruções numa sequência que leva a um objetivo |
| Hardware / software | Parte física / parte lógica (programas e sistema operacional) |
| Programa | Instruções que o computador executa numa ordem definida |
| Compilação | Traduz o programa inteiro antes de executar |
| Interpretação | Traduz e executa uma instrução por vez |
| Algoritmo | Passo a passo ordenado, finito e sem ambiguidade |
| Entrada → processamento → saída | O ciclo que todo programa segue |
| Níveis de linguagem | Máquina (binário), baixo nível (Assembly), alto nível (Python, Java…) |
