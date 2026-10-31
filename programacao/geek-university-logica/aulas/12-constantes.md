# Constantes

> 🗺️ **Nesta aula:** o que é uma constante e por que usá-la, como declarar em pseudocódigo, Java, C e Python, regras para dar nome e os tipos mais comuns (numérica, texto, booleana e enumerada).

## Definição

Uma **constante** é um nome associado a um valor que **não pode ser alterado** durante a execução do programa. Assim como a variável, tem **nome**, **tipo de dado** e **valor**, mas o valor é definido uma vez, na criação, e depois só pode ser lido.

Por que usar constantes?

- **Legibilidade:** `if (idade >= IDADE_MINIMA)` explica muito mais que `if (idade >= 18)`. Um número solto no código, sem explicação, é chamado de "número mágico".
- **Manutenção:** se o valor mudar (a taxa de juros, por exemplo), altera-se uma linha, não o código inteiro.
- **Segurança:** a linguagem impede que o valor seja modificado por engano.

## Como declarar nas linguagens do curso

```
// Pseudocódigo
Constante PI = 3.14159
Constante IDADE_MINIMA = 18
```

```java
// Java: a palavra-chave final impede reatribuição
public class Constantes {
  static final double PI = 3.14159;
  static final int IDADE_MINIMA = 18;

  public static void main(String[] args) {
    // PI = 3; // ❌ erro de compilação: cannot assign a value to final variable PI
    System.out.println("Área de raio 2: " + PI * 2 * 2);
  }
}
```

```c
// C: duas formas comuns
#include <stdio.h>

#define IDADE_MINIMA 18  // macro: substituída pelo valor antes da compilação
const double PI = 3.14159;  // constante com tipo, verificada pelo compilador

int main(void) {
  printf("Idade mínima: %d\n", IDADE_MINIMA);
  printf("PI: %.5f\n", PI);
  return 0;
}
```

```python
# Python: não existe constante "de verdade".
# Por convenção, nomes em MAIÚSCULAS indicam que o valor não deve ser alterado.
PI = 3.14159
IDADE_MINIMA = 18

print("Idade mínima:", IDADE_MINIMA)
```

> ℹ️ Em Python, nada impede `PI = 3` de funcionar. A constante é um **combinado** entre programadores, sinalizado pelo nome em maiúsculas. Em Java e C, o compilador realmente bloqueia a alteração.

## Princípios para nomear constantes

1. **Use nomes descritivos.** O nome deve dizer o que o valor representa: `TAMANHO_MAXIMO` em vez de `X`.
2. **Use MAIÚSCULAS com sublinhado** (*UPPER_SNAKE_CASE*). É a convenção em Java, C, Python e JavaScript, e separa visualmente constantes de variáveis: `MAXIMO_DE_TENTATIVAS`, `TAXA_DE_JUROS_ANUAL`.
3. **Seja conciso, mas descritivo.** Nem `T` nem `VALOR_DA_TAXA_DE_JUROS_COBRADA_AO_ANO_EM_CONTRATOS`. Evite abreviações obscuras.
4. **Evite nomes genéricos** como `DADO` ou `VALOR`, que não informam nada.
5. **Inclua unidade ou contexto quando necessário:** `TEMPO_LIMITE_SEGUNDOS`, `TAXA_DE_JUROS_ANUAL`. Isso evita confusão entre segundos e milissegundos, ou taxa mensal e anual.
6. **Seja consistente** em todo o código e em toda a equipe.
7. **Não use palavras reservadas** da linguagem (`final`, `const`, `int`…) nem nomes parecidos demais com elas.

> ⚠️ **Correção em relação à versão anterior:** camelCase (`tempoDeEspera`) é a convenção para **variáveis**, não para constantes. Usar o mesmo estilo nas duas faz as constantes parecerem variáveis comuns.

## Tipos comuns de constantes

**Numérica**

```
Constante PI = 3.14159
Constante VELOCIDADE_LUZ_M_S = 299792458
```

**Texto**

```
Constante MENSAGEM_BOAS_VINDAS = "Bem-vindo ao nosso programa!"
Constante NOME_DO_PROGRAMA = "MeuPrograma"
```

**Booleana**

```
Constante MODO_DEPURACAO = falso
```

Uma constante booleana costuma ser uma **configuração** (ligar ou desligar um recurso), e não algo como `VERDADEIRO = true`, que só repete um valor que a linguagem já tem.

**Enumerada**

Um *enum* agrupa um **conjunto fixo de constantes relacionadas**. A variável desse tipo só pode assumir um dos valores listados.

```java
public class ExemploEnum {
  enum DiaDaSemana {
    SEGUNDA, TERCA, QUARTA, QUINTA, SEXTA, SABADO, DOMINGO
  }

  public static void main(String[] args) {
    DiaDaSemana hoje = DiaDaSemana.SEXTA;
    System.out.println("Hoje é " + hoje); // Hoje é SEXTA
    // hoje = "sexta"; // ❌ erro: só aceita valores do enum
  }
}
```

## 📌 Resumo da aula

| Conceito | Lembre |
| --- | --- |
| Constante | nome + tipo + valor que **não muda** durante a execução |
| Por que usar | legibilidade (fim dos "números mágicos"), manutenção em um só lugar, proteção contra alteração |
| Java | `static final double PI = 3.14159;` |
| C | `#define IDADE_MINIMA 18` ou `const double PI = 3.14159;` |
| Python | só convenção: `PI = 3.14159` em maiúsculas |
| Nome | `UPPER_SNAKE_CASE`, descritivo, com unidade quando fizer sentido (`TEMPO_LIMITE_SEGUNDOS`) |
| Enum | conjunto fixo de constantes relacionadas (dias da semana, status) |
