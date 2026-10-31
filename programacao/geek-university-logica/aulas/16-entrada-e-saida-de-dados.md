# Entrada e saída de dados

> ✨ **Página nova:** `Leia` e `Escreva` aparecem em todos os algoritmos do curso. Esta página mostra como eles ficam em Python, Java e C, e os cuidados que evitam os erros mais comuns de iniciante.

> 🗺️ **Nesta aula:** ler dados do teclado e mostrar resultados na tela nas três linguagens, converter o texto digitado em número, formatar casas decimais e evitar as armadilhas clássicas (`input` devolve texto, `nextLine` depois de `nextInt`, `&` no `scanf`).

## 1. Visão geral

| Ação | Pseudocódigo | Python | Java | C |
| --- | --- | --- | --- | --- |
| Mostrar texto | `Escreva "Olá"` | `print("Olá")` | `System.out.println("Olá");` | `printf("Olá\n");` |
| Ler um inteiro | `Leia idade` | `idade = int(input())` | `int idade = sc.nextInt();` | `scanf("%d", &idade);` |
| Ler um real | `Leia preco` | `preco = float(input())` | `double preco = sc.nextDouble();` | `scanf("%lf", &preco);` |
| Ler um texto | `Leia nome` | `nome = input()` | `String nome = sc.nextLine();` | `scanf("%49s", nome);` (uma palavra) |
| Mostrar com 2 casas | `Escreva media` | `print(f"{media:.2f}")` | `System.out.printf("%.2f%n", media);` | `printf("%.2f\n", media);` |

> 💡 Boa prática: antes de cada leitura, mostre uma **mensagem** dizendo o que digitar (`Digite sua idade:`). Sem isso, o programa parece travado esperando algo que o usuário não sabe o que é.

## 2. Python

- `input("mensagem")` mostra a mensagem e devolve **sempre um texto** (`str`).
- Para fazer contas, converta: `int(...)` para inteiros e `float(...)` para reais.
- `print` aceita vários valores separados por vírgula; as **f-strings** (`f"...{variavel}..."`) montam frases e formatam números.

**Código exemplo**

```python
nome = input("Seu nome: ")
idade = int(input("Sua idade: "))
altura = float(input("Sua altura em metros (ex.: 1.75): "))

print("Olá,", nome)  # Olá, Ana  (vírgula insere espaço)
print(f"Daqui a 5 anos você terá {idade + 5} anos.")
print(f"Altura: {altura:.2f} m")  # 2 casas decimais
print("a", "b", "c", sep="-")  # a-b-c
print("sem quebra de linha", end="")
```

> ⚠️ **Armadilha:** sem conversão, `input()` + `input()` junta textos. Se o usuário digitar 2 e 3, `input() + input()` resulta em `"23"`, não em `5`. E `float("7,5")` dá erro: o Python usa **ponto** como separador decimal.

## 3. Java

- A leitura usa a classe `Scanner`, criada uma vez no início do programa.
- `nextInt()`, `nextDouble()` e `next()` leem um valor; `nextLine()` lê a linha inteira (nomes com espaço).
- `println` quebra a linha; `printf` formata (`%d` inteiro, `%.2f` real com 2 casas, `%s` texto, `%n` nova linha).

**Código exemplo**

```java
import java.util.Locale;
import java.util.Scanner;

public class EntradaSaida {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in).useLocale(Locale.US);  // aceita 1.75 com ponto

    System.out.print("Sua idade: ");
    int idade = sc.nextInt();
    sc.nextLine();  // descarta o Enter que sobrou (veja o aviso abaixo)

    System.out.print("Seu nome completo: ");
    String nome = sc.nextLine();

    System.out.print("Sua altura: ");
    double altura = sc.nextDouble();

    System.out.printf("%s tem %d anos e %.2f m.%n", nome, idade, altura);
    sc.close();
  }
}
```

> ⚠️ **Armadilha do **`nextLine`**:** `nextInt()` lê o número, mas deixa o **Enter** no buffer. O `nextLine()` seguinte lê esse Enter e devolve um texto vazio, "pulando" a pergunta do nome. A solução é chamar um `sc.nextLine()` extra logo depois do `nextInt()`.

## 4. C

- `printf` mostra textos e valores usando **especificadores de formato**.
- `scanf` lê valores e precisa do **endereço** da variável: `&idade`. Em vetores de `char` (textos), o nome já é o endereço e o `&` não é usado.

| Especificador | Tipo | No `printf` | No `scanf` |
| --- | --- | --- | --- |
| `%d` | `int` | ✅ | ✅ |
| `%f` | `float` / `double` | ✅ (`%.2f` = 2 casas) | `%f` para `float` |
| `%lf` | `double` | ✅ | ✅ (obrigatório para `double`) |
| `%c` | `char` | ✅ | ✅ (use `" %c"` com espaço) |
| `%s` | texto (`char[]`) | ✅ | lê até o primeiro espaço |

**Código exemplo**

```c
#include <stdio.h>

int main(void) {
  int idade;
  double altura;
  char nome[50];

  printf("Seu primeiro nome: ");
  scanf("%49s", nome);  // sem &: o vetor já é um endereço; 49 evita estourar o vetor

  printf("Sua idade: ");
  scanf("%d", &idade);  // & = endereço da variável

  printf("Sua altura: ");
  scanf("%lf", &altura);  // %lf para double

  printf("%s tem %d anos e %.2f m.\n", nome, idade, altura);
  return 0;
}
```

> ⚠️ **Armadilhas do C:** esquecer o `&` no `scanf` de um número faz o programa travar ou guardar lixo. Ler um `double` com `%f` (em vez de `%lf`) gera valores errados. E ao ler um `char` depois de um número, use `" %c"` (com espaço) para pular o Enter que sobrou.

## 5. Exemplo completo nas três linguagens

Problema: ler o preço de um produto e a quantidade, e mostrar o total com 2 casas decimais.

**Pseudocódigo, Python, Java e C**

```
Algoritmo TotalCompra
Início
  Declare preco, total: Real
  Declare qtd: Inteiro
  Escreva "Preço: "
  Leia preco
  Escreva "Quantidade: "
  Leia qtd
  total <- preco * qtd
  Escreva "Total: R$ ", total
Fim
```

```python
preco = float(input("Preço: "))
qtd = int(input("Quantidade: "))
total = preco * qtd
print(f"Total: R$ {total:.2f}")
```

```java
Scanner sc = new Scanner(System.in).useLocale(Locale.US);
System.out.print("Preço: ");
double preco = sc.nextDouble();
System.out.print("Quantidade: ");
int qtd = sc.nextInt();
double total = preco * qtd;
System.out.printf("Total: R$ %.2f%n", total);
```

```c
double preco, total;
int qtd;
printf("Preço: ");
scanf("%lf", &preco);
printf("Quantidade: ");
scanf("%d", &qtd);
total = preco * qtd;
printf("Total: R$ %.2f\n", total);
```

## 📌 Resumo da aula

| Linguagem | Ler | Mostrar | Cuidado principal |
| --- | --- | --- | --- |
| Python | `input()`  • `int()`/`float()` | `print()`, f-string `{x:.2f}` | `input` sempre devolve texto |
| Java | `Scanner`: `nextInt`, `nextDouble`, `nextLine` | `println`, `printf("%.2f%n")` | `nextLine` depois de `nextInt` lê o Enter que sobrou |
| C | `scanf("%d", &x)` | `printf("%.2f\n", x)` | `&` nas variáveis; `%lf` para `double` |
| Todas | mostre uma mensagem antes de cada leitura |  | use ponto como separador decimal |
