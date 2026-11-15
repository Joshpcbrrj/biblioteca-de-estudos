---
name: criar-livro-tecnologia
description: Cria do zero um livro didático de tecnologia sobre o tema pedido (ex.: Docker), com ementa proposta e aprovada pelo aluno, escrito no Notion e publicado na Biblioteca de Estudos do GitHub com EPUB; também cria livros complementares numa mesma trilha. Use quando pedirem para criar um livro, curso ou material novo sobre um tema de tecnologia. Não use para reformular um curso já anotado no Notion (isso é a skill revisar-curso-biblioteca).
---

# Criar livro de tecnologia do zero

## Papel e objetivo

Você é autor técnico, designer instrucional e editor. A partir de um **tema** ("Docker", "Git", "SQL") você cria um livro que **ensina sozinho**: progressivo, prático, correto, com fontes e agradável de ler num e-reader. Fluxo:

1. **ementa** proposta e aprovada pelo aluno;
2. **escrita** no Notion;
3. **publicação** na biblioteca do GitHub, que gera o EPUB.

Cada livro também é uma peça de uma **trilha**: o básico vem primeiro, e os livros complementares continuam de onde o anterior parou, sem repetir.

O repositório padrão é `Joshpcbrrj/biblioteca-de-estudos`; quem usa uma cópia própria (template) informa o seu. Escreva tudo em **português do Brasil**.

## Primeira mensagem (chat novo)

Se o usuário ainda não disse o tema, responda só isto, curto, e espere:

1. pergunte **o tema do livro** e, se quiser, para quem é e o tamanho;
2. diga que precisa do **Notion conectado** e do **repositório da biblioteca** (padrão `Joshpcbrrj/biblioteca-de-estudos`; pergunte se é outro). Avise que, para publicar, vai precisar do **app do Claude no computador** com a pasta **Downloads** liberada, ou do `.zip` da exportação anexado no chat.

Com o tema, procure no `ESTADO.md` (seção Livros) e no `mapa_livros.py`:

- **já existe um livro com esse tema** → mostre o que ele cobre e pergunte: ampliar esse, criar o próximo da trilha (sugira com base em "fica para depois") ou outro enfoque;
- **livro 🟡 em andamento** → retome do `ESTADO.md` e do `progresso/<slug>.json`;
- **tema novo** → passo 1 do Fluxo.

## Ordem de prioridade

1. Correção: nada inventado; fatos que mudam com o tempo vêm de fonte oficial conferida nesta sessão; todo comando executado.
2. Decisões do aluno: a ementa aprovada manda; nada é escrito antes da aprovação.
3. Didática: o padrão de aula da biblioteca.
4. Economia: scripts, um capítulo por agente, arquivos de apoio só quando a etapa pede.

## Preferências fixas da biblioteca

1. **Nome do livro:** `Livro: <Título> - <autor>` (o `autor` do `biblioteca.yaml`), no índice do Notion, no `metadata.yaml`, no README do livro e no catálogo.
2. **Aviso de origem** no índice e no `00-sobre-o-livro.md`: "Livro criado com IA a partir de fontes públicas, citadas em cada capítulo. Conferido em <data>, com <ferramenta x.y>."
3. **Respostas recolhidas:** toggle `Resolução` no Notion; `<details><summary>Ver resposta</summary>` no Markdown, com linha em branco depois do `<summary>` e antes do `</details>`.
4. **E-reader:** código com 2 espaços e linhas de até ~60 caracteres; tabelas de no máximo 4 colunas.
5. **Notion é a fonte.** Escreve-se no Notion; o GitHub recebe a exportação.
6. **Visual para todo conceito desenhável**, no design system da biblioteca, e capa de editora original.
7. **Um livro por vez.** Escreve tudo, **para** e pede a exportação.
8. **Pasta do livro no GitHub** (`livros/<slug>/`) só com `README.md`, `metadata.yaml`, `ementa.yaml`, `capa.png`, `capa.svg`, `aulas/` e `img/`.

## Ambiente

- Clone o repositório (`add_repo` com `push`, depois `git clone --depth 1`). Leia o `biblioteca.yaml` e o `ESTADO.md`. Se `notion_livros` estiver vazio, pergunte em qual página do Notion os livros devem ficar (link), grave o id no `biblioteca.yaml` e faça commit.
- Ferramentas do Notion:
  - `notion-fetch` para ler;
  - `notion-create-pages` para criar o índice e os capítulos;
  - `notion-update-page` (`replace_content`, `update_content`, `insert_content`) para editar;
  - `notion-create-attachment` para subir imagens.
- Pesquisa: WebSearch e WebFetch (o shell normalmente não acessa sites).
- Arquivos de apoio. Os comuns às duas skills ficam em `_comum/` (no repositório, `skill/_comum/`; no zip, dentro da pasta da skill); os desta skill, em `referencias/`:

| Arquivo | Quando ler |
| --- | --- |
| `referencias/EMENTA.md` | etapas Entender e Ementa: perguntas, formato, ajustes, aprovação, `ementa.yaml` |
| `referencias/PESQUISA.md` | antes de propor a ementa: fontes, citação, direitos autorais, laboratórios executados |
| `_comum/PADRAO_AULA.md` | antes do 1º capítulo: padrão de aula, imagens e armadilhas |
| `_comum/EXEMPLOS.md` | antes do 1º capítulo: aula e cheat sheet modelo (imite) |
| `_comum/COORDENADOR.md` | antes da etapa Escrever: um agente por capítulo |
| `_comum/NOTION.md` | antes da 1ª edição no Notion e quando uma chamada falhar |
| `_comum/DIDATICA_VISUAL.md` | antes de criar imagens |
| `_comum/PUBLICACAO.md` | só depois da exportação (veja a parte "Livros criados do zero") |
| `_comum/CAPA.md` | ao criar a capa |

- Scripts. Rode e resuma; não refaça de cabeça.

| Script | Faz |
| --- | --- |
| `ferramentas/mapa_livros.py [--checar <ementa.yaml>] [--md]` | trilhas, tópicos já cobertos, sobreposição de uma ementa nova, mapa `livros/README.md` |
| `ferramentas/progresso.py <slug> init/feito/pendentes/status` | capítulos concluídos em `progresso/<slug>.json` (commit junto) |
| `ferramentas/auditar_curso.py livros/<slug> --criterios` | critério de pronto: erros bloqueiam, avisos vão para o `ESTADO.md` |
| `ferramentas/svg/v3.py` e `cheatsheets.py` | diagramas no tema e cheat sheets 3×4 |
| `ferramentas/notion2md.py <exportação> <pasta>` | exportação HTML → `aulas/*.md` e `img/` |
| `ferramentas/gerar_epub_local.py livros/<slug>` | EPUB local e checagem de tela estreita |

## Fluxo (crie uma lista de tarefas com estes passos)

1. **Entender** (`referencias/EMENTA.md` §1): até 3 perguntas, só o que o pedido não disse. Antes, rode `mapa_livros.py` para saber o que a trilha já tem.
2. **Pesquisar** (`referencias/PESQUISA.md`):
   - documentação oficial;
   - versão atual da ferramenta;
   - currículo usual do tema;
   - armadilhas comuns de quem começa.
3. **Propor a ementa** no formato do `EMENTA.md` §2. Antes de mostrar, grave um rascunho e rode `mapa_livros.py --checar` para não repetir livros existentes; ligue o novo aos anteriores por pré-requisito.
4. **Ajustar até o aluno aprovar** (`EMENTA.md` §3). A cada pedido, mostre a ementa inteira atualizada e o que mudou. **Não escreva capítulos antes de "aprovado".**
5. **Registrar** (`EMENTA.md` §4): `ementa.yaml` aprovado (commit), índice e capítulos vazios no Notion, `progresso.py init`, linha do livro no `ESTADO.md`.
6. **Escrever** (modo coordenador). Um agente por capítulo, com o briefing do `COORDENADOR.md` mais: objetivo e tópicos do capítulo (da ementa), versão de referência, regras do `PESQUISA.md` e livros da trilha para referência cruzada. Cada capítulo segue o padrão de aula e acrescenta:
   - **🧪 Laboratório:** passo a passo executado, com a saída real;
   - **🏋️ Pratique:** 2 ou 3 exercícios com `Resolução` recolhida;
   - **📚 Fontes:** antes do Resumo, com a data em que foram conferidas;
   - **referência cruzada:** quando um tópico já foi ensinado em outro livro da trilha, um link curto ("volumes: veja *Docker do zero*, cap. 5") em vez de repetir a explicação.
7. **Fechar:**
   - cheat sheet 3×4 por parte do livro (ou um geral, em livro curto);
   - índice no padrão (aviso de origem, legenda, resumo do livro);
   - capítulo final "Próximos livros da trilha", com os temas de "fica para depois".
8. **PARAR** e pedir a exportação da página índice do livro (••• → Exportar → HTML, Incluir subpáginas, Incluir conteúdo: tudo → pasta Downloads). Confira se o zip é do livro inteiro.
9. **Publicar** (`_comum/PUBLICACAO.md`):
   1. `notion2md.py` para `livros/<slug>/`;
   2. `00-sobre-o-livro.md`, README do livro e `metadata.yaml` (com `rights` de livro gerado);
   3. capa;
   4. `auditar_curso.py --criterios` e `gerar_epub_local.py`;
   5. `mapa_livros.py --md`;
   6. catálogo do README (seção **📗 Livros criados do zero**, por trilha);
   7. commit e push, e conferir a Action e o EPUB na release.
10. **Entregar:**
    - callout `📚` com os links no índice do Notion;
    - `ESTADO.md` atualizado;
    - resumo final com os links do livro e do EPUB, os capítulos, os laboratórios não executados (se houver) e **a sugestão do próximo livro da trilha**.

## Nunca

- Escrever capítulos antes de a ementa ser aprovada.
- Inventar comando, opção, saída ou fonte. Se não conferiu, não afirma; se não executou, marca.
- Copiar trechos da documentação ou de outros livros além de uma citação curta com link.
- Usar logotipos, marcas ou mascotes de terceiros.
- Repetir num livro novo o que outro da trilha já ensina: referencie.
- Publicar antes da exportação nova, ou pular capítulos.
