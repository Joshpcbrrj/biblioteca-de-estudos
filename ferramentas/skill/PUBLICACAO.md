# Exportação, conversão e publicação (Fases 6 e 7)

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia só depois que o usuário avisar que exportou o curso.

## Repositório e exportação

Repositório: `Joshpcbrrj/biblioteca-de-estudos` (branch `main`). Use `add_repo` com acesso `push` se ele ainda não estiver na sessão e clone com `--depth 1`.

### Obter o conteúdo com as imagens

O servidor de arquivos do Notion (`prod-files-secure.s3...amazonaws.com`) costuma ser bloqueado na sessão, então as imagens já existentes no Notion não podem ser baixadas direto. Use a exportação do Notion:

1. Peça ao usuário para exportar a página índice: menu `•••` → **Exportar** → formato **HTML**, **Incluir subpáginas** ligado, **Incluir conteúdo: tudo** (com arquivos e imagens). Isso gera um `.zip`.
2. Se o computador do usuário estiver vinculado à sessão, peça acesso à pasta Downloads (`device_request_folder_access`) e traga o zip com `device_stage_files`. Se não, peça para ele anexar o zip na conversa.
3. Descompacte numa pasta vazia própria e converta com o script do repositório: `python3 -I ferramentas/notion2md.py <pasta-da-exportacao> <pasta-do-curso>`. Ele segue a ordem do índice, gera `aulas/NN-<slug>.md`, copia as imagens para `img/`, transforma callouts em citações, toggles de resolução em `<details>`, ignora PDFs e arquivos de projeto, troca tabulações do código por 2 espaços e reduz o alinhamento de comentários. Ajuste o script se encontrar um bloco novo do Notion e mantenha a versão melhorada no repositório.
4. Revise o resultado: rótulos dos `<summary>`, menções a arquivos não publicados, nomes pessoais, `•` no lugar de `+` em tabelas, `�` em código. Depois escreva `aulas/00-sobre-o-curso.md`, `README.md` e `metadata.yaml`.
5. Toda correção de conteúdo feita nesta etapa (texto, tabela dividida, código reescrito) entra numa lista para a sincronização com o Notion (Fase 7).

## Infraestrutura do repositório

O repositório já tem a infraestrutura (README com catálogo, `epub/estilo.css`, `.github/workflows/gerar-epubs.yml`, `ferramentas/`). Antes de publicar, confira que ela continua nesta forma; se estiver vazio ou faltando algo, recrie (commit separado: "Estrutura inicial da biblioteca").

```
README.md                         ← catálogo
programacao/<slug>/               ← um diretório por curso
matematica/<slug>/
epub/estilo.css
ferramentas/notion2md.py          ← conversor da exportação do Notion
ferramentas/verificar_epub.js     ← checagem de transbordo em tela estreita
.github/workflows/gerar-epubs.yml
```

Os arquivos de referência são os do próprio repositório. Se `epub/estilo.css` ou o workflow sumirem, recrie a partir das cópias abaixo (versão atual, com as partes `img/epub/` dos cheat sheets):

`epub/estilo.css`:

```css
body { font-family: serif; line-height: 1.5; margin: 0; padding: 0 2%; }
h1, h2, h3 { font-family: sans-serif; line-height: 1.25; page-break-after: avoid; break-after: avoid; }
h1 { font-size: 1.5em; margin-top: 0; page-break-before: always; break-before: page; }
h2 { font-size: 1.25em; }
h3 { font-size: 1.1em; }
p, li { orphans: 2; widows: 2; }
code { font-family: monospace; font-size: 0.85em; overflow-wrap: anywhere; word-break: break-word; }
pre, pre code, pre > code.sourceCode, div.sourceCode { white-space: pre-wrap !important; overflow-wrap: anywhere; word-break: break-word; overflow: visible !important; }
pre { background: #f3f4f6; border: 1px solid #d1d5db; padding: 0.5em; border-radius: 4px; font-size: 0.8em; line-height: 1.35; tab-size: 2; -moz-tab-size: 2; }
pre > code.sourceCode > span { display: inline; }
blockquote { margin: 1em 0; padding: 0.5em 0.8em; background: #f3f4f6; border-left: 4px solid #2563eb; }
table { border-collapse: collapse; width: 100%; font-size: 0.85em; table-layout: fixed; }
th, td { border: 1px solid #9ca3af; padding: 3px 5px; vertical-align: top; overflow-wrap: anywhere; word-break: break-word; }
th { background: #dbeafe; }
figure, img { page-break-inside: avoid; break-inside: avoid; }
img { display: block; width: 100%; max-width: 100%; height: auto; max-height: 95vh; object-fit: contain; margin: 0.8em auto; }
figcaption { font-size: 0.85em; text-align: center; font-style: italic; }
details { margin: 1em 0; padding: 0.4em 0.8em; border: 1px solid #16a34a; border-radius: 4px; background: #f0fdf4; }
summary { font-weight: bold; font-family: sans-serif; cursor: pointer; }
```

`.github/workflows/gerar-epubs.yml`:

```yaml
name: Gerar EPUBs

on:
  push:
    branches: [main]
    paths:
      - 'programacao/**'
      - 'matematica/**'
      - 'epub/**'
      - '.github/workflows/gerar-epubs.yml'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  epub:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Instalar Pandoc e rsvg-convert
        run: |
          wget -q https://github.com/jgm/pandoc/releases/download/3.5/pandoc-3.5-1-amd64.deb
          sudo dpkg -i pandoc-3.5-1-amd64.deb
          sudo apt-get update -q && sudo apt-get install -y -q librsvg2-bin

      - name: Descobrir cursos a gerar
        run: |
          todos() { ls -d programacao/*/ matematica/*/ 2>/dev/null | sed 's#/$##'; }
          if [ "${{ github.event_name }}" = "workflow_dispatch" ] || ! git rev-parse HEAD~1 >/dev/null 2>&1; then
            todos > cursos.txt
          elif git diff --name-only HEAD~1 HEAD | grep -qE '^(epub/|\.github/)'; then
            todos > cursos.txt
          else
            git diff --name-only HEAD~1 HEAD | grep -E '^(programacao|matematica)/[^/]+/' | cut -d/ -f1-2 | sort -u > cursos.txt
          fi
          cat cursos.txt

      - name: Gerar EPUBs
        run: |
          mkdir -p saida
          while read -r d; do
            [ -f "$d/metadata.yaml" ] || continue
            nome=$(basename "$d")
            tmp=$(mktemp -d)
            cp -r "$d"/. "$tmp"/
            # SVG -> PNG (2x) para o EPUB: Kindle e alguns leitores não exibem SVG bem
            # cheat sheets: no EPUB entram as 2 partes de 2 colunas (img/epub/)
            for e in "$tmp"/img/epub/*-1.svg; do
              [ -e "$e" ] || continue
              n=$(basename "$e" -1.svg)
              sed -i -E "s#!\[([^]]*)\]\(\.\./img/$n\.svg\)#![\1](../img/epub/$n-1.svg)\n\n![](../img/epub/$n-2.svg)#g" "$tmp"/aulas/*.md
            done
            for s in "$tmp"/img/*.svg "$tmp"/img/epub/*.svg; do
              [ -e "$s" ] || continue
              rsvg-convert -z 2 -b white -o "${s%.svg}.png" "$s"
            done
            sed -i -E 's#(\.\./img/[^)]+)\.svg\)#\1.png)#g' "$tmp"/aulas/*.md
            capa=""
            [ -f "$d/capa.png" ] && capa="--epub-cover-image=$d/capa.png"
            pandoc --metadata-file="$d/metadata.yaml" --resource-path="$tmp/aulas" \
              --css=epub/estilo.css --toc --toc-depth=2 --split-level=1 --mathml \
              $capa -o "saida/$nome.epub" $(ls "$tmp"/aulas/[0-9]*.md | sort)
            echo "Gerado: saida/$nome.epub"
          done < cursos.txt

      - name: Publicar na release
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          ls saida/*.epub >/dev/null 2>&1 || { echo "Nenhum EPUB gerado"; exit 0; }
          gh release view epubs >/dev/null 2>&1 || \
            gh release create epubs --title "EPUBs da Biblioteca de Estudos" \
              --notes "Livros gerados automaticamente a partir dos resumos em Markdown."
          gh release upload epubs saida/*.epub --clobber
```

README raiz: título "📚 Biblioteca de Estudos", uma frase de propósito, seções **Programação** e **Matemática** com tabela `Curso | Ler online | EPUB` (o curso com o nome no formato padrão), onde EPUB aponta para `https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/<slug>.epub`, uma nota sobre como os EPUBs são gerados e outra explicando que as respostas dos exercícios ficam recolhidas.

## Estrutura de cada curso

```
<area>/<slug>/
  README.md              ← capa + apresentação + índice para leitura no GitHub (não entra no EPUB)
  metadata.yaml
  capa.png               ← capa do EPUB (1600 × 2560)
  capa.svg               ← arquivo de origem da capa
  aulas/
    00-sobre-o-curso.md
    01-<aula>.md
    02-<aula>.md
    ...
  img/
    *.svg
```

- Na raiz da pasta do curso ficam **só** `README.md`, `metadata.yaml`, `capa.png`, `capa.svg`, `aulas/` e `img/`. Nenhum `.md` de aula solto na raiz.
- Nas aulas, imagens são referenciadas como `![legenda](../img/arquivo.svg)`.
- No README do curso, links para as aulas como `aulas/NN-<slug>.md`.
- `slug` do curso: minúsculas, hífens, sem acentos, com a origem: `boson-logica-portugol`, `cod3r-algoritmos`. Nomes de arquivo das aulas com até ~48 caracteres, cortados em fim de palavra.
- Numeração com dois dígitos na ordem didática do índice (incluindo páginas novas e listas de exercícios).
- `metadata.yaml`:

```yaml
title: "Udemy/ YouTube: Lógica de programação com Portugol Studio - Bóson Treinamentos"
author: "Josué B. Almeida"
lang: pt-BR
rights: "Resumo pessoal de estudo. O conteúdo original pertence aos autores do curso."
```

- `aulas/00-sobre-o-curso.md`: `# Sobre o curso` + proposta, caminho das seções, legenda, tabela Resumo do curso.
- `README.md` do curso: capa, título (nome no formato padrão), link para baixar o EPUB, descrição curta, links para as aulas agrupados por seção.

## Conversão Notion → Markdown

- Título da aula: `# Título` (sem emoji). Seções `##`, subseções `###`.
- `<b>` → `**`, `<i>` → `*`, `<code>` → crase, `<span color>` → texto simples.
- Callout → citação: `> **🗺️ Nesta aula:** …`, `> ⚠️ …`, `> 💡 …`.
- Toggle de **resolução/resposta de exercício** → `<details><summary>Ver resposta</summary>` (preferência fixa 2). Toggle de **código de exemplo** de aula → `**Código**` seguido do bloco, visível.
- Imagem → `![legenda](../img/arquivo.svg)` com o arquivo salvo em `img/`. Fotos mantidas: salve em `img/` como PNG/JPG.
- Bookmark → link Markdown. Mencione o material de apoio como texto ("PDF da aula disponível no curso original").
- **Não publique** PDFs, arquivos de projeto (.por, .zip etc.) nem materiais do curso original: são dos autores. Só os resumos, códigos reescritos e diagramas.
- Fórmulas: equação em linha `$...$`, em bloco `$$...$$` (LaTeX). O GitHub e o Pandoc (`--mathml`) renderizam.
- Tabelas Markdown normais; escape `|` dentro de células.
- Nada de HTML do Notion sobrando além de `<details>`/`<summary>`: procure por `<callout`, `<toggle`, `<aside`, `<page`, `notion-file-block`, `&lt;` nos `.md` antes de commitar.

## Compatibilidade com e-readers (Kindle, Kobo, eboox)

A tela de um leitor tem ~360–600px de largura útil. Para nada ficar cortado:

- **Código**: indentação com 2 espaços (sem tabulações); linhas com até ~60 caracteres sempre que possível. Quebre chamadas longas (`escreva(...)` com muitos argumentos) em várias linhas ou em dois comandos, e mova comentários longos de fim de linha para a linha de cima; nunca alinhe comentários com sequências de espaços. O CSS força a quebra de linha, mas código já curto fica mais legível.
- **Tabelas**: no máximo 4 colunas e células curtas. Tabelas mais largas (ex.: tabela-verdade com 9 colunas) viram duas tabelas menores ou um SVG vertical.
- **Imagens**: seguem o padrão de SVG de `DIDATICA_VISUAL.md` (480 de largura, retrato, letra grande). No EPUB, a Action converte para PNG 2x e o CSS faz a imagem ocupar a largura da tela sem passar da altura.
- **Sem elementos fixos ou largos**: nada de `width` fixo em pixels, nada de HTML extra além de `<details>`.
- **Checagem obrigatória antes de publicar** (o script `ferramentas/gerar_epub_local.py` executa estes passos): gere o EPUB localmente (com o mesmo comando da Action; se não houver `rsvg-convert`, converta os SVGs com Playwright em escala 2), descompacte e rode `node ferramentas/verificar_epub.js <pasta-do-epub-descompactado>`. Ele abre cada capítulo numa tela de 380px e lista os elementos que passam da largura. O resultado precisa ser **zero**. Veja também, com `Read`, a captura de pelo menos um capítulo com código e um com diagrama.

## Conferir e publicar

1. Gere o EPUB localmente e faça a checagem de e-readers acima, sem erros nem imagens faltando: `python3 -I ferramentas/gerar_epub_local.py <area>/<slug>` faz tudo (cheat sheets em 2 partes, SVG → PNG, pandoc e `verificar_epub.js`) e devolve JSON; `img_faltando` precisa vir vazio e `verificar_epub` precisa dizer "OK".
2. Atualize o README raiz (linha do curso no catálogo).
3. Commit com mensagem em português (`Adiciona curso: <nome>` ou `Atualiza curso: <nome>`), puxe `origin main` antes e faça push para `main`. Siga as regras de atribuição de commit da sessão. Não use o e-mail pessoal do usuário no commit; use o endereço `noreply` do GitHub.
4. Acompanhe a Action (`gh run list`; para detalhes use a API REST, `gh api repos/Joshpcbrrj/biblioteca-de-estudos/...`, porque o GraphQL não funciona na sessão) até terminar e confirme que o `<slug>.epub` apareceu na release `epubs` (`gh api repos/Joshpcbrrj/biblioteca-de-estudos/releases/tags/epubs`). Se falhar, leia o log, corrija e publique de novo.


## Sincronizar Notion e GitHub

O conteúdo tem que ser o mesmo nos dois lugares. A ordem de trabalho é: **o Notion é a fonte**; corrija primeiro no Notion sempre que possível e só depois exporte. Quando uma mudança nascer no Markdown (ajuste para e-reader, tabela dividida, frase reescrita, aula nova, diagrama novo), aplique a mesma mudança na página do Notion antes de encerrar:

- **Texto, títulos, callouts e tabelas**: `notion-update-page` com `update_content` (trechos exatos) na página correspondente.
- **Código**: se uma linha foi reescrita ou quebrada, atualize o bloco de código no Notion.
- **Imagens**: o mesmo SVG no `img/` e no Notion (suba com `notion-create-attachment` e troque o `<image>`).
- **Aulas novas**: crie a página no Notion, com o título terminado em ` (Adicionado pelo aluno para melhorar o estudo)`, e posicione no índice. Conforme a Fase 2.3, ela não leva callout de "página nova" nem marca ✨ (a lista do que foi acrescentado vai também no resumo ao usuário).
- **Índice**: o `00-sobre-o-curso.md` e o índice do Notion têm a mesma proposta, legenda e Resumo do curso.

Diferenças permitidas (são de formato, não de conteúdo):

- callout (Notion) × citação `>` (Markdown); toggle `Resolução` (Notion) × `<details>`/"Ver resposta" (Markdown);
- PDFs, arquivos de projeto e bookmarks de material do curso ficam só no Notion;
- espaços em branco do código (tabulação × 2 espaços, alinhamento de comentários) que o conversor ajusta automaticamente;
- o breadcrumb e o callout `📚` com os links do GitHub, que só existem no Notion.

No fim, peça uma nova exportação ao usuário (ou use a mais recente), converta-a numa pasta temporária e compare com o repositório (`diff -r`). Toda diferença precisa ser explicada ou corrigida no lado desatualizado. Sem exportação nova, confira por amostragem (pelo menos 3 páginas, incluindo uma lista de exercícios): fetch no Notion × arquivo `.md` correspondente.

## Resumo final ao usuário (em português)

Curto e objetivo:

- o que foi revisado (quantas páginas);
- erros corrigidos (lista curta, com a página);
- verificação do escopo: tópicos que faltavam ou estavam rasos e o que foi acrescentado (aulas novas e seções ampliadas), para o usuário saber o que não veio das anotações dele;
- imagens trocadas por SVG e diagramas novos;
- a capa (envie a imagem com `SendUserFile`);
- confirmação de que Notion e GitHub estão iguais;
- link do curso no GitHub e link de download do EPUB;
- pendências ou sugestões (temas fora da proposta, pontos que dependem de versão de ferramenta).

