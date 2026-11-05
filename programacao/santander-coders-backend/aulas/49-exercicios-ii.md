# Exercícios II

> 🗺️ **Nesta lista:** quatro perguntas sobre protected, polimorfismo, valores padrão e comentários, mais dois desafios sobre coleções e exceções.

## De onde paramos

Esta lista fecha o módulo de POO.

## Questão 1

Para que o modificador de acesso `protected` **não** serve?

<details>
<summary>Ver resposta</summary>

Para dar visibilidade a **qualquer classe de outro pacote**. O protected libera a própria classe, o mesmo pacote e as subclasses (mesmo em outros pacotes), mas não classes de fora que não sejam subclasses.

</details>

## Questão 2

Qual a definição de polimorfismo?

<details>
<summary>Ver resposta</summary>

É o princípio pelo qual classes derivadas de uma mesma superclasse (ou que implementam a mesma interface) respondem à **mesma chamada**, com a mesma assinatura, de **formas diferentes**, cada uma com seu comportamento, usando uma referência do tipo da superclasse.

</details>

## Questão 3

Qual destas frases é verdadeira sobre o valor padrão de uma String?

<details>
<summary>Ver resposta</summary>

Um **atributo** do tipo String (ou uma posição de um array de Strings) que não foi inicializado vale `null`.

</details>

> ⚠️ **Ajuste:** a resposta original dizia apenas "uma variável do tipo String tem seu default como null". Isso vale para atributos e elementos de array. Uma **variável local** não tem valor padrão: usá-la sem atribuir um valor é erro de compilação.

## Questão 4

Qual é uma forma de fazer comentários em Java?

<details>
<summary>Ver resposta</summary>

`// linha comentada`. Existem três formas:

```java
// comentário de uma linha

/* comentário
   de várias linhas */

/**
 * Javadoc: documenta classes e métodos.
 */
```

</details>

## Desafio 1: coleções

Dada uma lista de e-mails com repetidos, mostre quantos e-mails **diferentes** existem.

<details>
<summary>Ver resposta</summary>

```java
List<String> emails = List.of(
  "ana@exemplo.com", "beto@exemplo.com",
  "ana@exemplo.com");
Set<String> unicos = new HashSet<>(emails);
// 2
System.out.println(unicos.size());
```

</details>

## Desafio 2: exceções

O que este código mostra?

```java
try {
  int[] v = new int[3];
  v[3] = 10;
  System.out.println("A");
} catch (ArrayIndexOutOfBoundsException e) {
  System.out.println("B");
} finally {
  System.out.println("C");
}
```

<details>
<summary>Ver resposta</summary>

**B** e depois **C**. O índice 3 não existe num array de tamanho 3, então a exceção acontece antes do "A"; o catch mostra "B" e o finally sempre mostra "C".

</details>

> ➡️ **Próximo passo:** o módulo de banco de dados com PostgreSQL.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 | Modificador protected |
| 2 | Polimorfismo |
| 3 | Valores padrão |
| 4 | Comentários |
| Desafios | Set e try/catch/finally |
