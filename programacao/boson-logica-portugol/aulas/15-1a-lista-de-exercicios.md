# 1ª Lista de exercícios

> 🗺️ **Nesta lista:** sete exercícios que juntam variáveis, operadores aritméticos e `leia`/`escreva`: nome completo, diferença, ordem inversa, média ponderada, volume, área e velocidade.

## De onde paramos

A seção apresentou variáveis, constantes, entrada e saída e os operadores. Agora é hora de juntar tudo em programas completos.

Cada exercício traz o enunciado e a resolução, que fica recolhida: tente resolver antes de abrir. O arquivo `.por` original de cada exercício fica logo abaixo do enunciado.

> 💡 **Roteiro para qualquer exercício:** 1) quais dados entram (`leia`)? 2) que conta transforma esses dados? 3) o que sai (`escreva`)? Declare uma variável para cada dado e para cada resultado.

## Exercício 1: nome completo

Escreva um algoritmo que:

1. pergunte o nome de uma pessoa;
2. pergunte o sobrenome;
3. mostre o nome completo na tela.

<details>
<summary>Ver resposta</summary>

```c
programa
{
  cadeia nome, sobrenome
  inteiro idade

  funcao inicio()
  {
    escreva("Digite seu primeiro nome: ")
    leia(nome)
    escreva("Digite seu sobrenome: ")
    leia(sobrenome)
    // extra: o enunciado pede só nome e
    // sobrenome; a idade é um bônus
    escreva("Digite sua idade: ")
    leia(idade)

    // sem o " ", sairia "AnaSouza" grudado
    escreva("\nSeu nome é: ", nome, " ",
      sobrenome)
    escreva(", e sua idade é: ", idade,
      " anos.\n")
  }
}
```

</details>

## Exercício 2: diferença entre dois números

Leia dois valores numéricos e mostre a diferença entre eles (o primeiro menos o segundo).

<details>
<summary>Ver resposta</summary>

```c
programa
{
  real num_1, num_2

  funcao inicio()
  {
    escreva("Digite o primeiro número: ")
    leia(num_1)
    escreva("Digite o segundo número: ")
    leia(num_2)

    // a conta pode ir direto no escreva:
    // não precisa de variável se o
    // resultado só vai ser mostrado
    escreva("\n", num_1, " - ", num_2, " = ")
    escreva(num_1 - num_2, "\n")
  }
}
```

</details>

A resolução original foi além e virou uma calculadora com quatro operações:

<details>
<summary>Ver versão estendida (calculadora)</summary>

```c
programa
{
  real num_1, num_2
  caracter operacao

  funcao inicio()
  {
    escreva("Digite o primeiro número: ")
    leia(num_1)
    escreva("Digite o segundo número: ")
    leia(num_2)
    escreva("\n1-Soma  2-Subtração\n")
    escreva("3-Multiplicação  4-Divisão: ")
    // lido como caracter, por isso a
    // comparação é com '1' (entre aspas)
    leia(operacao)

    se (operacao == '1') {
      escreva("Soma: ", num_1 + num_2, "\n")
    }
    senao se (operacao == '2') {
      escreva("Subtração: ",
        num_1 - num_2, "\n")
    }
    senao se (operacao == '3') {
      escreva("Multiplicação: ",
        num_1 * num_2, "\n")
    }
    senao se (operacao == '4') {
      escreva("Divisão: ",
        num_1 / num_2, "\n")
    }
    senao {
      escreva("\nOpção inválida.\n")
    }
  }
}
```

</details>

## Exercício 3: ordem inversa

Leia dois números nas variáveis `num_a` e `num_b`, nessa ordem, e mostre-os em ordem inversa, um embaixo do outro. Se forem lidos 7 e 15, deve aparecer 15 e depois 7.

![Lido em uma ordem, mostrado na outra](../img/l1-inverte.svg)

> 💡 **Analogia:** é como empilhar dois pratos. O último que você colocou na pilha é o primeiro que você vê em cima. Aqui não precisa mexer nos pratos: basta "ler" a pilha de cima para baixo.

<details>
<summary>Ver resposta</summary>

```c
programa
{
  inteiro num_a, num_b

  funcao inicio()
  {
    escreva("Digite o 1º número: ")
    leia(num_a)
    escreva("Digite o 2º número: ")
    leia(num_b)

    // não é preciso trocar os valores:
    // basta escrever na ordem contrária
    escreva("\n", num_b, "\n")
    escreva(num_a, "\n")
  }
}
```

</details>

A versão original também recusava números iguais (`se (num_a != num_b)`). O enunciado não exige essa regra, mas ela não atrapalha.

## Exercício 4: média ponderada

Uma disciplina tem três provas: a primeira com peso 2, a segunda com peso 3 e a terceira com peso 5. Calcule a média final do aluno.

Na **média ponderada**, cada nota é multiplicada pelo seu peso e a soma é dividida pela soma dos pesos.

![Média ponderada com pesos 2, 3 e 5](../img/l1-ponderada.svg)

> 💡 **Analogia:** é uma votação em que alguns jurados valem mais. A prova 3 tem "5 votos", a prova 1 só "2". Você soma todos os votos dados e divide pelo total de votos (10), não pelo número de jurados (3).

<details>
<summary>Ver resposta (conforme o enunciado)</summary>

```c
programa
{
  real prova_1, prova_2, prova_3, media

  funcao inicio()
  {
    escreva("Nota da prova 1 (peso 2): ")
    leia(prova_1)
    escreva("Nota da prova 2 (peso 3): ")
    leia(prova_2)
    escreva("Nota da prova 3 (peso 5): ")
    leia(prova_3)

    // os parênteses garantem que a soma
    // inteira seja feita antes da divisão
    media = (prova_1 * 2 + prova_2 * 3
      + prova_3 * 5) / (2 + 3 + 5)

    escreva("\nA média final é: ", media, "\n")
  }
}
```

</details>

<details>
<summary>Ver versão estendida: 6 notas (provas e trabalhos) com situação final</summary>

```c
programa
{
  real prova_1, prova_2, prova_final
  real trab_1, trab_2, trab_final
  real soma, media_ponderada

  funcao inicio()
  {
    escreva("Nota do trabalho 1 (peso 1): ")
    leia(trab_1)
    escreva("Nota da prova 1 (peso 2): ")
    leia(prova_1)
    escreva("Nota do trabalho 2 (peso 2): ")
    leia(trab_2)
    escreva("Nota da prova 2 (peso 3): ")
    leia(prova_2)
    escreva("Nota do trabalho final ",
      "(peso 3): ")
    leia(trab_final)
    escreva("Nota da prova final (peso 5): ")
    leia(prova_final)

    // a soma é montada em partes para cada
    // linha ficar curta e fácil de conferir
    soma = trab_1 * 1 + prova_1 * 2
      + trab_2 * 2
    soma = soma + prova_2 * 3
      + trab_final * 3
    soma = soma + prova_final * 5
    // soma dos pesos: 1+2+2+3+3+5 = 16
    media_ponderada = soma / 16

    se (media_ponderada >= 7) {
      escreva("\nParabéns! Você está ",
        "aprovado.\n")
    }
    senao se (media_ponderada >= 4) {
      escreva("\nRecuperação. Ainda dá ",
        "para passar.\n")
    }
    senao {
      escreva("\nReprovado. Tente no ano ",
        "que vem.\n")
    }
    escreva("A média final é: ",
      media_ponderada, "\n")
  }
}
```

</details>

## Exercício 5: volume da caixa d'água

O usuário informa altura, largura e profundidade de uma caixa d'água, em cm. Mostre o volume.

![Volume = altura × largura × profundidade](../img/l1-volume.svg)

> 💡 **Analogia:** imagine encher a caixa com cubinhos de 1 cm. A largura diz quantos cabem numa fileira, a profundidade quantas fileiras formam uma camada, e a altura quantas camadas empilham. Multiplicar os três é contar todos os cubinhos.

<details>
<summary>Ver resposta</summary>

```c
programa
{
  real altura, largura, profund, vol

  funcao inicio()
  {
    escreva("Altura da caixa (cm): ")
    leia(altura)
    escreva("Largura da caixa (cm): ")
    leia(largura)
    escreva("Profundidade da caixa (cm): ")
    leia(profund)

    // cm × cm × cm = cm³
    vol = altura * largura * profund

    escreva("\nVolume: ", vol, " cm³\n")
    // 1000 cm³ = 1 litro: em litros o
    // número fica mais fácil de entender
    escreva("Equivale a ", vol / 1000,
      " litros.\n")
  }
}
```

</details>

## Exercício 6: área do triângulo

O usuário informa base e altura de um triângulo, em cm. Mostre a área. Fórmula: `área = base × altura / 2`.

![Área do triângulo: metade do retângulo](../img/l1-triangulo.svg)

> 💡 **Analogia:** corte um sanduíche quadrado na diagonal. Cada triângulo é exatamente metade do sanduíche, por isso a área é a do retângulo (base × altura) dividida por 2.

<details>
<summary>Ver resposta</summary>

```c
programa
{
  real base, altura, area_do_tri

  funcao inicio()
  {
    escreva("Base do triângulo (cm): ")
    leia(base)
    escreva("Altura do triângulo (cm): ")
    leia(altura)

    // metade do retângulo de mesma base
    // e mesma altura
    area_do_tri = (base * altura) / 2

    escreva("\nBase: ", base, " cm | Altura: ")
    escreva(altura, " cm\n")
    escreva("Área: ", area_do_tri, " cm²\n")
  }
}
```

</details>

## Exercício 7: velocidade e tempo de viagem

Leia a velocidade de um veículo em km/h e mostre:

- a velocidade convertida para m/s (divida por 3,6);
- quanto tempo leva uma viagem de São Paulo ao Rio de Janeiro (cerca de 435 km) nessa velocidade média.

![Conversão para m/s e tempo de viagem](../img/l1-velocidade.svg)

> 💡 **Analogia:** unidades são como moedas. Não dá para pagar uma conta em reais contando dólares sem converter. Distância em km só "conversa" com velocidade em km/h; misturar metros com km/h dá um número que não significa nada.

<details>
<summary>Ver resposta</summary>

```c
programa
{
  // constante: a distância não muda, e o
  // nome explica o que é o 435
  const real DISTANCIA_SP_RJ = 435.0

  real veloc, metro_por_segundo, tempo

  funcao inicio()
  {
    escreva("Velocidade média (km/h): ")
    leia(veloc)

    // 1 km/h = 1000 m / 3600 s = 1/3,6 m/s
    metro_por_segundo = veloc / 3.6
    // km ÷ km/h = horas
    tempo = DISTANCIA_SP_RJ / veloc

    escreva("\nEm m/s: ", metro_por_segundo,
      "\n")
    escreva("Tempo SP → RJ: ", tempo,
      " horas\n")
  }
}
```

</details>

> ⚠️ A resolução original pedia a distância em **metros** e dividia pela velocidade em **km/h**, misturando unidades: o resultado não correspondia a horas nem a segundos. Na versão acima, distância em km dividida por velocidade em km/h dá o tempo em horas. A 90 km/h, por exemplo, são cerca de 4,83 h (4 h 50 min).

## 🧠 Revisão rápida

<details>
<summary>Ver resposta: Notas 10, 5 e 5 com pesos 2, 3 e 5: qual a média ponderada?</summary>

(10×2 + 5×3 + 5×5) / 10 = (20 + 15 + 25) / 10 = 6.0.

</details>

<details>
<summary>Ver resposta: Uma caixa de 100 × 100 × 100 cm tem quantos litros?</summary>

1 000 000 cm³ ÷ 1000 = 1000 litros (1 m³).

</details>

<details>
<summary>Ver resposta: Quanto é 72 km/h em m/s?</summary>

72 ÷ 3,6 = 20 m/s.

</details>

> ➡️ **Próximo passo:** até aqui os programas executam todas as linhas, sempre. A próxima seção ensina o programa a escolher um caminho: **Estrutura de Decisão Condicional Simples (SE)**.

## 📌 Resumo

| Exercício | O que pratica |
| --- | --- |
| 1. Nome completo | Juntar cadeias no `escreva` com `" "` entre elas |
| 2. Diferença | Expressão direto no `escreva` |
| 3. Ordem inversa | Escrever as variáveis na ordem contrária à leitura |
| 4. Média ponderada | Multiplicar cada nota pelo peso e dividir pela soma dos pesos |
| 5. Volume | Produto de três medidas; 1000 cm³ = 1 litro |
| 6. Área do triângulo | `base * altura / 2` |
| 7. Velocidade | km/h ÷ 3,6 = m/s; distância ÷ velocidade = tempo (unidades compatíveis) |

## 🧭 Cheat sheet da seção

![Cheat sheet da seção: 12 cards para revisar variáveis, tipos, entrada e saída e operadores](../img/bo-mapa-variaveis.svg)
