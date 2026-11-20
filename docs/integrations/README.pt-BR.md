<!-- translation-of: README.md sha256:d994c4d7f4ee -->
# Integrações

[English](README.md) | **Português**

Tudo o que se conecta ou se instala à parte da skill. Nenhuma é obrigatória: sem elas, a skill cria o livro do mesmo jeito e entrega um zip para você baixar. Com elas, ela publica e busca materiais sozinha.

## Para que serve cada uma

| Integração | Para que serve | Quando a skill usa | Guia |
| --- | --- | --- | --- |
| **GitHub** | Guardar os livros no seu repositório, salvar o progresso e publicar | início (ponto de controle) e fim (publicação) | [github.pt-BR.md](github.pt-BR.md) |
| **Notion** | Ler um material seu para aprimorar; criar a cópia do livro para você anotar | modo Aprimorar e fim | [notion.pt-BR.md](notion.pt-BR.md) |
| **Google Drive** | Buscar documentos e arquivos seus para usar como fonte | quando você tiver materiais para usar | [google-drive.pt-BR.md](google-drive.pt-BR.md) |
| **Docling** | Converter PDF, DOCX, PPTX e outros documentos para texto, com tabelas e estrutura | quando você mandar documentos | [docling.pt-BR.md](docling.pt-BR.md) |
| **GitHub Pages** | Publicar o site com busca de todos os livros | depois da primeira publicação | [github-pages.pt-BR.md](github-pages.pt-BR.md) |

## Onde cada uma funciona

| Integração | App do Claude no computador | Claude no navegador | Claude Code |
| --- | --- | --- | --- |
| GitHub | acesso ao repositório com permissão de escrita | acesso ao repositório com permissão de escrita | `git` + `gh auth login` |
| Notion | conector | conector | servidor MCP do Notion (`claude mcp add`) |
| Google Drive | conector (Pro, Max, Team, Enterprise) | conector (Pro, Max, Team, Enterprise) | baixar os arquivos |
| Docling | servidor MCP local | não disponível: converta no seu computador e anexe | linha de comando |
| GitHub Pages | — | — | — |

Sem nenhuma delas, em qualquer plano: o zip para baixar sempre funciona, e o GitHub Pages é grátis em repositórios públicos.

## Como os guias estão organizados

Todo guia segue o mesmo roteiro:

1. **Para que serve**
2. **O que você precisa**
3. **Passo a passo**
4. **Como conferir que funcionou**
5. **Problemas comuns**
