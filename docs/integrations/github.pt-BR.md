<!-- translation-of: github.md sha256:446a8ca16c4d -->
# GitHub: guardar os livros no seu próprio repositório

[English](github.md) | **Português**

## Para que serve

A sua biblioteca fica num repositório seu no GitHub: os livros em Markdown, os EPUBs nas releases e o site no GitHub Pages. Com acesso a ele, o Syllabook salva o progresso a cada capítulo (num branch `draft/<livro>`) e publica o livro no fim. Sem acesso, ele entrega um zip e diz onde enviar.

## O que você precisa

- Uma conta no GitHub.
- Um repositório **público** para a sua biblioteca (o GitHub Pages é grátis para repositórios públicos). O jeito mais fácil: abra a [biblioteca de demonstração](https://github.com/Joshpcbrrj/syllabook-demo) para ver como uma biblioteca fica, depois crie um repositório vazio e deixe o Syllabook prepará-lo no primeiro livro.

## Passo a passo

Use a primeira opção que servir para onde você usa o Claude.

### Opção 1: app do Claude com acesso ao repositório

Quando o Syllabook pedir o repositório da biblioteca, dê ao Claude acesso a ele **com permissão de escrita**. O Claude então clona, faz o commit de cada capítulo e publica. A tela exata depende da versão do seu app do Claude; libere sempre só aquele repositório.

### Opção 2: Claude Code

O Claude Code usa o `git` do seu computador. Entre uma vez pela linha de comando do GitHub:

```bash
gh auth login
```

Escolha GitHub.com, HTTPS e "Login with a web browser": copie o código de 8 caracteres que o terminal mostra, cole na página que abrir e autorize.

### Opção 3: sem conexão

Diga "não" quando o Syllabook oferecer a conexão. No fim, ele entrega um zip com as pastas já no formato do repositório (`created-books/<livro>/...`). No seu repositório em github.com: **Add file → Upload files**, arraste a pasta e faça o commit. O site do GitHub aceita até 100 arquivos por envio; em livros maiores, o Syllabook divide o zip e diz a ordem.

### Avançado: servidor MCP do GitHub como conector personalizado

O GitHub mantém um servidor MCP em `https://api.githubcopilot.com/mcp/`. Adicioná-lo ao Claude como conector personalizado hoje exige um aplicativo OAuth seu no GitHub (ou um token pessoal no Claude Code), então não é o caminho recomendado. Nunca cole um token num chat.

## Como conferir que funcionou

- Opção 1 ou 2: peça ao Claude para "listar os arquivos do repositório da minha biblioteca". Devem aparecer o `library.yaml` e as pastas dos livros.
- Opção 2: `gh auth status` mostra `Logged in to github.com`.
- Depois da primeira publicação, a aba **Actions** do repositório mostra "Build EPUBs" e "Website" em verde.

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| O Claude lê, mas não consegue enviar | O acesso foi dado só para leitura. Dê permissão de escrita naquele repositório |
| O `gh` pede um código e a página do navegador está vazia | Copie o código da linha "First copy your one-time code" do terminal |
| "Build EPUBs" ou "Website" falha no primeiro envio | Abra a execução com falha em **Actions** e leia as últimas linhas; para o site, ative o GitHub Pages antes ([guia](github-pages.pt-BR.md)) |
| O envio pelo site para em 100 arquivos | Use as partes que o Syllabook criou, na ordem, ou o GitHub Desktop |
