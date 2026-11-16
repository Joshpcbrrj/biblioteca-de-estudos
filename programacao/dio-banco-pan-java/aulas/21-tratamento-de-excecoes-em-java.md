# Tratamento de exceções em Java

> 🗺️ **Nesta aula:** o que é uma exceção, a hierarquia `Error` / checked / unchecked, os blocos `try/catch/finally`, try-with-resources, `throw` × `throws` e como criar exceções próprias.

> 💡 Uma **exceção** é um evento inesperado que interrompe o fluxo normal do programa: dividir por zero, abrir um arquivo que não existe, converter "abc" em número… Tratar exceções é decidir **o que o programa faz quando algo dá errado**, em vez de simplesmente quebrar.

> 💡 **Analogia:** o `try` é o trapezista; o `catch` é a rede de proteção embaixo; o `finally` é a equipe que guarda o equipamento no fim do número, tenha ele dado certo ou não.

## De onde paramos

Até aqui os programas funcionam só no caminho feliz. Agora você vai decidir o que acontece quando algo sai do esperado.

## Palavras reservadas

| Palavra | Para que serve |
| --- | --- |
| `try` | Envolve o código que pode lançar uma exceção. |
| `catch` | Captura e trata um tipo específico de exceção. |
| `finally` | Bloco opcional que roda com ou sem exceção (ideal para liberar recursos). |
| `throw` | **Lança** uma exceção explicitamente. |
| `throws` | **Declara** na assinatura que o método pode lançar exceções. |

## Hierarquia de exceções

Todas as exceções descendem de `Throwable`, que se divide em dois ramos: `Error` e `Exception`.

![Throwable se divide em Error e Exception; RuntimeException é o ramo das unchecked.](../img/exc-hierarquia.svg)

### 🔴 Error

- Indica problemas graves no ambiente de execução (falta de memória, estouro de pilha). Em geral, o programa **não consegue se recuperar**.
- Não se costuma tratar `Error` — a correção está no código ou na configuração da JVM, não num `catch`.

### 🟠 Unchecked exceptions (não verificadas)

- Herdam de `RuntimeException` (e, tecnicamente, `Error` também é não verificado).
- O compilador **não obriga** a capturar nem a declarar.
- Se ocorrerem e ninguém tratar, o programa termina com o *stack trace* no console.
- Normalmente indicam **erro de lógica** e podem ser evitadas com código correto: checar `null`, validar índices, não dividir por zero.
- Exemplos: `ArithmeticException`, `NullPointerException`, `NumberFormatException`, `ArrayIndexOutOfBoundsException`.

### 🔵 Checked exceptions (verificadas)

- Herdam de `Exception`, mas **não** de `RuntimeException`.
- O compilador impõe a regra **"capture ou declare"**: todo método que pode lançá-las precisa de um `try/catch` ou de um `throws` na assinatura. Caso contrário, o código **não compila**.
- Representam situações externas que fogem do controle do programa: arquivo inexistente, rede fora do ar, banco indisponível.
- Exemplos: `IOException`, `FileNotFoundException`, `SQLException`.

> 💡 **Regra de bolso:** se o problema é **culpa do programador** (índice errado, `null`), é unchecked — conserte o código. Se é **culpa do mundo lá fora** (arquivo, rede), é checked — o compilador obriga você a ter um plano B.

### ✨ Exceções personalizadas

- Você pode criar suas próprias exceções para representar problemas do **seu domínio** (ex.: `SaldoInsuficienteException`).
- Basta estender uma classe existente: `Exception` para criar uma checked ou `RuntimeException` para criar uma unchecked.
- **Antes de criar**, verifique se a biblioteca do Java já tem uma exceção adequada (`IllegalArgumentException`, `IllegalStateException`…). Não reinvente a roda.

## Blocos try / catch / finally

![Com exceção, a execução salta para o catch; sem exceção, vai direto ao finally.](../img/exc-fluxo.svg)

**try**

- Contém o código que pode lançar a exceção.
- Assim que uma exceção ocorre, o resto do `try` é **pulado**.
- Não existe sozinho: precisa de pelo menos um `catch` ou de um `finally`.

**catch**

- Recebe como parâmetro o tipo de exceção que sabe tratar e só roda se esse tipo (ou subtipo) for lançado.
- Pode haver vários `catch`; executa **apenas o primeiro** compatível.
- Coloque sempre do **mais específico para o mais genérico**. Se `Exception` vier primeiro, ela captura tudo e os `catch` seguintes nunca são alcançados — o compilador acusa erro.
- Para tratar tipos diferentes da mesma forma, use o **multi-catch**: `catch (NumberFormatException | ArithmeticException e)`.

**finally**

- Opcional. Executa **com ou sem exceção** — até se houver um `return` no `try`.
- Só deixa de rodar se a JVM for encerrada antes (ex.: `System.exit(0)`).
- Pode conter outros blocos `try/catch/finally`.

> ⚠️ Nunca deixe um `catch` vazio (`catch (Exception e) {}`). O erro some sem deixar rastro e fica muito difícil descobrir por que o programa se comporta errado. No mínimo, registre a mensagem.

### try-with-resources (Java 7+)

Para recursos que precisam ser fechados (arquivos, conexões, `Scanner`), prefira declará-los no próprio `try`. Eles são fechados automaticamente, mesmo se houver exceção — dispensa o `finally` só para chamar `close()`.

```java
try (BufferedReader br = new BufferedReader(
    new FileReader("dados.txt"))) {
  System.out.println(br.readLine());
} catch (IOException e) {
  System.out.println("Falha ao ler: "
    + e.getMessage());
}
// br.close() é chamado automaticamente
```

## throw x throws

**throws** — na assinatura do método

- Avisa a quem chama que o método pode lançar aquelas exceções.
- Obrigatório apenas para exceções **checked**.
- Quem chama precisa tratar (`try/catch`) ou repassar (outro `throws`).

**throw** — dentro do código

- Lança explicitamente uma exceção: `throw new IllegalArgumentException("idade negativa");`
- Muito usado com exceções personalizadas e para validar parâmetros.

> 🔎 **O que acontece depois de um** `throw`**?** O fluxo normal para na hora. A JVM procura um `catch` compatível no `try` mais próximo; se não achar, sobe para o método que chamou, e assim por diante (*propagação pela pilha de chamadas*). Se ninguém tratar, o manipulador padrão imprime o *stack trace* e encerra a thread.

## Exemplo geral

```java
import java.util.Scanner;

public class Main {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    try {
      System.out.println("Número inteiro:");
      // NumberFormatException
      int numero =
        Integer.parseInt(sc.nextLine());

      System.out.println("Divisor:");
      int divisor =
        Integer.parseInt(sc.nextLine());
      // ArithmeticException se divisor = 0
      int resultado = numero / divisor;
      System.out.println("= " + resultado);

      int[] nums = new int[5];
      // ArrayIndexOutOfBoundsException
      // se resultado < 0 ou > 4
      nums[resultado] = 2;
      System.out.println("Posição "
        + resultado);

    } catch (NumberFormatException e) {
      System.out.println("Digite um inteiro.");
    } catch (ArithmeticException e) {
      System.out.println("Divisão por zero.");
    } catch (ArrayIndexOutOfBoundsException e) {
      System.out.println("Índice inválido.");
    } catch (Exception e) {
      // sempre por último: pega o resto
      System.out.println("Erro inesperado: "
        + e.getMessage());
    } finally {
      sc.close();
      System.out.println("Fim do programa.");
    }
  }
}
```

> 🛠️ **Ajustes no exemplo geral:**
>
> - Faltava o `import java.util.Scanner;`, então o código não compilava.
> - A linha `10 / 0` lançava a exceção sempre, deixando o teste do array inalcançável. Agora o divisor e o índice dependem da entrada, e cada `catch` pode ser exercitado.
> - O `Scanner` passou a ser fechado no `finally`.

## Análise de cada caso

**Código — unchecked exception**

```java
package tratamentoerros.uncheckedexceptions;

import javax.swing.*;

public class Main {

  public static void main(String[] args) {
    boolean continuar = true;

    do {
      String a = JOptionPane
        .showInputDialog("Numerador: ");
      String b = JOptionPane
        .showInputDialog("Denominador: ");

      try {
        int r = dividir(Integer.parseInt(a),
                Integer.parseInt(b));
        System.out.println("Resultado: " + r);
        continuar = false;
      }
      // digitou algo que não é inteiro
      catch (NumberFormatException e) {
        // pilha de chamadas no console
        e.printStackTrace();
        JOptionPane.showMessageDialog(null,
          "Só números inteiros. "
          + e.getMessage());
      }
      // denominador igual a zero
      catch (ArithmeticException e) {
        e.printStackTrace();
        JOptionPane.showMessageDialog(null,
          "Denominador não pode ser 0. "
          + e.getMessage());
      }
      finally {
        System.out.println("Passou no finally");
      }
    } while (continuar);

    System.out.println("O código continua...");
  }

  public static int dividir(int num, int den) {
    return num / den;
  }
}
```

**Código — checked exception**

```java
package tratamentoerros.checkedexception;

import javax.swing.*;
import java.io.*;

public class Main {
  public static void main(String[] args) {
    String arquivo = "romances.txt";
    try {
      imprimirArquivo(arquivo);
    }
    // subtipo de IOException: vem antes
    catch (FileNotFoundException e) {
      e.printStackTrace();
      JOptionPane.showMessageDialog(null,
        "Arquivo não encontrado: "
        + e.getMessage());
    }
    // outro problema de leitura/escrita
    catch (IOException e) {
      e.printStackTrace();
      JOptionPane.showMessageDialog(null,
        "Erro inesperado. Fale com o "
        + "suporte. " + e.getMessage());
    }
    finally {
      System.out.println("Passou no finally");
    }

    System.out.println("O programa continua...");
  }

  // "throws" repassa as exceções
  // para quem chamar o método
  public static void imprimirArquivo(
      String nome) throws IOException {
    try (BufferedReader br = new BufferedReader(
        new FileReader(nome))) {
      BufferedWriter bw = new BufferedWriter(
        new OutputStreamWriter(System.out));
      String linha;
      while ((linha = br.readLine()) != null) {
        bw.write(linha);
        bw.newLine();
      }
      bw.flush();
    }
  }
}
```

**Código — exceção personalizada**

**1º estudo — arquivo não encontrado**

```java
package tratamentoerros.customexception;

import javax.swing.*;
import java.io.*;

public class Main {
  public static void main(String[] args) {
    String nome = JOptionPane
      .showInputDialog("Nome do arquivo: ");

    imprimirArquivo(nome);
    System.out.println("\nO programa continua...");
  }

  public static void imprimirArquivo(
      String nome) {
    try (BufferedReader br = lerArquivo(nome)) {
      BufferedWriter bw = new BufferedWriter(
        new OutputStreamWriter(System.out));
      String linha;
      while ((linha = br.readLine()) != null) {
        bw.write(linha);
        bw.newLine();
      }
      bw.flush();
    }
    // nossa exceção, com mensagem amigável
    catch (ArquivoIndisponivelException e) {
      JOptionPane.showMessageDialog(
        null, e.getMessage());
    } catch (IOException e) {
      JOptionPane.showMessageDialog(null,
        "Erro inesperado. Fale com o "
        + "suporte. " + e.getMessage());
      e.printStackTrace();
    }
  }

  public static BufferedReader lerArquivo(
      String nome)
      throws ArquivoIndisponivelException {
    File file = new File(nome);
    try {
      return new BufferedReader(
        new FileReader(file));
    } catch (FileNotFoundException e) {
      // "traduz" a exceção técnica para uma
      // do nosso domínio, guardando a causa
      throw new ArquivoIndisponivelException(
        file.getName(),
        file.getAbsolutePath(), e);
    }
  }
}

class ArquivoIndisponivelException
    extends Exception {
  private final String nomeArquivo;
  private final String diretorio;

  public ArquivoIndisponivelException(
      String nomeArquivo, String diretorio,
      Throwable causa) {
    super("O arquivo " + nomeArquivo
      + " não foi encontrado em "
      + diretorio, causa);
    this.nomeArquivo = nomeArquivo;
    this.diretorio = diretorio;
  }

  public String getNomeArquivo() {
    return nomeArquivo;
  }
  public String getDiretorio() {
    return diretorio;
  }
}
```

**2º estudo — divisão não exata**

```java
package tratamentoerros.customexception;

import javax.swing.*;

public class Main {
  public static void main(String[] args) {
    int[] nums = {4, 5, 8, 10, 9};
    int[] dens = {2, 4, 0, 2, 8};

    for (int i = 0; i < nums.length; i++) {
      try {
        int r = dividirExato(nums[i], dens[i]);
        System.out.println(nums[i] + " / "
          + dens[i] + " = " + r);
      } catch (DivisaoNaoExataException e) {
        JOptionPane.showMessageDialog(
          null, e.getMessage());
      } catch (ArithmeticException e) {
        JOptionPane.showMessageDialog(
          null, "Não divida por zero.");
      }
    }
    System.out.println("O programa continua...");
  }

  public static int dividirExato(int num,
      int den)
      throws DivisaoNaoExataException {
    // se den = 0, o % já lança
    // ArithmeticException
    if (num % den != 0) {
      throw new DivisaoNaoExataException(
        "Divisão não exata!", num, den);
    }
    return num / den;
  }
}

class DivisaoNaoExataException
    extends Exception {
  private final int numerador;
  private final int denominador;

  public DivisaoNaoExataException(
      String msg, int num, int den) {
    super(msg + " " + num + " / " + den
      + " deixa resto.");
    this.numerador = num;
    this.denominador = den;
  }

  public int getNumerador() {
    return numerador;
  }
  public int getDenominador() {
    return denominador;
  }
}
```

> 🛠️ **Ajustes nos estudos de caso:**
>
> - **Leitura de arquivo (checked e 1º estudo):** o `do/while` escrevia a primeira linha antes de testar se ela era `null` — com arquivo vazio, `bw.write(null)` gerava `NullPointerException`. Troquei por `while ((linha = br.readLine()) != null)`. O `BufferedReader` não era fechado quando ocorria erro; agora usa **try-with-resources**. `new FileReader(file.getName())` descartava o caminho do arquivo; agora usa o próprio `File`.
> - **Exceção personalizada:** passou a guardar a **causa** original (`FileNotFoundException`) e a mostrar o caminho absoluto. O nome `ImpossivelAberturaDeArquivoException` foi encurtado para `ArquivoIndisponivelException`.
> - **2º estudo:** a classe `DivisaoNaoExataExecption` (com erro de digitação) não existia no código; criei `DivisaoNaoExataException`. A regra testava se o *numerador* era ímpar, e não se a divisão era exata (`numerador % denominador`). Os arrays tinham tamanhos diferentes (4 e 5), o que gerava `ArrayIndexOutOfBoundsException`, e o denominador 0 não era tratado — agora há um `catch (ArithmeticException)`.
> - Nomes de métodos e pacotes ajustados para a convenção Java (`dividir`, `imprimirArquivo`, pacotes em minúsculas) e mensagens corrigidas.

## 🔗 Referências

- [DevMedia — Trabalhando com exceções em Java](https://www.devmedia.com.br/trabalhando-com-excecoes-em-java/27601)
- [Vídeo — Tratamento de exceções](https://www.youtube.com/watch?v=ld2C4GcAtsg&t=296s)
- [ProgramCreek — Hierarquia das classes de exceção](https://www.programcreek.com/2009/02/diagram-for-hierarchy-of-exception-classes/)
- [Projeto Java Web — aula sobre exceções](https://www.projetojavaweb.com/certificado-aluno/plataforma-curso/aulaatual/467726283/idcurso/1/idvideoaula/161)
- [Oracle Docs — Error](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/Error.html)
- [Oracle Docs — Exception](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/Exception.html)
- [Oracle Docs — RuntimeException](https://docs.oracle.com/en/java/javase/11/docs/api/java.base/java/lang/RuntimeException.html)

> ➡️ **Próximo passo:** na próxima aula você conhece o Maven, a ferramenta que organiza o build e as dependências de um projeto Java.

## 🧠 Revisão rápida

**`NullPointerException` é checked ou unchecked?**

Unchecked: herda de `RuntimeException`. O compilador não obriga a tratar.

**Por que `catch (Exception e)` não pode vir antes de `catch (IOException e)`?**

Porque `Exception` captura tudo, tornando o `catch` seguinte inalcançável — o código não compila.

**O `finally` roda se o `try` tiver um `return`?**

Sim. Só não roda se a JVM for encerrada antes (ex.: `System.exit`).

**Qual a diferença entre `throw` e `throws`?**

`throw` lança uma exceção agora; `throws` avisa, na assinatura, que o método pode lançá-la.

**Para criar uma exceção própria que o compilador obrigue a tratar, estendo qual classe?**

`Exception`. Estendendo `RuntimeException`, ela seria unchecked.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `Error` | Falha grave da JVM (ex.: `OutOfMemoryError`); não se trata. |
| Unchecked | `RuntimeException` e filhas; erro de programação, o compilador não obriga tratar. |
| Checked | O compilador obriga tratar (`try/catch`) ou declarar (`throws`). |
| `try / catch / finally` | Tenta, trata o erro e executa a limpeza em qualquer caso. |
| try-with-resources | Fecha sozinho os recursos abertos no `try (...)`. |
| `throw` × `throws` | Lança uma exceção / avisa que o método pode lançá-la. |
| Exceção própria | Classe que estende `Exception` ou `RuntimeException` com um nome do domínio. |
