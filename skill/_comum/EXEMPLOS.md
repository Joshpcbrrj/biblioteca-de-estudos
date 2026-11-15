# Exemplos de referência: aula e cheat sheet

> Arquivo comum às skills da biblioteca. Leia antes da primeira página do curso e volte a ele sempre que estiver em dúvida sobre o tom ou o formato. **Imite estes exemplos**: eles valem mais que a lista de regras.

## 1. Aula: antes e depois

Aula real do curso da Bóson ("Estudo complementar de Constantes"). O *antes* já estava revisado no padrão anterior; o *depois* é o padrão atual, exatamente como foi gravado no Notion (`replace_content`).

### Antes (padrão anterior, em Markdown)

````markdown
# Estudo complementar de Constantes

> 🗺️ **Nesta aula:** a diferença entre variável e constante, quando usar constantes e como declarar uma com `const` no Portugol.

## Variáveis x constantes

|  | Variável | Constante |
| --- | --- | --- |
| O valor pode mudar? | Sim, quantas vezes for preciso durante a execução | Não: é definido uma vez e fica fixo até o fim |
| Quando recebe o valor | Pode ser declarada agora e receber o valor depois | Precisa receber o valor **na própria declaração** |
| Convenção de nome | minúsculas (`nota_final`) | MAIÚSCULAS (`PI`, `TAXA_JUROS`) |

![Variável muda; constante não muda](../img/c-const.svg)

Use constantes para valores que não devem mudar: o valor de π, uma taxa fixa, a nota mínima de aprovação. Além de proteger o valor (o programa dá erro se alguém tentar alterá-lo), o nome deixa o código mais legível: `MEDIA_MINIMA` diz mais que um `7` solto no meio do código.

> 💡 Assim como as variáveis, as constantes podem ser locais ou globais.

## Como declarar

```c
const tipo NOME_DA_CONSTANTE = valor
```

## Projeto: criando uma constante

**Código**

```c
programa
{
  const real PI = 3.1415  // declarada e inicializada na mesma linha

  funcao inicio()
  {
    escreva("Aqui usamos a constante para armazenar o valor de Pi: ", PI, "\n")

    // PI = 3.0  ← erro: não é possível alterar o valor de uma constante
  }
}
```

## 📌 Resumo

| Conceito | Em uma frase |
| --- | --- |
| Constante | Valor fixo, definido uma vez e nunca alterado |
| Declaração | `const tipo NOME = valor`, sempre com o valor na mesma linha |
| Nome | Em MAIÚSCULAS, por convenção |
| Para que serve | Proteger valores fixos e deixar o código mais legível |
````

### Depois (padrão atual, no Notion)

O breadcrumb e os anexos originais (`<unknown ... alt="breadcrumb" />`, `<file ...>`) ficam no lugar em que vieram; foram omitidos aqui. O `file-upload://` é o id devolvido pelo `notion-create-attachment`.

````markdown
<callout icon="🗺️" color="gray_bg">
<b>Nesta aula:</b> a diferença entre variável e constante, quando usar constantes e como declarar uma com <code>const</code> no Portugol.
</callout>

## De onde paramos

Variáveis existem para mudar de valor. Mas alguns valores nunca deveriam mudar, como o valor de π ou a nota mínima de aprovação. Para eles existe a constante.

## Variáveis x constantes

|  | Variável | Constante |
| --- | --- | --- |
| O valor pode mudar? | Sim, quantas vezes for preciso durante a execução | Não: é definido uma vez e fica fixo até o fim |
| Quando recebe o valor | Pode ser declarada agora e receber o valor depois | Precisa receber o valor <b>na própria declaração</b> |
| Convenção de nome | minúsculas (<code>nota_final</code>) | MAIÚSCULAS (<code>PI</code>, <code>TAXA_JUROS</code>) |

<image source="file-upload://ID-DO-UPLOAD">
Variável muda; constante não muda
</image>

<callout icon="💡" color="blue_bg">
<b>Analogia:</b> uma variável é o quadro branco da sala, que se apaga e reescreve o dia todo. Uma constante é a placa de metal parafusada na porta com o número da sala: definida uma vez, na instalação, e ninguém consegue trocar com um apagador.
</callout>

Use constantes para valores que não devem mudar: o valor de π, uma taxa fixa, a nota mínima de aprovação. Além de proteger o valor (o programa dá erro se alguém tentar alterá-lo), o nome deixa o código mais legível: <code>MEDIA_MINIMA</code> diz mais que um <code>7</code> solto no meio do código.

<callout icon="💡" color="red_bg">
Assim como as variáveis, as constantes podem ser locais ou globais.
</callout>

## Como declarar

```c
// const + tipo + NOME em maiúsculas + valor:
// o valor vem na mesma linha porque depois
// não poderá mais ser atribuído
const tipo NOME_DA_CONSTANTE = valor
```

## Projeto: criando uma constante

<toggle>
Código

```c
programa
{
  // global e fixa: qualquer função usa o
  // mesmo PI, e ninguém consegue alterá-lo
  const real PI = 3.1415

  funcao inicio()
  {
    escreva("Aqui usamos a constante para ",
      "armazenar o valor de Pi: ", PI, "\n")

    // a linha abaixo daria ERRO, e é
    // justamente essa proteção que queremos:
    // PI = 3.0
  }
}
```

Saída: <code>Aqui usamos a constante para armazenar o valor de Pi: 3.1415</code>
</toggle>

## 🧠 Revisão rápida

<toggle>
Posso declarar <code>const real PI</code> e atribuir o valor depois?

Não: a constante precisa receber o valor na própria declaração.
</toggle>

<toggle>
Por que escrever <code>MEDIA_MINIMA</code> em vez de usar o número 7 direto no código?

Porque o nome explica o significado e, se a regra mudar, você altera um lugar só.
</toggle>

<toggle>
O que acontece se o programa tentar fazer <code>PI = 3.0</code>?

Dá erro: o valor de uma constante não pode ser alterado.
</toggle>

<callout icon="➡️" color="gray_bg">
<b>Próximo passo:</b> até aqui, os valores foram escritos no próprio código. A próxima aula mostra como recebê-los do usuário e mostrar resultados: <b>Entrada e Saída de Dados com Leia e Escreva</b>.
</callout>

## 📌 Resumo

| Conceito | Em uma frase |
| --- | --- |
| Constante | Valor fixo, definido uma vez e nunca alterado |
| Declaração | <code>const tipo NOME = valor</code>, sempre com o valor na mesma linha |
| Nome | Em MAIÚSCULAS, por convenção |
| Para que serve | Proteger valores fixos e deixar o código mais legível |
````

### O que mudou, e por quê

| Mudança | Regra que ela aplica |
| --- | --- |
| `## De onde paramos` no início | cada aula se liga à anterior e explica por que o tema existe |
| Callout `Analogia:` logo abaixo da imagem, mapeando peça por peça (quadro branco = variável, placa parafusada = constante) | toda imagem tem uma analogia; nenhuma se repete em outra aula |
| Comentários na linha de cima explicando o **porquê** ("o valor vem na mesma linha porque depois não poderá mais ser atribuído") | comentário explica intenção, não repete o código |
| Linhas de código quebradas em até ~60 caracteres; recuo de 2 espaços | leitura em e-reader |
| O erro proposital (`PI = 3.0`) virou comentário com a explicação | o código mostrado sempre roda |
| Linha `Saída:` depois do código | todo exemplo mostra o resultado esperado |
| `## 🧠 Revisão rápida` com 3 toggles curtos (uma armadilha incluída) | revisão ativa no fim da aula |
| Callout `➡️ Próximo passo` com o nome exato da aula seguinte | o leitor sabe para onde vai e por quê |
| O resumo foi mantido (já estava bom) | só mude o que melhora |

## 2. Cheat sheet de seção

Fecha cada seção (na última página dela, normalmente a lista de exercícios), com o título `## 🧭 Cheat sheet da seção`. Imagem pronta deste exemplo: `programacao/boson-logica-portugol/img/bo-mapa-variaveis.svg`.

Os dados ficam em `ferramentas/svg/cheatsheets.py`; cada card é `C(título, ícone ASCII, 3 tópicos curtos, code=[...], tags=[...])`:

```python
S['bo-mapa-variaveis'] = ('boson-logica-portugol',
  'Variáveis e operadores',
  'Seção 2 · guardar, calcular e comparar', [
  C('Tipos', 'T', ['inteiro e real', 'caracter e cadeia',
    'logico'], tags=['inteiro', 'real', 'cadeia']),
  C('Variável', '[x]', ['caixa com etiqueta', 'tipo fixo',
    'valor muda'], code=['inteiro idade = 20']),
  C('Constante', 'K', ['const real PI', 'não muda',
    'nome em MAIÚSCULAS']),
  # ... 12 cards no total, na ordem em que a seção ensina
])
```

Como fica no Notion:

```
## 🧭 Cheat sheet da seção

<image source="file-upload://ID">
Cheat sheet da seção: 12 cards para revisar variáveis, tipos,
entrada e saída e operadores
</image>
```

Regras do exemplo: 12 cards, na ordem em que a seção ensina; tópicos de até ~28 caracteres; ícone só com ASCII; no máximo uma linha de código por card.
