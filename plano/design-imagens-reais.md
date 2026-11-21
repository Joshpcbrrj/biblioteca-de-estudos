# Design: imagens reais (fotos com licença livre e capturas da aplicação)

Aprovado pelo usuário em 2026-11-20. As "ilustrações normais" que ele quer são imagens reais: a aplicação do livro funcionando, fotos de autores, de eventos e de arquivos históricos. SVG continua só para diagramas.

## Duas fontes, um script: `scripts/images.py`

**Fotos com licença livre (Wikimedia Commons):**

- `images.py search "<busca>" [--limit 6]`: busca no Commons (API pública, sem chave) e lista só o que tem licença livre: domínio público, CC0, CC BY e CC BY-SA. Cada resultado traz título, autor, licença, link da licença, página de origem e tamanho.
- `images.py fetch "File:<título>" --name c03-eniac [--book B]`: baixa a versão de 1280 px para `img/c03-eniac.<ext>`, acrescenta a linha de créditos em `img/CREDITS.md` e imprime o Markdown da imagem e o crédito para a legenda.
- Licença não livre (ou sem licença) é recusada, mesmo pelo título exato.

**Capturas da aplicação do livro:**

- `images.py screenshot <url> --name c05-app [--book B] [--width 1280 --height 800]`: abre a aplicação que o capítulo acabou de subir num navegador automático (Playwright) e grava `img/c05-app.png`, com a linha "captura da aplicação do livro" em `img/CREDITS.md`.
- Sem Playwright instalado, o script explica como instalar (no Claude Code) ou pede a captura ao usuário (no claude.ai, que não abre navegador). Nunca simula uma captura.

## Checagem

- `audit.py`: uma foto ou captura (PNG/JPG sem spec em `img/_source/`) usada num capítulo sem linha em `img/CREDITS.md` é **erro**.

## Regras (VISUALS/SOURCES)

- Foto real só quando a aparência importa (uma pessoa, uma máquina, um documento, a tela da aplicação); estrutura e fluxo continuam em SVG.
- Legenda com o crédito: autor, licença e origem.
- Capturas só da aplicação real do livro, rodando; nunca montadas.

## Fora do escopo

Ilustrações desenhadas (modelos HTML, API de imagem paga): continuam adiadas.
