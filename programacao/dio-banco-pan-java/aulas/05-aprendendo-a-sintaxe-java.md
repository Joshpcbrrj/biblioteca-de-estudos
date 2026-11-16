# Aprendendo a sintaxe Java

> 🗺️ **Nesta aula:** como uma classe Java é organizada, os tipos primitivos e as variáveis, os operadores, como declarar métodos, o escopo das variáveis, as palavras reservadas, o Javadoc e como compilar e rodar pelo terminal.

## De onde paramos

Na aula anterior você instalou o JDK e uma IDE. Agora vai escrever o seu primeiro código Java e entender cada parte dele.

### Documentação do professor

🔗 [Table of contents](https://felipe-silva-aguiar.gitbook.io/dio-java/gitbook/summary)

## Anatomia das classes

> Uma classe bem estruturada não quer guerra com ninguém.

> 💡 **Nesta página:** como declarar uma classe, o método `main`, convenções de nomes, indentação, pacotes e boas práticas de nomenclatura (Java Beans).

### De onde paramos

Você já instalou o JDK e sabe rodar um programa. Agora vai ler, peça por peça, como uma classe Java é escrita.

### Criação de classes

- Um programa é escrito combinando **palavras reservadas** da linguagem (`public`, `class`, `int`…) com **nomes que nós escolhemos** para arquivos, classes, atributos e métodos.
- É comum misturar inglês com português no código. Muitos projetos preferem escrever tudo em inglês — o importante é **escolher um idioma e manter**.

#### Sintaxe de declaração de uma classe

![Partes da declaração de uma classe.](../img/cls-declaracao.svg)

> 💡 **Analogia:** a declaração de uma classe é como a capa de um formulário: diz qual é o documento (o nome), quem pode ver (`public`) e onde começam e terminam as informações (as chaves).

- Quase todas as classes começam com `public class`.
- Toda classe precisa de um nome, por exemplo `MinhaClasse`.
- O **nome do arquivo** deve ser **idêntico** ao nome da classe pública: `MinhaClasse.java`.
- Depois do nome vem o **corpo** `{ }`, onde ficam os atributos e métodos.

#### Localizando-se dentro das chaves

![Cada par de chaves delimita um nível: classe, método, bloco.](../img/cls-blocos.svg)

É essencial saber em qual par de chaves `{ }` você está: dentro da classe, dentro de um método ou dentro de um bloco (`if`, `for`…).

> 💡 **Analogia:** pense em caixas dentro de caixas. A classe é a caixa grande, cada método é uma caixa dentro dela, e cada `if` ou `for` é uma caixa ainda menor.

#### O método `main`

![Cada palavra da assinatura do main tem um papel.](../img/cls-main.svg)

> 💡 **Analogia:** o `main` é a porta de entrada de um prédio. A JVM bate nela, e cada palavra da assinatura diz quem pode bater (`public`), que não precisa de um morador para abrir (`static`) e o que ela não devolve (`void`).

- É o **ponto de entrada** do programa: a JVM começa a execução por ele.
- Recomenda-se que **apenas uma classe** da aplicação tenha `main`.
- Sua assinatura é sempre: visibilidade `public`, modificador `static`, retorno `void`, nome `main` e um parâmetro `String[] args`.

> 🛠️ **Correção:** o texto original dizia que o `main` recebe "um array de caracteres". Na verdade `String[]` é um **array de Strings** (textos) — os argumentos passados ao rodar o programa pelo terminal. Um array de caracteres seria `char[]`.

### Padrões de nomenclatura

| Elemento | Convenção | Exemplos |
| --- | --- | --- |
| Arquivo `.java` e classe | **PascalCase**: cada palavra começa com maiúscula; nome igual ao da classe | `Calculadora.java`, `CalculadoraCientifica.java` |
| Variável e método | **camelCase**: primeira letra minúscula, demais palavras com inicial maiúscula | `ano`, `anoFabricacao`, `calcularMedia()` |
| Constante | **SCREAMING_SNAKE_CASE**: tudo maiúsculo, separado por `_` | `PI`, `ESTADOS_BRASILEIROS` |
| Pacote | tudo minúsculo, domínio invertido | `com.suaempresa.conta` |

```java
// arquivo CalculadoraCientifica.java
public class CalculadoraCientifica {

}
```

> 📌 **Constantes:** quando um valor nunca deve mudar, usamos a palavra `final` e escrevemos o nome em maiúsculas.
>
> ```java
> final String BR = "Brasil";
> final double PI = 3.14;
> final int ESTADOS_BRASILEIROS = 27;
> final int ANO_2000 = 2000;
> final String CODIGO_BR = "055";
> ```
>
> Escrever o nome em maiúsculas é só convenção; quem **impede** a alteração é o `final`.

> 🛠️ **Correção no código:** no exemplo original faltavam os `;` no fim de cada linha e o `final` só aparecia na última constante — sem `final`, as demais seriam variáveis comuns que podem mudar.

#### Regras para nomes de variáveis

> ⚠️ - Use apenas letras, números, `_` (underline) e `$`.
> - Comece com letra (preferencialmente), `_` ou `$` — **nunca com número**.
> - Por boa prática, comece com letra **minúscula**.
> - **Sem espaços**.
> - **Não** use palavras reservadas (`int`, `long`, `class`…).
> - O nome deve ser **único** dentro do escopo.

```java
// Declarações INVÁLIDAS
int numero&um = 1; // & não é permitido
int 1numero = 1;  // começa com número
int numero um = 1; // tem espaço
int long = 1;  // palavra reservada

// Declarações VÁLIDAS
int numero$um = 1;
int numero1 = 1;
int numeroUm = 1;
int longo = 1;
```

### Declarando variáveis e métodos

Variáveis e métodos seguem estruturas parecidas:

```java
// Variável: Tipo nome = valor;
int idade = 23;
double altura = 1.62;
Dog spike; // sem valor ainda: é permitido

// Método: TipoRetorno nomeNoInfinitivo(params)
int somar(int numeroUm, int numeroDois)
String formatarCep(long cep)
```

> 💡 A **visibilidade** (`public`, `private`…) também faz parte da declaração, mas será vista mais adiante.

### Indentação

**Indentar** é recuar o código para mostrar sua hierarquia: o que está dentro de quê. O compilador ignora os espaços, mas para quem lê faz toda a diferença.

![A mesma lógica, sem e com indentação.](../img/cls-indent.svg)

> 💡 **Analogia:** é como os tópicos de um resumo: o recuo mostra quais itens estão dentro de qual tópico, sem mudar o conteúdo.

**Sem indentação**

```java
public class BoletimEstudantil {
public static void main(String[] args) {
int mediaFinal = 6;
if(mediaFinal<6)
System.out.println("REPROVADO");
else if(mediaFinal==6)
System.out.println("PROVA MINERVA");
else
System.out.println("APROVADO");
}
}
```

**Com indentação**

```java
public class BoletimEstudantil {
  public static void main(String[] args) {
    int mediaFinal = 6;
    if (mediaFinal < 6)
      System.out.println("REPROVADO");
    else if (mediaFinal == 6)
      System.out.println("PROVA MINERVA");
    else
      System.out.println("APROVADO");
  }
}
```

### Organizando arquivos em pacotes

Conforme o sistema cresce, surgem muitos arquivos. Eles são organizados em **pacotes** (*packages*), que na prática são pastas.

![Estrutura de pastas e o nome qualificado da classe.](../img/cls-pacotes.svg)

> 💡 **Analogia:** é como um arquivo de documentos com pastas. O nome qualificado é o caminho completo até o documento, e dois documentos com o mesmo título podem existir em pastas diferentes.

Com pacotes, cada classe passa a ter dois nomes:

- **Nome simples:** só o nome da classe — `ContaBanco`.
- **Nome qualificado:** pacote + classe — `com.suaempresa.conta.ContaBanco`.

O nome qualificado funciona como um endereço completo: pode haver duas classes `Conta` em pacotes diferentes, sem conflito.

### Java Beans: convenções de escrita

Código legível é aquele que o time (e você mesmo, no futuro) entende sem esforço. Por isso o Java sugere convenções para classes, atributos, métodos e pacotes.

#### Variáveis

- Nome **claro**, sem abreviações sem sentido.
- No **singular**, exceto quando representa um array ou coleção.
- **Um só idioma** em todo o código.

**Não recomendado**

```java
// abreviado, difícil de entender
double salMedio = 1500.23;
// plural para um único e-mail confunde
String emails = "aluno@escola.com";
// mistura de idiomas no nome
String myName = "JOSEPH";
```

**Recomendado**

```java
double salarioMedio = 1500.23;
String email = "aluno@escola.com";
String[] emails = {"aluno@escola.com",
                   "professor@escola.com"};
String meuNome = "JOSEPH";
```

#### Métodos

Nomes de métodos são **verbos** em camelCase e cada método deve ter **uma única responsabilidade**.

```java
somar(int n1, int n2) {}
abrirConexao() {}
concluirProcessamento() {}
findById(int id) {}  // muitos métodos em inglês
// problema: faz duas coisas;
// separe em calcular() e imprimir()
calcularImprimir() {}
```

> ➡️ **Próximo passo:** na próxima página você conhece os tipos primitivos e as variáveis que guardam os dados.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Classe pública | o arquivo tem exatamente o mesmo nome da classe |
| `main` | ponto de entrada: `public static void main(String[] args)` |
| Nomes | PascalCase para classes, camelCase para variáveis e métodos, MAIÚSCULAS_COM_UNDERSCORE para constantes |
| Pacotes | pastas em minúsculas; o nome qualificado é pacote + classe |
| Indentação | recuo que mostra a hierarquia, sem mudar o código |

### 🧠 Revisão rápida

**A classe pública `ContaCorrente` pode ficar no arquivo `conta.java`?**

Não: o arquivo precisa se chamar exatamente `ContaCorrente.java`.

**Qual a convenção para cada nome: `valor total` como variável, como classe e como constante?**

Variável: `valorTotal`. Classe: `ValorTotal`. Constante: `VALOR_TOTAL`.

## Tipos e variáveis

> 🗺️ **Nesta aula:** Java é **fortemente tipado** — toda variável tem um tipo definido. Os 8 tipos primitivos guardam valores simples; todo o resto (String, objetos, arrays) é **referência**.

### De onde paramos

Você já escreve uma classe com um método `main`. Agora vai decidir qual tipo de dado guardar em cada variável.

### Tipos primitivos

O Java tem palavras reservadas para os tipos de dados básicos, chamados **tipos primitivos**.

> 📌 **Os oito tipos primitivos:** `byte`, `short`, `int`, `long`, `float`, `double`, `boolean` e `char`. Eles **não são objetos**: representam o valor bruto. Quando declarados como variáveis locais, ficam diretamente na **stack** (pilha de memória).

![Primitivos guardam o valor; referências apontam para um objeto no heap.](../img/tipos-memoria.svg)

> 💡 **Analogia:** a variável primitiva é uma gaveta com o valor dentro. A variável de referência é uma gaveta com um papel que diz em qual armário (no heap) está o objeto.

#### Inteiros

| Tipo | Memória | Valor mínimo | Valor máximo |
| --- | --- | --- | --- |
| `byte` | 1 byte | -128 | 127 |
| `short` | 2 bytes | -32.768 | 32.767 |
| `int` | 4 bytes | -2.147.483.648 | 2.147.483.647 |
| `long` | 8 bytes | -9.223.372.036.854.775.808 | 9.223.372.036.854.775.807 |

#### Decimais (ponto flutuante)

| Tipo | Memória | Faixa aproximada | Precisão |
| --- | --- | --- | --- |
| `float` | 4 bytes | ±3,4028 × 10³⁸ | 6 a 7 dígitos |
| `double` | 8 bytes | ±1,7976 × 10³⁰⁸ | 15 a 16 dígitos |

#### Outros

| Tipo | Memória | Valores |
| --- | --- | --- |
| `boolean` | depende da JVM | `true` ou `false` |
| `char` | 2 bytes | um caractere Unicode, entre aspas simples: `'A'` |

> 🛠️ **Correção da tabela:** os valores máximos estavam errados — eles são sempre **um a menos** que o módulo do mínimo, porque o zero conta do lado positivo: `short` vai até **32.767**, `int` até **2.147.483.647** e `long` até **9.223.372.036.854.775.807**. Também foram incluídos `boolean` e `char`, que faltavam.

#### Qual tipo usar no dia a dia?

- `float` usa metade da memória do `double`, mas tem pouca precisão (6–7 dígitos), por isso é menos usado.
- `byte` e `short` raramente são necessários hoje — economia de memória quase nunca compensa.
- `long` aparece quando os números passam de cerca de 2 bilhões (ex.: IDs, timestamps em milissegundos).
- **Regra prática:** `int` para inteiros e `double` para decimais.

> 💰 **E dinheiro?** Para valores monetários reais (como num banco), use `BigDecimal`. `double` pode gerar erros de arredondamento: `0.1 + 0.2` dá `0.30000000000000004`.
>
> *Pergunta para fixar: qual tipo usar para a idade de uma pessoa? E para o salário de um funcionário?*

### Declaração de variáveis

Uma **variável** é um nome para um espaço de memória. É composta por **tipo + nome + valor (opcional)**.

```java
// <Tipo> <nomeVariavel> = <valor opcional>;
int idade;  // sem valor
int anoFabricacao = 2021;
double salarioMinimo = 2500.0;
```

> 🛠️ **Correção no código:** o original tinha `double salarioMinimo = 2.500;`. Em Java o ponto é o **separador decimal**, então isso vale **2,5** (dois e meio), não dois mil e quinhentos. O certo é `2500.0` — ou `2_500.0`, usando `_` para facilitar a leitura.

#### Peculiaridades de alguns tipos

```java
public class TipoDados {
  public static void main(String[] args) {
    byte idade = 123;
    short ano = 2021;
    // se começar com zero, o zero se perde!
    int cep = 21070333;
    long cpf = 98765432109L; // sufixo L
    float pi = 3.14F;  // sufixo F
    double salario = 1275.33;
  }
}
```

- Literais `long` terminam com `L` e literais `float` com `F`.
- **CEP e CPF** costumam ter zero à esquerda e não são usados em contas, por isso o ideal é guardá-los como `String`.

> Java é fortemente tipado.

### Variáveis e constantes

- **Variável:** área de memória com um nome e um tipo, cujo valor **pode mudar**. Diferente do JavaScript, em Java é obrigatório declarar o tipo (ou usar `var`, a partir do Java 10, quando o tipo pode ser inferido).
- **Constante:** valor que **não pode** ser alterado depois de atribuído. Usa a palavra `final` e, por convenção, nome em CAIXA ALTA.

> 🛠️ **Ajuste conceitual:** o texto original dizia que toda variável Java é uma "referência (ponteiro)". Isso vale só para **objetos**. Uma variável primitiva guarda o **próprio valor**; uma variável de objeto guarda o **endereço** do objeto (veja a imagem acima).

```java
public class ExemploVariavel {
  public static void main(String[] args) {
    // declaração: tipo + nome + valor
    int numero = 5;

    // reatribuição: o tipo não é repetido
    numero = 10;
    System.out.println(numero); // 10

    // final impede nova atribuição
    final double VALOR_DE_PI = 3.14;

    // ERRO de compilação: é uma constante
    VALOR_DE_PI = 3.15;
  }
}
```

> ➡️ **Próximo passo:** na próxima página você combina essas variáveis com operadores para calcular e comparar.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Inteiros | `byte`, `short`, `int` e `long`, do menor para o maior |
| Decimais | `float` (6 a 7 dígitos) e `double` (15 a 16 dígitos) |
| `boolean` e `char` | `true`/`false` e um caractere Unicode entre aspas simples |
| Dinheiro | use `BigDecimal`, nunca `double` |
| Declaração | tipo + nome + valor opcional |

### 🧠 Revisão rápida

**Qual tipo usar para idade? E para o salário de um funcionário num sistema bancário?**

Idade: `int` (ou `byte`, se quiser economizar). Salário: `BigDecimal`, para evitar erros de arredondamento.

**Por que `long x = 3000000000;` não compila?**

O literal sem sufixo é tratado como `int`, e 3 bilhões passa do máximo do `int`. O certo é `3000000000L`.

**Onde fica o texto "Ana" em `String nome = "Ana";`?**

No heap, como um objeto String. A variável `nome`, na stack, guarda só a referência para ele.

## Operadores

> 🗺️ **Nesta aula:** operadores são símbolos com significado especial para a linguagem: atribuem valores, fazem contas, comparam e combinam condições.

### De onde paramos

Você já guarda valores em variáveis. Agora vai usar operadores para calcular, comparar e combinar condições.

Um programa é um conjunto de instruções que, executadas, produzem um resultado. Quase sempre o fluxo é o mesmo: **receber dados**, **processá-los** com alguma lógica e **apresentar** o resultado. Os operadores são as ferramentas do meio desse caminho.

![Entrada, processamento e saída.](../img/op-ipo.svg)

> 💡 **Analogia:** é uma padaria. A farinha e os ovos são a entrada, a mistura e o forno são o processamento, e o pão pronto é a saída. Os operadores são as ferramentas usadas no meio do caminho.

> ➡️ **Próximo passo:** na próxima página você escreve métodos que recebem parâmetros e devolvem valores.

### 📌 Resumo

| Categoria | Operadores |
| --- | --- |
| Atribuição | `=` `+=` `-=` `*=` `/=` `%=` |
| Aritméticos | `+` `-` `*` `/` `%` |
| Unários | `+` `-` `++` `--` `!` |
| Ternário | `condição ? valorSeTrue : valorSeFalse` |
| Relacionais | `==` `!=` `>` `>=` `<` `<=` |
| Lógicos | `&&` `\|\|` `!` (e as versões sem curto-circuito `&` e `\|`) |

### Atribuição

O símbolo `=` define o valor inicial de uma variável ou sobrescreve o valor atual.

```java
String nome = "Ana";
String time = "Flamengo";
int idade = 22;
double peso = 99.9;
char sexo = 'M';
boolean doadorOrgao = true;
// import java.time.LocalDate;
LocalDate nascimento = LocalDate.of(2001, 5, 10);
```

Existem também as **atribuições compostas**, que operam e atribuem de uma vez: `x += 5` equivale a `x = x + 5`.

### Aritméticos

Fazem operações matemáticas: `+` (adição), `-` (subtração), `*` (multiplicação), `/` (divisão) e `%` (módulo — o **resto** da divisão).

```java
double soma = 10.5 + 15.7;  // 26.2
int subtracao = 113 - 25;  // 88
int multiplicacao = 20 * 7;  // 140
int divisao = 15 / 3;  // 5
int modulo = 18 % 3;  // 0
double r = (10 * 7) + (20 / 4);  // 75.0
```

> ⚠️ **Atenção:**
>
> - Com textos, o `+` faz **concatenação**: `"Olá, " + nome`.
> - Divisão entre dois `int` **descarta a parte decimal**: `7 / 2` dá `3`. Para obter `3.5`, um dos lados precisa ser decimal: `7 / 2.0` ou `(double) 7 / 2`.

### Unários

Atuam sobre **um único** operando: tornam positivo/negativo, incrementam, decrementam ou invertem um booleano.

| Operador | O que faz |
| --- | --- |
| `+` | valor positivo (já é o padrão) |
| `-` | inverte o sinal |
| `++` | soma 1 |
| `--` | subtrai 1 |
| `!` | inverte um booleano |

```java
int numero = 5;

System.out.println(-numero);  // -5

numero++;
System.out.println(numero);  // 6

// pós: imprime 6 e SÓ DEPOIS incrementa
System.out.println(numero++);
System.out.println(numero);  // 7

// pré: incrementa ANTES e imprime 8
System.out.println(++numero);

boolean verdadeiro = true;
System.out.println("Inverteu " + !verdadeiro);
// Inverteu false
```

> 🛠️ **Ajuste nos comentários:** no original, a linha `System.out.println(numero ++)` estava comentada como "imprime 7". Ela imprime **6**: no pós-incremento (`x++`) o valor é usado primeiro e incrementado depois; no pré-incremento (`++x`) incrementa primeiro.

### Ternário

Forma resumida de um `if/else` que **escolhe entre dois valores** em uma única linha.

`<condição> ? <valor se true> : <valor se false>`

```java
int a = 5;
int b = 6;

/* Mesma lógica com if/else:
String resultado;
if (a == b)
  resultado = "verdadeiro";
else
  resultado = "falso";
*/

String resultado = (a == b) ? "verdadeiro"
              : "falso";
System.out.println(resultado); // falso
```

> 🛠️ **Correção no código:** o original declarava `String resultado` duas vezes (erro de compilação: variável já definida), imprimia uma variável `valor` que não existia e misturava `"falso"` com `"false"`.

### Relacionais

Comparam dois valores e retornam um `boolean`.

| Operador | Significado |
| --- | --- |
| `==` | igual a |
| `!=` | diferente de |
| `>` | maior que |
| `>=` | maior ou igual a |
| `<` | menor que |
| `<=` | menor ou igual a |

```java
int n1 = 1;
int n2 = 2;

if (n1 > n2)
  System.out.println("n1 é maior");

if (n1 < n2)
  System.out.println("n1 é menor");  // imprime

if (n1 >= n2)
  System.out.println("n1 é maior ou igual");

if (n1 <= n2)
  System.out.println("n1 é menor ou igual"); // imprime

if (n1 != n2)
  System.out.println("n1 é diferente");  // imprime
```

#### Comparações avançadas: `==` x `equals`

> 📌 - `==` compara o **conteúdo** em primitivos, mas em **objetos** compara a **referência** (se são o mesmo objeto na memória).
> - `equals()` compara o **conteúdo** dos objetos.
>
> Por isso, para comparar `String`, `Integer` e outros objetos, use **sempre** `equals`.

```java
String nome1 = "JAVA";
String nome2 = "JAVA";
// true: literais iguais reaproveitam o
// mesmo objeto no String Pool
System.out.println(nome1 == nome2);

String nome3 = new String("JAVA");
// false: new cria outro objeto
System.out.println(nome1 == nome3);

String nome4 = nome3;
System.out.println(nome3 == nome4); // true

System.out.println(nome1.equals(nome2)); // true
System.out.println(nome2.equals(nome3)); // true
System.out.println(nome3.equals(nome4)); // true
```

```java
int primitivo1 = 130;
int primitivo2 = 130;
// true: primitivos comparam valor
System.out.println(primitivo1 == primitivo2);

Integer objeto1 = 130;
Integer objeto2 = 130;
// false: objetos diferentes
System.out.println(objeto1 == objeto2);
// true: mesmo conteúdo
System.out.println(objeto1.equals(objeto2));
```

> 🛠️ **Correção no código:** o original declarava `numero1` e `numero2` duas vezes no mesmo método (primeiro como `int`, depois como `Integer`), o que não compila; renomeei as variáveis. Curiosidade: com `Integer` entre **-128 e 127** o `==` dá `true`, porque o Java reaproveita esses objetos em cache — mais um motivo para usar sempre `equals`.

### Lógicos

Combinam duas ou mais expressões booleanas.

| Operador | Nome | Resultado `true` quando… |
| --- | --- | --- |
| `&&` | E | **as duas** condições são verdadeiras |
| `\|\|` | OU | **pelo menos uma** é verdadeira |
| `!` | NÃO | a condição é falsa |

```java
boolean condicao1 = true;
boolean condicao2 = false;

if (condicao1 && condicao2)
  System.out.println("As duas são true");

if (condicao1 || condicao2)
  System.out.println("Uma é true"); // imprime
```

#### Curto-circuito: `&&` x `&` e `||` x `|`

> 📌 Os operadores **duplos** (`&&` e `||`) fazem **curto-circuito**: param de avaliar assim que o resultado já está definido.
>
> - `A && B`: se **A for falso**, B nem é avaliado (o resultado já é falso).
> - `A || B`: se **A for verdadeiro**, B nem é avaliado (o resultado já é verdadeiro).
>
> Os **simples** (`&` e `|`) sempre avaliam os dois lados.

```java
int numero1 = 1;
int numero2 = 1;

if (numero1 == 2 & numero2++ == 2)
  System.out.println("As 2 são verdadeiras");

System.out.println("numero1 = " + numero1); // 1
// 2: o lado direito foi avaliado
System.out.println("numero2 = " + numero2);

// Troque & por && e rode de novo: como
// numero1 == 2 é falso, numero2++ NÃO roda
// e numero2 continua 1.
```

> 🛠️ **Correção conceitual:** o texto original dizia que, com `&&`, "se a condição1 atender aos critérios, não é necessário validar a condição2". É o contrário: no `&&`, a segunda condição é pulada quando a primeira é **falsa**; no `||`, quando a primeira é **verdadeira**.

> 💡 Uso prático do curto-circuito: `if (cliente != null && cliente.isAtivo())`. Se `cliente` for nulo, a segunda parte nem é chamada, e o programa não quebra com `NullPointerException`.

### 🧠 Revisão rápida

**Quanto vale `17 % 5`? E `17 / 5` com inteiros?**

`17 % 5` = 2 (o resto). `17 / 5` = 3 (a parte decimal é descartada).

**Com `int x = 3;`, o que imprime `System.out.println(x++ + ++x);`?**

8: `x++` usa 3 (e x vira 4); `++x` faz x virar 5 e usa 5. 3 + 5 = 8.

**Por que comparar Strings com `==` é perigoso?**

Porque `==` compara referências. Duas Strings com o mesmo texto podem ser objetos diferentes; use `equals`.

## Métodos

> Todas as ações de uma aplicação são métodos.

> 🗺️ **Nesta aula:** uma classe é formada por **atributos** (os dados, geralmente variáveis) e **métodos** (as ações, equivalentes a funções ou sub-rotinas).

![As partes da assinatura de um método.](../img/met-anatomia.svg)

> 💡 **Analogia:** a assinatura de um método é como o cabeçalho de um formulário: diz qual é o formulário (o nome), o que precisa ser preenchido (os parâmetros) e o que ele devolve ao final (o tipo de retorno).

### De onde paramos

Você já usa operadores e variáveis dentro do `main`. Agora vai separar essas instruções em métodos com nome, que podem ser reutilizados.

### Como nomear métodos

Não é obrigatório, mas seguir as convenções deixa o código legível para você e para o time:

- O nome deve ser um **verbo** (ação).
- Use **camelCase**: tudo minúsculo, com a inicial de cada palavra a partir da segunda em maiúscula.

```java
somar(int n1, int n2) {}
abrirConexao() {}
concluirProcessamento() {}
findById(int id) {}  // muitos métodos em inglês
// problema: deveria ter uma única finalidade
calcularImprimir() {}
```

> ⚠️ Em Java **não existem métodos globais**: todo método precisa estar dentro de uma classe.

### Como definir um método: 5 perguntas

1. **Qual é a finalidade do método?** Pergunte até entender exatamente o que ele deve fazer — e garanta que seja **uma** coisa só.
2. **Qual o tipo de retorno?** O método devolve algum valor? Se não devolver nada, o tipo é `void`.
3. **Quais parâmetros são necessários?** Que informações ele precisa receber para trabalhar?
4. **Ele pode lançar alguma exceção?** Se algo pode dar errado (ex.: divisão por zero, arquivo inexistente), é preciso prever e tratar.
5. **Qual a visibilidade?** Visível para toda a aplicação (`public`), só para o pacote (padrão), para subclasses (`protected`) ou só para a própria classe (`private`).

### Exemplo

```java
public class MinhaClasse {

    public double somar(int num1, int num2) {
        return num1 + num2; // devolve o resultado
    }

    public void imprimir(String texto) {
        // void: não precisa de return
        System.out.println(texto);
    }

    // throws: avisa que pode lançar exceção
    public double dividir(int dividendo,
                          int divisor)
            throws Exception {
        if (divisor == 0) {
            throw new Exception("Divisor zero");
        }
        return (double) dividendo / divisor;
    }

    // private: só dentro desta classe
    private void metodoPrivado() {}

    // ---- equívocos comuns ----

    public void validar() {
        // validação deveria retornar boolean
    }

    public void calcularEnviar() {
        // faz duas coisas: separe em
        // calcular() e enviar()
    }

    // muitos parâmetros soltos...
    public void gravarCliente(String nome,
            String cpf, String telefone) {}

    // ...ficam melhor agrupados em um objeto
    public void gravar(Cliente cliente) {}
}
```

> 🛠️ **Correções no código:** o exemplo original tinha `return ... ;` e `throws Exception{}` sem corpo nem retorno (não compilam) — completei os métodos. Também troquei `Integer telefone` por `String telefone` (telefone tem zeros e símbolos, não é número para contas) e removi o `....` da lista de parâmetros, que não é sintaxe válida.

> ➡️ **Próximo passo:** na próxima página você descobre onde uma variável existe e onde ela deixa de existir.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Assinatura | visibilidade, tipo de retorno, nome e parâmetros de um método |
| Nome | verbo em camelCase, com uma única responsabilidade |
| `return` | devolve o valor e encerra o método |
| `void` | indica que o método não devolve valor |
| `throws` | avisa que o método pode lançar exceção |

### 🧠 Revisão rápida

**Um método que verifica se um CPF é válido deveria retornar o quê?**

`boolean`: `true` se válido, `false` se não. Nome sugerido: `isCpfValido(String cpf)` ou `validarCpf`.

**Por que `(double) dividendo / divisor` e não só `dividendo / divisor`?**

Os dois são `int`; sem o cast, a divisão descartaria a parte decimal (7 / 2 daria 3).

## Escopo

> 🗺️ **Nesta aula:** escopo é a região do código onde uma variável existe e pode ser usada. Em Java, ele é definido pelo **bloco** `{ }` onde a variável foi declarada.

![Classe, método e bloco: cada nível tem seu escopo.](../img/escopo-niveis.svg)

### De onde paramos

Você já escreve métodos com variáveis locais. Agora vai entender até onde cada variável pode ser usada.

### Como funciona

- A variável passa a existir quando é **declarada** e deixa de existir quando a execução **sai do bloco** onde ela foi criada. Fora desse bloco, ela não pode ser lida nem alterada.
- **Atributos** (declarados no corpo da classe) são visíveis em **todos os métodos** da classe.
- **Variáveis locais** (declaradas dentro de um método) só existem **dentro daquele método**.
- **Variáveis de bloco** (dentro de `for`, `if`, `while`…) só existem **dentro daquele bloco**.
- Regra de ouro: **um bloco interno enxerga as variáveis dos blocos externos, mas nunca o contrário.**

> 💡 **Analogia:** pense numa casa. O que está na sala (atributo) todos os cômodos podem usar; o que está trancado no quarto (variável local) só quem está no quarto vê.

Dominar escopo evita erros estruturais: variáveis "sumindo", valores que não são atualizados e conflitos de nomes.

### Exemplo

```java
public class Conta {
  // atributo: disponível em toda a classe
  double saldo = 10.0;

  public void sacar(double valor) {
    // local: só existe dentro de sacar()
    double novoSaldo = saldo - valor;
    saldo = novoSaldo; // atualiza o atributo
  }

  public void imprimirSaldo() {
    // OK: atributo é visível aqui
    System.out.println(saldo);
    // ERRO: novoSaldo só existe em sacar()
    // System.out.println(novoSaldo);
  }

  public double calcularDivida() {
    double valorParcela = 50.0;
    double valorMontante = 0.0;

    // x: escopo do for
    for (int x = 1; x <= 5; x++) {
      // recriada a cada volta do laço
      double calculado = valorParcela * x;
      valorMontante += calculado;
    }
    // x e calculado NÃO existem aqui fora

    return valorMontante; // 750.0
  }
}
```

> 🛠️ **Correção no código:** no original, `imprimirSaldo()` tentava imprimir `novoSaldo`, o que **não compila** (era a ideia do exemplo, mas a linha estava ativa). Deixei comentada com a explicação. Também fiz `sacar()` atualizar o `saldo` — antes o cálculo era feito e perdido — e troquei `Double` por `double`, mais adequado para um parâmetro simples.

> ➡️ **Próximo passo:** na próxima página você conhece as palavras reservadas, que não podem ser usadas como nome de variável.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Escopo | região do código onde a variável existe, definida pelo bloco `{ }` |
| Atributo | visível em todos os métodos da classe |
| Variável local | existe só dentro do método que a declarou |
| Variável de bloco | existe só dentro do `for`, `if` ou `while` |
| Regra de ouro | um bloco interno enxerga o externo, nunca o contrário |

### 🧠 Revisão rápida

**Por que `calcularDivida()` retorna 750?**

50 × (1 + 2 + 3 + 4 + 5) = 50 × 15 = 750.

**Duas variáveis locais `total`, em métodos diferentes da mesma classe, dão conflito?**

Não: cada uma vive no seu método. Só haveria conflito se estivessem no mesmo escopo.

## Palavras reservadas

> 🗺️ **Nesta aula:** palavras reservadas já têm um significado para a linguagem, então **não podem** ser usadas como nomes de variáveis, classes, métodos ou atributos. Todas são escritas em minúsculas e a IDE costuma destacá-las com uma cor própria.

### De onde paramos

Você já escreveu classes, métodos e variáveis. Agora vai conhecer as palavras que a própria linguagem já usa, e que por isso não podem ser nomes.

### Referência

🔗 [http://www.linhadecodigo.com.br/artigo/83/as-52-palavras-reservadas-do-java.aspx](http://www.linhadecodigo.com.br/artigo/83/as-52-palavras-reservadas-do-java.aspx)

![As palavras reservadas agrupadas por finalidade.](../img/reservadas-grupos.svg)

> 💡 **Analogia:** é como os cargos de uma empresa. Ninguém pode se chamar "gerente" em um crachá se o nome é reservado para a função. Do mesmo modo, palavras como `class` e `int` já têm um papel na linguagem e não servem como nome.

> 🛠️ **Ajuste:** a lista clássica fala em "52 palavras", mas isso inclui os literais `true`, `false` e `null`, que tecnicamente não são *keywords*. Versões mais novas do Java adicionaram `enum` (Java 5) e palavras contextuais como `var`, `record`, `yield` e `sealed`. A tabela de primitivos também dizia que `short` tem 32 bits — o correto é **16 bits**.

### Por grupo

#### Controle de pacotes

| Palavra | Uso |
| --- | --- |
| `package` | Diz a qual pacote as classes do arquivo pertencem |
| `import` | Traz classes de outros pacotes para o código |

#### Modificadores de acesso

| Palavra | Quem acessa |
| --- | --- |
| `public` | Qualquer classe |
| `protected` | Classes do mesmo pacote e subclasses |
| `private` | Apenas a própria classe |

#### Tipos primitivos e `void`

| Palavra | Descrição |
| --- | --- |
| `boolean` | verdadeiro ou falso |
| `byte` | inteiro de 8 bits, com sinal |
| `short` | inteiro de **16** bits, com sinal |
| `int` | inteiro de 32 bits, com sinal |
| `long` | inteiro de 64 bits, com sinal |
| `float` | ponto flutuante de 32 bits |
| `double` | ponto flutuante de 64 bits |
| `char` | um caractere Unicode (16 bits, sem sinal) |
| `void` | indica que o método **não retorna** valor |

#### Modificadores de classes, variáveis e métodos

| Palavra | Uso |
| --- | --- |
| `class` | Declara uma classe |
| `interface` | Declara uma interface |
| `enum` | Declara um conjunto fixo de constantes |
| `extends` | Indica a superclasse que está sendo estendida |
| `implements` | Indica as interfaces que a classe implementa |
| `abstract` | Classe que não pode ser instanciada / método sem corpo que a subclasse deve implementar |
| `final` | Classe não pode ser estendida, método não pode ser sobrescrito, variável não pode ser reatribuída |
| `static` | Membro pertence à **classe**, não aos objetos |
| `new` | Cria um objeto, chamando seu construtor |
| `native` | Método implementado em outra linguagem (ex.: C) |
| `strictfp` | Força regras rígidas de ponto flutuante (sem efeito desde o Java 17) |
| `synchronized` | Só uma thread por vez executa o método/bloco |
| `transient` | Campo ignorado na serialização |
| `volatile` | Variável compartilhada entre threads, sempre lida da memória principal |

#### Controle de fluxo

| Palavra | Uso |
| --- | --- |
| `if` / `else` | Executa um bloco conforme uma condição / o bloco alternativo |
| `switch` / `case` / `default` | Escolhe um bloco conforme o valor de uma variável / caso padrão |
| `for` | Laço com contador |
| `while` | Repete enquanto a condição for verdadeira |
| `do` | Executa uma vez e depois testa a condição (`do…while`) |
| `break` | Sai do laço ou do `switch` |
| `continue` | Pula para a próxima volta do laço |
| `return` | Encerra o método (e pode devolver um valor) |
| `instanceof` | Testa se um objeto é de determinada classe ou interface |

#### Tratamento de erros

| Palavra | Uso |
| --- | --- |
| `try` | Bloco que pode lançar uma exceção |
| `catch` | Bloco que trata a exceção |
| `finally` | Bloco que sempre executa, com ou sem exceção |
| `throw` | **Lança** uma exceção |
| `throws` | **Declara** que o método pode lançar uma exceção |
| `assert` | Verifica uma suposição durante o desenvolvimento |

#### Variáveis de referência

| Palavra | Refere-se a… |
| --- | --- |
| `this` | O próprio objeto atual |
| `super` | A superclasse imediata |

#### Reservadas, mas sem uso

- `const` — não use para constantes; use `static final`.
- `goto` — nunca implementada, por ser considerada prejudicial.

#### Literais reservados

Pela especificação, `null`, `true` e `false` são **literais**, não *keywords* — mas também não podem ser usados como nomes.

### Onde cada palavra aparece

| Uso | Palavras | Observação |
| --- | --- | --- |
| Arquivo | `package`, `import`, `import static` | Sempre no topo do arquivo |
| Classe | `public`  • `final` ou `abstract`  • `extends` / `implements` | `private` e `protected` só em classes internas |
| Método | `public`/`protected`/`private`  • `static`, `final` ou `abstract`  • tipo de retorno ou `void` | `return` para devolver valor |
| Atributo | `public`/`protected`/`private`  • `static` e/ou `final`  • tipo | Tipo pode ser primitivo ou classe |

### Palavras "opostas"

| Palavra | Palavra | Diferença |
| --- | --- | --- |
| `package` | `import` | `package` diz **onde a classe está**; `import` diz **de onde trazer** outra classe (importante quando há classes com o mesmo nome em pacotes diferentes) |
| `extends` | `implements` | `extends`: classe herda de classe (ou interface de interface); `implements`: classe implementa interface |
| `final` | `abstract` | `final` **impede** alterações (herança, sobrescrita, reatribuição); `abstract` **exige** que a subclasse implemente. Se uma classe tem um método abstrato, ela inteira precisa ser abstrata |
| `throws` | `throw` | `throws` **avisa** que o método pode lançar uma exceção; `throw` **lança** a exceção de fato (mais detalhes em Exceções) |

> ➡️ **Próximo passo:** na próxima página você aprende a ler e gerar a documentação com Javadoc.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Palavras reservadas | não servem como nome de variável, classe, método ou atributo |
| Modificadores de acesso | `public`, `protected` e `private` |
| Controle de fluxo | `if`, `switch`, `for`, `while`, `break`, `continue` e `return` |
| Tratamento de erros | `try`, `catch`, `finally`, `throw` e `throws` |
| `throws` × `throw` | `throws` declara na assinatura; `throw` lança |

### 🧠 Revisão rápida

**`int Class = 3;` compila? E `int class = 3;`?**

O primeiro compila (Java diferencia maiúsculas); o segundo não, porque `class` é reservada. Mesmo assim, evite nomes que confundem.

**Qual a diferença entre `throw` e `throws`?**

`throws` vai na assinatura e avisa que o método pode lançar uma exceção; `throw` é o comando que lança a exceção.

## Java Doc

> 🗺️ **Nesta aula:** o Java sempre teve uma **documentação oficial rica**: dá para explorar pacotes, classes e métodos sem escrever uma linha de código. Saber ler documentação é uma das habilidades que mais separam iniciantes de devs avançados.

### De onde paramos

Você já sabe escrever classes com nomes que dizem o que fazem. Agora vai aprender a documentar o código e a ler a documentação oficial do Java.

### Documentação oficial

🔗 [https://docs.oracle.com/en/java/javase/21/docs/api/index.html](https://docs.oracle.com/en/java/javase/21/docs/api/index.html)

🔗 [https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/index.html](https://docs.oracle.com/javase/8/docs/technotes/guides/troubleshoot/index.html)

> 🛠️ **Ajuste de link:** o link original apontava para o guia de *troubleshooting* do Java 8, não para a documentação da API. Mantive-o e adicionei acima o link da **API do Java 21** (versão LTS), onde ficam as classes e métodos documentados.

### Tipos de comentário

```java
// Comentário de uma linha

/* Comentário de
   várias linhas */

/**
 * Comentário de documentação (Javadoc).
 * Começa com /** e é usado para gerar a documentação.
 */
```

### Tags do Javadoc

| Tag | Descrição |
| --- | --- |
| `@author` | Autor / criador |
| `@version` | Versão do recurso |
| `@since` | Versão ou data em que o recurso passou a existir |
| `@param` | Descreve um parâmetro do método |
| `@return` | Descreve o valor retornado |
| `@throws` | Exceção que o método pode lançar |
| `@see` | Referência a outra classe ou método relacionado |
| `@deprecated` | Indica que o recurso não deve mais ser usado |

> 🛠️ **Correção:** a tag é `@author` (em inglês). Com `@autor` o Javadoc não reconhece a informação.

#### Exemplo documentado

```java
/**
 * Realiza operações matemáticas simples.
 *
 * @author Ana Souza
 * @version 1.0
 * @since 2023
 */
public class Calculadora {

    /**
     * Divide dois números inteiros.
     *
     * @param dividendo número a ser dividido
     * @param divisor   número que divide; não pode ser zero
     * @return o resultado da divisão como double
     * @throws ArithmeticException se o divisor for zero
     */
    public double dividir(int dividendo, int divisor) {
        if (divisor == 0) throw new ArithmeticException("Divisor zero");
        return (double) dividendo / divisor;
    }
}
```

### A ferramenta `javadoc`

- O **Javadoc** é um gerador de documentação criado pela Sun que lê os comentários `/** */` do código-fonte e produz páginas **HTML** — exatamente no formato da documentação oficial do Java.
- É o padrão de documentação de classes Java, e as IDEs conseguem gerá-lo automaticamente (e mostrar esses comentários quando você passa o mouse sobre um método).

Gerando a documentação pelo terminal:

```bash
javadoc -encoding UTF-8 -docencoding UTF-8 -charset UTF-8 -d ../docs src/*.java
```

- `-encoding`: codificação dos arquivos `.java`.
- `-docencoding` / `-charset`: codificação do HTML gerado (use UTF-8 para acentos aparecerem corretamente).
- `-d ../docs`: pasta de destino.

> 🛠️ **Correção no comando:** o original usava `-docencoding ISO-8859-1`, o que pode quebrar os acentos no HTML. Com tudo em **UTF-8** o resultado fica consistente. Também troquei o bloco de `java` para `bash`, já que é um comando de terminal.

### Link útil

🔗 [Javadoc](https://pt.wikipedia.org/wiki/Javadoc)

> ➡️ **Próximo passo:** na próxima página você usa o terminal para compilar e executar um programa Java sem a IDE.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `javadoc` | gera documentação em HTML a partir dos comentários `/** */` |
| `@param` | descreve cada parâmetro do método |
| `@return` | descreve o valor devolvido |
| `@throws` | descreve a exceção que o método pode lançar |
| `@author` | nome de quem criou o recurso; a tag é em inglês |

### 🧠 Revisão rápida

**Qual tag do Javadoc descreve o valor devolvido pelo método?**

`@return`. A tag `@param` descreve cada parâmetro, e `@throws` descreve as exceções.

**Por que o comando `javadoc` usa UTF-8 nos parâmetros?**

Para que os acentos dos comentários apareçam corretamente no HTML gerado.

## Terminal

> 🗺️ **Nesta aula:** a IDE é só uma ferramenta de desenvolvimento. Para rodar um programa Java basta ter a **JVM** — e o terminal mostra o que a IDE faz "por baixo dos panos".

### Links úteis

🔗 [https://code.visualstudio.com/docs/java/java-debugging](https://code.visualstudio.com/docs/java/java-debugging)

🔗 [Pass parameters when debugging vscode java. [Note]](https://linuxtut.com/pass-parameters-when-debugging-vscode-java.-note-462e0/)

### Por que aprender a rodar pelo terminal?

- Seus clientes não vão instalar Eclipse ou VS Code para usar o sistema. Com a JVM configurada, o programa pode ser empacotado (ex.: um `.jar`) e executado em qualquer sistema operacional.
- Servidores normalmente não têm interface gráfica: tudo é feito por linha de comando.
- Entender `javac` e `java` ajuda a resolver erros de *classpath* e de compilação.

### A classe de exemplo

Crie o arquivo `MinhaClasse.java`:

```java
public class MinhaClasse {
  public static void main(String[] args) {
    System.out.println(
      "Oi, fui executado pelo Terminal");
  }
}
```

### Onde ficam os arquivos

![O .java fica em src; o .class compilado, em bin.](../img/term-pastas.svg)

> 💡 **Analogia:** é um escritório. A pasta `src` é a mesa com os rascunhos (o código que você escreve), e a pasta `bin` é a prateleira com as cópias prontas para uso (o bytecode).

- Um projeto criado pela IDE tem a pasta do **código-fonte** (`src`) e a pasta de **saída** com os arquivos `.class` (o bytecode). No Eclipse ela se chama `bin`; no IntelliJ, `out`; em projetos Maven, `target/classes`.
- Mesmo usando IDE, é importante saber **onde** estão as classes do projeto. No exemplo: `C:\estudos\dio-trilha-java-basico\java-terminal`.

### Executando pelo terminal

![Compilando e executando a classe no terminal.](../img/term-exec.svg)

> 💡 **Analogia:** o `javac` é um tradutor que transforma o rascunho em uma língua que a JVM entende. A JVM é um ator que lê esse roteiro traduzido e o executa na ordem.

1. Abra o **Prompt de Comando**, o **PowerShell** ou o terminal do VS Code.
2. Vá até a pasta do projeto:

`cd C:\estudos\dio-trilha-java-basico\java-terminal`
3. *(Se ainda não compilou pela IDE)* compile, mandando o `.class` para a pasta `bin`:

`javac -d bin src\MinhaClasse.java`
4. Entre na pasta `bin`:

`cd bin`
5. Execute a classe — informe o nome **sem** a extensão `.class`:

`java MinhaClasse`

> ✨ **Dicas:**
>
> - Sem entrar na pasta: `java -cp bin MinhaClasse` (`-cp` = *classpath*, onde procurar as classes).
> - Desde o Java 11, um arquivo único pode ser executado direto, sem compilar antes: `java src\MinhaClasse.java`.
> - Argumentos depois do nome da classe chegam no `String[] args` do `main`: `java MinhaClasse Ana 25`.

> 🛠️ **Complemento:** o passo a passo original pulava a **compilação** (`javac`), supondo que a IDE já tinha gerado o `.class`. Incluí o comando para que o roteiro funcione também fora da IDE.

> ➡️ **Próximo passo:** com o programa rodando no terminal, volte às estruturas de decisão e escolha caminhos diferentes com `if` e `switch`.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `javac` | compila o `.java` em `.class`, com bytecode |
| `java` | executa a classe pela JVM, informando o nome sem `.class` |
| `-d bin` | define a pasta de saída dos arquivos `.class` |
| `-cp` | indica onde procurar as classes |
| `args` | argumentos da linha de comando, que chegam sempre como texto |

### 🧠 Revisão rápida

**O que acontece com `java MinhaClasse.class`?**

Erro: a JVM procura uma classe chamada "MinhaClasse.class". Informe só o nome: `java MinhaClasse`.

**Em `java MinhaClasse Ana 25`, quanto vale `args[1]`?**

A String `"25"` (os argumentos sempre chegam como texto).

> ➡️ **Próximo passo:** agora que você sabe escrever uma classe, a próxima aula ensina a tomar decisões com `if` e `switch`.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Classe | arquivo `NomeDaClasse.java` com atributos e métodos; nomes em PascalCase |
| Tipos primitivos | `byte`, `short`, `int`, `long`, `float`, `double`, `char`, `boolean` |
| Constante | `final` impede nova atribuição; nome em MAIÚSCULAS |
| Operadores | atribuição, aritméticos, unários, ternário, relacionais e lógicos (`&&` e `\|\|` fazem curto-circuito) |
| Método | tipo de retorno, nome no infinitivo e parâmetros; uma única responsabilidade |
| Escopo | a variável só existe dentro do bloco `{ }` em que foi declarada |
| Javadoc | comentários `/** */` com tags como `@param` e `@return` viram documentação |
| Terminal | `javac Arquivo.java` compila; `java Arquivo` executa |
