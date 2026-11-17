# Classes

> 🗺️ **Nesta aula:** o que é uma classe, a anatomia (campos, construtor e métodos), instâncias com `new`, regras e convenções, e um panorama dos recursos modernos que o módulo detalha a seguir.

## De onde paramos

Os pilares da POO já usaram classes em vários exemplos. Agora vamos olhar a sintaxe com calma, parte por parte.

## O que é uma classe

Sem classes, criar dez usuários significaria escrever dez objetos à mão, cada um com os mesmos campos e as mesmas funções copiadas. Se um campo mudasse, você mudaria dez vezes. A classe resolve isso: você descreve **uma vez** o que todo usuário tem e faz, e depois cria quantos precisar com uma linha cada. É o que torna possível um sistema com milhares de objetos parecidos, como produtos, pedidos e clientes.

**Uma classe é um molde para criar objetos com a mesma estrutura: os mesmos atributos e os mesmos métodos.** Cada objeto criado a partir dela é uma **instância**, com seus próprios valores.

![Uma classe, várias instâncias.](../img/classe-instancias.svg)

> 💡 **Analogia:** a classe é a forma de biscoito; as instâncias são os biscoitos. Todos saem com o mesmo formato (os mesmos atributos e métodos), mas cada um pode ter uma cobertura diferente (os valores). Ter a forma não enche o pote: só o `new` assa um biscoito de verdade.

## Anatomia de uma classe

Leia a classe de cima para baixo. Os campos no topo dão o valor inicial que todo objeto nasce com. O `constructor` roda uma vez, na hora do `new`, e recebe os dados que vão preencher cada objeto, usando `this` para guardá-los, de modo que `this.nome = nome` significa "o nome deste objeto recebe o nome que chegou". Abaixo ficam os métodos, que são as ações. Todo objeto criado enxerga os mesmos métodos, mas guarda os seus próprios dados.

```jsx
class Pessoa {
  // 1. campos com valor inicial (opcional)
  pais = "Brasil";

  // 2. construtor: roda no new
  constructor(nome, idade) {
    this.nome = nome;
    this.idade = idade;
  }

  // 3. métodos (sem a palavra function)
  saudacao() {
    console.log(
      `Olá, sou ${this.nome}, ${this.idade} anos.`
    );
  }

  aniversario() {
    this.idade++;
    console.log(
      `Feliz aniversário! ${this.idade} anos.`
    );
  }
}

// 4. instanciação
const pessoa1 = new Pessoa("João", 25);
const pessoa2 = new Pessoa("Maria", 30);

pessoa1.saudacao();  // Olá, sou João, 25 anos.
pessoa2.aniversario();  // Feliz aniversário! 31 anos.
// cada instância tem os próprios dados
pessoa1.idade;  // 25
```

## Conceitos

| Conceito | O que é |
| --- | --- |
| **Construtor** | `constructor()`, executado no `new`; se não existir, a classe ganha um vazio |
| **Atributos** | os dados de cada instância (`this.nome`) |
| **Métodos** | as ações; ficam no *prototype* e são compartilhados |
| `this` | dentro da classe, a instância em uso |
| **Instância** | objeto criado com `new NomeDaClasse(...)` |

## Regras e convenções

Estas regras evitam erros comuns de quem está começando. O `new` é obrigatório porque é ele quem cria o objeto vazio, liga o `this` a ele e chama o construtor: sem o `new`, nada disso acontece, e o JavaScript avisa com um erro. O PascalCase (primeira letra maiúscula em cada palavra) não é regra da linguagem, mas é um acordo universal que deixa claro, ao ler `new Pedido()`, que `Pedido` é uma classe e não uma função qualquer.

- Nome de classe em **PascalCase** (`ContaBancaria`, `CarrinhoDeCompras`).
- Classes **precisam** de `new`: `Pessoa("João")` sem `new` gera `TypeError`.
- Diferente das funções, classes **não têm hoisting** útil: declare antes de usar.
- O corpo da classe roda em **modo estrito** automaticamente.
- Não coloque vírgulas entre os métodos (não é um objeto literal).

## Recursos modernos

Estes recursos servem para proteger e organizar os dados. O campo `#estoque` com o `#` na frente é **privado**: só o código dentro da classe consegue lê-lo ou alterá-lo, o que impede que alguém de fora coloque um valor absurdo, como estoque negativo. O `static` guarda um dado da classe inteira, como um contador de produtos criados. Cada um aparece com calma nas próximas aulas, então por ora basta reconhecer a sintaxe.

```jsx
class Produto {
  // campo privado
  #estoque = 0;
  // pertence à classe
  static totalCriados = 0;

  constructor(nome, preco) {
    this.nome = nome;
    this.preco = preco;
    Produto.totalCriados++;
  }

  // getter: lido como propriedade
  get disponivel() {
    return this.#estoque > 0;
  }

  repor(qtd) {
    this.#estoque += qtd;
    return this;
  }
}
```

Cada um desses recursos tem a sua aula neste módulo: **atributo estático**, **construtor**, **getters e setters** e **herança**.

## Exercício

Crie a classe `Retangulo` com `largura` e `altura` no construtor e os métodos `area()` e `perimetro()`. Crie duas instâncias e mostre a área de cada uma.

<details>
<summary>Ver resposta</summary>

```jsx
class Retangulo {
  constructor(largura, altura) {
    this.largura = largura;
    this.altura = altura;
  }
  area() {
    return this.largura * this.altura;
  }
  perimetro() {
    return 2 * (this.largura + this.altura);
  }
}

const r1 = new Retangulo(4, 5);
const r2 = new Retangulo(10, 2);
console.log(r1.area(), r2.area());  // 20 20
console.log(r1.perimetro());  // 18
```

</details>

## 🧠 Revisão rápida

**Qual a diferença entre classe e instância?**

A classe é o molde; a instância é um objeto criado a partir dele.

**O que acontece se chamar uma classe sem `new`?**

`TypeError`.

**Os métodos são copiados para cada instância?**

Não. Ficam no prototype e são compartilhados.

> ➡️ **Próximo passo:** e quando um dado pertence à classe, e não a cada objeto? Veja **Atributo estático da classe**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `class` | molde de objetos |
| `constructor` | prepara cada instância no `new` |
| Método | função da classe, compartilhada |
| `this` | a instância atual |
| `#campo` | atributo privado |
| PascalCase | convenção para nomes de classe |
