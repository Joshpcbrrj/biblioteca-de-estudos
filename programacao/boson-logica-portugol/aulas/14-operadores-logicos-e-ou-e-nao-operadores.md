# Operadores Lógicos e, ou e não (Operadores booleanos)

> 🗺️ **Nesta aula:** como os operadores lógicos combinam condições, os básicos (E, OU, NÃO) e os derivados (NAND, NOR, XOR, XNOR), a tabela-verdade e projetos com janelas abertas e fechadas.

## De onde paramos

Os operadores relacionais respondem uma pergunta de cada vez ("a nota é maior que 7?"). Na vida real as decisões juntam várias perguntas, e é aí que entram os operadores lógicos.

## Para que servem

Os operadores lógicos **combinam condições**. Com eles uma única expressão pode testar várias comparações ao mesmo tempo, como "a nota é maior que 7 **e** as faltas são menores que 10". O resultado continua sendo um valor lógico: `verdadeiro` ou `falso`.

![e, ou, nao: tabela-verdade e como montar os derivados](../img/lg-portas.svg)

> 💡 **Analogia:** pense na porta de um cofre de banco. Com **E**, ela só abre se o gerente **e** o caixa girarem a chave juntos. Com **OU**, é a porta da sua casa: qualquer morador com a chave abre. O **NÃO** é o aviso "não entre" virando "entre": só inverte a mensagem.

## Os operadores básicos

**E (AND)**: resulta em verdadeiro **só se as duas** entradas forem verdadeiras. Basta uma falsa para o resultado ser falso.

**OU (OR)**: resulta em verdadeiro se **pelo menos uma** das entradas for verdadeira. Só é falso quando as duas são falsas.

**NÃO (NOT)**: é o único que recebe **uma** entrada só, e simplesmente inverte o valor: verdadeiro vira falso e falso vira verdadeiro.

## Os operadores derivados

**NÃO-E (NAND)**: é o E seguido de um NÃO. Resulta em verdadeiro se pelo menos uma entrada for falsa.

**NÃO-OU (NOR)**: é o OU seguido de um NÃO. Resulta em verdadeiro só se as duas entradas forem falsas.

**OU-EXCLUSIVO (XOR)**: resulta em verdadeiro se **apenas uma** das entradas for verdadeira, ou seja, se as entradas forem **diferentes**.

**NÃO-OU-EXCLUSIVO (XNOR)**: o contrário do XOR. Resulta em verdadeiro se as entradas forem **iguais**.

## Tabela-verdade

Todas as combinações possíveis de duas entradas `a` e `b` (V = verdadeiro, F = falso):

**Operadores básicos**

| a | b | a e b | a ou b |
| --- | --- | --- | --- |
| V | V | **V** | **V** |
| V | F | F | **V** |
| F | V | F | **V** |
| F | F | F | F |

O `nao` só tem uma entrada: `nao V` dá F e `nao F` dá V.

**Operadores derivados: NAND e NOR**

| a | b | NAND | NOR |
| --- | --- | --- | --- |
| V | V | F | F |
| V | F | **V** | F |
| F | V | **V** | F |
| F | F | **V** | **V** |

**Operadores derivados: XOR e XNOR**

| a | b | XOR | XNOR |
| --- | --- | --- | --- |
| V | V | F | **V** |
| V | F | **V** | F |
| F | V | **V** | F |
| F | F | F | **V** |

> 💡 No Portugol só existem as palavras `e`, `ou` e `nao`. Os demais se montam com elas: NAND é `nao (a e b)`, NOR é `nao (a ou b)`, e, para variáveis do tipo `logico`, XOR é `a != b` e XNOR é `a == b`.

## Projeto: janelas abertas ou fechadas

Nos projetos abaixo, cada variável representa uma janela: `'a'` para aberta e `'f'` para fechada.

![As janelas da casa: e, ou e nao aplicados aos projetos abaixo](../img/lg-janelas.svg)

> 💡 **Analogia:** antes de viajar, você confere a casa. "Todas as janelas estão fechadas?" exige checar uma por uma (**e**). "Alguma está aberta?" termina na primeira aberta que você encontrar (**ou**).

**Operador e**

```c
programa
{
  caracter a1, a2, a3
  logico estado

  funcao inicio()
  {
    a1 = 'a'
    a2 = 'a'
    a3 = 'a'

    // e: verdadeiro só se as TRÊS
    // comparações forem verdadeiras
    estado = a1 == 'a' e a2 == 'a'
      e a3 == 'a'

    escreva("Janelas (a = aberta | ",
      "f = fechada)\n")
    escreva("a1: ", a1, "\na2: ", a2,
      "\na3: ", a3, "\n")

    escreva("\nTodas as janelas estão ",
      "abertas? ", estado, "\n")
    // se não estão todas abertas, alguma
    // está fechada: basta inverter
    escreva("Alguma janela está fechada? ",
      nao estado, "\n")
  }
}
```

**Operador ou**

```c
programa
{
  caracter a1, a2, a3
  logico estado

  funcao inicio()
  {
    a1 = 'a'
    a2 = 'f'
    a3 = 'f'

    // ou: basta UMA comparação verdadeira
    estado = a1 == 'a' ou a2 == 'a'
      ou a3 == 'a'

    escreva("Janelas (a = aberta | ",
      "f = fechada)\n")
    escreva("a1: ", a1, "\na2: ", a2,
      "\na3: ", a3, "\n")
    escreva("\nAlguma janela está aberta? ",
      estado, "\n")
  }
}
```

**Operador nao**

```c
programa
{
  caracter a1, a2, a3
  logico alguma_aberta

  funcao inicio()
  {
    a1 = 'a'
    a2 = 'f'
    a3 = 'f'

    alguma_aberta = a1 == 'a' ou a2 == 'a'
      ou a3 == 'a'

    escreva("Janelas (a = aberta | ",
      "f = fechada)\n")
    escreva("a1: ", a1, "\na2: ", a2,
      "\na3: ", a3, "\n")

    // se NÃO há nenhuma aberta, então
    // todas estão fechadas; aqui dá falso
    escreva("\nTodas as janelas estão ",
      "fechadas? ", nao alguma_aberta, "\n")
  }
}
```

> ⚠️ Na versão original do projeto `nao`, a mesma expressão `nao estado` respondia a duas perguntas diferentes ("todas abertas?" e "todas fechadas?"). Negar o "alguma aberta?" responde só à segunda. Para saber se todas estão abertas é preciso o `e`, como no primeiro projeto.

## Projeto maior: e, ou e nao juntos

**Código**

```c
programa
{
  caracter a1, a2, a3, b1, b2, b3
  cadeia c1, c2
  logico estado_a, estado_b
  logico afirmacao_d, negacao_d

  funcao inicio()
  {
    // 'a' = aberta | 'f' = fechada
    a1 = 'a'
    a2 = 'a'
    a3 = 'a'

    b1 = 'f'
    b2 = 'a'
    b3 = 'f'

    c1 = "dia"
    c2 = "noite"

    // todas as janelas a estão abertas?
    estado_a = a1 == 'a' e a2 == 'a'
      e a3 == 'a'
    // alguma janela b está aberta?
    estado_b = b1 == 'a' ou b2 == 'a'
      ou b3 == 'a'

    // cadeias também se comparam com ==
    afirmacao_d = c1 == "dia"
    negacao_d = nao afirmacao_d

    escreva("Janelas a: ", a1, " ", a2,
      " ", a3, "\n")
    escreva("Janelas b: ", b1, " ", b2,
      " ", b3, "\n")

    // verdadeiro
    escreva("\nTodas as janelas a estão ",
      "abertas? ", estado_a, "\n")
    // verdadeiro (b2 está aberta)
    escreva("Alguma janela b está aberta? ",
      estado_b, "\n")
    // verdadeiro
    escreva("9 horas da manhã é ", c1, "? ",
      afirmacao_d, "\n")
    // falso
    escreva("10 horas da ", c2, " é dia? ",
      negacao_d, "\n")
  }
}
```

> 💡 No original, `estado_b` testava `b1 == 'f' ou b2 == 'a' ou b3 == 'f'`, misturando "fechada" e "aberta" na mesma pergunta. Na versão acima as três comparações testam a mesma coisa (aberta). Também tirei o trecho final de brincadeira, que reproduzia letra de música.

## 🧠 Revisão rápida

**Com idade = 20 e tem_carteira = falso, quanto vale idade >= 18 e tem_carteira?**

`falso`: o `e` exige as duas verdadeiras, e a segunda é falsa.

**E idade >= 18 ou tem_carteira?**

`verdadeiro`: basta uma das duas ser verdadeira.

**Como escrever um XOR entre duas variáveis lógicas no Portugol?**

`a != b`: é verdadeiro quando as duas têm valores diferentes.

> ➡️ **Próximo passo:** hora de praticar tudo o que a seção mostrou (variáveis, operadores, entrada e saída) na **1ª Lista de exercícios**.

## 📌 Resumo

| Operador | No Portugol | Verdadeiro quando… |
| --- | --- | --- |
| E | `a e b` | as duas condições são verdadeiras |
| OU | `a ou b` | pelo menos uma é verdadeira |
| NÃO | `nao a` | inverte o valor |
| NAND | `nao (a e b)` | pelo menos uma é falsa |
| NOR | `nao (a ou b)` | as duas são falsas |
| XOR | `a != b` | as entradas são diferentes |
| XNOR | `a == b` | as entradas são iguais |
