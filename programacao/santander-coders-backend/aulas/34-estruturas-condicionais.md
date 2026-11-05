# Estruturas condicionais

> 🗺️ **Nesta aula:** if, if-else e if-else if-else em Java, o switch clássico com break, o efeito "fall-through" e o switch moderno com setas.

## De onde paramos

As estruturas de decisão do pseudocódigo (`se`, `senão`, `escolha`) existem em Java com outros nomes. A condição é sempre uma expressão boolean, montada com os operadores da aula anterior.

## if

Executa o bloco só se a condição for verdadeira.

```java
int idade = 20;

if (idade >= 18) {
  System.out.println("Você é maior de idade.");
}
```

## if-else

Um bloco para verdadeiro e outro para falso.

```java
int idade = 15;

if (idade >= 18) {
  System.out.println("Maior de idade.");
} else {
  System.out.println("Menor de idade.");
}
```

## if-else if-else

Testa as condições em ordem e executa só a primeira verdadeira.

```java
int nota = 80;

if (nota >= 90) {
  System.out.println("Aprovado com A");
} else if (nota >= 80) {
  System.out.println("Aprovado com B");
} else if (nota >= 70) {
  System.out.println("Aprovado com C");
} else {
  System.out.println("Reprovado");
}
```

> ⚠️ Sempre use chaves, mesmo com uma linha só. Sem elas, só a primeira instrução fica dentro do if, e uma linha acrescentada depois roda sempre, mesmo parecendo estar dentro do bloco.

## switch clássico

Compara **uma** expressão com valores exatos. Aceita `int`, `char`, `String` e enums.

```java
int diaDaSemana = 3;
String nomeDia;

switch (diaDaSemana) {
  case 1:
    nomeDia = "Domingo";
    break;
  case 2:
    nomeDia = "Segunda-feira";
    break;
  case 3:
    nomeDia = "Terça-feira";
    break;
  case 4:
    nomeDia = "Quarta-feira";
    break;
  case 5:
    nomeDia = "Quinta-feira";
    break;
  case 6:
    nomeDia = "Sexta-feira";
    break;
  case 7:
    nomeDia = "Sábado";
    break;
  default:
    nomeDia = "Dia inválido";
}

System.out.println("Dia: " + nomeDia);
```

### Por que o break é necessário

Sem `break`, a execução "cai" (fall-through) para o próximo case e continua até achar um `break` ou o fim do switch. Às vezes isso é usado de propósito, para vários casos com o mesmo resultado:

```java
switch (diaDaSemana) {
  case 1:
  case 7:
    System.out.println("Fim de semana");
    break;
  default:
    System.out.println("Dia útil");
}
```

## switch moderno (Java 14+)

Com a seta `->` não existe fall-through, vários valores cabem no mesmo case e o switch pode **devolver um valor**:

```java
int dia = 3;

String tipo = switch (dia) {
  case 1, 7 -> "Fim de semana";
  case 2, 3, 4, 5, 6 -> "Dia útil";
  default -> "Inválido";
};

// Dia útil
System.out.println(tipo);
```

> 💡 Prefira a forma com seta em código novo: é mais curta e elimina o risco de esquecer um break.

## 📝 Exercício

Leia o valor de uma compra e aplique: até R$ 100, sem desconto; de R$ 100,01 a R$ 500, 5%; acima de R$ 500, 10%. Mostre o total.

<details>
<summary>Ver resposta</summary>

```java
import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner in = new Scanner(System.in);
    double valor = in.nextDouble();
    double desconto;

    if (valor > 500) {
      desconto = 0.10;
    } else if (valor > 100) {
      desconto = 0.05;
    } else {
      desconto = 0;
    }

    double total = valor * (1 - desconto);
    System.out.printf("Total: R$ %.2f%n", total);
  }
}
```

Com 300: total R$ 285,00 (o separador decimal segue a configuração do sistema).

</details>

## 🧠 Revisão rápida

**O que acontece se faltar o break num case do switch clássico?**

A execução continua nos cases seguintes (fall-through) até achar um break ou o fim.

**Que tipos o switch aceita?**

int (e os menores: byte, short, char), String, enums e as classes wrapper deles.

> ➡️ **Próximo passo:** trabalhar com textos e datas.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| if / else | Executa um bloco conforme uma condição boolean. |
| else if | Testa várias condições; vale a primeira verdadeira. |
| switch clássico | Compara com valores exatos; precisa de break. |
| switch com -> | Sem fall-through e pode devolver valor. |
