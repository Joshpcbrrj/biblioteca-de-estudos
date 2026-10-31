# Exercícios de fixação

> ✨ **Página nova:** exercícios para praticar tudo o que foi visto até aqui: fases do algoritmo, pseudocódigo, variáveis, tipos, operadores, entrada e saída e decisões simples.

> 🗺️ **Como usar:** para cada exercício, (1) identifique entrada, processamento e saída, (2) escreva o pseudocódigo, (3) faça um teste de mesa com um exemplo e só então (4) abra a resposta. As respostas trazem pseudocódigo e Python; traduzir para Java ou C é um ótimo treino extra.

### 1. Converta uma temperatura de Celsius para Fahrenheit.

Fórmula: F = C × 9 ÷ 5 + 32. Teste: 25 °C deve resultar em 77 °F.

<details>
<summary>Ver resposta</summary>

```
Algoritmo CelsiusParaFahrenheit
Início
  Declare celsius, fahrenheit: Real
  Escreva "Temperatura em Celsius: "
  Leia celsius
  fahrenheit <- celsius * 9 / 5 + 32
  Escreva celsius, " °C = ", fahrenheit, " °F"
Fim
```

```python
celsius = float(input("Temperatura em Celsius: "))
fahrenheit = celsius * 9 / 5 + 32
print(f"{celsius} °C = {fahrenheit:.1f} °F")  # 25.0 °C = 77.0 °F
```

</details>

### 2. Leia um número inteiro e informe se ele é par ou ímpar.

<details>
<summary>Ver resposta</summary>

```
Algoritmo ParOuImpar
Início
  Declare n: Inteiro
  Leia n
  Se n mod 2 = 0 então
    Escreva n, " é par"
  Senão
    Escreva n, " é ímpar"
  FimSe
Fim
```

```python
n = int(input("Número: "))
if n % 2 == 0:
  print(f"{n} é par")
else:
  print(f"{n} é ímpar")
```

O resto da divisão por 2 só pode ser 0 (par) ou 1 (ímpar).

</details>

### 3. Leia uma quantidade de segundos e mostre em horas, minutos e segundos.

Teste: 3725 segundos = 1 h 2 min 5 s.

<details>
<summary>Ver resposta</summary>

```python
total = int(input("Segundos: "))

horas = total // 3600
resto = total % 3600  # o que sobra depois de tirar as horas
minutos = resto // 60
segundos = resto % 60

print(f"{horas} h {minutos} min {segundos} s")  # 1 h 2 min 5 s
```

| Variável | Cálculo | Valor |
| --- | --- | --- |
| `horas` | 3725 // 3600 | 1 |
| `resto` | 3725 % 3600 | 125 |
| `minutos` | 125 // 60 | 2 |
| `segundos` | 125 % 60 | 5 |

</details>

### 4. Calcule o troco de uma compra. Se o valor pago for menor que o total, informe quanto falta.

<details>
<summary>Ver resposta</summary>

```
Algoritmo Troco
Início
  Declare total, pago, diferenca: Real
  Leia total
  Leia pago
  diferenca <- pago - total
  Se diferenca >= 0 então
    Escreva "Troco: R$ ", diferenca
  Senão
    Escreva "Faltam R$ ", -diferenca
  FimSe
Fim
```

```python
total = float(input("Total da compra: "))
pago = float(input("Valor pago: "))
diferenca = pago - total

if diferenca >= 0:
  print(f"Troco: R$ {diferenca:.2f}")
else:
  print(f"Faltam R$ {-diferenca:.2f}")
# total 37.80 e pago 50 → Troco: R$ 12.20
```

</details>

### 5. Calcule o IMC (peso ÷ altura²) e classifique: abaixo de 18,5 abaixo do peso; até 24,9 normal; até 29,9 sobrepeso; a partir de 30 obesidade.

Teste: 70 kg e 1,75 m → IMC 22,86 (normal).

<details>
<summary>Ver resposta</summary>

```python
peso = float(input("Peso (kg): "))
altura = float(input("Altura (m): "))
imc = peso / altura ** 2  # potência antes da divisão

if imc < 18.5:
  situacao = "abaixo do peso"
elif imc < 25:
  situacao = "peso normal"
elif imc < 30:
  situacao = "sobrepeso"
else:
  situacao = "obesidade"

print(f"IMC {imc:.2f}: {situacao}")  # IMC 22.86: peso normal
```

- Usar `imc < 25` em vez de `imc <= 24.9` evita um buraco: um IMC de 24,95 não cairia em nenhuma faixa.
- A ordem dos testes importa: ao chegar em `imc < 25`, já se sabe que o IMC é pelo menos 18,5.

</details>

### 6. Um salário de até R$ 2.000 recebe 15% de aumento; acima disso, 10%. Mostre o novo salário.

Testes: R1.800→R 2.070; R3.000→R 3.300.

<details>
<summary>Ver resposta</summary>

```
Algoritmo Aumento
Início
  Constante LIMITE = 2000
  Declare salario, novo: Real
  Leia salario
  Se salario <= LIMITE então
    novo <- salario * 1.15
  Senão
    novo <- salario * 1.10
  FimSe
  Escreva "Novo salário: R$ ", novo
Fim
```

```python
LIMITE = 2000

salario = float(input("Salário atual: "))
if salario <= LIMITE:
  novo = salario * 1.15
else:
  novo = salario * 1.10
print(f"Novo salário: R$ {novo:.2f}")
```

O limite virou uma **constante**: se a regra mudar, basta alterar uma linha.

</details>

### 7. Desafio: leia três lados e diga se formam um triângulo.

Regra: cada lado deve ser menor que a soma dos outros dois. Teste: 3, 4, 5 → forma; 1, 2, 5 → não forma.

<details>
<summary>Ver resposta</summary>

```python
a = float(input("Lado A: "))
b = float(input("Lado B: "))
c = float(input("Lado C: "))

if a < b + c and b < a + c and c < a + b:
  print("Formam um triângulo")
else:
  print("Não formam um triângulo")
```

As três condições precisam ser verdadeiras ao mesmo tempo, por isso o operador **E** (`and`).

</details>

## 📌 O que cada exercício treina

| Exercício | Conceitos |
| --- | --- |
| 1. Celsius → Fahrenheit | fases do algoritmo, expressão aritmética |
| 2. Par ou ímpar | resto (`%`), decisão simples |
| 3. Segundos → h:min:s | divisão inteira e resto, teste de mesa |
| 4. Troco | decisão com dois caminhos, valores negativos |
| 5. IMC | potência, precedência, decisões encadeadas, faixas sem buracos |
| 6. Aumento | constantes, decisão |
| 7. Triângulo | operador lógico E com três condições |
