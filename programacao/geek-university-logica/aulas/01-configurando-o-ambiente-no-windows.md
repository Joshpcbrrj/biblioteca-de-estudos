# Configurando o ambiente no Windows

> 🗺️ **Nesta aula:** instalar e testar as ferramentas das três linguagens usadas no curso: o JDK para Java, o compilador GCC (MinGW-w64) para C e o interpretador Python, além dos editores e IDEs.

O curso mostra os algoritmos em três linguagens: **Java**, **C** e **Python**. Cada uma é executada de um jeito diferente, e por isso cada uma pede ferramentas próprias:

| Linguagem | Como o código vira programa | O que instalar |
| --- | --- | --- |
| Java | Compilado para *bytecode* e executado pela JVM | JDK (compilador `javac`  e JVM `java`) |
| C | Compilado direto para código de máquina (`.exe` no Windows) | Compilador GCC (via MinGW-w64) |
| Python | Interpretado linha a linha | Interpretador Python |

Depois de instalar cada ferramenta, o teste é sempre o mesmo: abrir um **novo** terminal (PowerShell) e pedir a versão. Se o comando não for reconhecido, a pasta da ferramenta não foi adicionada ao **PATH** do Windows (a lista de pastas onde o sistema procura programas).

## Para Java

### JDK

O **JDK** (*Java Development Kit*) traz o compilador e a máquina virtual. Instale uma versão **LTS** (*Long Term Support*, com suporte estendido). O curso usa a 17, mas qualquer LTS serve para os exemplos. Hoje a LTS mais recente é a 25, e a anterior é a 21.

🔗 [Azul Downloads](https://www.azul.com/downloads/#downloads-table-zulu)

Tutorial de como instalar:

🔗 [Instalar Java JDK 17 no Windows - OpenJDK Zulu](https://www.youtube.com/watch?v=QekeJBShCy4&ab_channel=DevSuperior)

Conferindo a instalação:

```powershell
java -version  # versão da JVM (quem executa)
javac -version  # versão do compilador (quem traduz o código)
```

### IDE IntelliJ ou Eclipse

Uma IDE (*Integrated Development Environment*) junta editor, compilador e depurador em um só programa. Para Java, as mais usadas são o IntelliJ IDEA (versão Community é gratuita) e o Eclipse.

🔗 [IntelliJ IDEA](https://www.jetbrains.com/idea/download/#section=windows)

🔗 [Eclipse Downloads | The Eclipse Foundation](https://www.eclipse.org/downloads/)

### Testando sem IDE

Salve como `Ola.java`. O nome do arquivo precisa ser igual ao nome da classe pública:

```java
public class Ola {
  public static void main(String[] args) {
    System.out.println("Olá, Java!");
  }
}
```

```powershell
javac Ola.java  # compila: gera Ola.class (bytecode)
java Ola  # executa a classe (sem a extensão)
```

## Para C

### Compilador MinGW-w64 (GCC)

O C precisa de um compilador. No Windows, o mais usado é o **GCC** distribuído pelo projeto **MinGW-w64**. O link abaixo é do MinGW original (32 bits), que não recebe mais atualizações. Prefira o **MinGW-w64**, instalado pelo **MSYS2**: é o caminho indicado na documentação do VS Code para C/C++.

🔗 [MinGW - Minimalist GNU for Windows](https://sourceforge.net/projects/mingw/)

🔗 [https://www.msys2.org/](https://www.msys2.org/)

Resumo da instalação via MSYS2:

1. Instale o MSYS2 e abra o terminal **MSYS2 UCRT64**.
2. Rode `pacman -S mingw-w64-ucrt-x86_64-gcc`.
3. Adicione `C:\msys64\ucrt64\bin` ao PATH do Windows.

Confirme, em um novo terminal, que o PATH foi configurado:

```powershell
gcc --version
```

### Plugins do VS Code para programar em C

O VS Code é um editor (não uma IDE completa). Com estas extensões ele passa a ter destaque de sintaxe, autocompletar, depuração e um botão para compilar e executar:

🔗 [https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools)

🔗 [https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools-extension-pack)

🔗 [https://marketplace.visualstudio.com/items?itemName=franneck94.c-cpp-runner](https://marketplace.visualstudio.com/items?itemName=franneck94.c-cpp-runner)

### Testando

Salve como `ola.c`:

```c
#include <stdio.h>

int main(void) {
  printf("Olá, C!\n");
  return 0;
}
```

```powershell
gcc ola.c -o ola  # compila e gera ola.exe
.\ola  # executa
```

## Para Python

### Interpretador

O Python **não é compilado** para um executável como o C: o **interpretador** lê e executa o código diretamente. Por isso o que se instala é o interpretador.

🔗 [Download Python](https://www.python.org/downloads/)

> ⚠️ Na primeira tela do instalador, marque **"Add python.exe to PATH"**. Sem isso, o comando `python` não funciona no terminal.

Confirme se o PATH foi configurado:

```powershell
python --version
```

### IDE PyCharm ou VS Code

🔗 [PyCharm](https://www.jetbrains.com/pycharm/download/#section=windows)

🔗 [https://code.visualstudio.com/download](https://code.visualstudio.com/download)

No VS Code, instale também a extensão **Python** (da Microsoft).

### Testando

Salve como `ola.py`:

```python
print("Olá, Python!")
```

```powershell
python ola.py
```

## 📌 Resumo da aula

| Linguagem | Instalar | Conferir | Compilar e executar |
| --- | --- | --- | --- |
| Java | JDK LTS (21 ou 25) | `java -version` e `javac -version` | `javac Ola.java` → `java Ola` |
| C | GCC via MSYS2 (MinGW-w64) | `gcc --version` | `gcc ola.c -o ola` → `.\ola` |
| Python | Interpretador (marcar "Add python.exe to PATH") | `python --version` | `python ola.py` |

Se um comando "não é reconhecido", a pasta da ferramenta não está no **PATH**. Abra um terminal **novo** depois de cada instalação.
