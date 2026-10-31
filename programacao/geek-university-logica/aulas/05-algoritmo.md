# Algoritmo

> 🗺️ **Nesta aula:** o que é um algoritmo, as cinco características de um bom algoritmo e um exemplo completo (o maior entre três números) em pseudocódigo e Python, com uma tabela de testes que inclui empates e negativos.

## Definição

Um **algoritmo** é uma **sequência finita de passos bem definidos** que resolve um problema ou executa uma tarefa.

Receitas de bolo, manuais de montagem e o caminho para chegar a um endereço são algoritmos. Na programação, o algoritmo é o **plano** da solução; o programa é esse plano escrito em uma linguagem que o computador entende.

O algoritmo **não depende de linguagem**: o mesmo algoritmo pode ser escrito em português (pseudocódigo), desenhado em um fluxograma ou implementado em Python, Java ou C.

## Características de um bom algoritmo

| Característica | Significado |
| --- | --- |
| **Finito** | Termina depois de um número limitado de passos (não fica em laço infinito) |
| **Definido** | Cada passo é claro e tem uma única interpretação |
| **Entrada** | Recebe zero ou mais dados para trabalhar |
| **Saída** | Produz pelo menos um resultado |
| **Efetivo** | Cada passo é executável na prática |

"Mexa até ficar bom" não é um passo definido. "Mexa por 5 minutos" é.

## Exemplo: encontrar o maior entre três números

### Em pseudocódigo

```
Algoritmo MaiorDeTres
Início
  Declare n1, n2, n3: Real

  Leia n1
  Leia n2
  Leia n3

  Se n1 >= n2 E n1 >= n3 então
    Escreva "O maior número é ", n1
  Senão se n2 >= n3 então
    Escreva "O maior número é ", n2
  Senão
    Escreva "O maior número é ", n3
  FimSe
Fim
```

**Raciocínio passo a passo**

1. Se `n1` é maior ou igual aos outros dois, ele é o maior.
2. Se não for, o maior está entre `n2` e `n3`: basta comparar os dois.
3. Se `n2` também não for, sobra `n3`.

> ⚠️ **Correção em relação à versão anterior:** com `>` (maior estrito) no lugar de `>=`, o algoritmo falha com números repetidos. Com `5, 5, 3`, nenhum dos dois primeiros testes é verdadeiro (5 não é **maior** que 5) e o algoritmo responderia `3`. Usar `>=` resolve os empates. Também não é preciso comparar `n2` com `n1` no segundo teste: se chegou lá, já se sabe que `n1` não é o maior.

### Em Python

```python
def maior_de_tres(n1, n2, n3):
  if n1 >= n2 and n1 >= n3:
    return n1
  elif n2 >= n3:
    return n2
  else:
    return n3

print(maior_de_tres(4, 9, 2))  # 9
print(maior_de_tres(5, 5, 3))  # 5 → empate tratado corretamente
print(maior_de_tres(1, 2, 8))  # 8
```

### Testando o algoritmo

Um algoritmo só está pronto depois de testado com casos variados, inclusive os "chatos":

| Entrada | Saída esperada | Por que testar |
| --- | --- | --- |
| 4, 9, 2 | 9 | Maior no meio |
| 1, 2, 8 | 8 | Maior no fim |
| 5, 5, 3 | 5 | Empate entre os maiores |
| 7, 7, 7 | 7 | Todos iguais |
| -3, -1, -8 | -1 | Números negativos |

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Algoritmo | sequência finita de passos bem definidos que resolve um problema |
| Independe da linguagem | o mesmo algoritmo vira pseudocódigo, fluxograma, Python, Java ou C |
| Características | finito, definido, com entrada, com saída e efetivo |
| Passo bem definido | "mexa por 5 minutos", nunca "mexa até ficar bom" |
| Testar | inclua casos-limite: empates, todos iguais, negativos, zero |
| `>` × `>=` | o sinal errado faz o algoritmo falhar justamente nos empates |
