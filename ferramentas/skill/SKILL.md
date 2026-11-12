---
name: "revisar-curso-biblioteca"
description: "Remodela um curso do Notion (aulas, código, imagens, cheat sheets) e publica na Biblioteca de Estudos do GitHub com EPUB. Use quando o usuário pedir para revisar, completar, refazer imagens ou publicar um curso do Notion. Não use para dúvidas pontuais sobre um conteúdo, para editar uma página avulsa do Notion que não é curso nem para outros repositórios."
---

# Revisar curso e publicar na Biblioteca de Estudos

Você recebe o link de um curso no Notion (página índice com subpáginas de aulas) e transforma as anotações em material de ensino e revisão de alta qualidade. Depois publica no repositório `Joshpcbrrj/biblioteca-de-estudos`, que gera um EPUB por curso. Todo texto produzido, e a resposta ao usuário, é em **português do Brasil**.

**Arquivos auxiliares e scripts ficam no repositório** (clone com `add_repo` acesso `push` e `git clone --depth 1`). Leia cada arquivo só quando a etapa pedir:

| Arquivo | Quando ler |
| --- | --- |
| `ferramentas/skill/DIDATICA_VISUAL.md` | antes de criar, trocar ou auditar imagens (Fase 4) |
| `ferramentas/skill/NOTION.md` | antes da primeira edição no Notion da sessão e sempre que uma chamada falhar |
| `ferramentas/skill/PUBLICACAO.md` | só depois que o usuário exportar (Fases 6 e 7) |
| `ferramentas/skill/CAPA.md` | só ao criar ou refazer a capa |
| `ferramentas/svg/README.md` | ao gerar diagramas com o kit |

## Preferências fixas do usuário

1. **Nome do curso:** `<Plataforma(s)>: <Nome do curso> - <Criador do curso>` (ex.: `Udemy/ YouTube: Lógica de programação com Portugol Studio - Bóson Treinamentos`). Várias plataformas separadas por `/ `. Vale no título do índice do Notion, no `title` do `metadata.yaml`, no README do curso e no catálogo. Mantenha ícone, capa e cabeçalho originais da página.
2. **Respostas recolhidas.** No Markdown, toda resolução de exercício ou desafio fica em `<details><summary>Ver resposta</summary>`, com **linha em branco depois do `<summary>` e antes do `</details>`** (sem elas o GitHub e o Pandoc não processam o Markdown de dentro). Versões alternativas: outro `<details>` com `Ver versão estendida`. Código de exemplo das aulas fica visível. No Notion, resoluções ficam em toggles `Resolução`.
3. **Leitura em e-readers** (Kindle, Kobo, eboox): nada cortado; código com linhas de até ~60 caracteres; tabelas de no máximo 4 colunas; diagramas legíveis em 6–7 polegadas.
4. **Pasta do curso no GitHub** só com `README.md`, `metadata.yaml`, `capa.png`, `capa.svg`, `aulas/` e `img/`.
5. **Capa de editora em todo livro**, original e diferente das outras, com `Criado por: Josué B. Almeida` (ver `CAPA.md`).
6. **Notion e GitHub com o mesmo conteúdo.** O Notion é a fonte; mudança nascida no Markdown volta para o Notion.
7. **O curso cumpre o escopo inteiro** (Fase 2): o que falta ou está raso é escrito como conteúdo do próprio curso.
8. **Exemplo visual para todo conceito desenhável** (estruturas de controle, dados, memória, fluxos, arquiteturas, protocolos, comparações, tabelas de banco, gráficos). Aula sem imagem só se o tema for puramente textual.
9. **Remodelar tudo, parar e esperar a exportação.** Faça as Fases 1 a 5 no Notion; ao terminar, **pare**, resuma e peça ao usuário para exportar o índice (HTML, com subpáginas). Não publique a partir de exportação antiga. Vale também para cursos já publicados.
10. **Um curso por vez**, na ordem que o usuário pedir.

## Checklist do workflow

Crie uma lista de tarefas com estes itens e marque ao concluir. Não volte a uma etapa marcada sem motivo novo.

1. **Preparar:** clonar o repositório; `python3 ferramentas/progresso.py <curso> status` para saber se já há trabalho feito (retome da `proxima`, nunca do início).
2. **Fase 1 – Levantamento:** fetch do índice e de **todas** as subpáginas; cadastrar os ids na ordem com `progresso.py <curso> init <ids...>`.
3. **Auditoria mecânica** (se o curso já está no repositório): `python3 -I ferramentas/auditar_curso.py <area>/<slug> --resumo`. Use o JSON como lista de trabalho (aulas sem imagem, imagens sem analogia, código longo ou sem comentário, tabelas largas, seções ausentes). Não refaça essas contagens à mão.
4. **Fase 2 – Escopo:** tabela escopo × conteúdo; completar o que falta.
5. **Fases 3, 4 e 5 – por página**, uma de cada vez: fetch → revisar texto e código (padrão 3.1) → gerar/atualizar SVGs → `raw_urls.py` → uploads → `replace_content` → `progresso.py <curso> feito <id>`. Commit + push dos SVGs antes dos uploads.
6. **Cheat sheet de cada seção** (DIDATICA_VISUAL.md) e índice no padrão da Fase 5.
7. **Parar e pedir a exportação** (preferência 9), com o resumo do que mudou.
8. **Fase 6 – Publicação** (PUBLICACAO.md): converter, revisar, `gerar_epub_local.py`, capa, commit, acompanhar a Action.
9. **Fase 7 – Sincronizar e resumir** (PUBLICACAO.md).

**Curso já revisado neste padrão:** refaça só a Fase 2 (e o que ela apontar), pare e peça a exportação (preferência 9), depois siga para a Fase 6.

Trabalhe de forma autônoma: só pergunte se algo for realmente ambíguo e caro de refazer (plataforma ou criador desconhecidos, área do curso).

## Scripts (execute e apresente o resultado; não refaça o cálculo raciocinando)

| Script | Entrada → saída | Quando |
| --- | --- | --- |
| `ferramentas/auditar_curso.py <area>/<slug> [--resumo]` | pasta do curso → JSON com estrutura, título, e por aula: imagens, imagens sem analogia, linhas de código > 60, blocos sem comentário, tabelas > 4 colunas, sobras de HTML do Notion, `<details>` sem linha em branco, seções ausentes; imagens faltando/órfãs | passo 3 e de novo antes do commit da Fase 6 |
| `ferramentas/progresso.py <curso> init/feito/nota/pendentes/status` | ids das páginas → estado em `/tmp/ss/progresso-<curso>.json` | ao cadastrar páginas, ao concluir cada uma, ao retomar |
| `ferramentas/raw_urls.py <area>/<slug> [arquivos.svg]` | nomes → JSON com links raw fixados no hash e se o commit já está no GitHub | antes de subir SVGs ao Notion (`publicado` precisa ser `true`) |
| `ferramentas/gerar_epub_local.py <area>/<slug> [saida.epub]` | curso → EPUB + JSON com imagens faltando e resultado do `verificar_epub.js` | Fase 6, antes do commit |
| `ferramentas/notion2md.py <exportação> <curso>` | exportação HTML → `aulas/` e `img/` | Fase 6 |
| `ferramentas/svg/cheatsheets.py [nomes]` e `v3.py` | dados dos cards → cheat sheets 3×4 + partes do EPUB; `restyle()` aplica o tema | Fase 4 |

Rode Python com `-I` quando o script ler arquivos baixados. Ao apresentar o resultado de um script, resuma os números e liste só o que exige ação.

---

## Fase 1. Levantamento

1. Fetch da página índice e de **todas** as subpáginas, uma por uma.
2. Identifique a **proposta**: nome, plataforma(s), criador, descrição, ementa (PDF ou bookmark, se houver). Sem proposta escrita, deduza pelo título e pelas aulas.
3. Renomeie o índice no formato da preferência 1.
4. Monte o mapa: seção → aulas → conceitos → códigos/fórmulas → imagens → anexos (pdf, file, bookmark).
5. Classifique a área: `programacao` ou `matematica`.

## Fase 2. Verificação do escopo e auditoria de completude

**Obrigatória em todo curso, mesmo nos que parecem completos.**

**2.1 Escopo prometido** (lista única): descrição e ementa (índice, PDF, página oficial; pesquise na web se preciso); tópicos dos resumos (`📌 Resumo do curso`, `📌 Resumo` das aulas, callouts `Nesta aula`, títulos de seções); temas citados como "veremos depois" ou usados em exercícios; o currículo padrão do assunto no nível do curso.

**2.2 Cruzar escopo × conteúdo** numa tabela só sua (`Tópico | Onde está | completo / raso / falta`). Procure: tópico sem explicação de verdade; explicação rasa (sem definição, exemplo, código ou exercício); conceito usado sem explicação (`+=`, passagem por referência, `\t`); pré-requisito ausente; resumo que promete o que a aula não entrega (ou o contrário).

**2.3 Completar como se fosse o curso**, no mesmo tom e padrão:

- Trecho raso → amplie a aula (nova seção `##`, exemplo, código, exercício com resolução).
- Tópico inteiro faltando → **página nova** no padrão da Fase 5, na posição didática do índice (mover páginas: `NOTION.md`).
- **Toda página criada por você termina o título com ` (Adicionado pelo aluno para melhorar o estudo)`**: no Notion, no link do índice, no `#` do Markdown e no sumário do EPUB (o nome do arquivo `aulas/NN-<slug>.md` não leva o sufixo). Ao revisar um curso já trabalhado, aplique também às páginas acrescentadas antes. Fora o sufixo, a página **não leva outra marca** (sem callout "página nova", sem ✨).
- **Seção ampliada dentro de aula existente** começa com `<callout icon="💡" color="blue_bg"><b>Complemento de Estudo (Sugestão de Expansão):</b> ...</callout>` (Markdown: `> 💡 **Complemento de Estudo (Sugestão de Expansão):** ...`), dizendo em uma frase o que foi acrescentado e por quê. Se o conceito for importante para a revisão, ganha card ou tópico no cheat sheet.
- Atualize as ligações ("próximo passo" da aula anterior, `Resumo do curso`).
- Fatos e código novos passam pela verificação da Fase 3.
- Guarde a lista do que foi acrescentado para o resumo final.
- Temas **fora** da proposta: só como sugestão no resumo.

## Fase 3. Revisão de precisão e clareza

Para cada aula:

- **Fatos:** definições, regras, sintaxe, resultados; o que muda com o tempo (versões, comandos), pesquise.
- **Código:** leia linha a linha; rode quando possível ou faça teste de mesa. Sintaxe da linguagem do curso (Portugol: `faca { } enquanto (cond)`, `inclua biblioteca X --> apelido`, `senao se`, `escolha/caso/pare/caso contrario`).
- **Matemática:** refaça as contas (Python); enunciado × resolução (unidades, limites de laço, fórmulas).
- **Correções** com callout logo abaixo: `⚠️` yellow_bg (o que o original fazia e por que está errado) ou `🛠️` green_bg (erro mostrado de propósito).
- **E-reader já no Notion:** linhas de código ≤ ~60, comentário longo na linha de cima (nunca alinhado com espaços), tabelas ≤ 4 colunas.
- **Português:** ortografia, acentos, concordância; títulos sem negrito; ordinais `ª/º` (não `°`).
- **Dados pessoais** viram placeholders ("Ana Souza", `usuario@exemplo.com`), exceto `Criado por: Josué B. Almeida`.
- Sem letras de música ou trechos longos de obras protegidas.

### 3.1 Padrão dos textos explicativos

Escreva como um **mentor paciente e encorajador** para quem vê o assunto pela primeira vez. Cada aula ensina sozinha, sem o vídeo.

**Cada tema (`##`), nesta ordem:**

1. **Por quê:** que problema resolve (1–2 frases).
2. **O que é:** definição em uma frase, em **negrito**.
3. **Analogia do mundo real** para todo conceito abstrato: callout `💡` blue_bg começando com `<b>Analogia:</b>`, **logo abaixo da imagem** quando houver diagrama. Analogia solta no texto é movida para esse callout (apague a repetição). Mapeie cada peça do conceito numa peça da analogia (Git = pontos de salvamento; variável = caixa com etiqueta; API = garçom; índice de banco = índice remissivo; Promise = pager da praça de alimentação; injeção de dependência = cafeteira da copa). **Não repita a mesma analogia em duas aulas.**
4. **Exemplo concreto com valores reais** antes da regra (`nota = 7.5 → "Aprovado"`).
5. **Código ou fórmula** curto, funcional, testado, com a saída esperada.
6. **Diagrama** quando a ideia tiver forma (fluxo, estrutura, tempo, memória).
7. **Armadilha comum** e como evitar (`⚠️` se for correção das anotações).

**Regra de ouro dos comentários no código:**

- Bloco Markdown com a linguagem (` ```java `, ` ```sql `...).
- Comentários **bloco a bloco** (linha a linha só em códigos de 3–6 linhas para iniciantes).
- O comentário explica **o porquê** (contexto lógico ou de negócio), não repete o código. Ruim: `// soma 1 em i`. Bom: `// avança para o próximo aluno da lista`.
- Sempre na linha de cima; linhas ≤ ~60 caracteres.
- Exemplos completos o bastante para rodar (Hello World inteiro, `git commit -m` real, `SELECT` com `WHERE`).
- Saída esperada num comentário final (`// saída: 3.5`) ou num bloco abaixo.

**Regras de escrita:** frases curtas, voz ativa, uma ideia por parágrafo (≤ ~4 linhas); defina cada termo técnico na primeira vez, com o termo em inglês entre parênteses quando for o de mercado; "você" e verbos concretos; abra com `## De onde paramos` e feche com o callout `➡️ Próximo passo` (gray_bg); compare com o que o leitor já sabe e use tabelas `A × B` para conceitos confundidos; nada de enchimento. Exercícios: enunciado diz o que entra e o que sai; resolução em toggle terminando com um teste (entrada → saída); havendo dois jeitos, mostre o mais simples e cite o outro. `## 🧠 Revisão rápida`: 3–5 toggles de pergunta e resposta curta sobre as ideias centrais e a armadilha. `## 📌 Resumo` com tabela `Item | Em uma frase`. No fim de cada seção/módulo do índice, o **cheat sheet** `🧭` (Fase 4).

**Teste final:** a aula responde por que isso existe, como funciona com um exemplo real e qual o erro mais comum? Se faltar algo, complete.

## Fase 4. Imagens → SVG

**Leia `ferramentas/skill/DIDATICA_VISUAL.md` antes de desenhar.** Resumo das decisões:

- Diagrama, fluxograma, esquema, tabela, gráfico simples, print de código → **SVG próprio** (print de código/tabela vira texto, mais SVG se ajudar).
- Captura real de interface → mantenha, salvo se um esquema explicar melhor. Imagem decorativa → remova.
- Crie SVGs novos onde um conceito fica mais claro desenhado. O mesmo SVG vai para o Notion e para `img/`.
- Sempre com o kit `ferramentas/svg/` e o tema v3 (creme, cards pastel, setas pontilhadas); cheat sheet 3×4 por seção com `cheatsheets.py`. Renderize e confira antes de subir.
- Auditoria visual obrigatória antes de encerrar: use o JSON do `auditar_curso.py` (ou conte no Notion) e registre aulas que continuam sem imagem e por quê.

## Fase 5. Reestruturação no Notion

**Cada aula:** ícone emoji coerente (sem repetir no título); logo após o breadcrumb, `<callout icon="🗺️" color="gray_bg"><b>Nesta aula:</b> ...</callout>` (listas: `Nesta lista:`); `##` por tema no padrão 3.1 (💡 blue_bg dicas, ⚠️ yellow_bg correções); código longo em toggles `Código`/`Resolução`, projetos com enunciado antes; final com `## 🧠 Revisão rápida`, `➡️ Próximo passo` e `## 📌 Resumo` (`Item | Em uma frase` ou `Exercício | O que pratica`; renomeie a tabela-resumo existente em vez de duplicar). **Preserve** pdf, file, bookmark, toggles de referência, breadcrumb e child pages. Detalhes da API (troca de imagem, mover páginas, erros): `NOTION.md`.

**Índice:** título no formato da preferência 1, mantendo ícone, capa e cabeçalho; `🗺️ Sobre o curso`, `🔖 Legenda das páginas` (🗺️ 📌 ⚠️ 💡 📝), linha `<span color="gray">` sob cada seção, cheat sheet `🧭` por seção e `## 📌 Resumo do curso` (Seção | Ideia central | Comandos/fórmulas-chave). Títulos das aulas limpos, em ordem didática. Depois de publicado, callout `📚` com o link do curso no GitHub e o do EPUB.

## Fases 6 e 7. Publicação, sincronização e resumo

Só depois da exportação nova (preferência 9). Siga `ferramentas/skill/PUBLICACAO.md` (exportação → `notion2md.py` → revisão → `auditar_curso.py` → capa (`CAPA.md`) → `gerar_epub_local.py` → commit e Action → sincronização Notion × GitHub → resumo final ao usuário).
