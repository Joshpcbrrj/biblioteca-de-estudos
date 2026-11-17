# Objetos

> 🗺️ **Nesta aula:** criar objetos literais, acessar e alterar propriedades, métodos, atalhos modernos (propriedades curtas, desestruturação, spread), percorrer objetos e uma primeira olhada em JSON.

## De onde paramos

Arrays guardam listas em ordem. Mas um produto tem nome, preço e estoque, e cada dado tem um significado diferente. Para agrupar dados com nome, usamos objetos.

## O que é um objeto

**Um objeto agrupa dados relacionados em pares de chave e valor.** Ele representa uma "coisa" (uma pessoa, um produto, um pedido) com suas características (**propriedades**) e ações (**métodos**).

![Cada chave aponta para um valor; quando o valor é uma função, chamamos de método.](../img/objeto.svg)

> 💡 **Analogia:** um objeto é como uma ficha cadastral. Cada linha da ficha tem um rótulo (a chave: "Nome", "Idade") e o que foi preenchido (o valor). Um array é uma lista numerada; um objeto é uma ficha com campos nomeados, em que você procura pelo nome do campo, e não pela posição.

## Criando (objeto literal)

Um objeto literal é escrito entre chaves, com pares `chave: valor` separados por vírgula. É a forma mais direta de descrever uma coisa: em vez de três variáveis soltas (`nome`, `idade`, `cidade`), você tem um único objeto `pessoa` que carrega as três. Passar `pessoa` para uma função é passar tudo de uma vez, e isso deixa o código mais curto e mais difícil de errar. Os valores podem ser de qualquer tipo, até outros objetos e arrays.

```jsx
const pessoa = {
  nome: "João",
  idade: 25,
  cidade: "São Paulo",
  // chaves com espaço precisam de aspas
  "nome completo": "João da Silva",
};
```

## Acessando e alterando

Há duas formas de ler uma propriedade. O ponto (`pessoa.nome`) é a mais comum e a mais limpa. Os colchetes (`pessoa["nome completo"]`) servem quando a chave tem espaço ou quando o nome vem de uma variável, como num formulário em que o usuário escolhe qual campo ver. Para alterar ou criar uma propriedade, basta atribuir: `pessoa.idade = 26` muda o valor, e `pessoa.pais = "Brasil"` cria uma chave nova. Ler uma chave que não existe devolve `undefined`, sem erro.

```jsx
// notação de ponto
pessoa.nome;  // "João"
// notação de colchetes
pessoa["nome completo"];  // "João da Silva"

// chave vinda de uma variável
const campo = "cidade";
pessoa[campo];  // "São Paulo"

pessoa.idade = 30;  // altera
pessoa.email = "joao@exemplo.com";  // cria
delete pessoa.cidade;  // remove

pessoa.telefone;  // undefined
"nome" in pessoa;  // true
```

## Métodos e `this`

Quando o valor de uma propriedade é uma função, ela vira um **método**: uma ação que o objeto sabe fazer. Dentro do método, `this` aponta para o objeto que o chamou, então `this.nome` lê o nome daquele objeto. Isso permite que a mesma função se comporte de forma diferente em objetos diferentes. A armadilha é a arrow function: ela não tem um `this` próprio e usa o de fora, então `this.nome` viraria `undefined`. Em métodos de objeto, use sempre a forma curta `saudacao() { ... }`.

```jsx
const pessoa = {
  nome: "João",
  // forma curta de método
  saudacao() {
    console.log(`Olá, eu sou o ${this.nome}!`);
  },
};

pessoa.saudacao();  // "Olá, eu sou o João!"
```

Dentro de um método, `this` é o objeto que chamou o método. Por isso, **não use arrow function como método** quando precisar do `this` (veja a aula anterior).

## Atalhos modernos

```jsx
const nome = "Ana";
const idade = 28;

// propriedades curtas: chave = nome da variável
const usuario = { nome, idade };
// { nome: "Ana", idade: 28 }

// desestruturação, com renomeação e padrão
const { nome: n, cidade = "N/D" } = usuario;

// spread: copiar e mesclar
const atualizado = { ...usuario, idade: 29 };

// encadeamento opcional
usuario.endereco?.rua;  // undefined, sem erro
```

## Percorrendo

Para trabalhar com todas as propriedades, você tem quatro caminhos. O `for...in` visita cada chave. `Object.keys` devolve só as chaves, `Object.values` só os valores e `Object.entries` devolve pares `[chave, valor]`, ótimo para transformar um objeto em lista ou tabela. Num carrinho de compras, por exemplo, `Object.values(precos)` lista os preços, e você pode somá-los com um laço.

```jsx
for (const chave in pessoa) {
  console.log(`${chave}: ${pessoa[chave]}`);
}

Object.keys(pessoa);  // ["nome", "idade", ...]
Object.values(pessoa);  // ["João", 25, ...]
Object.entries(pessoa);  // [["nome", "João"], ...]

for (const [chave, valor] of Object.entries(pessoa)) {
  console.log(chave, valor);
}
```

## Vários objetos com a mesma estrutura

Para criar muitos objetos parecidos, use uma **classe**:

```jsx
// class: molde para criar objetos com nome e idade
class Pessoa {
  constructor(nome, idade) {
    this.nome = nome;
    this.idade = idade;
  }
}

// new cria um objeto novo a partir do molde
const pessoa1 = new Pessoa("João", 25);
const pessoa2 = new Pessoa("Maria", 30);
```

Classes são o assunto do módulo de **POO em JavaScript**.

## JSON

JSON é um formato de texto baseado em objetos JS, usado para trocar dados com APIs:

```jsx
const texto = JSON.stringify({ nome: "Ana", idade: 28 });
// '{"nome":"Ana","idade":28}'

// de volta para objeto
const obj = JSON.parse(texto);
```

Ele é detalhado na aula **JSON e fetch**.

## Exercício

Crie um objeto `carrinho` com uma propriedade `itens` (array vazio) e dois métodos: `adicionar(nome, preco)` e `total()`, que soma os preços.

<details>
<summary>Ver resposta</summary>

```jsx
const carrinho = {
  itens: [],
  adicionar(nome, preco) {
    this.itens.push({ nome, preco });
  },
  total() {
    return this.itens.reduce((s, i) => s + i.preco, 0);
  },
};

carrinho.adicionar("Café", 39.9);
carrinho.adicionar("Bolo", 25);
carrinho.total();  // 64.9
```

</details>

## 🧠 Revisão rápida

**Quando usar colchetes em vez de ponto?**

Quando a chave tem espaço ou caractere especial, ou quando vem de uma variável.

**O que `{ ...usuario, idade: 29 }` faz?**

Cria um objeto novo com as propriedades de `usuario`, trocando a idade.

**Como percorrer chave e valor ao mesmo tempo?**

`for (const [k, v] of Object.entries(obj))`.

> ➡️ **Próximo passo:** o que fazer quando algo dá errado, como um JSON inválido? Veja **Tratamento de erros**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Objeto literal | `{ chave: valor }` |
| Propriedade / método | dado / função do objeto |
| Ponto ou colchetes | `obj.nome` ou `obj["nome"]` |
| `delete` / `in` | remove / testa uma chave |
| Desestruturação | tira propriedades para variáveis |
| Spread | copia e mescla objetos |
| `Object.entries` | lista pares chave e valor |
| JSON | texto para trocar dados |
