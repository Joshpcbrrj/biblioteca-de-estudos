# Sobre o curso

**Udemy: Aprenda Lógica de Programação (Direto ao ponto) - Intellectuale Tecnologia e Treinamento**

Prof. Eduardo Casavella, Intellectuale Tecnologia e Treinamento.

> 🗺️ **Sobre o curso:** lógica de programação direto ao ponto, usando o Flowgorithm para montar e executar fluxogramas. O caminho vai dos conceitos (algoritmo, fluxograma, pseudocódigo) a variáveis e operações, decisões, operadores lógicos, laços de repetição, vetores e, por fim, funções e recursão. Cada aula traz projetos com fluxograma e pseudocódigo.

> 🧭 **Como usar este material:** as páginas seguem a ordem do curso; cada uma começa com a explicação do assunto e exemplos curtos e termina com os projetos da aula. Quando o código original tinha algum erro, a versão foi revisada e um trecho **"O que mudou"** explica a correção.

> 🔖 **Legenda**
>
> - 🗺️ **Nesta aula**: o que a página cobre, logo no início
> - 📌 **Resumo**: tabela de revisão, no final
> - ⚠️ atenção a um erro comum ou detalhe importante
> - 💡 dica ou observação importante
> - 📝 exercícios: as respostas ficam recolhidas em **Ver resposta**; tente resolver antes de abrir

## Seções

### 1. Conceitos básicos e ambiente de trabalho

O que é lógica, algoritmo, fluxograma e pseudocódigo; instalação do Flowgorithm; variáveis, tipos de dados e os comandos da ferramenta.

- Definições importantes/ Instalando o flowgorithm
- Detalhando ambiente de trabalho/ tipo de dados/ pseudocódigo

### 2. Operações básicas

Operadores aritméticos, resto da divisão, precedência, inteiro × real e porcentagem.

- Estudo de operações básicas

### 3. Estruturas de decisão

Operadores relacionais, `If` simples, composto e encadeado; operadores lógicos E, OU e NÃO.

- Estudo de estrutura de decisão
- Estudo de operadores lógicos

### 4. Estruturas de repetição

Laços `For`, `While` e `Do`, contadores, acumuladores e validação de entrada.

- Estudo das estruturas de repetição

### 5. Arranjos de dados

Vetores: declarar, preencher, percorrer, maior valor, busca, vetores paralelos.

- Estudo de vetores

### 6. Sub-rotinas e funções

Funções e procedimentos, parâmetros, retorno, escopo e recursão.

- Estudo de sub programas

## 📌 Resumo do curso

| Seção | Ideia central | Comandos-chave |
| --- | --- | --- |
| Conceitos | Algoritmo é uma sequência finita e ordenada de passos | fluxograma, pseudocódigo |
| Variáveis e operações | Dados têm tipo; contas seguem a precedência | `Declare`, `Assign`, `Input`, `Output`, `%` |
| Decisão | O programa escolhe um caminho conforme uma condição | `If`, `False:`, `&&`, `\|\|`, `!` |
| Repetição | Repetir um número fixo de vezes ou enquanto algo vale | `For`, `While`, `Do` |
| Vetores | Vários valores sob um nome, índices a partir de 0 | `Array`, `v[i]` |
| Sub-rotinas | Dividir o programa em partes reutilizáveis | `Function`, `Return`, `Call` |

## Cola rápida do Flowgorithm

```
... VARIÁVEIS
Declare Integer idade        ... inteiro
Declare Real nota            ... decimal (use ponto: 7.5)
Declare String nome          ... texto, entre aspas
Declare Boolean ativo        ... true / false
Declare Integer Array v[10]  ... vetor, índices 0 a 9

... ENTRADA, PROCESSAMENTO, SAÍDA
Output "Digite seu nome: "
Input nome
Assign media = (n1 + n2) / 2
... & junta textos
Output "Olá, " & nome & "! Média: " & media

... DECISÃO
If media >= 7
    Output "Aprovado"
False:  ... senão
    Output "Reprovado"
End

... REPETIÇÃO
For i = 1 to 10  ... número fixo de voltas
    Output i
End

While x <= 10  ... testa antes
    Assign x = x + 1
End

Loop  ... Do: executa e testa depois
    Input n
Do n < 0  ... repete enquanto for verdadeira

... FUNÇÕES
Assign r = minhaFuncao(a, b)  ... com retorno
Call meuProcedimento(a)       ... sem retorno
```

| Tipo | Operadores |
| --- | --- |
| Aritméticos | `+` `-` `*` `/` `%` (resto) `^` (potência) |
| Relacionais | `==` `!=` `>` `<` `>=` `<=` |
| Lógicos | `&&` (E) `\|\|` (OU) `!` (NÃO) |
| Texto | `&` (concatenar) |

> Este é um resumo pessoal de estudo. O conteúdo original do curso pertence à Intellectuale Tecnologia e Treinamento; PDFs e arquivos de fluxograma (`.fprg`) do curso não estão incluídos.
