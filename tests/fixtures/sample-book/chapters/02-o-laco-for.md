# 2. O laço for

> 🗺️ **Neste capítulo:** como somar todos os itens de uma lista sem copiar linhas. · ⏱️ ~30 min

## De onde paramos

No capítulo 1 você guardou as notas numa lista. Agora vamos usar cada uma delas.

## O laço for

O Python foi lançado em 1991 por Guido van Rossum, e o laço `for` existe nele desde o começo.

**O laço `for` repete um bloco uma vez para cada item de uma lista.**

```python
notas = [7.5, 8.0, 6.5]
total = 0
# a cada volta, "nota" vale um item da lista
for nota in notas:
    # acumula para dividir no fim
    total += nota
print(f"Média: {total / len(notas):.2f}")
```

Saída:

```text
Média: 7.33
```

> ⚠️ **Erro comum:** dividir com a lista vazia causa `ZeroDivisionError`.

## 🏋️ Pratique

Qual é a média de `[10, 6]`?

<details>
<summary>Ver resposta</summary>

8,00: a soma é 16 e há 2 itens.

</details>

## 🧠 Revisão rápida

O que `len([2, 4])` devolve? (capítulo 1)

<details>
<summary>Ver resposta</summary>

2.

</details>

## 🤖 Estude com um tutor de IA

- "Corrija meu laço for sem me dar a resposta."

> ➡️ **Próximo passo:** o simulado final.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Laço for | Repete um bloco para cada item |

## 📚 Fontes

- [The Python Tutorial](https://docs.python.org/3/tutorial/), conferido em 2026-11-20.

> 🔁 **Revise hoje:** 1
