# Paradigma estrutural (PE) vs POO

> 🗺️ **Nesta aula:** o que é um paradigma de programação, como funcionam a programação estruturada e a orientada a objetos, o mesmo exemplo nos dois estilos e quando usar cada um.

## De onde paramos

No módulo de JavaScript você escreveu funções e objetos literais, e viu uma primeira classe. Este módulo organiza isso em uma forma de pensar: a **programação orientada a objetos**. Primeiro, vamos compará-la com o estilo que você já usa.

## Dois jeitos de organizar um programa

Um **paradigma** é um estilo de organizar o código. Os dois mais comuns no início da carreira são o **estruturado** (ou procedural) e o **orientado a objetos** (POO). O JavaScript permite os dois e ainda o funcional.

![No estruturado, dados e funções andam separados; na POO, eles vivem juntos no objeto.](../img/pe-vs-poo.svg)

## Programação estruturada

- O código é dividido em **funções** que recebem dados, processam e devolvem resultados.
- A ênfase está na **sequência de passos** (sequência, decisão e repetição).
- Os dados ficam em variáveis ou estruturas separadas e são passados para as funções.
- Simples e direta para scripts, automações e problemas pequenos.

```jsx
let saldo = 1000;

function depositar(saldo, valor) {
  return saldo + valor;
}
function sacar(saldo, valor) {
  return valor <= saldo ? saldo - valor : saldo;
}

saldo = depositar(saldo, 500);
saldo = sacar(saldo, 200);
```

## Programação orientada a objetos

- O código é organizado em **objetos** que juntam **dados** (atributos) e **comportamentos** (métodos).
- **Classes** são os moldes; objetos são as **instâncias**.
- Objetos colaboram chamando métodos uns dos outros.
- Apoia-se em quatro pilares: **encapsulamento, abstração, herança e polimorfismo**.

```jsx
class ContaBancaria {
  // privado: só a classe acessa
  #saldo = 0;

  depositar(valor) {
    this.#saldo += valor;
  }
  sacar(valor) {
    if (valor <= this.#saldo) this.#saldo -= valor;
  }
  get saldo() {
    return this.#saldo;
  }
}

const conta = new ContaBancaria();
conta.depositar(1000);
conta.sacar(200);
conta.saldo;  // 800
```

## Comparação

|  | Estruturada | Orientada a objetos |
| --- | --- | --- |
| Unidade principal | função | objeto (classe) |
| Dados e comportamento | separados | juntos |
| Proteção dos dados | qualquer função altera | só os métodos do objeto |
| Reuso | funções | classes, herança e composição |
| Melhor para | scripts e problemas pequenos | sistemas com muitas entidades e regras |
| Risco | código "espaguete" ao crescer | complexidade desnecessária |

> 💡 Um paradigma não é "melhor" que o outro: cada um encaixa em um tipo de problema. No dia a dia do JavaScript é comum misturar: classes para modelar entidades e funções puras (estilo funcional) para transformar dados.

> ⚠️ **Ajuste:** a tabela original dizia que a POO tem, por definição, "mais reutilização" e "mais facilidade de modificar". Isso depende de um bom design: POO mal aplicada também fica difícil de manter.

## Exercício

Um sistema de biblioteca precisa registrar livros e empréstimos. Liste quais seriam as classes, com dois atributos e dois métodos cada.

<details>
<summary>Ver resposta (uma possibilidade)</summary>

```jsx
class Livro {
  constructor(titulo, autor) {
    this.titulo = titulo;
    this.autor = autor;
    this.disponivel = true;
  }
  emprestar() { this.disponivel = false; }
  devolver() { this.disponivel = true; }
}

class Leitor {
  constructor(nome) {
    this.nome = nome;
    this.livros = [];
  }
  pegar(livro) {
    if (!livro.disponivel) return false;
    livro.emprestar();
    this.livros.push(livro);
    return true;
  }
  devolver(livro) {
    livro.devolver();
    this.livros = this.livros.filter(l => l !== livro);
  }
}
```

Os substantivos do problema (livro, leitor) costumam virar classes; os verbos (emprestar, devolver), métodos.

</details>

## 🧠 Revisão rápida

**O que caracteriza a programação estruturada?**

Funções que recebem dados separados, processam e devolvem resultados.

**O que um objeto junta na POO?**

Dados (atributos) e comportamentos (métodos).

**O JavaScript é estruturado ou orientado a objetos?**

Multiparadigma: permite os dois, além do funcional.

> ➡️ **Próximo passo:** conheça os **Principais pilares de programação orientada a objetos em JavaScript**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Paradigma | estilo de organizar o código |
| Estruturada | funções e dados separados |
| POO | objetos com dados e métodos |
| Classe | molde dos objetos |
| Instância | objeto criado com `new` |
| Multiparadigma | JS combina estilos |
