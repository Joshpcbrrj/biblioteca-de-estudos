# Examples: chapter excerpts to imitate

Read **only the section for the book's area**. Each excerpt shows the pattern in `TEACHING.md` applied to a real case, written in Portuguese (pt-BR), the default book language. Imitate the structure, the tone and the level of detail, not the topic. For another book language, keep the structure and follow `style/<language>.md`.

## Contents

1. stem: programming (a `for` loop in Python)
2. languages: English for Portuguese speakers (third-person -s)
3. skills: guitar (changing between two chords)
4. knowledge: history of computing (the "first bug")

## 1. stem

~~~~markdown
# 4. Repetir sem copiar: o laço for

> 🗺️ **Neste capítulo:** como repetir uma ação para cada item de uma lista, sem copiar linhas. · ⏱️ ~30 min

> 🔥 **Aquecimento:** o que `len([7.5, 8.0, 6.5])` devolve?
>
> <details>
> <summary>Ver resposta</summary>
>
> `3`: a quantidade de itens da lista (capítulo 3).
>
> </details>

## De onde paramos

No capítulo 3 você guardou várias notas numa lista. Agora falta fazer algo com cada uma delas sem escrever uma linha por nota.

## O laço for

Calcular a média de 40 alunos escrevendo `total = total + nota1`, `+ nota2`... seriam 40 linhas quase iguais, e bastaria errar uma para a média sair errada.

**O laço `for` repete um bloco de código uma vez para cada item de uma lista.**

Antes de rodar, preveja: com as notas 7,5, 8,0 e 6,5, quantas vezes a linha `total += nota` executa? Que média aparece?

```python
notas = [7.5, 8.0, 6.5]
total = 0
# percorre a lista: a cada volta, "nota" vale um item
for nota in notas:
    # acumula para poder dividir no fim
    total += nota
media = total / len(notas)
print(f"Média: {media:.2f}")
```

Saída:

```text
Média: 7.33
```

A linha de dentro do laço executou 3 vezes, uma por nota: o total passou por 7,5 e 15,5 e chegou a 22,0. Dividido por 3, dá 7,33.

![Três voltas do laço: nota vale 7,5, 8,0 e 6,5, e o total cresce até 22,0](../img/c04-for-acumula.svg)

> ⚠️ **Erro comum:** rodar o mesmo código com uma lista vazia. O laço não executa nenhuma vez, `len(notas)` vale 0 e a divisão falha com `ZeroDivisionError: division by zero`. Confira se a lista tem itens antes de dividir.
~~~~

Why it works: a problem before the definition; the definition in one bold sentence; prediction before the output; real values in the code, the output and the image; the comment explains why; the common mistake shows the real error.

## 2. languages

~~~~markdown
## O -s da terceira pessoa

Em português, o verbo muda com a pessoa: eu trabalho, ela trabalha. No inglês do dia a dia, ele quase não muda. A exceção que todo iniciante esquece é esta:

**No presente, com *he*, *she* e *it*, o verbo ganha -s.**

| Pessoa | Frase | Tradução |
| --- | --- | --- |
| I / you / we / they | They **work** at night. | Eles trabalham à noite. |
| he / she / it | She **works** at night. | Ela trabalha à noite. |

Pronúncia do -s (o som depende do fim do verbo):

| Verbo | IPA | Aproximação |
| --- | --- | --- |
| works | /wɜːks/ | "uérks" (som de s) |
| plays | /pleɪz/ | "plêiz" (som de z) |
| watches | /ˈwɒtʃɪz/ | "uótchiz" (sílaba a mais) |

> ⚠️ **Erro comum de quem fala português:** "She work at night." Como o português já marca a pessoa no verbo de outro jeito, o -s some na fala. Diga em voz alta três frases com *she* antes de seguir.

### 🏋️ Pratique

**Complete:** My brother ___ (live) in Recife.

<details>
<summary>Ver resposta</summary>

**lives**. *My brother* = *he*, então o verbo ganha -s. Se você escreveu *live*, é o erro comum desta seção: releia a tabela acima.

</details>
~~~~

Why it works: a contrast with the reader's native language; one rule in bold; pronunciation in IPA plus an approximation for Portuguese speakers; the mistake typical of Portuguese speakers; a commented answer that says what a wrong answer means.

## 3. skills

~~~~markdown
## Trocar entre Mi menor e Lá menor

Tocar uma música não depende de saber muitos acordes, e sim de **trocar entre eles no tempo**. Por isso esta seção treina só a troca.

```text
Mi menor (Em)          Lá menor (Am)
e |--0--|              e |--0--|
B |--0--|              B |--1--|  dedo 1
G |--0--|              G |--2--|  dedo 3
D |--2--|  dedo 3      D |--2--|  dedo 2
A |--2--|  dedo 2      A |--0--|
E |--0--|              E |--x--|  não toque
```

Repare: o dedo 2 só desce uma corda (de Lá para Ré). Mexer o mínimo é o segredo de uma troca rápida.

### 🎯 Rotina (10 min)

1. **2 min:** monte cada acorde, toque corda por corda e confira se nenhuma soa abafada.
2. **5 min:** metrônomo a **60 bpm**, 4 batidas em Em e 4 em Am, sem parar.
3. **3 min:** suba para **80 bpm**.

**Pronto quando:** você fizer 8 trocas seguidas a 80 bpm sem parar o ritmo, mesmo que alguma nota saia abafada. A limpeza vem com a repetição; o ritmo, não.

> ⚠️ **Postura:** se o punho da mão esquerda doer, pare. Polegar atrás do braço do violão, punho reto, e retome no dia seguinte.
~~~~

Why it works: the chords as copyable text; the key move pointed out; a timed routine with tempos; a measurable done criterion; a safety note about strain.

## 4. knowledge

~~~~markdown
## O "primeiro bug" da computação

**Pergunta-guia:** a palavra *bug* nasceu de um inseto de verdade?

**A história popular:** em 1947, um inseto preso num computador teria criado o termo *bug*.

**O que os registros mostram:** em 9 de setembro de 1947, a equipe do Harvard Mark II encontrou uma mariposa presa num relé da máquina e a colou no caderno de registro, com a anotação "First actual case of bug being found" ("primeiro caso real de bug encontrado"). O caderno está hoje no Smithsonian.

**O que isso quer dizer:** a piada da anotação só funciona porque *bug* **já** era usado para defeitos. Engenheiros falavam em *bugs* desde o século XIX; Thomas Edison usou a palavra nesse sentido em cartas da década de 1870. O episódio de 1947 não criou o termo: virou a história mais famosa sobre ele.

> 💡 **Curiosidade (com fonte):** a cientista Grace Hopper, que trabalhava no Mark II, ajudou a popularizar a história contando-a por décadas.

### 🧠 Revisão rápida

Por que a anotação de 1947 é uma prova de que o termo já existia?

<details>
<summary>Ver resposta</summary>

Porque a frase só é engraçada se os leitores já conhecessem *bug* como "defeito": "o primeiro caso **real**" brinca com o sentido figurado que já circulava.

</details>
~~~~

Why it works: a guiding question; legend, record and interpretation separated and labeled; dates and names that go through `facts.py`; a curiosity marked as such and backed by a source; a review question that asks for reasoning, not memory.
