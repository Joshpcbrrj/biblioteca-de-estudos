# Operadores de atribuição compostos (+=, -=, *=, /=) (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** os atalhos que combinam uma conta com a atribuição, a equivalência com a forma longa e onde eles aparecem no curso.

## De onde paramos

O `x++` soma exatamente 1. Mas muitas vezes o passo é outro: somar uma nota ao total, descontar um saque do saldo, dobrar um valor. Para esses casos existem os operadores compostos.

## O que são

É muito comum atualizar uma variável a partir do próprio valor dela: somar algo ao total, descontar do saldo, dobrar um número. Os operadores compostos escrevem isso de forma mais curta, sem repetir o nome da variável.

![Atribuição composta: faz a conta e guarda](../img/ac-ops.svg)

> 💡 **Analogia:** é o cofrinho. `cofre += 5` é "coloque 5 reais no cofre": você não esvazia o cofre, conta tudo e guarda de novo; só acrescenta ao que já está lá. `cofre -= 2` é tirar 2 reais do mesmo cofre.

A leitura é sempre a mesma: `x += 3` significa "pegue o valor atual de x, some 3 e guarde o resultado em x". É a mesma ideia do `x++`, mas com qualquer valor e qualquer uma das quatro operações.

> 💡 O lado direito é calculado inteiro antes da operação: `x *= 2 + 1` é `x = x * (2 + 1)`, e não `x = x * 2 + 1`.

## Onde aparecem no curso

- **Acumuladores**: `soma += notas[i]` na média de notas e `soma += matriz[lin][col]` na soma da matriz.
- **Somatórios**: `soma += 1.0 / denominador` na soma das 20 frações (3ª lista).
- **Passos diferentes de 1**: `num -= 2` para descer de 2 em 2 nos números pares (3ª lista).

## Projeto: caixa eletrônico simples

```c
programa
{
  real saldo = 1000.0
  real valor
  inteiro opcao

  funcao inicio()
  {
    // faca-enquanto: o menu aparece pelo
    // menos uma vez e repete até digitar 0
    faca {
      escreva("\nSaldo: R$ ", saldo, "\n")
      escreva("1 - Depositar | 2 - Sacar",
        " | 0 - Sair: ")
      leia(opcao)

      se (opcao == 1) {
        escreva("Valor do depósito: ")
        leia(valor)
        // acrescenta ao que já existe:
        // saldo = saldo + valor
        saldo += valor
      }
      senao se (opcao == 2) {
        escreva("Valor do saque: ")
        leia(valor)
        // conferir antes evita saldo negativo
        se (valor <= saldo) {
          // saldo = saldo - valor
          saldo -= valor
        }
        senao {
          escreva("Saldo insuficiente.\n")
        }
      }
    } enquanto (opcao != 0)

    escreva("\nSaldo final: R$ ", saldo, "\n")
  }
}
```

O menu usa o `faca-enquanto`, visto na seção de repetição: ele mostra as opções pelo menos uma vez e repete até o usuário digitar 0.

## 🧠 Revisão rápida

**Se `total` vale 10, quanto vale depois de `total -= 4`?**

6: é o mesmo que `total = total - 4`.

**Com `x = 2`, quanto vale `x` depois de `x *= 3 + 1`?**

8: o lado direito (3 + 1 = 4) é calculado primeiro, e 2 * 4 = 8.

**`x += 1` e `x++` fazem a mesma coisa?**

Sim: os dois somam 1 a `x`.

> ➡️ **Próximo passo:** com as contas dominadas, falta o programa saber comparar valores. É o assunto dos **operadores relacionais**.

## 📌 Resumo

| Operador | Equivale a | Uso típico |
| --- | --- | --- |
| `x += v` | `x = x + v` | Acumular, somar ao total |
| `x -= v` | `x = x - v` | Descontar, contar de v em v para baixo |
| `x *= v` | `x = x * v` | Multiplicar acumulando (potências, fatorial) |
| `x /= v` | `x = x / v` | Dividir sucessivamente (conversão para binário) |
| Ordem | O lado direito é calculado primeiro | `x *= 2 + 1` multiplica por 3 |
