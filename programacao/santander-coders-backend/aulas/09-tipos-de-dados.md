# Tipos de dados

> 🗺️ **Nesta aula:** os principais tipos de dados, a diferença entre variável e constante e um algoritmo de soma corrigido.

## De onde paramos

Na aula anterior o algoritmo recebia um nome e mostrava um cumprimento. Para guardar esse nome foi preciso uma **variável**, e toda variável tem um **tipo**.

## Os principais tipos de dados

O tipo diz que espécie de valor cabe na variável e quais operações fazem sentido com ele (somar números, juntar textos...). Os nomes mudam de linguagem para linguagem, mas a ideia é a mesma.

| Tipo | O que guarda | Exemplos |
| --- | --- | --- |
| Inteiro (`int`) | números sem parte decimal | -10, 0, 42 |
| Real (`float`, `double`) | números com parte decimal | 3.14, -0.5 |
| Caractere (`char`) | um único símbolo | 'a', '9', '$' |
| Texto (`string`) | sequência de caracteres | "Olá, mundo!" |
| Lógico (`bool`) | verdadeiro ou falso | true, false |

> 💡 Algumas linguagens, como Python e JavaScript, não têm um tipo caractere separado: uma letra sozinha é um texto de tamanho 1. Java tem `char` (aspas simples) e `String` (aspas duplas).

Além desses tipos **primitivos**, existem tipos que **agrupam** valores, estudados mais adiante:

- **Arrays (vetores)**: quantidade fixa de elementos do mesmo tipo. Ex.: `int[] numeros = {1, 2, 3, 4};` em Java.
- **Listas**: coleções que crescem e diminuem. Ex.: `[1, 2, 3, 4]`.
- **Registros e classes**: vários campos com tipos próprios. Ex.: uma Pessoa com nome (texto) e idade (inteiro).
- **Ponteiros e referências**: guardam o endereço de outro valor na memória, em vez do valor em si.
- **Tipos definidos pelo usuário**: classes e estruturas criadas por você (tema do módulo de POO).

## Variáveis e constantes

Uma **variável** é um espaço de memória com nome, que guarda um valor que pode mudar durante a execução. Você a declara, dá um valor inicial e pode alterá-lo quantas vezes quiser.<br />Uma **constante** também tem nome e valor, mas o valor é fixo: definido uma vez, não muda mais. Use para valores que não devem ser alterados por engano, como π, a taxa de um imposto ou o limite de tentativas de senha.

```
var saldo: real
const TAXA_SAQUE: real = 2.50

definir 100 -> saldo
// pode: a variável muda
definir saldo - TAXA_SAQUE -> saldo
// erro: constante não muda
definir 3.00 -> TAXA_SAQUE
```

> 💡 Java e C# são linguagens de **tipagem estática**: o tipo é declarado e não muda. JavaScript e Python têm **tipagem dinâmica**: a mesma variável pode guardar um número e depois um texto.

## Exemplo: algoritmo de soma

```
inicio principal
  var n1: inteiro
  var n2: inteiro
  var resultado: inteiro

  definir 0 -> n1
  definir 0 -> n2

  mostrar "Digite o primeiro número: "
  esperar_digitacao -> n1
  mostrar "Digite o segundo número: "
  esperar_digitacao -> n2

  somar n1, n2 -> resultado
  mostrar resultado
fim
```

> ⚠️ **Correção:** o original tinha `definir 0 -> n1` duas vezes; a segunda linha deveria inicializar `n2`. Aqui não muda o resultado, porque n2 recebe o valor digitado logo depois, mas em outros programas uma variável sem valor inicial causa erro.

## 📝 Exercício

Qual tipo você usaria para cada dado? (a) quantidade de alunos; (b) preço de um produto; (c) se o cliente é VIP; (d) o CPF.

<details>
<summary>Ver resposta</summary>

(a) inteiro; (b) real; (c) lógico; (d) texto: apesar de ter dígitos, o CPF não entra em contas e pode começar com zero, que um inteiro perderia.

</details>

## 🧠 Revisão rápida

**Qual a diferença entre variável e constante?**

A variável pode mudar de valor durante a execução; a constante é fixa.

**Por que "42" e 42 são diferentes?**

O primeiro é texto e o segundo é inteiro: "4" + "2" junta textos, 4 + 2 soma números.

> ➡️ **Próximo passo:** fazer o algoritmo tomar decisões com se/senão.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Tipo de dado | Define que valores a variável aceita e que operações valem. |
| Primitivos | Inteiro, real, caractere, texto e lógico. |
| Variável | Espaço de memória com nome cujo valor pode mudar. |
| Constante | Valor com nome que não muda depois de definido. |
