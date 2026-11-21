<!-- translation-of: notion.md sha256:060885713b46 -->
# Notion: ler seus materiais e guardar uma cópia de cada livro

[English](notion.md) | **Português**

## Para que serve

- **Modo Aprimorar:** o Syllabook lê as suas anotações de curso direto do Notion, página por página.
- **No fim de cada livro:** ele cria uma cópia do livro no Notion, dentro de uma página que você escolher, para você fazer as suas anotações. A cópia tem o texto, as respostas como toggles e os diagramas SVG. Fotos e capturas de tela ficam no EPUB e no site.

## O que você precisa

- Uma conta no Notion com acesso às páginas que você quer usar.
- A página do Notion onde os livros vão ficar (copie o link: **••• → Copiar link**).

## Passo a passo

### App do Claude ou claude.ai

1. **Configurações → Conectores**, procure o **Notion** e escolha **Conectar**.
2. Entre no Notion e libere o acesso às páginas que o Syllabook vai ler e escrever (pelo menos a página onde os livros vão ficar).
3. Num chat, as ferramentas do Notion passam a aparecer no menu de conectores; deixe o Notion ligado naquele chat.

### Claude Code

Num terminal, adicione uma vez o servidor MCP oficial do Notion, para todos os projetos:

```bash
claude mcp add --scope user --transport http notion https://mcp.notion.com/mcp
```

Depois, dentro do Claude Code, digite `/mcp`, escolha **notion** e entre na sua conta. Em seguida, abra uma sessão nova do Claude Code, para ela carregar as ferramentas do Notion.

## Como conferir que funcionou

Peça ao Claude para "abrir a minha página do Notion <link>". Devem aparecer o título e o conteúdo da página. Na primeira publicação, o Syllabook pede o link da página onde os livros vão ficar e o guarda no `library.yaml` (`notion_page`).

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| O Claude diz que não vê a página | A página não foi liberada ao conectar. Conecte de novo e selecione a página, ou compartilhe a página acima dela |
| Falta um diagrama na cópia do Notion | O envio de imagens expira em cerca de uma hora. Peça ao Claude para refazer a página daquele capítulo |
| As respostas aparecem como texto `<details>` | A página não foi feita pelo conversor do Syllabook. Peça ao Claude para refazer com o `notion.py` |
| O `/mcp` mostra "Needs authentication" ou "Invalid redirect_uri" | Rode `/mcp` de novo e repita a entrada; atualize o Claude Code se continuar falhando |
