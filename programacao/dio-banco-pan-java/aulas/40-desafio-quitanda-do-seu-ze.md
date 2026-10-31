# Desafio quitanda do seu Zé

> 🗺️ **Nesta aula:** desafio de preço por faixa de peso com desconto condicional: calcular o valor de uma compra de frutas usando `if` e operadores lógicos. Tente resolver antes de abrir a resolução.

## Desafio

Seu Zé vende frutas com a seguinte tabela de preços:

| Fruta | Até 5 kg | Acima de 5 kg |
| --- | --- | --- |
| Morango | R$ 2,50 por kg | R$ 2,20 por kg |
| Maçã | R$ 1,80 por kg | R$ 1,50 por kg |

Se o cliente comprar **mais de 8 kg** de frutas no total **ou** o valor da compra passar de **R$ 25,00**, ele ganha **10% de desconto** sobre o total.

Leia a quantidade (em kg) de morangos e de maçãs e informe o valor a pagar.

## Entrada

A quantidade em kg de morangos e, em seguida, a de maçãs.

## Saída

O valor a ser pago.

| Entrada (morangos, maçãs) | Saída | Conta |
| --- | --- | --- |
| 3, 2 | 11.1 | 3 × 2,50 + 2 × 1,80 = 11,10. Sem desconto. |
| 1, 1 | 4.3 | 2,50 + 1,80 = 4,30. Sem desconto. |
| 5, 5 | 19.35 | 12,50 + 9,00 = 21,50. São 10 kg (mais de 8), então 21,50 × 0,9 = 19,35. |

> 🛠️ **Correção:** a tabela do 3º exemplo estava embaralhada (entradas 5 e 15 com saídas 4.3 e 19.35). A saída 19.35 corresponde à entrada **5 kg de morango e 5 kg de maçã**, como mostra a conta acima. Também corrigido "quintanda" → "quitanda".

## Resolução

1. Ler as duas quantidades.
2. Calcular o preço de cada fruta conforme a faixa (até 5 kg ou acima).
3. Somar os dois preços.
4. Se o total passar de R$ 25,00 **ou** o peso total passar de 8 kg, aplicar 10% de desconto.
5. Imprimir o valor.

## Código

<details>
<summary>Ver resposta</summary>

```java
import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner input = new Scanner(System.in);
    int morangos = input.nextInt();
    int macas = input.nextInt();

    double precoMorango = morangos * (morangos <= 5 ? 2.50 : 2.20);
    double precoMaca = macas * (macas <= 5 ? 1.80 : 1.50);
    double precoTotal = precoMorango + precoMaca;

    if (precoTotal > 25.00 || morangos + macas > 8) {
      precoTotal *= 0.90; // 10% de desconto
    }

    System.out.println(precoTotal);
  }
}
```

</details>

> 💡 O operador ternário `condição ? a : b` substitui o `if/else` quando só se escolhe entre dois valores. O resultado é o mesmo da versão com `if`, que também está correta.

> ⚠️ O `println(double)` imprime o valor "cru" do `double`, o que funciona nos exemplos do desafio. Em outros casos, pode aparecer algo como `13.950000000000001`. Para um valor monetário, formate com `String.format(Locale.US, "%.2f", precoTotal)` ou use `BigDecimal`.

## 📌 Resumo

| Item | O que o desafio pratica |
| --- | --- |
| Preço por faixa | o preço do quilo muda acima de 5 kg |
| `\|\|` (OU) | o desconto vale se o total passar de R$ 25,00 ou o peso passar de 8 kg |
| Desconto | multiplicar por 0.9 aplica 10% de desconto |
| Ordem do cálculo | primeiro o preço de cada fruta, depois a soma, por último o desconto |
