# Desafio: Fábrica de carros

> 🗺️ **Nesta aula:** desafio de entrada, cálculo de porcentagem e saída: o preço final de um carro a partir do custo de fábrica, do distribuidor e dos impostos. Tente resolver antes de abrir a resolução.

## O que fazer?

O preço de um carro novo para o consumidor é o **custo de fábrica** somado à **porcentagem do distribuidor** e à **porcentagem dos impostos** — as duas porcentagens aplicadas sobre o custo de fábrica. Escreva um programa que leia esses três valores e imprima o preço final.

### Entrada

Três inteiros: o custo de fábrica, a porcentagem do distribuidor e a porcentagem de impostos.

### Saída

O preço final do carro.

### Exemplos

| Entrada | Cálculo | Saída |
| --- | --- | --- |
| `20000` `28` `45` | 20000 + 28% (5600) + 45% (9000) | `34600` |
| `30000` `10` `10` | 30000 + 10% (3000) + 10% (3000) | `36000` |

> 🛠️ **Ajuste:** nas tabelas originais as entradas estavam emendadas (`200002845`, `300001010`). São **três valores separados**: `20000 28 45` e `30000 10 10`.

> 🧮 **Fórmula:** `preço = custo + custo × distribuidor / 100 + custo × impostos / 100`, ou, simplificando, `custo × (100 + distribuidor + impostos) / 100`.

## Código da resposta

<details>
<summary>Ver resposta</summary>

```java
package fabricadecarros;

import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner scan = new Scanner(System.in);

    int custoFabrica = scan.nextInt();
    int percentualDistribuidor = scan.nextInt();
    int percentualImpostos = scan.nextInt();

    int valorDistribuidor = custoFabrica * percentualDistribuidor / 100;
    int valorImpostos = custoFabrica * percentualImpostos / 100;
    int custoConsumidor = custoFabrica + valorDistribuidor + valorImpostos;

    System.out.println(custoConsumidor);
    scan.close();
  }
}
```

</details>

> 🛠️ **Ajustes no código:** variáveis como `Distribuidor`, `ValorImpostos` e `PercentualImpostos` começavam com maiúscula — em Java isso é reservado para **classes**; variáveis usam camelCase. Também juntei declaração e atribuição numa linha só e fechei o `Scanner`. Como a entrada é inteira, a divisão por 100 é inteira; se os valores pudessem ter centavos, o certo seria usar `double` (ou `BigDecimal`).

## 📌 Resumo

| Item | O que o desafio pratica |
| --- | --- |
| `Scanner.nextInt()` | ler números inteiros da entrada |
| Porcentagem | `valor × percentual / 100`, aplicado sobre o custo de fábrica |
| Divisão inteira | com `int` a divisão descarta os centavos; para dinheiro use `BigDecimal` |
| Nomes | variáveis em camelCase, começando com minúscula |
