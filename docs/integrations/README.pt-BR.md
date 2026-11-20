<!-- translation-of: README.md sha256:bb87a693ab2a -->
# Integrações

[English](README.md) | **Português**

Tudo o que se conecta ou se instala à parte da skill. Nenhuma é obrigatória: sem elas, a skill cria o livro do mesmo jeito e entrega um zip para você baixar. Com elas, ela publica e busca materiais sozinha.

## Para que serve cada uma

| Integração | Para que serve | Quando a skill usa | Guia |
| --- | --- | --- | --- |
| **GitHub** | Guardar os livros no seu repositório, salvar o progresso e publicar | início (ponto de controle) e fim (publicação) | a escrever |
| **Notion** | Ler um material seu para aprimorar; criar a cópia do livro para você anotar | modo Aprimorar e fim | a escrever |
| **Google Drive** | Buscar livros, PDFs e documentos seus como fonte | quando você tiver materiais para usar | a escrever |
| **Docling** | Converter PDF, DOCX, PPTX e outros documentos para texto, com tabelas e estrutura | quando você mandar documentos | [docling.pt-BR.md](docling.pt-BR.md) |
| **GitHub Pages** | Publicar o site com busca de todos os livros | depois da primeira publicação | a escrever |

## Onde cada uma funciona

| Integração | App do Claude no computador | Claude no navegador | Claude Code | Plano gratuito |
| --- | --- | --- | --- | --- |
| GitHub (conector) | sim | sim | sim (git direto) | sim, mas só cabe 1 conector personalizado |
| Notion (conector) | sim | sim | sim (MCP) | a conferir |
| Google Drive (conector) | sim | sim | sim (MCP) | a conferir |
| Docling (no seu computador) | sim (MCP local) | não | sim (linha de comando) | sim |
| GitHub Pages | — | — | — | grátis em repositório público |

Os itens "a conferir" serão testados na fase 3 da reformulação, antes de virarem regra.

## Como os guias estão organizados

Todo guia segue o mesmo roteiro:

1. **Para que serve**
2. **O que você precisa**
3. **Passo a passo**
4. **Como conferir que funcionou**
5. **Problemas comuns**
