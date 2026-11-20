# Plano de reformulação: Criador de Estudos e Aprimorador de Materiais

Documento de trabalho. Reúne as decisões tomadas com o dono do projeto (nov/2026) e serve de roteiro para refazer a skill, os scripts e a documentação. Quando a reformulação terminar, este arquivo e a pasta `plano/` saem do repositório (os pilotos viram `avaliacoes/`).

## Conteúdo

1. Objetivo e casos de uso
2. Decisões já tomadas
3. Repositórios: kit (template) × biblioteca pessoal
4. Estrutura da skill (padrão Agent Skills)
5. Fluxo
6. Perfis de área
7. Entradas (Docling e outros formatos)
8. Saídas (Markdown, EPUB, site com busca, GitHub, Notion)
9. Anatomia do livro (para quem estuda sozinho)
10. Imagens
11. Perfis de leitura
12. Didática
13. Fidelidade ao material (modo Aprimorar)
14. Confiança: fatos, fontes e revisão
15. Comunidade e licenças
16. Plano gratuito × pago
17. Fases
18. Pilotos (avaliações)
19. Fora do escopo
20. Economia de tokens
21. Robustez

## 1. Objetivo e casos de uso

Uma skill do Claude para **aprender habilidades em geral como autodidata**: o foco maior é programação, matemática e áreas correlatas, mas também idiomas, música e outras habilidades úteis. A explicação é a parte mais importante. Dois modos de produção (além de "Publicar livro pronto" e "Continuar", seção 5):

1. **Criar livro-curso a partir de uma ementa discutida** com o usuário, sobre qualquer tema (programação, matemática, inglês, violão, história da computação...). Do básico ao intermediário, com prática em todo capítulo e próximos caminhos.
2. **Aprimorar material** existente (Notion, PDF, EPUB, texto, link) para melhor compreensão, revisão e uso como base de pesquisa: manter a proposta do original, corrigir, completar o que falta e reescrever no padrão.

As diferenças entre áreas ficam em **perfis** (seção 6), não em skills separadas: um arquivo por área, lido só quando o tema é daquela área (padrão "organização por domínio" do guia oficial). Um tema pode combinar dois perfis (ex.: eletrônica = habilidades práticas + exatas). Se os pilotos mostrarem que uma área tem um fluxo realmente diferente (candidato: idiomas), ela vira uma skill própria depois.

O que faz o autodidata desistir é falta de **rumo** (por onde começar, quanto falta), de **retorno** (estou acertando?) e de **constância**. Todo livro responde a essas três coisas (seção 9).

## 2. Decisões já tomadas

| Tema | Decisão |
| --- | --- |
| Nome | "Criador de Estudos e Aprimorador de Materiais"; `name` técnico `criador-de-estudos`; repositório renomeado para `criador-de-estudos` |
| Onde roda | Claude (claude.ai / app), pago e gratuito; também deve funcionar no Claude Code |
| Fonte da verdade | Markdown. Notion deixa de ser a fonte; vira cópia feita no fim |
| Final padrão | **Publicar no GitHub + criar a cópia no Notion** (o fundamental); se não houver conexão e o usuário não quiser conectar, entrega o zip e explica onde enviar |
| Código | Sempre em bloco copiável. Nunca vira imagem |
| Respostas | `<details>` no Markdown e no site; apêndice "Respostas" com links de ida e volta no EPUB |
| Imagens | Escolha do usuário no início (seção 10) |
| Leitura | Telas grandes por padrão; leitor pequeno P&B se o usuário pedir (seção 11) |
| Site com busca | Parte fixa: GitHub Pages gerado dos mesmos Markdowns |
| Entradas | Notion, PDF, EPUB, DOCX, texto, link; Docling para converter documentos |
| Materiais do usuário | Nos dois modos, a skill oferece usar livros, PDFs, EPUBs ou uma pasta do Google Drive do usuário como fonte de apoio (seção 7) |
| Complementos | Google Drive, Notion, GitHub, Docling: cada um com um guia em `docs/complementos/`, e um README central que explica tudo; a skill só dá o link do guia |
| Licenças | CC BY-SA 4.0 (conteúdo) e MIT (código) no template; cada pessoa escolhe a sua |
| Conteúdo atual | Apagado (cursos, livros, progresso, ESTADO, releases `epubs` e `skill`). Os originais estão no Notion e serão base de futuras reformulações |
| Flashcards | Fora do escopo (nem app, nem arquivo de cards). A revisão espaçada fica dentro do livro |
| Áreas | Uma skill com 4 perfis: exatas e programação, idiomas, habilidades práticas, conhecimento geral |
| Execução | Livro inteiro num chat só, segmentado (um capítulo por vez, estado em arquivo), sem agentes; economia máxima de tokens |
| Conexões | Verificadas no início (GitHub e Notion); se faltar, pede e ensina; se o usuário recusar, segue e pergunta de novo no fim; se recusar de novo, zip e passo a passo |
| Livro já feito | Modo "Publicar livro pronto": recebe o pacote de um livro criado antes e só publica no GitHub e copia para o Notion |
| Laboratórios | Sessão → computador do usuário → execução guiada (usuário roda e cola a saída) → "não executado" |
| Pilotos | Docker Compose, Inglês, Violão, História da computação; falta um de Aprimorar (seção 18) |

## 3. Repositórios: kit (template) × biblioteca pessoal

"Use this template" do GitHub copia **todos** os arquivos do repositório. Para quem copiar receber a skill e não os livros do autor:

- **Este repositório vira o kit** (`criador-de-estudos`, marcado como template): skill, scripts, instaladores, modelo de biblioteca vazio, licenças, avaliações. Sem livros.
- **Cada pessoa cria a sua biblioteca** a partir do template (inclusive o autor, num repositório novo). Os livros ficam em `livros-criados/` e `materiais-aprimorados/` do repositório de cada um.
- A skill é **autocontida** (os scripts vão dentro dela, em `scripts/`). A biblioteca só precisa das pastas de livros, de `site/`, de `biblioteca.yaml`, `epub/estilo.css`, licenças e workflows; a skill confere e recria isso se faltar.
- **Workflows só do kit** (empacotar a skill na release, testes do kit) rodam apenas no repositório original (`if: github.repository == '<dono>/criador-de-estudos'`). Assim, quem cria a biblioteca a partir do template não gera releases da skill sem querer; nas bibliotecas rodam só os workflows de EPUB e do site.
- A skill avisa quando há versão nova: `livro.py status` lê só o número da última release do kit (poucos bytes). A skill **não** baixa instruções da internet durante o uso (gasta tokens, depende de rede e abriria espaço para instruções alteradas sem o usuário ver).

Estrutura do repositório (o kit é o template; a biblioteca de cada pessoa nasce igual, com as pastas de livros vazias):

```text
README.md                    ← porta de entrada curta: o que é, para quem, começo rápido, links
CONTRIBUTING.md              ← como contribuir com o kit (erros, temas, código)
CODE_OF_CONDUCT.md           ← código de conduta (Contributor Covenant, em português)
SECURITY.md                  ← como relatar problema de segurança
CHANGELOG.md                 ← mudanças por versão da skill (Keep a Changelog + versão semântica)
LICENSE  LICENSE-CODIGO      ← CC BY-SA 4.0 (conteúdo) e MIT (código), trocáveis
biblioteca.yaml              ← autor, repositório, licença, preferências padrão

livros-criados/              ← 1) livros feitos a partir de ementa (modo Criar)
  README.md                  ← lista GERADA (gerar.py): título, nível, duração, links
  <slug>/ ...                ← estrutura de um livro (abaixo)
materiais-aprimorados/       ← 2) materiais aprimorados (modo Aprimorar)
  README.md                  ← lista GERADA
  <slug>/ ...
site/                        ← 3) fonte do site no GitHub Pages (configuração e página inicial)
  README.md                  ← o que é, como ativar o Pages, endereço
  index.md  <config do gerador>
                             (o site gerado NÃO fica no repositório: a Action monta e publica)

docs/                        ← documentação do kit, no modelo Diátaxis
  README.md                  ← índice da documentação
  tutorial/                  ← aprender fazendo: "seu primeiro livro, do zero ao site"
  complementos/              ← tudo o que se conecta ou instala à parte
    README.md                ← visão geral: o que é cada um, para que serve, se é obrigatório,
                               em qual modo é usado e onde funciona (matriz abaixo)
    github.md  notion.md  google-drive.md  docling.md  github-pages.md
  guias/                     ← outras tarefas: criar sua biblioteca, publicar livro pronto, continuar livro
  referencia/                ← consulta: estrutura de pastas, livro.yaml, biblioteca.yaml, scripts
  explicacao/                ← entender: como a skill funciona, didática, economia de tokens
  decisoes/                  ← registros de decisão (ADR): 0001-uma-skill-com-perfis.md ...
skill/criador-de-estudos/    ← a skill (seção 4)
instalar/                    ← instaladores do Docling
avaliacoes/                  ← pilotos
epub/estilo.css
.github/
  workflows/                 ← epub.yml e site.yml (bibliotecas); kit.yml e testes.yml (só no kit)
  ISSUE_TEMPLATE/            ← reportar-erro.yml, sugerir-tema.yml
  PULL_REQUEST_TEMPLATE.md
```

Cada livro (`livros-criados/<slug>/` ou `materiais-aprimorados/<slug>/`):

```text
README.md             ← capa, mapa do livro com links, errata
livro.yaml            ← ementa, origem (criado | aprimorado, fonte), escolhas, progresso, edição
capa.png  capa.svg
capitulos/            ← 00-como-estudar.md, 01-..., NN-simulado.md, glossario.md
img/                  ← SVG, PNG, CREDITOS.md, _fonte/
projetos/             ← gerado: código extraído dos blocos (cursos de programação)
```

- A pasta do livro sai da `origem` do `livro.yaml`; o `slug` é único nas duas pastas.
- O site mostra as duas coleções na página inicial ("Livros criados" e "Materiais aprimorados"), com uma busca só para tudo.
- **Complementos:** o `docs/complementos/README.md` é o ponto único de entrada. Cada guia segue o mesmo roteiro (para que serve → o que precisa → passo a passo → como conferir que funcionou → problemas comuns). Quando falta um complemento, a skill explica em até 3 linhas e manda o link do guia, em vez de explicar tudo no chat (economiza tokens e a explicação fica sempre igual). Matriz de compatibilidade do README central (a conferir na fase 3):

  | Complemento | App no computador | Navegador | Claude Code | Plano gratuito |
  | --- | --- | --- | --- | --- |
  | GitHub (conector) | sim | sim | git direto | 1 conector personalizado |
  | Notion (conector) | sim | sim | via MCP | a conferir |
  | Google Drive (conector) | sim | sim | via MCP | a conferir |
  | Docling (MCP local) | sim | não | sim (CLI) | sim |
  | GitHub Pages | — | — | — | grátis em repositório público |

- **Uma fonte para cada informação:** `docs/` é escrito para pessoas; a skill, para o Claude. Quando os dois precisam do mesmo dado (ex.: campos do `livro.yaml`), `docs/referencia/` aponta para o arquivo da skill em vez de copiar.
- O `plano/` sai do repositório no fim; as decisões que importam viram ADRs em `docs/decisoes/`.

`livro.yaml` junta o que hoje está em `ementa.yaml` + `metadata.yaml` + `progresso/<slug>.json`.

**Grafo de conceitos** (ideia dos "livros didáticos inteligentes" de Dan McCreary): o `livro.yaml` lista os conceitos do livro, cada um com o capítulo onde é ensinado e de quais outros depende:

```yaml
conceitos:
  - {id: servico, nome: "serviço", capitulo: 1, depende: []}
  - {id: rede-projeto, nome: "rede do projeto", capitulo: 6, depende: [servico]}
```

`livro.py validar` recusa a ementa se um conceito depende de outro ensinado depois; `livro.py briefing` diz a cada capítulo quais conceitos já pode usar e quais deve ensinar; `gerar.py` usa o grafo para o mapa do livro e o glossário. Custa poucos tokens e protege a progressão.

## 4. Estrutura da skill (padrão Agent Skills)

Base: guia oficial de boas práticas (platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) e o repositório anthropics/skills.

**Uma skill, um arquivo por modo.** O padrão da Anthropic é uma skill por capacidade (pdf, docx, xlsx, pptx), com fluxos condicionais dentro dela (a docx tem "criar" e "editar"). Criar e Aprimorar compartilham a maior parte (didática, escrita, imagens, publicação). O que evita perda de contexto: SKILL.md curto, arquivos lidos só na etapa certa, checklist copiado na resposta, estado no `livro.yaml` e validação por script.

Esboço do `SKILL.md` e do modo Criar em `plano/esboco/` (2026-11-20).

```text
skill/criador-de-estudos/
  SKILL.md                  ← menu, regras gerais, laço de cada capítulo, modo Continuar (~120 linhas)
  modos/
    CRIAR.md                ← tema → pesquisa → parecer + ementa → aprovado
    APRIMORAR.md            ← material → ingestão → mapa → diagnóstico → plano
    PUBLICAR.md             ← conexões, GitHub, Notion; também o modo "Publicar livro pronto"
  referencias/
    DIDATICA.md             ← fundamentos e padrão de capítulo
    LIVRO.md                ← anatomia do livro (seção 9)
    areas/                  ← exatas.md, idiomas.md, habilidades.md, conhecimento.md
    FONTES.md               ← pesquisa, citação, checagem de fatos, direitos autorais
    VISUAL.md               ← famílias de imagem, design system, perfis de leitura
    EMENTA.md               ← modelo do livro.yaml (com grafo de conceitos), mudanças depois de aprovado
    EXEMPLOS.md             ← uma seção de exemplo por perfil
    CAPA.md
  scripts/                  ← executados, não lidos
    ingerir.py  livro.py  fatos.py  projetos.py  auditar.py
    diagrama.py  gerar.py  notion.py  ilustrar.py  svg/
  assets/                   ← modelos HTML das ilustrações, estilo.css, workflows, licenças
```

Regras do guia a aplicar:

- [ ] `description` em terceira pessoa, com o que faz e quando usar (cita "livro", "curso", "apostila", "PDF", "EPUB", "Notion", "história", "estudar")
- [ ] SKILL.md < 500 linhas (meta: < 200); referências a **um nível** de profundidade
- [ ] Arquivos com mais de 100 linhas começam com sumário
- [ ] Sem informação datada no texto da skill (versões e datas ficam no `livro.yaml`)
- [ ] Um termo por conceito (capítulo, livro)
- [ ] Um padrão com saída de emergência, não várias opções
- [ ] Ferramentas MCP com nome completo (`Notion:notion-fetch`)
- [ ] Scripts que resolvem o erro; dependências listadas e instaladas pelo próprio script
- [ ] Ciclo validar → corrigir → repetir (`auditar.py`) antes de cada entrega
- [ ] Plano verificável antes de executar (`livro.yaml` conferido por script)
- [ ] Avaliações (os pilotos) e teste com Haiku, Sonnet e Opus
- [ ] Sem duplicação: preferências num lugar só

## 5. Fluxo

```text
0 Conexões: verifica GitHub e Notion ─► falta alguma? pede e ensina ─► usuário recusa? segue sem
Menu
 ├─ 1 Criar a partir de ementa : tema ─► pesquisa ─► parecer ─► ementa ──────────────┐
 ├─ 2 Aprimorar material       : material ─► ingestão ─► mapa e diagnóstico ─► plano ┤  ajustes até "aprovado"
 │                                                                                   ▼
 │   perfil de área + escolhas (imagens, leitura) ─► escrever o livro inteiro, um capítulo por vez,
 │   no MESMO chat (checar fatos, auditar e salvar ponto de controle a cada capítulo)
 │       ─► EPUB + pacote ─► próximos caminhos ─► PUBLICAR (abaixo)
 ├─ 3 Publicar livro pronto    : recebe o pacote (zip) de um livro feito antes ─► confere ─► PUBLICAR
 └─ 4 Continuar                : só se o chat cair ou bater o limite de uso; lê o ponto de controle e retoma

PUBLICAR (padrão: GitHub + Notion)
 GitHub conectado? ── sim ─► envia para livros-criados/ ou materiais-aprimorados/<slug>/ ─► site e EPUB pela Action
                   └─ não ─► "Quer conectar?" ─► sim: ensina, confere de novo ─► envia
                                             └─ não: zip + onde extrair e como enviar
 Notion conectado? ── sim ─► pede o link da página ─► cria a cópia (só com SVG)
                   └─ não ─► "Quer conectar?" ─► sim: ensina, confere de novo ─► cria a cópia
                                             └─ não: encerra (pode voltar depois pelo modo 3)
```

- **Conexões no início:** a skill verifica sozinha quais ferramentas existem (não pergunta o que dá para descobrir). Se faltar o GitHub ou o Notion, explica em poucas linhas para que serve, ensina a conectar e espera. Se o usuário não quiser, segue sem: o livro é feito do mesmo jeito.
- **Publicar livro pronto (modo 3):** para quem fez o livro antes sem publicar. O usuário envia o zip que a skill entregou (ele traz o `livro.yaml`); a skill roda o auditor, envia para o caminho certo do repositório do usuário (`livros-criados/<slug>/` ou `materiais-aprimorados/<slug>/`, pela `origem` do `livro.yaml`) e cria a cópia no Notion. Material que não foi feito pela skill vai para o modo Aprimorar.

- Os dois modos terminam no mesmo `livro.yaml` aprovado; dali em diante o processo é um só.
- **O livro inteiro sai num chat só.** Cada capítulo vai para arquivo assim que termina, e o `livro.yaml` guarda o progresso e o resumo de cada capítulo. Se o chat for compactado automaticamente (o Claude resume o histórico quando ele fica grande), nada se perde, porque a skill trabalha a partir dos arquivos e não da memória da conversa.
- **Ponto de controle:** se o GitHub estiver conectado (seção 8), commit silencioso numa branch de rascunho (`rascunho/<slug>`) a cada capítulo; "publicar" no fim é juntar à `main`. Sem GitHub, a skill oferece um zip parcial a cada parte do livro. Assim um limite de uso ou uma queda não perde trabalho.
- **GitHub desde o começo:** com a conexão feita no início, o ponto de controle (branch de rascunho) funciona desde o 1º capítulo. Se o usuário só conectar no fim, não há rascunho no GitHub; o ponto de controle foi o zip parcial.
- **Notion no fim:** a cópia é parte do final padrão. Se o conector não estiver ativo, a skill explica onde ativar (Configurações → Conectores), espera o usuário confirmar, pede o link da página onde o livro vai ficar e faz a cópia.
- **Parecer do tema:** o que é, para que serve, pré-requisitos, currículo usual (ementas de universidades, livros-texto, documentação oficial), equívocos comuns, tempo típico de estudo. No perfil "conhecimento geral": obras de referência, fatos e nomes centrais, mitos populares a corrigir.
- Escopo padrão: básico → intermediário. "Fica para depois" vira **Próximos caminhos** (2 a 4 livros sugeridos).

## 6. Perfis de área

Cada perfil é um arquivo em `referencias/areas/`, lido só quando o tema é daquela área. Define a prática, a verificação, as fontes confiáveis, as imagens típicas e os cuidados.

| Perfil | Temas | Prática | Verificação | Imagens típicas | Cuidados |
| --- | --- | --- | --- | --- | --- |
| **Exatas e programação** | programação, matemática, estatística, cálculo de circuitos | exercícios graduados, questões e provas, laboratórios, projetos com código em blocos | executar o código e os testes; refazer contas; conferir demonstrações | arquitetura, fluxo, estrutura, gráficos, figuras geométricas | fórmulas em LaTeX; versão de referência e data de revisão em tecnologia |
| **Idiomas** | inglês e outros | o essencial da língua; ler, ouvir, falar, escrever; rotina autodidata | gabarito e critérios de correção | linha do tempo de tempos verbais, mapas de vocabulário | como aprender rápido com base em evidência; pronúncia em IPA + aproximação para falante de português; indicar onde ouvir (o livro não tem áudio) |
| **Habilidades práticas** | música, eletrônica, desenho, culinária... | rotina de prática deliberada (minutos, andamento, repetições) | critério de "pronto" mensurável | diagrama de acorde, tablatura, esquema elétrico, protoboard, passo a passo | **segurança obrigatória** quando houver risco (tensão de rede, baterias, ferramentas); lista de materiais; simulador quando não há peças; cifra e tablatura também em texto; sem letras protegidas |
| **Conhecimento geral** | história da computação, ciências, conceitos | questões de compreensão, linha do tempo, análise de fontes | checagem de fatos e fontes | linha do tempo, mapa conceitual, imagens de época | fato × interpretação × lenda; datas e nomes conferidos; curiosidades só com fonte |

Temas de saúde, direito e finanças, em qualquer perfil: fonte oficial obrigatória e aviso de que não substitui um profissional.

## 7. Entradas (Docling e outros formatos)

`scripts/ingerir.py <arquivo|pasta|url>` normaliza tudo para Markdown + sumário (JSON):

| Entrada | Padrão | Saída de emergência |
| --- | --- | --- |
| PDF, DOCX, PPTX, HTML, imagem | Docling onde ele existir: MCP no app do computador, terminal do usuário, Claude Code | na sessão do Claude (onde instalar o Docling é pesado: modelos de vários GB), extração leve por biblioteca Python ou leitura nativa do PDF anexado |
| EPUB | zip → XHTML → Markdown (script) | Docling no HTML extraído |
| Notion | `Notion:notion-fetch` página a página | exportação HTML |
| Link | WebFetch | texto colado pelo usuário |
| Texto/Markdown | direto | — |
| Google Drive | conector do Google Drive: busca por assunto, abre só os arquivos escolhidos | o usuário baixa e anexa |

**Materiais do usuário como fonte de apoio** (nos dois modos):

- **Criar:** junto das perguntas iniciais, a skill oferece (sem obrigar): "Se tiver livros, PDFs, EPUBs ou uma pasta no Google Drive sobre o tema, pode mandar: uso como fonte".
- **Aprimorar:** além do material principal, aceita materiais correlatos para completar lacunas e conferir fatos.
- **Economia:** cada material passa pelo `ingerir.py`, que devolve só o sumário; a skill lê apenas as seções úteis para cada capítulo, nunca o livro inteiro. No Drive, busca por assunto e lista os arquivos antes de abrir; o usuário confirma quais usar.
- **Direitos autorais:** livros e PDFs do usuário servem para entender, estruturar e conferir; nada é copiado nem publicado. Entram em `## 📚 Fontes` como referência ("Livro X, cap. 3"). Vale o mesmo contrato da seção 13.
- O Docling converte esses materiais onde existir (seção 7, tabela acima). O guia `docs/complementos/docling.md` e os instaladores em `instalar/` ensinam a instalação local.

**Docling local (instalador):** `instalar/instalar-docling.ps1` (Windows) e `instalar/instalar-docling.sh` (macOS/Linux): instala o `uv`, pré-baixa o Docling e os modelos, e (opcional) grava o bloco `mcpServers` no `claude_desktop_config.json` no nível certo, com o caminho do `uvx` detectado. Situação verificada na máquina do autor (2026-11-19): Docling CLI 2.140 instalado; MCP `docling` configurado no app (`docling-mcp[local]==2.1.0`, `mcp<2`, stdio) e iniciando sem erro. Limite conhecido: o MCP pela ponte do app espera ~80 s por chamada; PDF grande vai pelo terminal ou é anexado.

## 8. Saídas

1. **Pacote para baixar** (sempre): zip com a pasta do livro já no caminho do repositório (`livros-criados/<slug>/` ou `materiais-aprimorados/<slug>/`) e `<slug>.epub`. Funciona sem GitHub, inclusive no plano gratuito.
2. **EPUB**, gerado na sessão (Pandoc via `pip install pypandoc_binary`) e pela Action:
   - `gerar.py` move cada `<details>` para o apêndice "Respostas", com "Ver resposta" (ida) e "Voltar ao exercício" (volta);
   - filtro de links converte `capitulo.md#secao` em links internos do EPUB.
3. **Site com busca** (parte fixa): a cada envio para o GitHub, uma Action gera um site estático a partir dos mesmos Markdowns e publica no GitHub Pages, em `https://<usuario>.github.io/<repositorio>/`. Ninguém mexe no site à mão.
   - **Página inicial:** a estante da biblioteca, com a capa, o nível, a duração e o link de cada livro, e a busca no topo.
   - **Página de cada livro:** sumário lateral com os capítulos, mapa do livro, texto com imagens, código com botão "copiar", `<details>` funcionando, "anterior / próximo", modo escuro e botão para baixar o EPUB.
   - **Busca:** instantânea, em todos os livros ao mesmo tempo, funcionando no computador, no celular e no navegador do Ebox.
   - **Ativação única:** no repositório, Settings → Pages → Source: "GitHub Actions" (um clique; a skill ensina na primeira publicação).
   - **Custo:** grátis para repositório público; repositório privado precisa de plano pago do GitHub para ter Pages.
   - Ferramenta escolhida na fase 3 (MkDocs/Zensical, que faz uma busca única para a biblioteca inteira, ou mdBook), conferindo qual está mais bem mantida.
4. **GitHub**, em três níveis (o primeiro que der certo):
   1. **Conector do GitHub:** a skill pergunta se o usuário quer conectar. O caminho oficial é o servidor MCP hospedado pelo próprio GitHub (`https://api.githubcopilot.com/mcp/`), adicionado como conector personalizado (Configurações → Conectores → Adicionar conector personalizado). Funciona em todos os planos; no gratuito, só cabe **um** conector personalizado. Com ele: branch de rascunho, commit por capítulo e publicação no fim. A autenticação no claude.ai (OAuth ou token) e as ferramentas de escrita disponíveis precisam ser conferidas no piloto.
   2. **Ambiente com git** (Claude Code, ou app com o repositório já disponível na sessão): commit e push direto.
   3. **Sem conexão** (o usuário não quer ou não consegue): o zip já vem com as pastas do repositório (`livros-criados/<slug>/...` ou `materiais-aprimorados/<slug>/...`); a skill diz onde extrair e dá o passo a passo pelo site do GitHub ("Add file → Upload files", arrastando a pasta) ou pelo GitHub Desktop. O site aceita até 100 arquivos por envio: livro com mais arquivos vai em partes, e a skill diz quais.

   Nunca pedir que o usuário cole um token do GitHub no chat. O Markdown também se lê direto no GitHub; cada capítulo termina com "◀ anterior · mapa do livro · próximo ▶" (gerado por script).
5. **Notion** (parte do final padrão): `notion.py` converte (`<details>` → toggle, `>` → callout), sobe os SVGs e omite as ilustrações PNG. O índice do livro no Notion ganha os links do site, do GitHub e do EPUB.

## 9. Anatomia do livro (para quem estuda sozinho)

Novo `referencias/LIVRO.md`. Todo livro tem:

| Parte | O que resolve | Conteúdo |
| --- | --- | --- |
| **Mapa do livro** (README e início do EPUB) | rumo | cheat sheet do livro inteiro + sumário em texto com links para cada capítulo e seção; tempo estimado de cada capítulo |
| **Cap. 0 — Como estudar este livro** | constância | técnicas de estudo em 1 página (recuperação, espaçamento, explicar com as próprias palavras), cronograma em três ritmos (leve, médio, intenso) para o leitor escolher, como usar as revisões e o simulado |
| **Nivelamento** | rumo | pré-teste curto com rota ("acertou 1 a 3? comece no cap. 4") |
| **Cheat sheet por seção** | rumo | abre cada seção, seguido de links para os capítulos dela |
| **Capítulos** | aprendizagem | padrão da seção 12; seções marcadas **essencial** ou **aprofundamento** (caminho mínimo para quem tem pouco tempo); capítulo 1 sempre com uma vitória concreta |
| **Retorno sem professor** | retorno | gabarito comentado (por que o certo é certo e os erros comuns); critérios de correção para respostas abertas; comandos prontos para usar qualquer IA como tutor ("corrija sem me dar a resposta", "faça 5 perguntas sobre este capítulo") |
| **Revisão espaçada no livro** | constância | fim de cada capítulo: "revise hoje os capítulos X e Y" + perguntas cumulativas de capítulos anteriores |
| **Projetos** (programação, eletrônica...) | aplicação | código dividido em blocos com o nome do arquivo, dentro de `<details>`; `projetos.py` extrai os blocos, monta o projeto e executa; se não rodar, o livro não é entregue |
| **Simulado final** | retorno | questões ligadas a cada objetivo da ementa; gabarito comentado com link para o capítulo; tabela "errou 3, 7 e 12 → revise caps. 4 e 9" |
| **Glossário e índice remissivo** | consulta | termos com link para onde são explicados (em TI e idiomas, com o termo em inglês) |
| **Próximos caminhos** | continuidade | 2 a 4 livros sugeridos |
| **Transparência** | confiança | data da conferência, fontes, "revisado por humano: sim/não", edição e histórico de mudanças, errata |

## 10. Imagens

Perguntado ao usuário no início (gravado no `livro.yaml`):

1. **Só diagramas SVG** (padrão no plano gratuito)
2. **SVG + ilustrações** (HTML→PNG pelo Playwright, texto sempre correto)
3. **SVG + ilustrações com API de imagem paga** (pede chave e liberação de rede; sem texto gerado pela IA dentro da imagem)

| Família | Uso | Notion |
| --- | --- | --- |
| SVG (kit v3) | esquema, estrutura, comparação, fluxograma com valores, linha do tempo, diagrama de acorde, esquema elétrico, cheat sheet | sim |
| Ilustração PNG | processo ou visão geral em que a imagem explica melhor que o texto | não |
| Imagem real com licença livre | fotos e obras de época (história), instrumentos, componentes; de acervos como Wikimedia Commons, só domínio público ou licença livre | sim |

Regras:

- O que o aluno precisa **reproduzir** fica em texto (código, fórmula, comando, cifra, tablatura, passo a passo).
- Cor e ícone sempre com significado; texto alternativo descritivo em toda imagem.
- Imagem real: autor, fonte, licença e link registrados em `img/CREDITOS.md` e na legenda. Sem logotipos ou marcas de terceiros.
- Fonte das ilustrações guardada em `img/_fonte/` para regerar.

## 11. Perfis de leitura

Perguntado ao usuário junto com as imagens (gravado no `livro.yaml`; o gerador de diagramas e o auditor leem os limites dali):

| Item | Telas grandes (padrão) | Leitor pequeno (Kindle/Kobo, P&B) |
| --- | --- | --- |
| Para | monitor, leitores de 10" ou mais, coloridos | telas de 6–7" em tons de cinza |
| Largura dos diagramas | ~960 (PNG 2x no EPUB) | 480 |
| Linha de código | ~80 caracteres | 60 |
| Tabelas | até 6 colunas | até 4 |
| Cheat sheet | folha inteira | dividido em 2 partes no EPUB |
| Cor | pode carregar sentido, sempre com rótulo junto | nunca o único sinal |

Opcional a decidir: gerar PDF (A4) além do EPUB.

## 12. Didática

Novo `referencias/DIDATICA.md`, com fundamento explícito. Esqueleto: Primeiros Princípios de Merrill (problema → ativação → demonstração → aplicação → integração), mais carga cognitiva (Sweller), multimídia (Mayer), prática de recuperação, espaçamento e intercalação, elaboração, exemplos concretos, alinhamento construtivo (Biggs) e planejamento reverso (Wiggins e McTighe).

| Manter | Mudar |
| --- | --- |
| Nesta aula, De onde paramos, por quê → definição → exemplo, armadilha comum, objetivos com verbo de ação, respostas recolhidas | Analogia só quando o conceito é abstrato e novo, dizendo onde ela falha (fim da cota "uma por imagem" e do aviso `sem_analogia`) |
| | Revisão com perguntas cumulativas de capítulos anteriores + aquecimento no início |
| | Escada de prática em todo capítulo: exemplo resolvido → completar → fazer sozinho → desafio |
| | Prever antes de ver / explicar com as próprias palavras |
| | Mapa da seção no início; Revisão e Resumo no fim; cheat sheet como consulta |
| | Estrutura base fixa, ordem ajustada pelo perfil de área (em conhecimento geral: pergunta-guia → contexto → narrativa → fontes → interpretações → síntese) |

Retirar: mapas mentais de Buzan (evidência fraca); manter mapas conceituais (Novak).

## 13. Fidelidade ao material (modo Aprimorar)

Contrato apresentado no plano e aprovado pelo usuário:

1. **Promessa do material** por escrito: objetivo, público, nível, sequência.
2. **Tabela de correspondência** original → capítulo novo; nada some sem explicação.
3. **Acréscimos classificados:** lacuna essencial (pré-requisito usado e não ensinado, item prometido e ausente, passo que quebra a prática) → entra; aprofundamento útil → quadro curto; fora da promessa → só em Próximos caminhos.
4. **Limite:** conteúdo novo ≤ ~20%; capítulo novo só se estiver no plano aprovado; ordem do original mantida salvo erro didático explicado.
5. **Conferência final:** cada capítulo aponta de onde veio.
6. **Direitos autorais:** do material de terceiros só estrutura, tópicos e objetivos; explicações próprias; nada copiado; o original nunca é publicado.

## 14. Confiança: fatos, fontes e revisão

- **Checagem de fatos** em todo capítulo, antes da auditoria: uma segunda leitura lista cada afirmação com data, número, nome ou citação e confere com as fontes do `livro.yaml`. Afirmação sem fonte é corrigida, marcada ou removida.
- **Fato × interpretação × lenda** separados no texto (obrigatório no perfil conhecimento geral; vale para qualquer tema com controvérsia).
- Citação curta (< 15 palavras) entre aspas e com link; nada copiado.
- `## 📚 Fontes` em todo capítulo, com data de conferência; bibliografia comentada ("para saber mais") no fim do livro.
- Em temas que mudam (tecnologia, leis, saúde): data de "revisar em" no `livro.yaml`.

## 15. Comunidade e licenças

- `LICENSE` (CC BY-SA 4.0, conteúdo) e `LICENSE-CODIGO` (MIT) no template; a skill pergunta a licença na primeira vez que monta a biblioteca da pessoa.
- Modelos de issue: "reportar erro" e "sugerir tema". Errata no README de cada livro.
- Edição do livro (`1.0`, `1.1`...) com histórico de mudanças.

## 16. Plano gratuito × pago

- Skills funcionam no plano gratuito com execução de código ligada (Configurações → Recursos). O gratuito tem limites menores e não tem Opus.
- Por isso: um capítulo por vez, estado sempre no `livro.yaml` e ponto de controle a cada capítulo. Se o limite de uso acabar no meio, o usuário continua no mesmo chat quando o limite renovar (ou num chat novo, pelo modo Continuar).
- GitHub e Notion são o **final padrão**, mas não são obrigatórios: sem eles o livro é feito do mesmo jeito e o pacote para baixar é sempre gerado. No gratuito cabe só um conector personalizado (o do GitHub); conferir no piloto se o Notion, que é do catálogo de conectores, fica fora desse limite.
- Sem agentes: tudo no próprio chat, segmentado (ver seção 20). O modo coordenador da skill antiga sai.
- Testar a skill com Haiku e Sonnet, não só Opus.

## 17. Fases

| Fase | Entregas |
| --- | --- |
| 0. Esboço | `plano/esboco/`: SKILL.md e modo Criar para o dono revisar antes de apagar qualquer coisa |
| 1. Repositório | Apagar conteúdo antigo e releases; renomear para `criador-de-estudos` e marcar como template; `livros-criados/`, `materiais-aprimorados/` e `site/` vazios com README; arquivos de comunidade (CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, CHANGELOG, licenças, modelos de issue e PR); README curto; esqueleto de `docs/` (Diátaxis, com `complementos/` e o README central) |
| 2. Skill | `criador-de-estudos` com menu e modos; DIDATICA, LIVRO, areas/, VISUAL, FONTES novos; scripts dentro da skill; checklist da seção 4; zip na release |
| 3. Entradas e saídas | `ingerir.py` + instaladores do Docling; materiais do usuário (anexos e Google Drive); guias de `docs/complementos/` conferidos de verdade (matriz de compatibilidade); `gerar.py` (pacote zip, EPUB com apêndice de respostas e links internos, navegação, mapa, glossário, catálogo); site com busca; `projetos.py`; `notion.py`; `modos/APRIMORAR.md` e `modos/PUBLICAR.md` |
| 4. Imagens e leitura | escolha do usuário; modelos HTML→PNG; imagens com licença livre e créditos; perfis de leitura; API paga opcional |
| 5. Pilotos | rodar os pilotos da seção 18 em chats novos, anotar falhas e voltar à fase 2 |
| 6. Doações (no fim) | Seção "Apoie o projeto" no README do kit: Pix, transferência bancária e criptomoedas (o autor ainda vai aprender a criar a carteira). Cuidados: não expor dados pessoais (chave Pix aleatória ou e-mail), `.github/FUNDING.yml` (botão "Sponsor"), e o template não pode levar os dados de doação do autor para os repositórios dos outros sem aviso |

## 18. Pilotos (avaliações)

Ficam em `plano/pilotos/` e viram `avaliacoes/` na fase 2. Cada um tem o pedido, as entradas e os comportamentos esperados. Em todos, além do que está no arquivo: conexões verificadas no início, livro inteiro num chat só, e final padrão (GitHub + Notion, ou zip com passo a passo se o usuário recusar).

1. `01-docker-compose.md`: Criar, com ementa já aprovada (tecnologia, projeto executado).
2. `02-ingles.md`: Criar a partir só do tema (idiomas, autodidata, estado da arte).
3. `03-violao.md`: Criar a partir só do tema (música, prática motora, diagramas em SVG).
4. `04-historia-da-computacao.md`: Criar a partir só do tema (conhecimento geral, checagem de fatos, linha do tempo, imagens de época).
5. *A definir:* Aprimorar, a partir de um curso do Notion ou de um PDF.

## 19. Fora do escopo

- Programa ou arquivo de flashcards (a revisão espaçada fica dentro do livro).
- Áudio e vídeo gerados.

## 20. Economia de tokens

Requisito do dono: gastar o mínimo possível no plano pago. Regra geral: **o Claude escreve explicação; script faz todo o resto.**

| Onde se gasta | Como economizar |
| --- | --- |
| Instruções da skill | SKILL.md com ~120 linhas (esboço: 117); cada arquivo lido só na etapa que pede; um perfil de área e um exemplo por livro (o do perfil), nunca todos |
| Texto repetitivo | Script gera o esqueleto do capítulo (títulos das seções fixas), a navegação, o mapa do livro, o glossário com links, o apêndice de respostas, o catálogo, o EPUB e o site. O Claude só preenche o conteúdo |
| Diagramas | O Claude escreve uma especificação curta (YAML/JSON de ~20 linhas); o script desenha o SVG (hoje o SVG inteiro chega a 200+ linhas). Cheat sheets já funcionam assim |
| Conferir imagens | Validador por script (texto saindo da caixa, sobreposição, tamanho) em vez de olhar cada PNG; quando precisar ver, uma folha de contato com todas as imagens do capítulo numa imagem só |
| Continuidade entre capítulos | Ao terminar um capítulo, gravar no `livro.yaml` um resumo de 3–5 linhas (o que ensinou, termos, exemplos usados). O próximo capítulo lê esse resumo, não o capítulo anterior |
| Histórico do chat | O livro sai num chat só (decisão do dono). O histórico é reenviado a cada passo e cresce; por isso o conteúdo pesado (texto dos capítulos, saídas de scripts) vai para arquivo e não é repetido no chat, e cada capítulo começa só com o briefing compacto (capítulo do `livro.yaml` + resumo do anterior) |
| Saída dos scripts | JSON curto só com o que exige ação (erros com arquivo e linha); nunca imprimir arquivos inteiros |
| Correções | Editar o trecho apontado pelo auditor, não reescrever o capítulo |
| Material de entrada (Aprimorar) | `ingerir.py` divide o material por seção; cada capítulo lê só a seção de origem dele |
| Pesquisa | Uma vez, na etapa do parecer; as fontes ficam no `livro.yaml` e os capítulos reaproveitam. Buscas com pergunta específica, sem baixar páginas inteiras |
| Checagem de fatos | Script extrai as frases com datas, números e nomes; só elas são conferidas |
| Trabalho segmentado, sem agentes | **Segmentar sempre:** um capítulo por vez, com briefing compacto e saída em arquivo. **Sem agentes** (decisão do dono): a Anthropic mede que um agente gasta ~4× e um sistema com vários agentes ~15× os tokens de um chat, e capítulos de um livro dependem uns dos outros, o caso em que vários agentes funcionam mal |
| Mensagens ao usuário | Status curto; o detalhe fica nos arquivos |
| Modelo | Recomendar Opus (ou o mais forte disponível) para parecer, ementa e plano; Sonnet para escrever os capítulos, que é a parte mais longa |

Os pilotos medem o gasto (tokens por capítulo, quando a interface mostrar; no Claude Code é visível) para comparar antes e depois de cada ajuste.

## 21. Robustez

| Risco | Como a skill se protege |
| --- | --- |
| Ambiente varia (app, navegador, Claude Code; gratuito ou pago; com ou sem GitHub, Notion, agentes, Docling, rede) | Checagem do ambiente no início, sem perguntar ao usuário; cada recurso tem um caminho alternativo (seção 7, seção 8) |
| Chat compactado ou limite de uso no meio do livro | Estado e capítulos em arquivo; ponto de controle por capítulo (branch de rascunho ou zip parcial); modo Continuar |
| Publicar no GitHub não disponível no ambiente | Três níveis da seção 8: conector do GitHub → git na sessão → zip com as pastas do repositório e passo a passo |
| Laboratório que precisa de serviço (Docker, banco de dados) e não roda na sessão | Nesta ordem: (1) rodar na sessão; (2) rodar no computador do usuário, se ligado ao app; (3) **execução guiada**: a skill passa os comandos, o usuário roda e cola só as linhas pedidas da saída, e a skill usa a saída real; (4) se o usuário não quiser, marcar "não executado" com aviso e listar no resumo |
| Ferramentas locais (MCP do Docling, conectores locais) não existem no navegador | Só funcionam nos chats do app no computador; no navegador, Docling pelo terminal do usuário ou leitura nativa do PDF |
| Instalação de Pandoc/Playwright falhar na sessão | EPUB e site gerados pela Action do GitHub; sem GitHub, entregar só o Markdown e avisar |
| Fato inventado ou desatualizado | Pesquisa com fontes no parecer, checagem de fatos por capítulo, "revisado por humano: não" até o usuário revisar |
| Material de terceiros (Aprimorar) | Contrato de fidelidade e regras de direitos autorais (seção 13) |
| Script com erro | Testes automáticos do kit a cada push; scripts que podem ser rodados de novo sem estragar nada |
| Skill que piora com o tempo | Pilotos como avaliação fixa; rodar de novo a cada mudança grande |
