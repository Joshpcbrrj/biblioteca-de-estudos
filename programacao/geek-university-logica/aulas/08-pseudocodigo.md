# Pseudocódigo

> 🗺️ **Nesta aula:** o que é pseudocódigo (Portugol), as convenções de escrita usadas no curso, quatro exemplos completos (média, positivo/negativo, média ponderada e contagem) e como traduzir o pseudocódigo para Python.

## O que é pseudocódigo

**Pseudocódigo** é uma forma de escrever algoritmos em linguagem próxima da natural (português), mas com uma estrutura parecida com a de uma linguagem de programação. Ele **não é executado** pelo computador: serve para planejar e comunicar a solução antes de escrever o código real.

Vantagens:

- Permite focar na **lógica**, sem se preocupar com detalhes de sintaxe (ponto e vírgula, chaves, tipos).
- Pode ser traduzido para **qualquer** linguagem depois.
- É fácil de ler por quem ainda não programa.

No Brasil, o pseudocódigo em português costuma ser chamado de **Portugol**, e pode ser executado em ferramentas didáticas como o **VisuAlg** e o **Portugol Studio**.

## Convenções usadas nesta página

Não existe um padrão único, mas o importante é ser consistente. Aqui usamos:

| Pseudocódigo | Significado | Python |
| --- | --- | --- |
| `Declare x: Real` | Cria a variável `x` do tipo real | (não precisa declarar) |
| `x <- 5` | Atribui 5 a `x` | `x = 5` |
| `Leia x` | Lê um valor digitado e guarda em `x` | `x = float(input())` |
| `Escreva "texto", x` | Mostra texto e valores na tela | `print("texto", x)` |
| `Se ... então / Senão / FimSe` | Decisão | `if ... : / else:` |
| `Para i de 1 até 10 faça / FimPara` | Repetição com contador | `for i in range(1, 11):` |
| `Enquanto ... faça / FimEnquanto` | Repetição com condição | `while ...:` |

A seta `<-` é usada para atribuição justamente para não ser confundida com o `=` de comparação.

## Exemplos de pseudocódigo

### Média de três números com aprovação

```
Algoritmo MediaTresNumeros
Início
  Declare num1, num2, num3, media: Real

  Escreva "Digite as três notas: "
  Leia num1
  Leia num2
  Leia num3

  media <- (num1 + num2 + num3) / 3

  Se media >= 7 então
    Escreva "Aprovado com média: ", media
  Senão
    Escreva "Reprovado com média: ", media
  FimSe
Fim
```

Os parênteses em `(num1 + num2 + num3) / 3` são obrigatórios: sem eles, só `num3` seria dividido por 3, porque a divisão tem prioridade sobre a soma.

### Verificar se um número é positivo, negativo ou zero

```
Algoritmo VerificarNumero
Início
  Declare numero: Real

  Escreva "Digite um número: "
  Leia numero

  Se numero > 0 então
    Escreva "O número é positivo"
  Senão se numero < 0 então
    Escreva "O número é negativo"
  Senão
    Escreva "O número é igual a zero"
  FimSe
Fim
```

### Média ponderada

Na média ponderada, cada nota tem um **peso**. A fórmula é: (nota1 × peso1 + nota2 × peso2 + nota3 × peso3) ÷ (peso1 + peso2 + peso3).

```
Algoritmo MediaPonderada
Início
  Declare nota1, nota2, nota3, peso1, peso2, peso3, mediaPonderada: Real

  Escreva "Digite a primeira nota: "
  Leia nota1
  Escreva "Digite o peso da primeira nota: "
  Leia peso1

  Escreva "Digite a segunda nota: "
  Leia nota2
  Escreva "Digite o peso da segunda nota: "
  Leia peso2

  Escreva "Digite a terceira nota: "
  Leia nota3
  Escreva "Digite o peso da terceira nota: "
  Leia peso3

  mediaPonderada <- (nota1 * peso1 + nota2 * peso2 + nota3 * peso3) / (peso1 + peso2 + peso3)

  Escreva "A média ponderada é: ", mediaPonderada
Fim
```

Exemplo: notas 6, 8 e 10 com pesos 1, 2 e 3 → (6 + 16 + 30) ÷ 6 = **8,67**.

### Contagem de 1 até 10

```
Algoritmo ContagemAte10
Início
  Declare contador: Inteiro

  Para contador de 1 até 10 passo 1 faça
    Escreva contador
  FimPara
Fim
```

## Do pseudocódigo para o código

A tradução é quase linha a linha. A média ponderada em Python:

```python
nota1 = float(input("Digite a primeira nota: "))
peso1 = float(input("Digite o peso da primeira nota: "))
nota2 = float(input("Digite a segunda nota: "))
peso2 = float(input("Digite o peso da segunda nota: "))
nota3 = float(input("Digite a terceira nota: "))
peso3 = float(input("Digite o peso da terceira nota: "))

media_ponderada = (nota1 * peso1 + nota2 * peso2 + nota3 * peso3) / (peso1 + peso2 + peso3)

print(f"A média ponderada é: {media_ponderada:.2f}")
```

E a contagem de 1 até 10:

```python
for contador in range(1, 11):  # range para ANTES do 11
  print(contador)
```

`input()` sempre devolve **texto**. Por isso o `float(...)` converte para número antes de fazer contas.

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Pseudocódigo | algoritmo em português estruturado; não é executado, serve para planejar |
| Portugol | nome do pseudocódigo em português; roda no VisuAlg e no Portugol Studio |
| Atribuição | `<-` (para não confundir com o `=` de comparação) |
| Entrada / saída | `Leia` / `Escreva` |
| Decisão | `Se ... então / Senão / FimSe` |
| Repetição | `Para ... faça / FimPara` (contador) · `Enquanto ... faça / FimEnquanto` (condição) |
| Tradução | quase linha a linha; em Python, converta o `input()` com `float()` ou `int()` |

Outra forma de representar o mesmo algoritmo, em desenho, está na página **Fluxograma**.
