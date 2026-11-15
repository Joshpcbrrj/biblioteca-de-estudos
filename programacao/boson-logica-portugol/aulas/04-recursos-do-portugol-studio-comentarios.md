# Recursos do Portugol Studio: comentários, caracteres especiais e depuração (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** comentários, caracteres especiais dentro de textos (`\n`, `\t`, `\"`), o comando `limpa()` e como depurar um programa passo a passo.

## De onde paramos

O Portugol Studio já está aberto. Antes de escrever programas maiores, vale conhecer quatro recursos que aparecem no curso inteiro: comentários, caracteres especiais, a limpeza do console e a depuração.

## Comentários

Comentários são textos que o programa ignora na execução. Servem para explicar o código para quem vai lê-lo, inclusive você mesmo daqui a alguns meses.

```c
// comentário de uma linha: vai do //
// até o fim da linha

/* comentário de várias linhas:
   tudo entre a barra-asterisco e o
   asterisco-barra é ignorado */

// a idade vem do cadastro e não muda aqui
inteiro idade = 30
```

> 💡 Um bom comentário explica o **porquê**, não o óbvio. `// soma 1 em i` não ajuda; `// pula o cabeçalho, que está na posição 0` ajuda. Comentários também servem para desativar uma linha temporariamente sem apagá-la.

Ao salvar um arquivo, o Portugol Studio acrescenta no final um bloco `/* $$$ Portugol Studio $$$ ... */` com informações do editor (posição do cursor, trechos dobrados). É um comentário comum e pode ser ignorado.

## Caracteres especiais em textos

Dentro de uma `cadeia`, a barra invertida `\` indica um caractere especial: o que vem logo depois dela não é escrito literalmente.

![Caracteres especiais dentro de textos; em verde, o que aparece na tela](../img/ps-escapes.svg)

> 💡 **Analogia:** a barra invertida é como as aspas de "fala do narrador" num roteiro de teatro. O ator não lê em voz alta "(pausa)" ou "(muda de linha)"; ele executa a instrução. Do mesmo jeito, `\n` não aparece na tela: ele manda o texto pular de linha.

O `\t` (tabulação) é o jeito mais simples de alinhar colunas, como nas tabelas e matrizes do curso:

```c
// \t empurra até a próxima "coluna" fixa,
// por isso os números ficam alinhados
escreva("Produto\tQtd\n")
escreva("Arroz\t10\n")
escreva("Feijão\t25\n")
```

## Limpando o console: limpa()

O comando `limpa()` apaga tudo o que já foi escrito no console. Os usos mais comuns no curso:

- esconder um dado, como o número secreto do jogo de adivinhação ou o voto na urna eletrônica;
- mostrar o resultado numa tela limpa, depois de várias perguntas.

```c
escreva("Jogador 1, digite o número secreto: ")
leia(secreto)
// apaga a tela para o jogador 2 não ver
// o número que acabou de ser digitado
limpa()
```

## Depuração: executando passo a passo

![Depurar: uma linha de cada vez, com as variáveis à vista](../img/bo-depuracao.svg)

> 💡 **Analogia:** depurar é como assistir à reprise de um lance de futebol em câmera lenta, quadro a quadro. Na velocidade normal você só vê que deu errado; em câmera lenta você vê exatamente em qual movimento a jogada se perdeu. O inspetor de variáveis é o placar ao lado da tela, atualizado a cada quadro.

Quando o programa não dá o resultado esperado, a ferramenta de depuração do Portugol Studio deixa você acompanhar a execução linha por linha. É a versão automática do **teste de mesa**.

1. Em vez de **Executar** (Shift + F6), use o botão **Depurar**, ao lado dele na barra de ferramentas.
2. O programa para na primeira linha, que fica destacada. Cada clique em **Depurar** executa a próxima instrução.
3. Para acompanhar valores, arraste variáveis para o **Inspetor de variáveis**, o painel lateral do editor. O valor de cada uma é atualizado a cada passo.
4. Para pular direto até um trecho, clique ao lado do número da linha para criar um **ponto de parada**; a execução para quando chega nele.

> ⚠️ Os nomes dos botões e painéis podem variar um pouco entre versões do Portugol Studio, e o Portugol Webstudio (no navegador) tem menos recursos de depuração. A ideia é a mesma: executar aos poucos e observar as variáveis.

## 🧠 Revisão rápida

**O que aparece na tela com `escreva("A\tB")`?**

A letra A, um espaço de tabulação e a letra B. O `\t` não é escrito, ele é executado.

**Qual a diferença entre um bom e um mau comentário?**

O bom explica o porquê do código; o mau repete o que o próprio código já diz.

**Para que serve um ponto de parada?**

Para a execução parar numa linha escolhida, sem precisar avançar passo a passo desde o início.

> ➡️ **Próximo passo:** fim da seção de fundamentos. A próxima seção começa pelo que todo programa manipula: **O que são Tipos de Dados em Lógica de Programação**.

## 📌 Resumo

| Recurso | Para que serve |
| --- | --- |
| `// texto` | Comentário de uma linha |
| `/* texto */` | Comentário de várias linhas |
| `\n` | Quebra de linha dentro do texto |
| `\t` | Tabulação, para alinhar colunas |
| `\"` e `\\` | Aspas e barra invertida dentro do texto |
| `limpa()` | Apaga o console |
| Depurar | Executa uma instrução por vez e mostra as variáveis |
| Ponto de parada | Faz a execução parar numa linha escolhida |

## 🧭 Cheat sheet da seção

![Cheat sheet da seção de fundamentos: 12 cards para revisar lógica, algoritmo e o Portugol Studio.](../img/bo-mapa-fundamentos.svg)
