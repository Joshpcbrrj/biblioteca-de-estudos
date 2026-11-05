# Projeto: caixa eletrônico em pseudocódigo

> 🗺️ **Nesta aula:** um projeto que junta variáveis, decisão, repetição e funções: um caixa eletrônico com menu, escrito em pseudocódigo e traduzido para Java, Python e C.

## De onde paramos

Você já tem todas as peças: variáveis, se/senão, laços e funções. Agora elas se juntam num programa completo.

## O enunciado

Criar um caixa eletrônico que mostra um menu repetidamente até o usuário escolher sair:

1. Mostrar saldo.
2. Efetuar depósito (valor maior que zero).
3. Efetuar saque (só se houver saldo suficiente).
4. Sair.<br />Qualquer outra opção mostra "Opção inválida!".

## Planejando

- Um **laço** mantém o programa rodando enquanto `encerrar` for falso.
- Uma **função** `mostrar_menu` exibe as opções e retorna a escolha.
- Um **se/senão se** (ou escolha/caso) trata cada opção.
- O saldo é um **acumulador**: soma nos depósitos, subtrai nos saques.

## Pseudocódigo

```
funcao mostrar_menu(): texto
  var opcao: texto
  mostrar "[1] Mostrar saldo"
  mostrar "[2] Efetuar depósito"
  mostrar "[3] Efetuar saque"
  mostrar "[4] Sair"
  esperar_digitacao -> opcao
  retornar opcao
fim funcao

inicio principal
  var opcao: texto
  var valor, saldo: inteiro
  var encerrar: lógico
  definir 0 -> saldo
  definir falso -> encerrar

  enquanto (encerrar == falso) faça
    definir mostrar_menu() -> opcao

    se (opcao == "1") então
      mostrar "Saldo: " + saldo
    senão se (opcao == "2") então
      mostrar "Valor a depositar: "
      esperar_digitacao -> valor
      se (valor <= 0) então
        mostrar "Valor inválido"
      senão
        somar saldo, valor -> saldo
        mostrar "Depósito efetuado"
      fim se
    senão se (opcao == "3") então
      mostrar "Valor a retirar: "
      esperar_digitacao -> valor
      se (valor <= 0 ou valor > saldo) então
        mostrar "Saque não permitido"
      senão
        subtrair saldo, valor -> saldo
        mostrar "Saque efetuado"
      fim se
    senão se (opcao == "4") então
      definir verdadeiro -> encerrar
    senão
      mostrar "Opção inválida!"
    fim se
  fim enquanto
fim
```

> ⚠️ **Correções em relação ao original:**
>
> 1. O depósito fazia `somar valor, saldo -> valor`, guardando o resultado em `valor`: o saldo nunca mudava. O certo é guardar em `saldo`. O mesmo valia para o saque.
> 2. A mensagem "Saque efetuado" ficava fora do senão e aparecia até quando o saque era negado. Agora ela só aparece no caminho em que o saque acontece. O erro estava também nas versões em Java, Python e C.
> 3. Faltava fechar as aspas em `mostrar "[1] Mostrar saldo"`.
> 4. Acrescentamos a validação de valores menores ou iguais a zero: sem ela, um "saque" de −50 aumentaria o saldo.

## Teste de uso

Entradas: 2 → 100, 3 → 500, 3 → 30, 1, 9, 4.

```
Valor a depositar: 100
Depósito efetuado
Valor a retirar: 500
Saque não permitido
Valor a retirar: 30
Saque efetuado
Saldo: 70
Opção inválida!
```

## Em Java

**Código**

```java
import java.util.Scanner;

public class Banco {
  // um único Scanner para o programa todo
  static Scanner entrada = new Scanner(System.in);

  public static void main(String[] args) {
    int saldo = 0;
    boolean encerrar = false;

    while (!encerrar) {
      String opcao = mostrarMenu();

      switch (opcao) {
        case "1":
          System.out.println("Saldo: " + saldo);
          break;
        case "2":
          System.out.print("Valor a depositar: ");
          int deposito = lerValor();
          if (deposito <= 0) {
            System.out.println("Valor inválido");
          } else {
            saldo += deposito;
            System.out.println("Depósito efetuado");
          }
          break;
        case "3":
          System.out.print("Valor a retirar: ");
          int saque = lerValor();
          if (saque <= 0 || saque > saldo) {
            System.out.println("Saque não permitido");
          } else {
            saldo -= saque;
            System.out.println("Saque efetuado");
          }
          break;
        case "4":
          encerrar = true;
          break;
        default:
          System.out.println("Opção inválida!");
      }
    }
  }

  static String mostrarMenu() {
    System.out.println("[1] Mostrar saldo");
    System.out.println("[2] Efetuar depósito");
    System.out.println("[3] Efetuar saque");
    System.out.println("[4] Sair");
    System.out.print("Opção: ");
    return entrada.nextLine().trim();
  }

  static int lerValor() {
    int valor = entrada.nextInt();
    // descarta o Enter que ficou na entrada
    entrada.nextLine();
    return valor;
  }
}
```

> ⚠️ O original criava um `new Scanner(System.in)` a cada chamada de função. Cada Scanner guarda parte da entrada num buffer próprio, então dados digitados podem se perder. O certo é ter um único Scanner para o programa. Também trocamos o `if/else if` por `switch`, que aceita `String` desde o Java 7.

## Em Python

**Código**

```python
def mostrar_menu():
  print("[1] Mostrar saldo")
  print("[2] Efetuar depósito")
  print("[3] Efetuar saque")
  print("[4] Sair")
  return input("Opção: ").strip()

def ler_valor(mensagem):
  return int(input(mensagem))

saldo = 0
encerrar = False

while not encerrar:
  opcao = mostrar_menu()

  if opcao == "1":
    print("Saldo:", saldo)
  elif opcao == "2":
    deposito = ler_valor("Valor a depositar: ")
    if deposito <= 0:
      print("Valor inválido")
    else:
      saldo += deposito
      print("Depósito efetuado")
  elif opcao == "3":
    saque = ler_valor("Valor a retirar: ")
    if saque <= 0 or saque > saldo:
      print("Saque não permitido")
    else:
      saldo -= saque
      print("Saque efetuado")
  elif opcao == "4":
    encerrar = True
  else:
    print("Opção inválida!")
```

## Em C

**Código**

```c
#include <stdio.h>

char mostrar_menu(void) {
  char opcao;
  printf("[1] Mostrar saldo\n");
  printf("[2] Efetuar depósito\n");
  printf("[3] Efetuar saque\n");
  printf("[4] Sair\n");
  printf("Opção: ");
  /* o espaço antes de %c pula o Enter anterior */
  scanf(" %c", &opcao);
  return opcao;
}

int ler_valor(void) {
  int valor = 0;
  scanf("%d", &valor);
  return valor;
}

int main(void) {
  int saldo = 0;
  int encerrar = 0;

  while (!encerrar) {
    char opcao = mostrar_menu();

    if (opcao == '1') {
      printf("Saldo: %d\n", saldo);
    } else if (opcao == '2') {
      printf("Valor a depositar: ");
      int deposito = ler_valor();
      if (deposito <= 0) {
        printf("Valor inválido\n");
      } else {
        saldo += deposito;
        printf("Depósito efetuado\n");
      }
    } else if (opcao == '3') {
      printf("Valor a retirar: ");
      int saque = ler_valor();
      if (saque <= 0 || saque > saldo) {
        printf("Saque não permitido\n");
      } else {
        saldo -= saque;
        printf("Saque efetuado\n");
      }
    } else if (opcao == '4') {
      encerrar = 1;
    } else {
      printf("Opção inválida!\n");
    }
  }
  return 0;
}
```

> 💡 As três versões foram testadas com as mesmas entradas e dão a mesma saída. Repare que a lógica é idêntica: o pseudocódigo é a planta, e cada linguagem só muda a sintaxe.

## 📝 Desafio

Acrescente a opção [5] Extrato, que mostra quantos depósitos e quantos saques foram feitos.

<details>
<summary>Ver resposta (pseudocódigo)</summary>

```
// no início
var qtd_depositos, qtd_saques: inteiro
definir 0 -> qtd_depositos
definir 0 -> qtd_saques

// depois de "Depósito efetuado"
somar qtd_depositos, 1 -> qtd_depositos
// depois de "Saque efetuado"
somar qtd_saques, 1 -> qtd_saques

// nova opção
senão se (opcao == "5") então
  mostrar "Depósitos: " + qtd_depositos
  mostrar "Saques: " + qtd_saques
```

Lembre de incluir `[5] Extrato` em `mostrar_menu`.

</details>

> ➡️ **Próximo passo:** medir se um algoritmo é rápido ou lento com a notação Big O.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Laço do menu | Repete até a opção Sair mudar `encerrar` para verdadeiro. |
| Acumulador | O saldo soma depósitos e subtrai saques. |
| Validação | Bloqueia valores ≤ 0 e saques maiores que o saldo. |
| Tradução | Mesma lógica em Java, Python e C. |
