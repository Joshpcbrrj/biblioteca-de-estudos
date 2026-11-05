# Laços de repetição

> 🗺️ **Nesta aula:** while, do-while, for e for-each em Java, os comandos break e continue, laços aninhados e uma tabuada completa.

## De onde paramos

Os laços `enquanto`, `faça-enquanto` e `para` do pseudocódigo viram `while`, `do-while` e `for` em Java. A lógica é a mesma; muda a sintaxe.

## while

Testa a condição **antes** de cada volta.

```java
int contador = 0;
while (contador < 5) {
  System.out.println("Contador: " + contador);
  contador++;
}
// mostra 0, 1, 2, 3 e 4
```

## do-while

Testa **depois**: o bloco roda pelo menos uma vez. Repare no `;` depois do `while`.

```java
int contador = 0;
do {
  System.out.println("Contador: " + contador);
  contador++;
} while (contador < 5);
```

## for

Inicialização, condição e atualização na mesma linha. Ideal quando se sabe quantas voltas dar.

```java
for (int i = 0; i < 5; i++) {
  System.out.println("i = " + i);
}
```

> 💡 A variável `i` declarada no `for` só existe dentro do laço. Tentar usá-la depois dá erro de compilação.

## for-each

Percorre todos os elementos de um array ou coleção, sem índice.

```java
int[] numeros = {1, 2, 3, 4, 5};
for (int numero : numeros) {
  System.out.println(numero);
}
```

Leia como "para cada `numero` em `numeros`". Ele não dá acesso à posição nem permite trocar o elemento do array; para isso use o `for` comum.

## break e continue

- `break`: sai do laço imediatamente.
- `continue`: pula o resto desta volta e vai para a próxima.

```java
for (int i = 0; i < 10; i++) {
  // para tudo quando i chega a 5
  if (i == 5) {
    break;
  }
  System.out.println(i);
}
// mostra 0 a 4
```

```java
for (int i = 0; i < 10; i++) {
  // pula os pares
  if (i % 2 == 0) {
    continue;
  }
  System.out.println(i);
}
// mostra 1, 3, 5, 7, 9
```

## Laços aninhados: tabuada de 1 a 10

Um laço dentro do outro: para cada volta do externo, o interno roda inteiro.

```java
public class Main {
  public static void main(String[] args) {
    // números de 1 a 10
    for (int i = 1; i <= 10; i++) {
      System.out.println("Tabuada do " + i + ":");

      // multiplicadores de 1 a 10
      for (int j = 1; j <= 10; j++) {
        System.out.println(i + " x " + j + " = " + i * j);
      }

      // linha em branco entre as tabuadas
      System.out.println();
    }
  }
}
```

São 10 × 10 = 100 linhas de conta: laços aninhados sobre n elementos custam O(n²), como vimos em desempenho de algoritmos.

> ⚠️ Num laço aninhado, o `break` só sai do laço **mais interno**. Para sair dos dois, use um rótulo (`externo: for (...)` e `break externo;`) ou uma variável de controle.

## 📝 Exercício

Peça números ao usuário até ele digitar 0 e mostre a soma e a quantidade de números digitados (sem contar o 0).

<details>
<summary>Ver resposta</summary>

```java
import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    int soma = 0;
    int quantidade = 0;
    int n;

    do {
      System.out.print("Número (0 para sair): ");
      n = in.nextInt();
      if (n != 0) {
        soma += n;
        quantidade++;
      }
    } while (n != 0);

    System.out.println("Soma: " + soma);
    System.out.println("Quantidade: " + quantidade);
  }
}
```

O do-while é a escolha natural: é preciso ler pelo menos um número antes de testar.

</details>

## 🧠 Revisão rápida

**Qual laço garante pelo menos uma execução?**

O do-while.

**O que o continue faz?**

Pula o restante da volta atual e segue para a próxima.

> ➡️ **Próximo passo:** guardar muitos valores com arrays e matrizes.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| while | Testa antes; pode não executar. |
| do-while | Testa depois; executa ao menos uma vez. |
| for | Laço com contador numa linha. |
| for-each | Percorre todos os elementos sem índice. |
| break / continue | Sai do laço / pula para a próxima volta. |
