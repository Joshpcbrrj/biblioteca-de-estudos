# Métodos e atributos da classe

> 🗺️ **Nesta aula:** atributos (o estado do objeto) e métodos de instância (o comportamento), a palavra this e a diferença entre membros de instância e static.

## De onde paramos

A classe `Carro` tinha marca, modelo e ano (atributos) e acelerar e frear (métodos). Vamos ver cada parte com calma, com uma classe `Pessoa`.

## Atributos

Os **atributos** (ou campos) são variáveis que guardam o **estado** de cada objeto.

- São declarados dentro da classe, mas fora dos métodos.
- Podem ser de qualquer tipo: `int`, `double`, `String`, outras classes, listas.
- Cada objeto tem a **sua cópia**.
- Se não forem inicializados, recebem um valor padrão: 0, false ou null.

```java
public class Pessoa {
  // atributos
  String nome;
  int idade;
  double altura;
}
```

## Métodos de instância

Os **métodos** definem o **comportamento**. Um método de instância (sem `static`) roda "em nome" de um objeto e enxerga os atributos dele.

```java
public class Pessoa {
  String nome;
  int idade;

  // void: não devolve nada
  public void apresentar() {
    System.out.println("Olá, meu nome é " + nome
        + " e tenho " + idade + " anos.");
  }

  // devolve um boolean calculado a partir do estado
  public boolean ehMaiorDeIdade() {
    return idade >= 18;
  }

  // altera o estado
  public void fazerAniversario() {
    idade++;
  }
}
```

```java
Pessoa p = new Pessoa();
p.nome = "Ana";
p.idade = 17;

p.fazerAniversario();
// Olá, meu nome é Ana e tenho 18 anos.
p.apresentar();
// true
System.out.println(p.ehMaiorDeIdade());
```

> 💡 Boa prática: cada método faz **uma** coisa só, e o nome diz qual. `fazerAniversario()` é melhor que `atualizarDados()` fazendo cinco coisas diferentes.

## A palavra this

Dentro de um método, `this` é o próprio objeto que recebeu a chamada. É usada principalmente para diferenciar um atributo de um parâmetro com o mesmo nome:

```java
public void setNome(String nome) {
  // atributo recebe o parâmetro
  this.nome = nome;
}
```

## Instância × static

|  | De instância | static |
| --- | --- | --- |
| Pertence a | cada objeto | à classe |
| Acesso | `objeto.metodo()` | `Classe.metodo()` |
| Enxerga atributos de instância? | sim | não (não há objeto) |
| Exemplo | `p.apresentar()` | `Math.sqrt(16)` |
| Um atributo `static` é compartilhado por todos os objetos: só existe uma cópia, na classe. Mais detalhes na aula de modelagem. |  |  |

## 📝 Exercício

Na classe `Pessoa`, crie o método `calcularImc(double peso)`, que devolve o IMC usando a altura do objeto (peso ÷ altura²).

<details>
<summary>Ver resposta</summary>

```java
public double calcularImc(double peso) {
  return peso / (altura * altura);
}
```

Com altura 1.75 e peso 70: 70 ÷ 3,0625 ≈ 22,86.

</details>

## 🧠 Revisão rápida

**Onde se declaram os atributos?**

Dentro da classe, fora de qualquer método.

**Um método static pode usar o atributo nome de Pessoa diretamente?**

Não: ele pertence à classe e não está ligado a nenhum objeto, então não há "o nome" para usar.

> ➡️ **Próximo passo:** proteger os atributos com modificadores de acesso, construtores e getters e setters.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Atributo | Variável que guarda o estado de cada objeto. |
| Método de instância | Comportamento que usa e altera o estado do objeto. |
| this | Referência ao próprio objeto. |
| static | Membro da classe, compartilhado, sem objeto. |
