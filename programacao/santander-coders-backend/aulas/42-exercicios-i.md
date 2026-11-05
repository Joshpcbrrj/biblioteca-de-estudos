# Exercícios I

> 🗺️ **Nesta lista:** cinco perguntas sobre tipos primitivos, classe × objeto, public void, break no switch e membros static, mais um desafio de código.

## De onde paramos

Esta lista revisa o módulo de Java e o começo de POO.

## Questão 1

Qual tipo primitivo abrange os valores de −2.147.483.648 a 2.147.483.647?

<details>
<summary>Ver resposta</summary>

**int**: 32 bits, de −2³¹ a 2³¹ − 1.

</details>

## Questão 2

Qual a diferença entre uma classe e um objeto?

<details>
<summary>Ver resposta</summary>

A **classe** é o molde: define os atributos e métodos. O **objeto** é uma instância concreta criada a partir dela com `new`, com valores próprios, que executa os métodos e tem o estado alterado por eles.

</details>

## Questão 3

O que significa usar `public` junto com `void` na assinatura de um método?

<details>
<summary>Ver resposta</summary>

`public`: o método pode ser chamado de qualquer classe. `void`: ele não devolve nenhum valor.

</details>

## Questão 4

Para que serve o `break` no switch?

<details>
<summary>Ver resposta</summary>

Para **sair do switch** depois de executar o case escolhido. Sem ele, a execução continua nos cases seguintes (fall-through). O programa segue normalmente na primeira linha depois do switch.

</details>

## Questão 5

É verdade que as variáveis estáticas são...

<details>
<summary>Ver resposta</summary>

...variáveis que pertencem à **classe** e são **compartilhadas por todos os objetos** dela: só existe uma cópia, acessada por `NomeDaClasse.variavel`.

</details>

## Desafio

Crie a classe `Contador` com um atributo `static int total` que aumenta a cada objeto criado. Crie três objetos e mostre o total.

<details>
<summary>Ver resposta</summary>

```java
public class Contador {
  private static int total = 0;

  public Contador() {
    total++;
  }

  public static int getTotal() {
    return total;
  }
}
```

```java
new Contador();
new Contador();
new Contador();
// 3
System.out.println(Contador.getTotal());
```

</details>

> ➡️ **Próximo passo:** toString, membros static, final e abstract, e como o Java cuida da memória.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 | Tipos primitivos |
| 2 | Classe × objeto |
| 3 | Modificadores e retorno |
| 4 | switch e break |
| 5 e desafio | Membros static |
