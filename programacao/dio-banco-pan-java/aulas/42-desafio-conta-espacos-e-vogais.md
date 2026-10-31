# Desafio conta espaços e vogais

> 🗺️ **Nesta aula:** desafio de manipulação de texto: percorrer uma frase caractere por caractere e contar espaços e vogais. Tente resolver antes de abrir a resolução.

## Desafio

Jorginho é professor do primário e tem 100.000 alunos. Ele precisa de um programa que conte quantos **espaços em branco** e quantas **vogais** existem em uma frase. Ajude-o antes que o prazo do semestre acabe!

## Entrada

Uma frase (string).

## Saída

A quantidade de espaços em branco e de vogais, no formato do exemplo:

| Entrada | Saída |
| --- | --- |
| Amo a DIO | Espacos em branco: 2 Vogais: 5 |
| Esse desafio foi facil | Espacos em branco: 3 Vogais: 10 |
| Navegar nas aguas do teu mar | Espacos em branco: 5 Vogais: 11 |

## Resolução

1. Ler a linha inteira com `nextLine()`.
2. Converter para minúsculas, para que `A` e `a` contem igual.
3. Percorrer **cada caractere** da frase:
  - se for `' '`, somar um ao contador de espaços;
  - se for uma das vogais `a e i o u`, somar um ao contador de vogais.
4. Imprimir os dois contadores.

## Código

<details>
<summary>Ver resposta</summary>

```java
import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    String frase = sc.nextLine().toLowerCase();

    int espacos = 0;
    int vogais = 0;

    for (char c : frase.toCharArray()) {
      if (c == ' ') {
        espacos++;
      } else if ("aeiou".indexOf(c) >= 0) {
        vogais++;
      }
    }

    System.out.println("Espacos em branco: " + espacos + " Vogais: " + vogais);
  }
}
```

</details>

> 🛠️ **Bug na versão anterior:** ela separava a frase com `split(" ")` e contava os espaços como `partes.length - 1`. Mas o `split` **descarta as partes vazias do final**: com espaços no fim da frase (ex.: `"Amo a DIO  "`), a contagem saía menor que a real. Além disso, o `if (c == ' ')` dentro do laço nunca era verdadeiro, porque as palavras já vinham sem espaços. Percorrer a frase original, caractere a caractere, resolve as duas coisas e simplifica o código.

> 💡 Vogais acentuadas (á, ê, õ...) não são contadas por `"aeiou"`. Se precisar delas, use `"aeiouáàâãéêíóôõú"`, ou remova os acentos antes com `java.text.Normalizer`.

## 📌 Resumo

| Item | O que o desafio pratica |
| --- | --- |
| `nextLine()` | ler a frase inteira, com os espaços |
| `toLowerCase()` | contar `A` e `a` da mesma forma |
| `charAt(i)` / `toCharArray()` | percorrer o texto caractere por caractere |
| Dois contadores | um para espaços e outro para vogais, no mesmo laço |
