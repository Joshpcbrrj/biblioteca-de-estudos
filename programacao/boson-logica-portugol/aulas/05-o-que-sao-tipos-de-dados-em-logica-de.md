# O que são Tipos de Dados em Lógica de Programação

> 🗺️ **Nesta aula:** o que são dados, por que cada dado tem um tipo, os tipos primitivos (numéricos, caracteres e texto, lógicos) e os compostos, e as palavras de cada tipo no Portugol.

## 🧭 Cheat sheet da seção

Antes de começar, veja o mapa da seção: é o que as próximas aulas vão explicar. Volte a ele no fim para revisar.

![Cheat sheet da seção: 12 cards para revisar variáveis, tipos, entrada e saída e operadores](../img/bo-mapa-variaveis.svg)

## De onde paramos

A primeira seção mostrou o ciclo entrada → processamento → saída. Esta seção trata do que circula nesse ciclo: os **dados**. Antes de guardá-los em variáveis, é preciso saber de que tipo cada um é.

## O que são dados

Dado é qualquer fato que pode ser observado ou medido e depois guardado: uma idade, um nome, uma temperatura, a resposta "sim" ou "não". Para o computador, dados são a matéria-prima que o programa recebe, processa e transforma em informação.

## Tipos de dados

Cada dado tem um **tipo**, que diz ao computador quanto espaço reservar na memória e que operações são permitidas com ele (dá para somar números, mas não nomes).

![Tipos de dados no Portugol, com exemplos de valor](../img/t-tipos.svg)

> 💡 **Analogia:** os tipos são como as embalagens do supermercado. Leite vai na caixa de leite, ovos vão na cartela de ovos, e ninguém tenta guardar ovos na caixa de leite. Cada embalagem tem o tamanho certo para o que guarda e diz como você pode usar o conteúdo: dá para despejar o leite, não os ovos. Do mesmo jeito, o tipo diz quanto espaço reservar e que operações fazem sentido.

### Numéricos (tipo primitivo)

Números usados diretamente em cálculos. Dividem-se em dois tipos:

- **Inteiro** (`int`): números sem casa decimal, positivos ou negativos. Ex.: `5`, `-90`, `0`.
- **Real** (`float`): números com casas decimais, positivos ou negativos. Ex.: `5.0`, `-45.23`, `0.333`.

No código, a casa decimal é separada por **ponto**, não por vírgula: `7.5`, e não `7,5`.

### Caracteres e texto (tipo primitivo)

Letras, dígitos e símbolos tratados como texto. Não servem para cálculos, mesmo quando são dígitos: `"10"` é um texto, não o número dez.

- **Caractere** (`char`): um único símbolo, entre aspas simples. Ex.: `'A'`, `'7'`, `'#'`.
- **Cadeia** (`string`): sequência de caracteres (palavra ou frase), entre aspas duplas. Ex.: `"Olá, mundo"`.

### Lógicos (tipo primitivo)

Também chamados de booleanos. Só podem ter dois valores: **verdadeiro** ou **falso** (em muitas linguagens, `true`/`false`, representados internamente por 1 e 0). São o resultado de comparações e controlam as decisões do programa.

### Compostos (ou de referência)

São formados pela combinação de vários dados, primitivos ou compostos. Exemplos que aparecem mais adiante no curso: **vetores** e **matrizes**, que guardam vários valores sob um mesmo nome.

> ⚠️ **Armadilha comum:** guardar um telefone ou um CEP como número. Eles parecem números, mas ninguém soma telefones, e o zero da frente sumiria (`021` viraria `21`). Dado que não entra em conta é texto: use `cadeia`.

## 🧠 Revisão rápida

**`"10"` e `10` são a mesma coisa?**

Não: `"10"` é uma cadeia (texto) e não entra em contas; `10` é um número inteiro.

**Qual tipo usar para o preço de um produto, como 19.90?**

`real`, porque tem casas decimais.

**Quais valores um dado lógico pode ter?**

Só dois: `verdadeiro` ou `falso`.

> ➡️ **Próximo passo:** com o tipo escolhido, falta um lugar na memória para guardar o dado: **Declaração e Atribuição de Variáveis em Lógica de Programação**.

## 📌 Resumo: os tipos no Portugol

| Tipo | Palavra no Portugol | Exemplo de valor |
| --- | --- | --- |
| Inteiro | `inteiro` | `32` |
| Real | `real` | `7.5` |
| Caractere | `caracter` | `'x'` |
| Cadeia (texto) | `cadeia` | `"Ana"` |
| Lógico | `logico` | `verdadeiro` / `falso` |
