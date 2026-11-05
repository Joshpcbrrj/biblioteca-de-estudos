# Terminal e linha de comando

> 🗺️ **Nesta aula:** como navegar entre pastas, criar e apagar arquivos e encadear comandos no terminal, o básico para usar Git, npm e Node nos próximos módulos.

## De onde paramos

A aula anterior apresentou o shell, a interface em texto do sistema operacional. Agora você vai usá-lo. Git, npm, Node e servidores são usados principalmente pelo terminal, então dominar o básico economiza muito tempo.

## Por que aprender o terminal

**O terminal é uma forma de controlar o computador digitando comandos em vez de clicar.** Cada comando tem o formato `programa opções argumentos`, por exemplo `ls -la projetos`.

- **Windows:** use o **Git Bash** (instalado junto com o Git) ou o **PowerShell**. Os comandos abaixo são do Bash.
- **macOS e Linux:** o app **Terminal**.
- **VS Code:** `Ctrl + '` abre um terminal integrado já na pasta do projeto.

## Navegando entre pastas

```bash
pwd  # mostra em que pasta você está
ls  # lista o conteúdo
ls -la  # inclui ocultos e detalhes
cd projetos  # entra na pasta "projetos"
cd ..  # volta uma pasta
cd ~  # vai para a pasta do usuário
cd -  # volta para a pasta anterior
```

![O mesmo arquivo pode ser apontado por um caminho absoluto ou relativo.](../img/terminal-caminhos.svg)

**Caminho absoluto** parte da raiz (`/home/ana/projetos`); **caminho relativo** parte da pasta atual (`css/style.css`). `..` significa "a pasta acima" e `.` significa "a pasta atual".

## Criando, copiando, movendo e apagando

```bash
mkdir meu-site  # cria pasta
mkdir -p src/css/temas  # cria a pasta e as intermediárias
touch index.html  # cria arquivo vazio
cp index.html sobre.html  # copia
mv sobre.html paginas/  # move (ou renomeia)
rm arquivo.txt  # apaga arquivo
rm -r pasta-velha  # apaga pasta e conteúdo
```

> ⚠️ `rm` **não manda para a lixeira**: o arquivo some de vez. Confira o caminho antes de apertar Enter e nunca rode `rm -rf` com um caminho que você não entendeu.

## Lendo arquivos

```bash
cat README.md  # mostra o arquivo inteiro
head -n 5 log.txt  # primeiras 5 linhas
tail -f log.txt  # acompanha o fim em tempo real
grep "erro" log.txt  # procura um texto
```

## Atalhos que fazem diferença

| Atalho | Faz |
| --- | --- |
| `Tab` | completa nomes de pastas e arquivos |
| `↑` / `↓` | percorre comandos anteriores |
| `Ctrl + C` | interrompe o programa em execução (ex.: um servidor) |
| `Ctrl + L` ou `clear` | limpa a tela |
| `Ctrl + R` | busca no histórico de comandos |

## Encadeando comandos

```bash
# && só roda o segundo se o primeiro der certo
mkdir app && cd app
# | (pipe) envia a saída de um comando para outro
ls | grep .js
# > grava em arquivo (sobrescreve)
echo "node_modules" > .gitignore
# >> acrescenta ao final
echo ".env" >> .gitignore
```

## Pedindo ajuda

`comando --help` mostra as opções de quase qualquer programa (`git --help`, `npm --help`). No macOS e no Linux, `man ls` abre o manual completo.

## Exercício

Pelo terminal, crie a estrutura `meu-site/` com `index.html`, `css/style.css` e `js/main.js`, e depois liste tudo.

<details>
<summary>Ver resposta</summary>

```bash
mkdir -p meu-site/css meu-site/js
cd meu-site
touch index.html css/style.css js/main.js
ls -R
```

O `-p` cria as pastas de uma vez, e `ls -R` lista as subpastas também.

</details>

## 🧠 Revisão rápida

**Você está em `/home/ana/projetos`. Para onde leva `cd ..`?**

Para `/home/ana`.

**Qual a diferença entre `>` e `>>`?**

`>` sobrescreve o arquivo; `>>` acrescenta ao final.

**Como parar um servidor rodando no terminal?**

`Ctrl + C`.

> ➡️ **Próximo passo:** depois de ver as máquinas e o sistema, volte um pouco no tempo para entender como elas passaram a se conectar: **Surgimento da internet e aplicações Web**.

## 📌 Resumo

| Comando | Faz |
| --- | --- |
| `pwd` · `ls` · `cd` | onde estou · o que tem aqui · mudar de pasta |
| `mkdir` · `touch` | cria pasta · cria arquivo |
| `cp` · `mv` · `rm` | copia · move/renomeia · apaga de vez |
| `cat` · `grep` | mostra arquivo · procura texto |
| `&&` e pipe · `>` | encadeia comandos · grava em arquivo |
| `--help` | ajuda de qualquer comando |
