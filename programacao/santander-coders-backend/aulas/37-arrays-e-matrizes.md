# Arrays e matrizes

> 🗺️ **Nesta aula:** como criar e percorrer arrays em Java, matrizes (arrays de duas dimensões), a classe utilitária Arrays (toString, sort) e um algoritmo de maior, menor e média.

## De onde paramos

No módulo de algoritmos vimos array e lista em pseudocódigo. Agora em Java: o array é a estrutura mais básica da linguagem, e as listas (`ArrayList`) aparecem no módulo de POO.

## Array (vetor)

Guarda vários valores do **mesmo tipo** numa variável. O tamanho é **fixo**, definido na criação. O primeiro índice é 0 e o último é `length - 1`.

```java
// criar com tamanho e preencher depois
String[] frutas = new String[5];
frutas[0] = "Maçã";
frutas[1] = "Banana";
frutas[2] = "Laranja";
frutas[3] = "Abacaxi";
// índice 4 = 5 - 1, o último
frutas[4] = "Melancia";

// ou criar já com os valores
int[] numeros = {9, 10, 12, 25, 2};

// percorrer com for-each
for (String fruta : frutas) {
  System.out.println(fruta);
}
```

> 💡 Ao criar com `new`, cada posição recebe um valor padrão: 0 para números, false para boolean e `null` para objetos, como String.

> ⚠️ Acessar `frutas[5]` num array de 5 posições lança `ArrayIndexOutOfBoundsException`. Para percorrer com índice, use sempre `i < frutas.length`, nunca `<=`.

## A classe Arrays

O pacote `java.util` traz a classe `Arrays`, com métodos prontos:

```java
import java.util.Arrays;

public class Main {
  public static void main(String[] args) {
    String[] frutas = {"Maçã", "Banana", "Laranja"};
    int[] c = {5, 3, 8, 1};

    // imprimir o conteúdo: [Maçã, Banana, Laranja]
    System.out.println(Arrays.toString(frutas));

    // ordenar: [1, 3, 5, 8]
    Arrays.sort(c);
    System.out.println(Arrays.toString(c));
  }
}
```

> ⚠️ **Correção:** o exemplo original usava `Arrays.toString` sem o `import java.util.Arrays;` e não compilava.

### Por que precisa do Arrays.toString

Todo objeto Java tem o método `toString()`, chamado automaticamente pelo `println`. Em arrays, a versão padrão devolve algo como `[I@1b6d3586` (tipo + código de memória), que não ajuda. `Arrays.toString` monta o texto com os elementos. Nas suas próprias classes, você pode **sobrescrever** o `toString()` para mostrar o que quiser (módulo de POO).

## Matriz (array de duas dimensões)

É um array de arrays: cada elemento é acessado por **linha** e **coluna**.

![notas[linha][coluna]](../img/java-matriz.svg)

```java
double[][] notas = {
  {7.5, 8.0, 9.0},
  {6.0, 5.5, 7.0},
  {9.5, 9.0, 10.0}
};

for (int i = 0; i < notas.length; i++) {
  double soma = 0;
  for (int j = 0; j < notas[i].length; j++) {
    soma += notas[i][j];
  }
  double media = soma / notas[i].length;
  System.out.printf("Aluno %d: média %.2f%n", i, media);
}
```

Saída: médias 8,17, 6,17 e 9,50. Para imprimir a matriz inteira de uma vez, use `Arrays.deepToString(notas)`.

### Exemplo: escalação em matriz

Uma matriz de Strings com 11 linhas (jogadores) e 2 colunas (nome e posição):

```java
public class Time {
  public static void main(String[] args) {
    // cada linha: {jogador, posição}
    String[][] barca2015 = {
      {"Ter Stegen", "goleiro"},
      {"Daniel Alves", "lateral direito"},
      {"Piqué", "zagueiro"},
      {"Mascherano", "zagueiro"},
      {"Jordi Alba", "lateral esquerdo"},
      {"Busquets", "volante"},
      {"Rakitic", "meio-campo"},
      {"Iniesta", "meia"},
      {"Neymar", "ponta esquerda"},
      {"Messi", "ponta direita"},
      {"Suárez", "centroavante"}
    };

    for (String[] linha : barca2015) {
      System.out.println(linha[0] + " (" + linha[1] + ")");
    }
  }
}
```

> ⚠️ **Ajuste:** o original criava `new String[11][1]`, uma matriz de uma coluna só, que na prática é um array comum, e guardava nome e posição juntos no mesmo texto. Com duas colunas, cada informação fica no seu lugar e pode ser usada separadamente.

## Algoritmo: maior, menor e média

```java
public class Main {
  public static void main(String[] args) {
    int[] numeros = {9, 10, 12, 25, 2};

    int maior = numeros[0];
    int menor = numeros[0];
    int soma = 0;

    for (int n : numeros) {
      if (n > maior) {
        maior = n;
      }
      if (n < menor) {
        menor = n;
      }
      soma += n;
    }

    // converte para double para não perder as casas
    double media = (double) soma / numeros.length;

    // 25
    System.out.println("Maior: " + maior);
    // 2
    System.out.println("Menor: " + menor);
    // 11.6
    System.out.println("Média: " + media);
  }
}
```

> 💡 Começar `maior` e `menor` com o **primeiro elemento**, e não com 0, é o que faz o algoritmo funcionar também com números negativos. A variável que o original chamava `media_num` guardava na verdade a soma; além disso, em Java a convenção é camelCase (`mediaNum`).

## 📝 Exercício

Dado `int[] v = {3, 8, 1, 9, 4}`, crie um novo array com os elementos na ordem inversa e imprima com `Arrays.toString`.

<details>
<summary>Ver resposta</summary>

```java
import java.util.Arrays;

public class Main {
  public static void main(String[] args) {
    int[] v = {3, 8, 1, 9, 4};
    int[] inv = new int[v.length];

    for (int i = 0; i < v.length; i++) {
      inv[i] = v[v.length - 1 - i];
    }

    // [4, 9, 1, 8, 3]
    System.out.println(Arrays.toString(inv));
  }
}
```

</details>

## 🧠 Revisão rápida

**Como saber o tamanho de um array? E de uma String?**

`array.length` (atributo, sem parênteses) e `texto.length()` (método).

**Numa matriz m, o que é m[0].length?**

A quantidade de colunas da linha 0.

> ➡️ **Próximo passo:** organizar o código em métodos.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Array | Tamanho fixo, mesmo tipo, índice de 0 a length − 1. |
| Matriz | Array de arrays: m[linha][coluna]. |
| Arrays.toString | Mostra o conteúdo do array (precisa de import). |
| Arrays.sort | Ordena o array. |
