# Como as linguagens de programação funcionam

> 🗺️ **Nesta aula:** o que forma uma linguagem de programação e as três camadas de regras (léxica, sintática e semântica) que o computador confere antes de executar seu código.

## 🧭 Cheat sheet da seção

Antes de começar, veja o mapa do módulo: é o que as próximas aulas vão explicar. Volte a ele no fim para revisar.

![Mapa mental para revisar o módulo II](../img/st-mapa-02.svg)

## De onde paramos

No módulo I você viu que o computador só executa linguagem de máquina e que existem linguagens de alto nível mais próximas de nós. Agora vamos olhar para dentro dessas linguagens: do que são feitas e como o computador decide se o que você escreveu é válido.

## O que é uma linguagem de programação?

**Uma linguagem de programação é uma linguagem formal, com regras rígidas, usada para escrever algoritmos que um computador consegue executar.**

O que o programador escreve é o **código-fonte**. Um **compilador** ou **interpretador** traduz esse código em instruções de máquina. Toda linguagem oferece:

- **palavras-chave** (`if`, `while`, `function`, `return`);
- **operadores** (`+`, `==`, `&&`);
- **estruturas de controle** (decisões e repetições);
- **tipos de dados** (números, textos, listas);
- **bibliotecas** prontas para tarefas comuns (datas, rede, arquivos).

Exemplos populares: C, C++, Java, C#, Python, JavaScript, Go, Rust, PHP, Ruby, Swift e Kotlin.

## As 3 camadas de uma linguagem

Para um programa ser aceito, ele precisa passar por três filtros, do mais simples ao mais profundo. O primeiro é o **léxico**: as palavras e símbolos usados existem na linguagem? O segundo é o **sintático**: essas palavras estão dispostas numa ordem válida? O terceiro é o **semântico**: a frase faz sentido e faz o que você pretendia? Em português, “gato” passa no léxico, “O gato bebe” passa no sintático e “O gato bebe a mesa” passa nos dois, mas falha no semântico. O computador consegue conferir bem os dois primeiros filtros; o terceiro depende de você e dos seus testes.

Assim como o português tem vocabulário, gramática e significado, toda linguagem de programação tem três camadas de regras:

![A mesma linha de código analisada nas camadas léxica, sintática e semântica.](../img/ling-3-camadas.svg)

> 💡 **Analogia:** "Gato o mesa em subiu" tem palavras válidas (léxica ok), mas gramática errada. "A mesa comeu o gato" tem gramática perfeita, mas não faz sentido (erro semântico). O compilador confere seu código nessas mesmas três camadas, na mesma ordem.

### 1. Léxica: as "palavras" válidas

Define quais sequências de caracteres formam **tokens** válidos: identificadores, números, operadores e palavras-chave.

```jsx
// em JS, ç é permitido em identificadores,
// então este token é válido
let preço = 10;
// ✖ identificador não pode começar com número:
// o leitor de tokens acharia que "2" é um número
let 2total = 5;
```

### 2. Sintática: a gramática

Define como os tokens podem ser combinados, ou seja, a **estrutura** das frases. O resultado é uma árvore sintática (AST).

```jsx
// ✖ erro de sintaxe: falta fechar o parêntese,
// e o compilador não sabe onde a condição acaba
if (idade >= 18 {
  console.log("maior");
}
```

### 3. Semântica: o significado

Mesmo com a gramática correta, a frase precisa **fazer sentido**: a variável existe? os tipos combinam? a função recebe esses argumentos?

```jsx
// ✖ ReferenceError se 'preco' não foi declarada:
// a frase é válida, mas fala de algo inexistente
const total = preco * 2;
// NaN: sintaxe ok, mas multiplicar texto
// por número não tem significado útil
const x = "abc" * 2;
```

## Erro em tempo de compilação × em tempo de execução

O momento em que o erro aparece muda o tamanho do estrago. O erro de **compilação** (ou de sintaxe) é detectado **antes** de o programa rodar, como um parêntese esquecido, e o programa nem inicia: é o erro mais fácil de resolver, porque a mensagem aponta a linha. O erro de **execução** aparece **durante** o uso, como dividir por zero ou acessar uma posição que não existe, e pode surgir só com certos dados, quando o usuário já está usando o sistema. Há ainda o erro de **lógica**, o mais difícil: o programa roda sem reclamar, mas dá a resposta errada. Esse só é achado com testes e teste de mesa.

- Erros **léxicos e sintáticos** são encontrados **antes** de rodar: o editor sublinha e o programa nem começa.
- Muitos erros **semânticos** só aparecem **durante a execução**, quando aquela linha roda (como o `ReferenceError` acima).
- O pior tipo é o **erro de lógica**: o programa roda sem reclamar, mas faz a coisa errada (ex.: usar `+` em vez de `-`). Só testes encontram esse erro.

## 🧠 Revisão rápida

**`let 2total = 5;` quebra qual regra?**

A léxica: um identificador não pode começar com número.

**Um código com a gramática perfeita pode estar errado?**

Sim: pode ter erro semântico (variável inexistente, tipos incompatíveis) ou de lógica.

**O que é o código-fonte?**

O texto do programa escrito pelo programador, antes de ser traduzido para a máquina.

> ➡️ **Próximo passo:** quem confere essas camadas e traduz o código é um compilador ou um interpretador. A diferença entre eles está em **Tipos de linguagens**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Código-fonte | o texto que o programador escreve |
| Léxica | quais tokens são válidos |
| Sintática | como os tokens se combinam (gramática) |
| Semântica | se a frase faz sentido |
| Erro de lógica | roda, mas faz a coisa errada |
