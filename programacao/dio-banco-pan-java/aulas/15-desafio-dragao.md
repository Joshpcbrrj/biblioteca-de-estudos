# Desafio: Dragão

> 🗺️ **Nesta aula:** desafio com vários casos de teste: ler a quantidade de casos e, para cada valor, decidir entre duas mensagens com `if`/`else`. Tente resolver antes de abrir a resolução.

## O que fazer ?

Daenerys é a khaleesi dos Dothraki. Juntamente com Drogon, eles vão atrás do Tyrion, para tentar dominar Westeros. Ela possui, além do seu dragãozinho, um rastreador que mede o nível de energia de qualquer ser vivo. Todos os seres com o nível menor ou igual a 8000, ela considera como se fosse um inseto. Quando passa deste valor, que foi o caso do Drogon, ela se espanta e grita “Mais de 8000”. Baseado nisso, utilize a mesma tecnologia e analise o nível de energia dos seres vivos.

### Entrada

A primeira linha contém um número inteiro **C** relativo ao número de casos de teste. Em seguida, haverá **C** linhas, com um número inteiro **N** (100 <= **N** <= 100000) relativo ao nível de energia de um ser vivo.

### Saída

Para cada valor lido, imprima o texto correspondente.

| Exemplo de Entrada | Exemplo de Saída |
| --- | --- |
| 3 | mais de 8000! |
| 8001 | Inseto! |
| 100 | Inseto! |
| 200 |  |

### Código

<details>
<summary>Ver resposta</summary>

```java
package Dragao;

import java.util.Scanner;

public class Main {
  public static void main(String[] args) {

    int casos, poderDeLuta;

    Scanner ler = new Scanner(System.in);

    casos = ler.nextInt();// lê o número de casos de teste

    for(int i = 0; i < casos; i++){
      poderDeLuta = ler.nextInt(); // lê o nível de energia do ser vivo

      //Implemente a condição adequada para a impressão dos textos conforme o solicitado no desafio:
      if(poderDeLuta > 8000){
        System.out.println("Mais de 8000!");
      } else {
        System.out.println("Inseto!");
      }
    }
  }
}
```

</details>

> 🧮 **Lendo o exemplo:** a primeira linha (`3`) é a quantidade de casos. Depois vêm `8001` → **Mais de 8000!**, `100` → **Inseto!** e `200` → **Inseto!**. A condição é estritamente **maior que** 8000: exatamente 8000 ainda é inseto.

> 🛠️ **Atenção à saída exata:** a tabela de exemplo mostrava "mais de 8000!" em minúsculas e o código imprime "Mais de 8000!". Corretores automáticos comparam o texto **caractere por caractere** — confira maiúsculas, acentos e pontuação no enunciado original da plataforma.

## 📌 Resumo

| Item | O que o desafio pratica |
| --- | --- |
| Casos de teste | a 1ª linha diz quantas leituras vêm depois |
| `for` | repetir a leitura e a decisão para cada caso |
| `>` × `>=` | "mais de 8000" é estritamente maior: 8000 ainda é inseto |
| Saída exata | corretores comparam caractere por caractere |
