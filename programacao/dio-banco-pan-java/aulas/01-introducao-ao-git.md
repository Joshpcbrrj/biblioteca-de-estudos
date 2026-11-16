# Introdução ao Git

> 🗺️ **Nesta aula:** o que é o Git e por que ele mudou o controle de versão, como ele guarda o histórico por dentro, os primeiros comandos (configurar, iniciar, adicionar, commitar) e como desfazer alterações e resolver conflitos.

> 💡 **Analogia:** o Git funciona como um jogo com pontos de salvamento. Você salva o progresso num ponto marcado, continua jogando e, se errar, volta ao ponto salvo sem perder o que já estava certo.

## De onde paramos

Esta é a primeira aula do curso, então não é preciso saber nada de Git. Você vai aprender a salvar versões de um projeto, a desfazer mudanças com segurança e a enviar o seu código para o GitHub.

## Git: Revolução no Controle de Versão

### História do Git

O Git foi criado em 2005 por **Linus Torvalds**, o criador do kernel Linux. O projeto Linux era enorme e tinha milhares de colaboradores, e as ferramentas de controle de versão da época não davam conta: eram lentas ou dependiam de um servidor central. Linus então criou a própria ferramenta, com três objetivos:

- **velocidade**, mesmo em projetos com milhões de linhas;
- **ser distribuído**: cada desenvolvedor tem uma cópia completa do repositório, com todo o histórico;
- **integridade**: nenhuma alteração passa despercebida.

> 💡 **Controle de versão** é como o "histórico de versões" de um documento na nuvem, só que para o projeto inteiro: cada ponto salvo (commit) pode ser comparado, restaurado ou combinado com o trabalho de outras pessoas.

### Vantagens do Git

1. **Desempenho**: operações como commit, diff e troca de branch são quase instantâneas, porque acontecem localmente.
2. **Sistema distribuído**: dá para trabalhar offline e sincronizar depois. Se o servidor cair, qualquer cópia local tem o histórico inteiro.
3. **Branches baratas**: criar, mesclar e apagar ramificações é rápido, o que permite desenvolver várias funcionalidades em paralelo.
4. **Histórico completo e rastreável**: cada alteração registra quem fez, quando e por quê, o que ajuda a encontrar a origem de bugs.

### GitHub

O GitHub, lançado em 2008, é uma plataforma que **hospeda repositórios Git** na nuvem e acrescenta recursos de colaboração: repositórios públicos e privados, pull requests, issues, integração contínua (GitHub Actions) e páginas de projeto. Hoje é a maior comunidade de código aberto do mundo.

### Git x GitHub

![Git é a ferramenta; GitHub é o serviço que hospeda repositórios](../img/git-vs-github.svg)

> 💡 **Analogia:** o Git é um processador de texto que guarda todas as revisões do documento no seu próprio computador. O GitHub é uma estante online onde você publica esse documento para outras pessoas lerem e comentarem.

| Git | GitHub |
| --- | --- |
| Programa instalado no computador | Serviço online |
| Controla as versões do projeto | Hospeda repositórios Git e permite colaborar |
| Funciona sem internet | Precisa de internet |
| Ferramenta de linha de comando | Interface web com recursos extras (PRs, issues, Actions) |

Existem alternativas ao GitHub que também usam Git, como GitLab e Bitbucket.

### Conclusão

O Git trouxe um controle de versão distribuído, rápido e flexível, que funciona bem tanto num projeto pessoal quanto num projeto com milhares de pessoas. O GitHub complementa o Git com uma plataforma para compartilhar código e colaborar. Juntos, são ferramentas essenciais no desenvolvimento de software atual.

### 🧠 Revisão rápida

**Dá para usar Git sem GitHub?**

Sim. O Git funciona sozinho, na sua máquina. O GitHub só hospeda uma cópia do repositório para compartilhar e colaborar.

**O que significa o Git ser "distribuído"?**

Cada cópia do repositório tem o histórico completo, não só os arquivos atuais. Não há dependência de um servidor central para trabalhar.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Git | controle de versão distribuído, criado em 2005 por Linus Torvalds |
| Distribuído | cada cópia do repositório tem o histórico completo |
| GitHub | serviço online que hospeda repositórios Git e adiciona colaboração |
| Git × GitHub | o Git é a ferramenta; o GitHub é o serviço que a hospeda |

## Como o Git funciona

### SHA-1: a identidade de cada objeto

O **SHA-1** (*Secure Hash Algorithm 1*) é uma função de hash criada pela NSA, a agência de segurança dos EUA. Ela recebe qualquer conteúdo e gera um identificador de **40 caracteres hexadecimais**, com duas propriedades importantes:

- o mesmo conteúdo gera **sempre o mesmo hash**;
- qualquer alteração, por menor que seja, gera um hash **completamente diferente**.

> 💡 **Analogia:** o hash é como a impressão digital de um arquivo: curta, mas identifica o original sem ambiguidade. Duas pessoas com a mesma impressão digital são a mesma pessoa, e qualquer marca nova muda a impressão inteira.

![Mesmo conteúdo, mesmo hash; conteúdo diferente, hash diferente](../img/git-sha1.svg)

O Git usa o SHA-1 para identificar tudo o que guarda: cada arquivo, pasta e commit tem seu hash. É por isso que cada commit aparece com um código como `a3f9c2e…` (as primeiras letras do hash), que pode ser usado em comandos como `git checkout`, `git revert` e `git reset`. Como o hash depende do conteúdo, o Git percebe na hora se algo foi alterado ou corrompido.

> ⚠️ O SHA-1 é considerado inseguro para criptografia desde 2017, quando pesquisadores demonstraram uma colisão prática, e por isso não deve ser usado para proteger senhas ou dados sensíveis. No Git ele serve para **identificar** conteúdos e garantir integridade. O Git também já tem suporte experimental ao SHA-256.

#### Testando no terminal

```bash
# No Git Bash, dentro da pasta do arquivo:
openssl sha1 nome_do_arquivo.txt

# O terminal mostra o hash do arquivo.
# Altere uma letra e rode de novo:
# o hash muda completamente.
```

### Objetos internos do Git

Dentro da pasta oculta `.git`, o Git guarda o projeto como três tipos de objeto, cada um identificado pelo seu SHA-1:

- **Blob**: o **conteúdo** de um arquivo. Não guarda nome, pasta nem histórico, só os dados. Dois arquivos com conteúdo idêntico viram um único blob.
- **Tree**: uma **pasta**. Lista os nomes dos arquivos e subpastas, cada um apontando para o hash do blob ou da tree correspondente.
- **Commit**: uma **versão** do projeto. Aponta para a tree principal e guarda autor, data, mensagem e o hash do commit anterior (o pai).

![Hierarquia dos objetos: commit, tree e blobs](../img/git-objetos.svg)

> 💡 **Analogia:** pense num prontuário. O blob é a folha com o conteúdo, a tree é a pasta que organiza as folhas e o commit é a capa datada que aponta para a pasta daquele dia.

Como cada commit aponta para o seu pai, os commits formam uma cadeia, que é o histórico do projeto:

![Anatomia de um commit e a cadeia de pais](../img/commit-anatomia.svg)

> 💡 **Analogia:** os commits são como os pontos de salvamento de um jogo. Cada save guarda o estado atual e lembra qual foi o save anterior, então você pode voltar a qualquer um deles.

### O fluxo completo

1. Ao fazer `git add`, o Git cria um **blob** para o conteúdo de cada arquivo adicionado.
2. Ao fazer `git commit`, ele monta as **trees** com a estrutura das pastas e cria o **commit**, que aponta para a tree principal.

O resultado é um histórico completo e verificável: os blobs guardam os dados, as trees organizam os blobs em pastas e os commits registram cada versão.

![Do arquivo ao commit](../img/git-fluxo.svg)

> 💡 **Analogia:** é uma linha de montagem. As peças (arquivos) viram caixas etiquetadas (blobs), as caixas são organizadas em prateleiras (trees) e a nota fiscal fechada no fim (commit) registra o que saiu da fábrica naquele dia.

### 🧠 Revisão rápida

**Dois arquivos com nomes diferentes e conteúdo idêntico geram quantos blobs?**

Um só: o blob guarda apenas o conteúdo, e o hash é o mesmo. Os nomes ficam na tree.

**Por que mudar um commit antigo altera os hashes de todos os commits seguintes?**

Cada commit guarda o hash do pai. Se o pai muda, o conteúdo do filho muda e o hash dele também, em cadeia.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| SHA-1 | hash de 40 caracteres que identifica cada objeto e garante a integridade |
| Blob | conteúdo de um arquivo, sem nome nem pasta |
| Tree | pasta que liga nomes aos blobs e a outras trees |
| Commit | versão do projeto que aponta para a tree principal e para o commit anterior |

## Iniciando Git e criando commit

### Links úteis

Documentação oficial do Git:

🔗 [Git - git Documentation](https://git-scm.com/docs/git)

Download do Git:

🔗 [GitHub Desktop](https://git-scm.com/downloads)

GitHub Desktop (interface gráfica, opcional):

🔗 [https://desktop.github.com/](https://desktop.github.com/)

### Configuração inicial

Depois de instalar, informe seu nome e e-mail. Eles aparecem em todos os commits que você fizer. A opção `--global` vale para todos os repositórios do computador.

```bash
# Nome e e-mail do autor dos commits
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Conferir as configurações
git config --list

# Apagar uma configuração (para definir de novo)
git config --global --unset user.email
```

### Ajuda no terminal

```bash
# Manual completo do Git
man git

# Resumo dos comandos mais usados
git help

# Ajuda de um comando específico
git help commit
```

### Iniciando um repositório

```bash
# Transforma a pasta atual num repositório
# (cria a pasta oculta .git)
git init

# Lista também os arquivos ocultos
ls -a

# Renomeia a branch atual para main
git branch -M main

# Lista as branches do repositório
git branch
```

> 💡 Logo depois do `git init`, o `git branch` ainda não mostra nada: a branch só passa a existir de fato depois do primeiro commit. O `git branch -M main` garante que ela se chame `main`, o padrão do GitHub.

### Exemplo: versionando uma receita

#### Criando o arquivo

```bash
# Markdown (.md): texto simples que vira HTML
touch strogonoff.md
```

Conteúdo do arquivo:

```markdown
# Strogonoff de frango :chicken:

### Ingredientes
* 1 kg de frango sem pele
* 1 tablete de caldo de galinha
* 3 colheres (sopa) de óleo
* 2 latas de creme de leite sem soro
* 2 colheres (sopa) de molho de tomate
* 2 colheres (sopa) de ketchup
* 2 colheres (sopa) de mostarda
* Champignon a gosto
* Batata palha e arroz branco

### Modo de preparo
1. Em fogo médio, coloque o óleo e dissolva
   o caldo. Junte o frango em cubos e
   cozinhe, mexendo para não queimar.
2. Acrescente o molho de tomate, o ketchup,
   a mostarda e o champignon.
3. Abaixe o fogo, junte o creme de leite e
   mexa até ficar homogêneo.
4. Está pronto para servir.

> Receitinha testada e aprovada!
```

#### 1. Adicionar à staging area

```bash
# Um arquivo específico
git add strogonoff.md

# Ou todos os arquivos novos e modificados
git add .
```

#### 2. Fazer o commit

```bash
# A mensagem resume o que foi feito
git commit -m "Adiciona receita de strogonoff"
```

> 💡 Uma boa mensagem de commit completa a frase "este commit…": *Adiciona receita*, *Corrige quantidade de óleo*. Curta, no imperativo e dizendo o porquê quando não for óbvio.

#### 3. Ligar ao repositório remoto do GitHub

Crie um repositório vazio no GitHub e copie a URL dele.

```bash
# "origin" é o apelido padrão do remoto
git remote add origin \
  https://github.com/usuario/receitas.git

# Confere se o remoto foi cadastrado
git remote -v
```

#### 4. Enviar o código

```bash
# Envia a branch main para o remoto origin.
# O -u liga as duas: depois basta "git push"
git push -u origin main
```

![Do projeto local ao código no GitHub](../img/remoto-fluxo.svg)

> 💡 **Analogia:** o seu computador é o caderno sobre a mesa; o GitHub é a cópia guardada no cofre do banco. O `git push` é levar as páginas novas do caderno até o cofre.

### 🧠 Revisão rápida

**Qual a ordem dos comandos para o primeiro envio ao GitHub?**

`git init` → `git add` → `git commit` → `git remote add origin URL` → `git push -u origin main`.

**Para que serve o `-u` no primeiro push?**

Liga a branch local `main` à remota `origin/main`. Depois disso, `git push` e `git pull` funcionam sem argumentos.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Configuração | `git config --global user.name` e `user.email` definem o autor dos commits |
| Repositório | `git init` transforma a pasta em repositório e cria a pasta `.git` |
| Commit | `git add` prepara as mudanças; `git commit -m` registra a versão |
| Envio | `git remote add origin URL` liga ao GitHub; `git push -u origin main` envia |

## Entendendo alguns pontos importantes

### Ciclo de vida dos arquivos

Todo arquivo de um repositório está em um destes quatro estados:

1. **Untracked** (não rastreado): o Git ainda não acompanha o arquivo. Ele não entra em commits nem tem histórico.
2. **Unmodified** (não modificado): o arquivo é rastreado e está igual ao último commit.
3. **Modified** (modificado): o arquivo mudou desde o último commit, mas as mudanças ainda não foram preparadas.
4. **Staged** (preparado): as mudanças foram adicionadas com `git add` e vão entrar no próximo commit.

> 💡 **Analogia:** a staging area é a mesa onde você separa as fotos que vão para o álbum. O `git add` põe a foto na mesa; o `git commit` cola tudo o que está na mesa no álbum, como uma página nova.

![Os quatro estados e os comandos que levam de um a outro](../img/ciclo-estados.svg)

Para ver em que estado cada arquivo está:

```bash
# Mostra arquivos não rastreados, modificados
# e preparados, e sugere o próximo comando
git status
```

### Desfazendo alterações: git restore

O `git restore` devolve arquivos a um estado anterior: descarta mudanças no diretório de trabalho ou tira arquivos da staging area.

```bash
# Descarta as mudanças não preparadas
# (volta à versão do último commit)
git restore arquivo

# Tira o arquivo da staging area
# (as mudanças continuam no arquivo)
git restore --staged arquivo

# Restaura o arquivo de um commit específico
git restore --source=<hash> arquivo
```

![O que cada forma do git restore desfaz](../img/restore-areas.svg)

> 💡 **Analogia:** é a borracha de um lápis. O `git restore` apaga o rascunho a lápis e devolve a folha como estava na última versão passada a caneta (o commit).

> ⚠️ `git restore arquivo` apaga as mudanças não salvas em commit, e elas não podem ser recuperadas pelo Git.

### Desfazendo commits: git reset

O `git reset` move a branch atual de volta para um commit anterior, "desfazendo" os commits que vieram depois. O que acontece com as alterações desses commits depende do modo:

```bash
# Desfaz o commit; alterações voltam ao staging
git reset --soft <commit>

# Desfaz o commit; alterações ficam no
# diretório de trabalho (modo padrão)
git reset --mixed <commit>

# Desfaz o commit e DESCARTA as alterações
git reset --hard <commit>

# Desfaz só o último commit, mantendo o trabalho
git reset --soft HEAD~1
```

![Onde ficam as alterações em cada modo do git reset](../img/reset-modos.svg)

> 💡 **Analogia:** pense num relatório entregue por engano. Com `--soft` você recolhe o relatório e o deixa pronto na gaveta de rascunhos; com `--mixed` você o deixa solto sobre a mesa; com `--hard` você joga as folhas no lixo.

> ⚠️ O `git reset` reescreve o histórico. Não use em commits que já foram enviados e compartilhados com a equipe: para desfazer um commit público, prefira `git revert`, que cria um novo commit desfazendo o anterior. E cuidado com o `--hard`: as alterações descartadas não voltam.

### Resolvendo conflitos

Um conflito acontece quando o Git tenta juntar duas versões de um arquivo (num merge ou pull) e as duas alteraram **o mesmo trecho** de formas diferentes. Ele não sabe qual escolher e pede ajuda.

1. **Identifique**: o `git status` lista os arquivos em conflito.
2. **Abra o arquivo**: o Git marca o trecho em conflito assim:`<<<<<<< HEAD
versão da sua branch
=======
versão da branch sendo mesclada
>>>>>>> feature`
3. **Edite**: escolha uma versão (ou combine as duas) e apague as linhas de marcação `<<<<<<<`, `=======` e `>>>>>>>`.
4. **Marque como resolvido**: `git add arquivo`.
5. **Conclua**: `git commit` registra o merge com a resolução.

![Passo a passo para resolver um conflito](../img/conflito-passos.svg)

> 💡 **Analogia:** dois colegas editam o mesmo parágrafo de um documento compartilhado. O editor não adivinha qual texto vale mais; ele mostra as duas versões e pede que alguém decida.

Depois de resolver, teste o projeto para garantir que tudo continua funcionando. Para desistir do merge no meio do caminho, use `git merge --abort`.

### 🧠 Revisão rápida

**Você deu `git add` num arquivo por engano. Como tirá-lo do próximo commit sem perder a edição?**

`git restore --staged arquivo`: ele volta a Modified, com as mudanças intactas.

**Qual modo do `git reset` é o perigoso, e por quê?**

O `--hard`: além de desfazer os commits, apaga as alterações do diretório de trabalho.

**Num conflito, o que indicam as linhas entre `=======` e `>>>>>>> feature`?**

A versão que veio da branch `feature`, a que está sendo mesclada.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Estados | untracked, unmodified, modified e staged, conforme o arquivo está no commit e na staging area |
| `git restore` | desfaz mudanças em arquivos ou tira arquivos da staging area |
| `git reset` | move o branch para um commit anterior (`--soft`, `--mixed`, `--hard`) |
| Conflito | o Git marca o trecho divergente; você escolhe, faz `git add` e `git commit` |

> ➡️ **Próximo passo:** na próxima aula você verá branches, repositórios remotos e pull requests, que são o dia a dia do trabalho em equipe.

## 🧠 Revisão rápida

**O que é um commit, em uma frase?**

Um ponto salvo do projeto, com uma mensagem que descreve a mudança.

**Qual a diferença entre `git restore` e `git reset`?**

`git restore` descarta mudanças em arquivos; `git reset` move o branch para um commit anterior.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Git | sistema de controle de versão distribuído: cada cópia tem o histórico completo |
| GitHub | plataforma que hospeda repositórios Git e adiciona colaboração (pull requests, issues) |
| SHA-1 | hash que identifica cada objeto (blob, tree, commit) e garante a integridade |
| Ciclo de vida | untracked → staged (`git add`) → committed (`git commit`) → modified |
| `git restore` | descarta mudanças no arquivo ou o tira da área de staging |
| `git reset` | volta o branch para um commit anterior (`--soft`, `--mixed`, `--hard`) |
| Conflito | o Git marca os trechos divergentes; você escolhe o resultado, adiciona e commita |
