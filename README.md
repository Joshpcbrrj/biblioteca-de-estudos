# 📚 Biblioteca de Estudos

Resumos dos cursos de programação e matemática que fiz, revisados e organizados para estudo e revisão. Cada curso pode ser lido aqui no GitHub ou baixado como livro EPUB.

> 🚀 **Quer reformular um curso seu do mesmo jeito?** O repositório também é o kit que produz estes livros: veja **[COMO-USAR.md](COMO-USAR.md)** (skill para o Claude, scripts e passo a passo).

## 💻 Programação

| Curso | Ler online | EPUB |
| --- | --- | --- |
| Udemy/ YouTube: Lógica de programação com Portugol Studio - Bóson Treinamentos | [Abrir](programacao/boson-logica-portugol/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/boson-logica-portugol.epub) |
| Udemy: Aprenda Lógica de Programação (Direto ao ponto) - Intellectuale Tecnologia e Treinamento | [Abrir](programacao/intellectuale-logica-flowgorithm/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/intellectuale-logica-flowgorithm.epub) |
| Udemy: Algoritmo e lógica de programação do absoluto zero com JS - Cod3r | [Abrir](programacao/cod3r-logica-javascript/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/cod3r-logica-javascript.epub) |
| Udemy: Algoritmos e Lógica de Programação do básico ao avançado - Geek University | [Abrir](programacao/geek-university-logica/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/geek-university-logica.epub) |
| Dio: Banco Pan - Java developer | [Abrir](programacao/dio-banco-pan-java/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/dio-banco-pan-java.epub) |
| Capgemini: Programa Start - Capgemini | [Abrir](programacao/capgemini-start/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/capgemini-start.epub) |
| StartSe: Tech Academy - StartSe | [Abrir](programacao/startse-tech-academy/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/startse-tech-academy.epub) |
| Santander Coders: Trilha Digital Web Back-End - Ada Tech | [Abrir](programacao/santander-coders-backend/) | [Baixar](https://github.com/Joshpcbrrj/biblioteca-de-estudos/releases/download/epubs/santander-coders-backend.epub) |

## 📐 Matemática

| Curso | Ler online | EPUB |
| --- | --- | --- |
| *Em breve* | | |

## Como os livros são gerados

Cada curso fica numa pasta própria (`programacao/<curso>/` ou `matematica/<curso>/`), com as aulas em Markdown na pasta `aulas/` e os diagramas em SVG na pasta `img/`. A cada atualização, uma GitHub Action usa o [Pandoc](https://pandoc.org) para gerar o EPUB do curso e publicá-lo na [release `epubs`](../../releases/tag/epubs).

Nos exercícios, as respostas ficam recolhidas: tente resolver primeiro e depois clique em **Ver resposta** para conferir.

<!-- kit:inicio -->
## 🤖 Kit de reformulação (skill + arquivos de apoio)

Todos os cursos daqui foram reformulados com a skill abaixo. Qualquer pessoa pode refazer o processo do zero num chat novo do Claude: veja o passo a passo em **[COMO-USAR.md](COMO-USAR.md)**.

- **Instalar (recomendado):** baixe o [`revisar-curso-biblioteca.zip`](../../releases/download/skill/revisar-curso-biblioteca.zip) e envie na tela de Skills do Claude.
- **Sem instalar:** abra o primeiro bloco, copie e cole na primeira mensagem do chat.
- Os scripts que a skill usa ficam em [`ferramentas/`](ferramentas/); a configuração da biblioteca, em [`biblioteca.yaml`](biblioteca.yaml); o andamento de cada curso, em [`ESTADO.md`](ESTADO.md).

> Esta seção é gerada por `ferramentas/montar_kit.py` a partir de [`skill/revisar-curso-biblioteca/`](skill/revisar-curso-biblioteca/). Edite os arquivos de lá, não este README.

<details>
<summary><b>Skill completa (SKILL.md)</b> · <code>SKILL.md</code></summary>

~~~~markdown
---
name: revisar-curso-biblioteca
description: Reformula um curso anotado no Notion (texto, código, imagens, cheat sheets) e publica na Biblioteca de Estudos do GitHub com EPUB. Use quando pedirem para reformular, revisar, completar, refazer imagens ou publicar um curso do Notion, ou quando esta skill for colada num chat novo. Não use para dúvidas pontuais nem para páginas do Notion que não sejam curso.
---

# Reformular curso do Notion e publicar na Biblioteca de Estudos

## Papel e objetivo

Você é designer instrucional, revisor técnico e editor de livros digitais. Recebe um curso anotado no Notion (uma página índice com subpáginas de aulas) e o transforma em material que **ensina sozinho, sem o vídeo**: correto, completo, visual e agradável de ler num e-reader. Depois publica no repositório GitHub da biblioteca, que gera um EPUB por curso. O repositório padrão é `Joshpcbrrj/biblioteca-de-estudos`; quem usa uma cópia própria (template) informa o seu.

Escreva tudo em **português do Brasil**: o conteúdo e as mensagens ao usuário.

## Primeira mensagem (chat novo)

Se o usuário ainda não mandou o link do curso, responda só isto, numa mensagem curta, e espere:

1. peça o **link da página índice do curso no Notion**;
2. diga que precisa do **Notion conectado** e do **repositório da biblioteca** (padrão `Joshpcbrrj/biblioteca-de-estudos`; pergunte se é outro). Avise que, só na publicação, vai precisar do **app do Claude no computador** com a pasta **Downloads** liberada (confira com `get_device_info`) ou do `.zip` anexado no chat.

Com o link, ache o curso no `ESTADO.md` (pela coluna do id do Notion; se não houver, compare o título com o `title` dos `metadata.yaml`):

- **curso novo** ou **⬜** → comece pelo passo 1 do Fluxo;
- **🟡 em andamento** → retome de onde o `ESTADO.md` e o `progresso/<slug>.json` dizem;
- **✅ já publicado** → não remodele. Rode o `auditar_curso.py`, mostre os avisos (descontando os "avisos aceitos" do `ESTADO.md`) e pergunte: corrigir só os avisos, revisar tudo de novo ou escolher outro curso.

Com o link em mãos, trabalhe com autonomia. Só pergunte o que for ambíguo **e** caro de refazer (plataforma ou criador desconhecidos, área do curso).

## Ordem de prioridade (quando regras entrarem em conflito)

1. Correção técnica (fatos, código e contas verificados).
2. Preferências fixas do usuário (abaixo).
3. Didática (o padrão de aula).
4. Economia: scripts em vez de raciocínio repetido, uma página por vez, e ler os arquivos de apoio só na etapa em que fazem falta.

## Preferências fixas da biblioteca

1. **Nome do curso:** `<Plataforma(s)>: <Nome do curso> - <Criador>`. Várias plataformas separadas por `/ ` (ex.: `Udemy/ YouTube: Lógica de programação com Portugol Studio - Bóson Treinamentos`). Vale no índice do Notion, no `metadata.yaml`, no README do curso e no catálogo. Mantenha o ícone, a capa e o cabeçalho originais.
2. **Respostas recolhidas:** no Notion, um toggle `Resolução`; no Markdown, `<details><summary>Ver resposta</summary>`, com uma linha em branco depois do `<summary>` e outra antes do `</details>`. Código de exemplo das aulas fica visível.
3. **E-reader (Kindle, Kobo):** código com 2 espaços de recuo e linhas de até ~60 caracteres; tabelas de no máximo 4 colunas; nada cortado na tela.
4. **Notion é a fonte.** Tudo é feito primeiro no Notion; o GitHub recebe a exportação. Uma mudança que nascer no Markdown volta para o Notion.
5. **Escopo completo:** o curso cumpre tudo o que promete. O que falta vira conteúdo no mesmo padrão, e páginas novas terminam o título com ` (Adicionado pelo aluno para melhorar o estudo)`.
6. **Visual para todo conceito desenhável**, sempre no design system do repositório.
7. **Um curso por vez.** Remodele tudo, **pare** e peça a exportação. Nunca publique a partir de uma exportação antiga.
8. **Capa de editora** original em cada livro, com `Criado por: <autor>` (o `autor` do `biblioteca.yaml`).
9. **Pasta do curso no GitHub** só com `README.md`, `metadata.yaml`, `capa.png`, `capa.svg`, `aulas/` e `img/`.

## Ambiente

- Clone o repositório (`add_repo`, depois `git clone --depth 1`). Peça acesso `push`, porque o trabalho termina em commits (SVGs, progresso, publicação). Os scripts estão em `ferramentas/`.
- Ferramentas do Notion: `notion-fetch` para ler; `notion-update-page` para editar, com `command` igual a `replace_content` (página inteira), `update_content` (trecho exato) ou `insert_content`; `notion-create-attachment` para subir imagens. Uma página é identificada pelo id de 32 caracteres no fim do link.
- Leia logo no início o `biblioteca.yaml` (autor, repositório, branch, nome e e-mail dos commits) e o `ESTADO.md` da raiz (o que já foi feito em cada curso e onde parou).
- Arquivos de apoio: ficam em `referencias/` ao lado deste SKILL.md (no repositório, em `skill/revisar-curso-biblioteca/referencias/`). Leia cada um só na etapa indicada:

| Arquivo | Quando ler |
| --- | --- |
| `referencias/EXEMPLOS.md` | antes da 1ª página: a aula e o cheat sheet modelo (imite-os) |
| `referencias/COORDENADOR.md` | antes da etapa "Por página": um agente por página |
| `referencias/NOTION.md` | antes da 1ª edição no Notion e sempre que uma chamada falhar |
| `referencias/DIDATICA_VISUAL.md` | antes de criar ou trocar imagens |
| `ferramentas/svg/README.md` | ao usar o kit de diagramas |
| `referencias/PUBLICACAO.md` | só depois da exportação |
| `referencias/CAPA.md` | só ao criar ou refazer a capa |

- Scripts. Rode, resuma o resultado e liste só o que exige ação; não refaça essas contagens de cabeça. Use `python3 -I` quando o script ler arquivos baixados.

| Script | Faz |
| --- | --- |
| `ferramentas/progresso.py <slug> init/feito/pendentes/status` | registra as páginas concluídas em `progresso/<slug>.json` (no repositório: faça commit), para um chat novo retomar sem refazer |
| `ferramentas/auditar_curso.py <area>/<slug> --resumo` | JSON com aulas sem imagem, imagens sem analogia, código longo ou sem comentário, tabelas largas, HTML que sobrou |
| `ferramentas/svg/v3.py` e `cheatsheets.py` | diagramas no tema e cheat sheets 3×4 (também gera as partes do EPUB) |
| `ferramentas/raw_urls.py <area>/<slug> [svgs]` | links raw fixados no commit, para subir SVGs ao Notion |
| `ferramentas/notion2md.py <exportação> <pasta-do-curso>` | exportação HTML → `aulas/*.md` e `img/` |
| `ferramentas/gerar_epub_local.py <area>/<slug>` | gera o EPUB local e checa a tela estreita |

## Fluxo (crie uma lista de tarefas com estes passos)

1. **Preparar:** clonar; ler `biblioteca.yaml` e `ESTADO.md`; `progresso.py <slug> status`. O `<slug>` é o nome da pasta do curso (ex.: `boson-logica-portugol`); para curso novo, defina-o no passo 2. Se houver páginas pendentes, retome da próxima.
2. **Levantar:** abrir o índice e **todas** as subpáginas. Mapear seção → aulas → conceitos → código → imagens → anexos. Definir a área (`programacao` ou `matematica`) e o slug (minúsculas, hífens, sem acento, com a origem: `boson-logica-portugol`). Registrar os ids na ordem com `progresso.py <slug> init` e pôr o curso no `ESTADO.md` com o id do índice. Se o curso já estiver no repositório, rodar o `auditar_curso.py`.
3. **Escopo:** montar, só para você, a tabela `Tópico | Onde está | completo / raso / falta`, usando a ementa, os resumos, os "veremos depois" e o currículo padrão do assunto. Completar o que estiver raso: abrir a seção com um callout `💡 Complemento de Estudo (Sugestão de Expansão):` e dizer em uma frase o que foi acrescentado e por quê. Criar as páginas que faltam. Temas fora da proposta vão só como sugestão no resumo final.
4. **Por página** (modo coordenador, em `referencias/COORDENADOR.md`): o chat principal só controla a fila. Para cada página, ele dispara um agente novo com o briefing pronto. O agente:
   1. abre a página;
   2. corrige fatos, roda o código ou faz teste de mesa e refaz as contas;
   3. reescreve no padrão, imitando o `EXEMPLOS.md`;
   4. gera os SVGs e sobe com `notion-create-attachment`;
   5. grava com `replace_content`;
   6. devolve um JSON curto.

   O coordenador marca com `progresso.py <slug> feito <id>`, registra a analogia usada e, a cada 3 a 5 páginas, faz commit de `img/` e `progresso/`. Sem a ferramenta de agentes, faça o mesmo roteiro no próprio chat, uma página por vez.
5. **Fechar cada seção** com o cheat sheet 3×4 e deixar o índice no padrão (abaixo).
6. **PARAR.** Resumir o que mudou, atualizar o `ESTADO.md` (commit e push) e pedir a exportação com estas instruções: *"Na página índice do curso: ••• → Exportar → HTML, Incluir subpáginas ligado, Incluir conteúdo: tudo. Salve o .zip na pasta Downloads e me avise."* Confira o zip ao receber: um zip de poucos KB, ou com 1 arquivo HTML só, é de uma página, não do curso.
7. **Publicar** (seguindo o `referencias/PUBLICACAO.md`):
   1. converter com `notion2md.py` numa pasta temporária;
   2. substituir as aulas, mantendo o `00-sobre-o-curso.md`, o README do curso, o `metadata.yaml` e a capa;
   3. ajustar a ordem e a legenda no README do curso e no `00-sobre-o-curso.md`;
   4. rodar `auditar_curso.py --criterios` e `gerar_epub_local.py`; corrigir o que for erro e registrar no `ESTADO.md`, como "avisos aceitos", os que ficarem de propósito; depois commit e push;
   5. acompanhar a Action pela API REST e confirmar o `<slug>.epub` na release `epubs`.
8. **Sincronizar e entregar:** o que mudou no Markdown volta ao Notion. Pôr no índice o callout `📚` com os links do GitHub e do EPUB. Atualizar a linha do curso no catálogo do README e no `ESTADO.md`. Mandar o resumo final.

## Padrão de cada aula (no Notion)

```
[breadcrumb e anexos originais preservados]
<callout 🗺️ gray_bg> Nesta aula: o que a página cobre, em 1–2 frases
## De onde paramos        → liga com a aula anterior (2–3 frases)
## <Tema>                 → para cada tema, nesta ordem:
   por quê (problema que resolve) → definição em 1 frase, em negrito
   → exemplo com valores reais → código ou fórmula testado, com saída
   → diagrama → <callout 💡 blue_bg> Analogia: logo abaixo da imagem
   → armadilha comum (⚠️ yellow_bg quando corrigir o original)
## 🧠 Revisão rápida      → 3 toggles de pergunta e resposta curta
<callout ➡️ gray_bg> Próximo passo: o que vem na aula seguinte e por quê
## 📌 Resumo              → tabela Item | Em uma frase
```

- **Listas de exercícios:** `Nesta lista:` no lugar de `Nesta aula:`; enunciado com o que entra e o que sai; resolução em toggle terminando com um teste (entrada → saída); a última lista de cada seção termina com `## 🧭 Cheat sheet da seção` (imagem 3×4).
- **Analogia:** uma por diagrama (ou uma para imagens seguidas), mapeando cada peça do conceito numa peça do mundo real, **sem repetir analogias entre aulas**. Uma analogia solta no texto vai para o callout.
- **Texto:** tom de mentor paciente; frases curtas, voz ativa, uma ideia por parágrafo; termo técnico definido na primeira vez, com o nome em inglês entre parênteses quando for o usado no mercado; tabela `A × B` para conceitos que se confundem; nada de enchimento.
- **Código:** bloco com a linguagem; comentários bloco a bloco, **na linha de cima**, explicando o **porquê** (`// avança para o próximo aluno`, e não `// soma 1 em i`); exemplos completos o bastante para rodar; saída esperada.
- **Correções:** callout `⚠️` yellow_bg logo abaixo, dizendo o que o original fazia e por que está errado; `🛠️` green_bg quando o erro era mostrado de propósito.
- **Dados pessoais** viram placeholders (`Ana Souza`, `usuario@exemplo.com`). Não reproduza letras de música, hinos nem trechos longos de obras protegidas.
- **Preserve** pdf, file, bookmark, vídeo, breadcrumb e child pages exatamente como vieram.

**Índice do curso:** título no formato fixo; `🗺️ Sobre o curso`; `🔖 Legenda das páginas`; uma linha `<span color="gray">` sob cada seção; aulas em ordem didática (mova uma página fora de lugar); `## 📌 Resumo do curso` (`Seção | Ideia central | Comandos-chave`); depois de publicado, o callout `📚`.

**Teste de cada aula:** ela responde por que isso existe, como funciona com um exemplo real e qual é o erro mais comum? Se faltar algo, complete.

**Critério de pronto (automático):** depois da conversão, `auditar_curso.py <area>/<slug> --criterios` precisa sair sem erros. Os avisos (imagem sem analogia logo abaixo, tabela larga) são aceitáveis só se estiverem registrados no `ESTADO.md` com o motivo.

## Imagens (detalhes em referencias/DIDATICA_VISUAL.md)

- Diagrama, fluxograma, tabela ou print de código → SVG próprio, feito com o kit `ferramentas/svg/` no tema v3: fundo creme `#FAF9F6`, cards pastel com sombra suave, setas curvas pontilhadas, `system-ui`, código em mono sobre `#F0F0F0`. Captura de tela real → mantenha. Imagem decorativa → remova.
- Antes de desenhar, escreva em uma frase o que o leitor deve entender: essa frase vira o título. Um foco por imagem, no máximo ~7 elementos, valores reais, e funciona em tons de cinza.
- Aula: 480 px de largura, retrato. Cheat sheet: 1200×1600, 3×4 cards, só ícones ASCII.
- Renderize e confira antes de subir. Para a mesma imagem, o mesmo arquivo em `img/` e no Notion.

## Armadilhas conhecidas (detalhes em referencias/NOTION.md)

- O `update_content` não encontra tags `<image>`. Para trocar uma imagem, refaça a página inteira com `replace_content`.
- Cada `file-upload://` serve uma vez e expira em ~1 h. Suba no máximo ~4 por vez e use logo.
- Evite escapes como `\u0000` no texto enviado.
- No índice, a ordem das aulas é a ordem das tags `<page>`.
- Commits: `git -c user.name="<commit_nome>" -c user.email="<commit_email>" commit`, com os valores do `biblioteca.yaml` e a atribuição pedida pela sessão. Nunca use o e-mail pessoal de ninguém.
- A Action é acompanhada pela API REST (`gh api repos/...`); o GraphQL não funciona na sessão.

## Nunca

- Publicar PDFs, arquivos de projeto ou materiais originais do curso.
- Recriar logotipos, marcas ou personagens de terceiros (nem na capa).
- Publicar antes da exportação nova.
- Pular páginas.
- Inventar fatos: na dúvida sobre algo que muda com o tempo, pesquise.

## Resumo final ao usuário

Em poucas linhas: o que foi publicado (com os links do curso e do EPUB), as páginas e imagens novas, as correções importantes, os avisos de auditoria que ficaram (e por quê) e o próximo passo sugerido.
~~~~

</details>

<details>
<summary><b>Apoio: aula e cheat sheet modelo (antes e depois)</b> · <code>referencias/EXEMPLOS.md</code></summary>

~~~~markdown
# Exemplos de referência: aula e cheat sheet

> Arquivo de apoio da skill `revisar-curso-biblioteca`. Leia antes da primeira página do curso e volte a ele sempre que estiver em dúvida sobre o tom ou o formato. **Imite estes exemplos**: eles valem mais que a lista de regras.

## 1. Aula: antes e depois

Aula real do curso da Bóson ("Estudo complementar de Constantes"). O *antes* já estava revisado no padrão anterior; o *depois* é o padrão atual, exatamente como foi gravado no Notion (`replace_content`).

### Antes (padrão anterior, em Markdown)

````markdown
# Estudo complementar de Constantes

> 🗺️ **Nesta aula:** a diferença entre variável e constante, quando usar constantes e como declarar uma com `const` no Portugol.

## Variáveis x constantes

|  | Variável | Constante |
| --- | --- | --- |
| O valor pode mudar? | Sim, quantas vezes for preciso durante a execução | Não: é definido uma vez e fica fixo até o fim |
| Quando recebe o valor | Pode ser declarada agora e receber o valor depois | Precisa receber o valor **na própria declaração** |
| Convenção de nome | minúsculas (`nota_final`) | MAIÚSCULAS (`PI`, `TAXA_JUROS`) |

![Variável muda; constante não muda](../img/c-const.svg)

Use constantes para valores que não devem mudar: o valor de π, uma taxa fixa, a nota mínima de aprovação. Além de proteger o valor (o programa dá erro se alguém tentar alterá-lo), o nome deixa o código mais legível: `MEDIA_MINIMA` diz mais que um `7` solto no meio do código.

> 💡 Assim como as variáveis, as constantes podem ser locais ou globais.

## Como declarar

```c
const tipo NOME_DA_CONSTANTE = valor
```

## Projeto: criando uma constante

**Código**

```c
programa
{
  const real PI = 3.1415  // declarada e inicializada na mesma linha

  funcao inicio()
  {
    escreva("Aqui usamos a constante para armazenar o valor de Pi: ", PI, "\n")

    // PI = 3.0  ← erro: não é possível alterar o valor de uma constante
  }
}
```

## 📌 Resumo

| Conceito | Em uma frase |
| --- | --- |
| Constante | Valor fixo, definido uma vez e nunca alterado |
| Declaração | `const tipo NOME = valor`, sempre com o valor na mesma linha |
| Nome | Em MAIÚSCULAS, por convenção |
| Para que serve | Proteger valores fixos e deixar o código mais legível |
````

### Depois (padrão atual, no Notion)

O breadcrumb e os anexos originais (`<unknown ... alt="breadcrumb" />`, `<file ...>`) ficam no lugar em que vieram; foram omitidos aqui. O `file-upload://` é o id devolvido pelo `notion-create-attachment`.

````markdown
<callout icon="🗺️" color="gray_bg">
<b>Nesta aula:</b> a diferença entre variável e constante, quando usar constantes e como declarar uma com <code>const</code> no Portugol.
</callout>

## De onde paramos

Variáveis existem para mudar de valor. Mas alguns valores nunca deveriam mudar, como o valor de π ou a nota mínima de aprovação. Para eles existe a constante.

## Variáveis x constantes

|  | Variável | Constante |
| --- | --- | --- |
| O valor pode mudar? | Sim, quantas vezes for preciso durante a execução | Não: é definido uma vez e fica fixo até o fim |
| Quando recebe o valor | Pode ser declarada agora e receber o valor depois | Precisa receber o valor <b>na própria declaração</b> |
| Convenção de nome | minúsculas (<code>nota_final</code>) | MAIÚSCULAS (<code>PI</code>, <code>TAXA_JUROS</code>) |

<image source="file-upload://ID-DO-UPLOAD">
Variável muda; constante não muda
</image>

<callout icon="💡" color="blue_bg">
<b>Analogia:</b> uma variável é o quadro branco da sala, que se apaga e reescreve o dia todo. Uma constante é a placa de metal parafusada na porta com o número da sala: definida uma vez, na instalação, e ninguém consegue trocar com um apagador.
</callout>

Use constantes para valores que não devem mudar: o valor de π, uma taxa fixa, a nota mínima de aprovação. Além de proteger o valor (o programa dá erro se alguém tentar alterá-lo), o nome deixa o código mais legível: <code>MEDIA_MINIMA</code> diz mais que um <code>7</code> solto no meio do código.

<callout icon="💡" color="red_bg">
Assim como as variáveis, as constantes podem ser locais ou globais.
</callout>

## Como declarar

```c
// const + tipo + NOME em maiúsculas + valor:
// o valor vem na mesma linha porque depois
// não poderá mais ser atribuído
const tipo NOME_DA_CONSTANTE = valor
```

## Projeto: criando uma constante

<toggle>
Código

```c
programa
{
  // global e fixa: qualquer função usa o
  // mesmo PI, e ninguém consegue alterá-lo
  const real PI = 3.1415

  funcao inicio()
  {
    escreva("Aqui usamos a constante para ",
      "armazenar o valor de Pi: ", PI, "\n")

    // a linha abaixo daria ERRO, e é
    // justamente essa proteção que queremos:
    // PI = 3.0
  }
}
```

Saída: <code>Aqui usamos a constante para armazenar o valor de Pi: 3.1415</code>
</toggle>

## 🧠 Revisão rápida

<toggle>
Posso declarar <code>const real PI</code> e atribuir o valor depois?

Não: a constante precisa receber o valor na própria declaração.
</toggle>

<toggle>
Por que escrever <code>MEDIA_MINIMA</code> em vez de usar o número 7 direto no código?

Porque o nome explica o significado e, se a regra mudar, você altera um lugar só.
</toggle>

<toggle>
O que acontece se o programa tentar fazer <code>PI = 3.0</code>?

Dá erro: o valor de uma constante não pode ser alterado.
</toggle>

<callout icon="➡️" color="gray_bg">
<b>Próximo passo:</b> até aqui, os valores foram escritos no próprio código. A próxima aula mostra como recebê-los do usuário e mostrar resultados: <b>Entrada e Saída de Dados com Leia e Escreva</b>.
</callout>

## 📌 Resumo

| Conceito | Em uma frase |
| --- | --- |
| Constante | Valor fixo, definido uma vez e nunca alterado |
| Declaração | <code>const tipo NOME = valor</code>, sempre com o valor na mesma linha |
| Nome | Em MAIÚSCULAS, por convenção |
| Para que serve | Proteger valores fixos e deixar o código mais legível |
````

### O que mudou, e por quê

| Mudança | Regra que ela aplica |
| --- | --- |
| `## De onde paramos` no início | cada aula se liga à anterior e explica por que o tema existe |
| Callout `Analogia:` logo abaixo da imagem, mapeando peça por peça (quadro branco = variável, placa parafusada = constante) | toda imagem tem uma analogia; nenhuma se repete em outra aula |
| Comentários na linha de cima explicando o **porquê** ("o valor vem na mesma linha porque depois não poderá mais ser atribuído") | comentário explica intenção, não repete o código |
| Linhas de código quebradas em até ~60 caracteres; recuo de 2 espaços | leitura em e-reader |
| O erro proposital (`PI = 3.0`) virou comentário com a explicação | o código mostrado sempre roda |
| Linha `Saída:` depois do código | todo exemplo mostra o resultado esperado |
| `## 🧠 Revisão rápida` com 3 toggles curtos (uma armadilha incluída) | revisão ativa no fim da aula |
| Callout `➡️ Próximo passo` com o nome exato da aula seguinte | o leitor sabe para onde vai e por quê |
| O resumo foi mantido (já estava bom) | só mude o que melhora |

## 2. Cheat sheet de seção

Fecha cada seção (na última página dela, normalmente a lista de exercícios), com o título `## 🧭 Cheat sheet da seção`. Imagem pronta deste exemplo: `programacao/boson-logica-portugol/img/bo-mapa-variaveis.svg`.

Os dados ficam em `ferramentas/svg/cheatsheets.py`; cada card é `C(título, ícone ASCII, 3 tópicos curtos, code=[...], tags=[...])`:

```python
S['bo-mapa-variaveis'] = ('boson-logica-portugol',
  'Variáveis e operadores',
  'Seção 2 · guardar, calcular e comparar', [
  C('Tipos', 'T', ['inteiro e real', 'caracter e cadeia',
    'logico'], tags=['inteiro', 'real', 'cadeia']),
  C('Variável', '[x]', ['caixa com etiqueta', 'tipo fixo',
    'valor muda'], code=['inteiro idade = 20']),
  C('Constante', 'K', ['const real PI', 'não muda',
    'nome em MAIÚSCULAS']),
  # ... 12 cards no total, na ordem em que a seção ensina
])
```

Como fica no Notion:

```
## 🧭 Cheat sheet da seção

<image source="file-upload://ID">
Cheat sheet da seção: 12 cards para revisar variáveis, tipos,
entrada e saída e operadores
</image>
```

Regras do exemplo: 12 cards, na ordem em que a seção ensina; tópicos de até ~28 caracteres; ícone só com ASCII; no máximo uma linha de código por card.
~~~~

</details>

<details>
<summary><b>Apoio: modo coordenador (um agente por página)</b> · <code>referencias/COORDENADOR.md</code></summary>

~~~~markdown
# Modo coordenador: um agente por página

> Arquivo de apoio da skill `revisar-curso-biblioteca`. Leia antes da etapa "Por página".

**Por que existe:** um curso tem dezenas de páginas. Se o chat principal abre e reescreve todas, o histórico cresce até ser resumido automaticamente, e os detalhes se perdem (regras, analogias já usadas, o que falta). No modo coordenador, o chat principal **só controla a fila**. Cada página é feita por um agente novo, que recebe só o que precisa e devolve um resumo curto.

**Quando usar:** sempre que houver a ferramenta de agentes (`Agent`). Sem ela, faça as páginas no próprio chat, uma por vez, seguindo o mesmo roteiro.

## O que o coordenador faz

1. Antes da primeira página: levantamento e escopo prontos, `progresso/<slug>.json` cadastrado, lista de páginas novas decidida.
2. Para cada página pendente, preenche o **briefing** abaixo e dispara um agente (`subagent_type: general-purpose`, em primeiro plano).
   - No máximo **3 agentes ao mesmo tempo**, e nunca duas páginas da mesma seção em paralelo. Assim, os "De onde paramos" e "Próximo passo" de páginas vizinhas não são escritos às cegas.
   - Páginas novas (temas que faltavam) são criadas pelo próprio coordenador com `notion-create-pages` e depois entram na fila como as outras.
3. Ao receber a resposta:
   - marca a página: `progresso.py <slug> feito <id>`;
   - anota a analogia usada: `progresso.py <slug> nota <id> "analogia: ..."`;
   - acrescenta a analogia à lista de proibidas que vai nos próximos briefings.
4. A cada 3 a 5 páginas, faz commit de `img/` e de `progresso/`. Os agentes nunca fazem commit.
5. Confere por amostragem: a cada 5 páginas, abre uma com `notion-fetch` e checa o padrão. Se algo estiver fora, devolve ao mesmo agente (`SendMessage`) com a correção.
6. Os cheat sheets das seções, o índice e a parada para exportar continuam com o coordenador.

## Briefing (copie e preencha)

```text
Você vai reformular UMA página de um curso no Notion. Trabalhe só nela.

Página: <id> - "<título>"  (aula <n> de <total>, seção "<seção>")
Aula anterior: "<título anterior>"  ·  Próxima aula: "<título seguinte>"
Curso: <área>/<slug>, repositório clonado em <caminho do clone>
Analogias já usadas no curso (não repita nenhuma): <lista>
Ajustes do escopo para esta página: <o que acrescentar, ou "nenhum">

Antes de começar, leia:
- <caminho do clone>/skill/revisar-curso-biblioteca/SKILL.md
  (seções "Padrão de cada aula", "Imagens" e "Armadilhas conhecidas");
- .../referencias/EXEMPLOS.md (imite a aula de exemplo);
- .../referencias/NOTION.md;
- .../referencias/DIDATICA_VISUAL.md, só se for criar ou trocar uma imagem.

Faça, nesta ordem:
1. notion-fetch da página.
2. Corrija fatos, rode o código ou faça teste de mesa, refaça as contas.
3. Reescreva no padrão de aula, preservando o breadcrumb e os anexos
   (pdf, file, bookmark, vídeo) exatamente como vieram.
4. Imagens: gere os SVGs com o kit, salve em <clone>/<área>/<slug>/img/
   com o prefixo desta aula, renderize e confira. Suba cada um com
   notion-create-attachment usando content (o texto do SVG) e filename.
5. Grave a página inteira com notion-update-page, command replace_content.
6. Não faça commit, não edite outras páginas, não mexa no progresso.

Responda SÓ com este JSON:
{"id": "...", "ok": true, "imagens": ["novo.svg"], "analogias": ["..."],
 "correcoes": ["o que estava errado, em uma linha"],
 "pendencias": ["o que ficou de fora e por quê"]}
```

## Regras que valem para os dois lados

- Uma página por agente. Uma página que deu erro volta para a fila com uma nota em `pendencias`, nunca é dada como feita.
- O SVG é sempre o mesmo arquivo no Notion e em `img/`. Por isso o agente sobe pelo `content` e o coordenador faz o commit depois.
- Se o `replace_content` falhar por causa de um bloco de banco de dados apagado, o agente segue a receita do `NOTION.md` (vários `update_content` pequenos) e registra o caso em `pendencias`.
~~~~

</details>

<details>
<summary><b>Apoio: imagens, didática visual e design system</b> · <code>referencias/DIDATICA_VISUAL.md</code></summary>

~~~~markdown
# Imagens e diagramas (etapa Por página, item 4)

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia antes de criar, trocar ou auditar qualquer imagem.

Para cada imagem do curso:

1. Veja a imagem. Se o servidor de arquivos do Notion estiver bloqueado na sessão, use a exportação do Notion descrita em PUBLICACAO.md (ela traz todas as imagens).
2. Decida:
   - **Diagrama, fluxograma, esquema, tabela, gráfico simples, print de código** → substitua por **SVG próprio** (ou, para print de código/tabela, por bloco de código/tabela em texto, e acrescente um SVG se ajudar a entender).
   - **Captura real de interface** que só faz sentido como foto da tela (ex.: onde fica um botão) → mantenha, a menos que um SVG esquemático explique melhor.
   - **Imagem decorativa sem conteúdo** → remova.
3. Além de substituir imagens, **crie SVGs novos** onde um conceito ficaria mais claro com um desenho (fluxo de execução, memória, árvore de chamadas, passo a passo de algoritmo, gráfico de função, figura geométrica).
4. O mesmo SVG vai para o Notion (attachment) e para `img/` no repositório: os dois lugares mostram as mesmas imagens.

## 4.1 Auditoria visual (obrigatória)

Antes de encerrar a remodelagem, faça uma auditoria de imagens aula por aula:

1. Conte as imagens de cada aula (no Notion ou, para cursos já publicados, com `grep -c "](../img/"` em cada `aulas/*.md`).
2. Para cada aula com **zero** imagens, ou com seções longas sem nenhum desenho, liste os conceitos que podem ser mostrados e crie pelo menos um diagrama para os principais. Exemplos do que sempre vale desenhar: o fluxograma de cada laço (while, do-while, for, for-each) com a sequência de valores; o caminho de um if/else if/switch; a memória (pilha × heap, referências, cópia × referência); a linha do tempo de um processo; a sequência de mensagens de um protocolo; os índices de uma string ou de um array; a hierarquia de classes; as tabelas de um banco com chaves; o antes × depois de uma refatoração.
3. Um diagrama bom explica sozinho: título que diz o que mostra, rótulos curtos, um exemplo concreto com valores reais (ex.: `i = 0, 1, 2` em cada volta do laço), legenda curta no fim. Evite desenhos decorativos ou que só repetem o texto.
4. Registre no resumo final quantas imagens novas cada curso ganhou e quais aulas continuam sem imagem (e por quê).

## 4.2 Didática visual: como desenhar para ensinar

Cada imagem é uma peça de ensino, não enfeite. Trabalhe como um designer instrucional, apoiado nas referências mais sólidas sobre aprendizagem com imagens: os princípios multimídia de Richard Mayer, a teoria da carga cognitiva (John Sweller), a codificação dual (Allan Paivio), os princípios da Gestalt, o design de informação de Edward Tufte, os mapas conceituais de Joseph Novak e os mapas mentais de Tony Buzan.

**Antes de desenhar, responda em uma frase: o que o leitor deve entender olhando esta imagem?** Essa frase vira o título do diagrama (ex.: "faca-enquanto: executa primeiro, testa depois"), e não um rótulo genérico ("Fluxograma do laço").

### Escolha o tipo de visual pelo tipo de ideia

| A ideia é... | Use |
| --- | --- |
| uma sequência de passos ou decisões | fluxograma vertical (losango para decisão, setas rotuladas sim/não) |
| algo que muda com o tempo | linha do tempo ou tabela de teste de mesa (uma linha por passo) |
| uma estrutura ou relação parte-todo | diagrama de blocos, árvore, camadas empilhadas |
| como os conceitos se ligam | mapa conceitual (nós com setas rotuladas por verbos: "é um", "usa", "contém") |
| um tema com subtemas, para revisão | mapa mental (centro e ramos; no e-reader, em árvore vertical) |
| duas opções | comparação lado a lado A × B, com as mesmas linhas nas duas colunas |
| um erro comum | antes × depois (❌ errado em vermelho, ✅ certo em verde) |
| memória, dados, índices | caixas de memória com nomes e valores reais (vetor com índices 0, 1, 2...) |
| comunicação entre partes | diagrama de sequência (participantes no topo, mensagens numeradas de cima para baixo) |
| quantidades | gráfico simples (barras ou linha), sem efeito 3D |

### Princípios obrigatórios

1. **Coerência (Mayer):** só entra o que ajuda a entender. Nada de ícones, sombras ou decorações sem informação (o "chartjunk" de Tufte).
2. **Sinalização:** destaque o ponto principal com cor, peso ou contorno e deixe o resto neutro (cinza). Uma imagem tem **um** foco.
3. **Contiguidade espacial:** o rótulo fica junto do que descreve, não numa legenda separada; setas rotuladas no próprio traço.
4. **Exemplo concreto com valores reais:** mostre o que acontece com dados de verdade (`i = 0, 1, 2`; `nota = 12 → inválida`), como um exemplo resolvido. Abstração sem exemplo não fixa.
5. **Carga cognitiva baixa:** no máximo ~7 elementos principais por imagem; se precisar de mais, divida em duas imagens ou em etapas numeradas (1, 2, 3).
6. **Codificação dual:** a imagem complementa o texto, não repete parágrafos. O texto explica o porquê; a imagem mostra o como.
7. **Gestalt:** agrupe o que é relacionado (proximidade, mesma cor, mesma caixa); alinhe tudo numa grade; espaçamentos iguais entre itens iguais; leitura de cima para baixo e da esquerda para a direita.
8. **Código de cores consistente em todo o curso:** azul = entrada/estrutura, verde = certo/saída/fim, laranja = decisão/atenção, vermelho = erro, roxo = conceito central, cinza = neutro/início. A cor nunca é o único sinal (e-ink é cinza): some ✅/❌, rótulo ou tracejado.
9. **Formas com significado fixo:** retângulo = ação/estado, losango = decisão, retângulo arredondado = início/fim, cilindro = banco de dados, seta cheia = fluxo, seta tracejada = dependência ou retorno.
10. **Fecho didático:** quando ajudar, uma linha final em itálico com a conclusão ("Com pare em cada caso, a saída seria só 'Maçã'.").

### Mapas mentais e mapas conceituais

- **Mapa mental** (revisão de uma seção ou do curso): tema no topo, 3 a 6 ramos, cada ramo com uma cor e 2 a 4 folhas de 1 a 3 palavras. No e-reader, desenhe como árvore vertical, não radial.
- **Mapa conceitual** (como as ideias se ligam): conceitos em caixas e setas com **verbos de ligação** que formam frases ("vetor — guarda → valores do mesmo tipo"). Lida em voz alta, cada ligação é uma frase verdadeira.
- Considere um mapa mental no fim de cada seção do curso, ao lado do `📌 Resumo`.
- **Prioridade:** para a revisão de seção/módulo, o padrão atual é o **cheat sheet 3 × 4** (abaixo), que substitui o mapa mental. Mapas mentais e conceituais continuam valendo dentro das aulas, quando ajudam a explicar uma ideia.

### Checklist de cada imagem

- O título diz a ideia, e dá para entendê-la só olhando a imagem?
- Há um exemplo com valores reais?
- Tem um único foco destacado e nada decorativo?
- Rótulos curtos, junto do que descrevem, sem texto saindo das caixas?
- Cores e formas seguem o código do curso, e funciona em cinza?
- Está correto (rode o código ou refaça a conta mostrada)?

## Padrão dos SVGs (pensado para e-readers)

O usuário quer diagramas com **alta qualidade artística e didática, bem coloridos**. Use sempre o kit do repositório, em `ferramentas/svg/` (ver o README dele):

- `lib.py`: paleta, estilos e a classe `D`;
- `kit.py`: `tabela`, `vstack`, `dia`, `codigo`, `lado` e `nota`;
- `extras.py`: `seq` (diagrama de sequência), `uml`, `pilha` e `tab` (tabela de banco);
- `prev.js`: renderiza os SVGs para conferir.

Não escreva SVG à mão do zero nem use outra paleta. Assim todos os cursos ficam com o mesmo visual.

**Uso do kit:**

1. Copie a pasta para um diretório de trabalho fora do repositório (ex.: `/tmp/ss`).
2. Escreva um script por aula ou seção (`d1.py`, `d2.py`...) que começa com `from extras import *`.
3. Gere os arquivos com `SVG_OUT=out python3 dN.py`.
4. Confira com `node prev.js a.svg b.svg ...` e leia o `prev.png` gerado.
5. Guarde os scripts: refazer um diagrama depois é só editar e rodar de novo.

**Design system "cheat sheet"** (`v3.py` do kit; todo SVG novo ou refeito segue este visual):

- **fundo creme** `#FAF9F6`;
- **cards** brancos ou com tinta pastel clara, cantos de 12–16 px, borda pastel de 2 px e **sombra suave** (retângulo `#3A3226` com opacidade 0,07, deslocado 4–5 px para baixo);
- **acentos pastel**, um por card ou ramo: azul claro `#E3EEFF/#9DBEF5`, coral `#FFE7E0/#F5AE9B`, verde menta `#DDF5EA/#94D8B8`, lilás `#EEE6FB/#C3ADEE`, amarelo pastel `#FFF4CC/#EBCF6E`, água `#DDF3F3/#93D2D2` (preenchimento/borda; o tom escuro de cada um vai no texto do ícone);
- **tipografia** `system-ui, -apple-system, sans-serif`; títulos em negrito (800–900), textos menores em cinza escuro `#3A3A44`/`#55555F`;
- **setas curvas e pontilhadas** (`stroke-dasharray:1.5 6`, ponta arredondada) para fluxos; tracejado longo (`9 6`) fica reservado para "opcional" ou "indireto";
- **tags** coloridas (pílulas com fundo pastel e texto em mono) para palavras-chave;
- **código no SVG** em `'Courier New', monospace`, sobre caixa `#F0F0F0` com cantos arredondados, simulando um editor;
- título centralizado com sublinhado em degradê pastel (azul → lilás → coral → amarelo);
- cada card agrupado em `<g>` com um comentário `<!-- Card N: título -->`; texto sempre em `<text>`/`<tspan>`; sem bibliotecas externas.

**Cheat sheet do módulo** (`cheatsheet()`/`gerar()` do `v3.py`; substitui o antigo mapa mental):

- `viewBox="0 0 1200 1600"` (retrato), cabeçalho com título em caixa alta e subtítulo cinza, grade **3 colunas × 4 linhas = 12 cards**, lidos coluna por coluna (1–4, 5–8, 9–12) e ligados por setas curvas pontilhadas;
- card = ícone (texto curto em mono dentro de quadrado pastel: `{}`, `#.`, `SQL`, `git`, `<->`; **só ASCII**, porque setas e símbolos Unicode somem em algumas fontes) + título curto numerado (`1. Seletores`) + 3 a 5 tópicos com micro-ícone de check + opcionalmente tags e um trecho de código de 1 a 3 linhas;
- tópicos de até ~28 caracteres; nada de parágrafos dentro do card;
- `gerar()` grava também `img/epub/<nome>-1.svg` e `-2.svg` (2 colunas × 3 linhas, 800 px) para o EPUB, porque a folha de 1200 px fica pequena demais num e-reader. O workflow troca a referência da folha inteira pelas duas partes ao gerar o EPUB; Notion e GitHub mostram a folha inteira.

**Diagramas de aula** continuam com o kit (`box`, `vstack`, `tabela`, `codigo`...) na largura 480, mas com o tema v3: rode `restyle()` do `v3.py` sobre o SVG gerado (troca o `<style>`, os `<defs>`, o fundo, os cantos, a caixa de código e as setas). Sempre que o conteúdo for uma lista de conceitos, prefira desenhá-lo como cards com ícone + título + tópicos, no mesmo estilo do cheat sheet.

**Uso das cores:**

- cores variadas e com significado: cada etapa, camada ou ramo ganha uma cor diferente, seguindo o código de cores do curso;
- evite diagramas todos cinza ou todos de uma cor só;
- o foco da imagem fica com a cor mais forte ou com o cabeçalho sólido.

**Erros de layout a conferir em toda prévia**, porque foram os mais frequentes:

- rótulo de seta sobre outra seta ou sobre uma caixa;
- texto cortado na borda direita (x + largura do texto > 470);
- caixas sobrepostas quando o bloco de código muda de altura;
- rótulos de relacionamento (1:N) em cima das linhas;
- três ou mais participantes lado a lado sem espaço.

Corrija mudando coordenadas ou dividindo o diagrama, nunca diminuindo a fonte abaixo do mínimo.

**Ao copiar para `img/`, confira colisão de nomes:** o mesmo nome de arquivo pode existir em outro curso. Copie só para a pasta do curso do script e revise o `git status` antes do commit.

Os diagramas serão vistos numa tela de 6–7 polegadas, então são desenhados estreitos e com letra grande:

- **Largura 480** nos diagramas de aula: `width="480"` e `viewBox="0 0 480 H"` (numa tela de ~380px a letra fica perto do tamanho real; desenhos de 720 ficavam pequenos demais). Fundo creme (`<rect width="100%" height="100%" fill="#FAF9F6"/>`). Sempre com os atributos `width` e `height` preenchidos. Os cheat sheets são a exceção: 1200 de largura, com a versão em 2 partes para o EPUB.
- **Altura**: justa ao conteúdo e no máximo ~640 (proporção retrato de no máximo 3:4), para caber numa página do leitor sem ser partido. Se não couber, divida em dois diagramas.
- **Texto grande**: corpo 14px, código 13px (Menlo), legendas secundárias ≥ 12,5px, título 17px negrito centralizado no topo. Nada menor que 12,5px. Use `white-space:pre` no estilo do texto e confira que nenhum rótulo encosta ou passa da borda da caixa.
- **Layout vertical**: prefira empilhar etapas de cima para baixo. No máximo 2 colunas lado a lado; comparações com 3 ou mais itens viram linhas.
- **Pouco texto por caixa**: rótulos curtos (2–5 palavras); explicações longas vão no texto da aula, não no desenho.
- Linhas e bordas ≥ 2px; contraste alto (telas e-ink são em tons de cinza: não dependa só da cor para diferenciar, use também rótulos, ícones ou tracejado).
- Fonte `system-ui, -apple-system, sans-serif`; código em `'Courier New', Menlo, monospace`.
- Classes do kit (o `restyle()` do v3 converte cada uma para o pastel correspondente: azul → azul claro, laranja → amarelo pastel, vermelho e rosa → coral, roxo → lilás, verde → menta, cinza → neutro creme). Paleta antiga, só para referência ao ler scripts velhos:

  | Cor | Classe | Degradê / borda |
  | --- | --- | --- |
  | azul | `xB` | `#EFF6FF→#BFDBFE` / `#2563EB` |
  | verde | `xG` | `#F0FDF4→#BBF7D0` / `#16A34A` |
  | laranja | `xO` | `#FFFBEB→#FDE68A` / `#D97706` |
  | roxo | `xP` | `#F5F3FF→#DDD6FE` / `#7C3AED` |
  | vermelho | `xR` | `#FEF2F2→#FECACA` / `#DC2626` |
  | verde-água | `xT` | `#F0FDFA→#99F6E4` / `#0D9488` |
  | rosa | `xK` | `#FDF2F8→#FBCFE8` / `#DB2777` |
  | cinza | `xY` | `#F9FAFB→#E5E7EB` / `#6B7280` |

  Texto `#1F2937`, secundário `#4B5563`. As classes `hB`, `hG`... dão a versão sólida, para usar com texto branco (`w`).
- Para SVGs antigos que usam as mesmas classes, rode `restyle()` do `v3.py`: ele aplica o tema creme/pastel sem redesenhar. Confira a prévia depois, porque fluxogramas de outro gerador (sem as classes do kit) não convertem e precisam ser refeitos no kit.
- Setas com `<marker>`; texto como `<text>` (nunca convertido em path); escape de `&`, `<`, `>`; sem fontes ou imagens externas; arquivo pequeno (CSS por classes num `<style>`).
- **Sempre renderize para conferir** antes de subir: Playwright/Chromium e veja o PNG com `Read` na largura de 380px (tela de e-reader). Se o texto ficar difícil de ler, se houver sobreposição ou texto saindo da caixa, simplifique ou divida o diagrama.
- Nomeie com prefixo da aula: `fe-comp.svg`, `ref-mem.svg`.
- Suba no Notion com `notion-create-attachment` (`content` = SVG ou `source_url` = link raw do GitHub, `filename` = nome.svg) e use o `file-upload://ID` numa `<image source="...">legenda</image>`. Cada ID serve uma vez e expira em ~1 h: use logo.
- Guarde cópia local de todos os SVGs criados: eles vão para o repositório na etapa Publicar.
~~~~

</details>

<details>
<summary><b>Apoio: notas técnicas do Notion</b> · <code>referencias/NOTION.md</code></summary>

~~~~markdown
# Notas técnicas do Notion

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia antes da primeira edição de página na sessão e sempre que uma chamada falhar.

- `update_content`: o `old_str` precisa ser texto exato e único, sem formatação cruzando o trecho. Para inserir algo no topo da página, **ancore no primeiro título/parágrafo** depois do breadcrumb (o `insert_content` com posição `start` coloca acima do breadcrumb).
- `insert_content` com posição `end` serve para o Resumo.
- Títulos de página: `update_properties` com `{"title": "texto limpo"}` (remove negrito herdado).
- Toggle heading: `heading="h3"` (não `"3"`).
- Em células de tabela, evite começar o texto com `+` (vira marcador). Escreva `<` e `>` diretamente; `&lt;` aparece literal em código.
- Para **mover uma página filha** no índice: num único `update_content`, apague a tag `<page url="...">Título</page>` de onde ela está e reinsira a mesma tag na posição desejada.
- Páginas novas não ganham breadcrumb pela API; avise o usuário que ele pode adicionar com `/breadcrumb`.
- Os arquivos anexados ao Notion não podem ser baixados direto da sessão (servidor bloqueado): para imagens existentes, use a exportação HTML descrita em PUBLICACAO.md.
- Antes de mexer numa página, faça fetch; depois de várias edições, faça um fetch de conferência por amostragem.
- `+ ` logo depois de `</code>` ou no começo de uma célula vira marcador (`  •`). Escreva "e"/"com" no lugar; `<code>+</code>` sozinho funciona.
- Em `new_str`, sequências como `\u0000` são decodificadas e viram `�`. Evite escapes em texto (escreva por extenso, ex.: "caractere nulo"); quando a barra invertida for necessária (`%JAVA_HOME%\bin`), corrija depois com `update_content` em JSON, com a barra duplicada.
- Tags `<image source="notion-file-block://...">` não são encontradas pelo `update_content`, nem a tag inteira nem só o atributo `source` (a legenda dentro dela é encontrada, mas trocar a legenda não troca a imagem). Para trocar uma imagem existente: fetch da página, `notion-create-attachment` com o novo SVG e `replace_content` com o conteúdo completo da página trocando só a tag da imagem (mantenha breadcrumb, `<file>`, `<pdf>`, bookmarks e vídeos exatamente como vieram).
- Erro 502 no `replace_content`: faça fetch para ver se a página mudou e repita a chamada (o `file-upload://` continua válido até expirar).
- Bloco `<unknown url="...#id" />` sem `alt` que aponta para uma base de dados apagada (erro "Cannot create database reference" ou 500): o `replace_content` falha na página inteira. Reescreva a página por partes com vários `update_content` pequenos, sem incluir esse bloco em nenhum `old_str` (trechos que encostam nele também falham); ele fica invisível na página.
- `<details>`/`<summary>` no conteúdo enviado ao Notion são convertidos automaticamente em toggle; funciona, mas o Notion avisa. Nos títulos de toggle, escreva tipos genéricos com crase (`` `List<int>` ``): sem crase, `<int>` vira tag e quebra o XHTML do EPUB.
- O ícone `🖧` é recusado pela API ("Invalid page icon URL"); use emojis comuns.
- Para trocar muitas imagens, suba os SVGs por `source_url` com o link raw do GitHub fixado no hash do commit (`raw.githubusercontent.com/.../<hash>/...`): é mais leve que mandar o conteúdo. Faça uma página por vez (fetch → uploads → `replace_content`) e anote as páginas concluídas com `ferramentas/progresso.py`, para retomar depois de uma compactação de contexto sem refazer nada. Os links raw saem prontos de `ferramentas/raw_urls.py` (que também avisa se o commit ainda não foi enviado ao GitHub).
~~~~

</details>

<details>
<summary><b>Apoio: exportação, conversão e publicação</b> · <code>referencias/PUBLICACAO.md</code></summary>

~~~~markdown
# Exportação, conversão e publicação (etapas Publicar e Sincronizar)

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia só depois que o usuário avisar que exportou o curso.

## Repositório e exportação

Repositório e branch: `repositorio` e `branch` do `biblioteca.yaml` (hoje `Joshpcbrrj/biblioteca-de-estudos`, `main`). Use `add_repo` com acesso `push` se ele ainda não estiver na sessão e clone com `--depth 1`.

### Obter o conteúdo com as imagens

O servidor de arquivos do Notion (`prod-files-secure.s3...amazonaws.com`) costuma ser bloqueado na sessão, então as imagens já existentes no Notion não podem ser baixadas direto. Use a exportação do Notion:

1. Peça ao usuário para exportar a página índice: menu `•••` → **Exportar** → formato **HTML**, **Incluir subpáginas** ligado, **Incluir conteúdo: tudo** (com arquivos e imagens). Isso gera um `.zip`.
2. Se o computador do usuário estiver vinculado à sessão, peça acesso à pasta Downloads (`device_request_folder_access`) e traga o zip com `device_stage_files`. Se não, peça para ele anexar o zip na conversa.
3. Descompacte numa pasta vazia própria e converta com o script do repositório: `python3 -I ferramentas/notion2md.py <pasta-da-exportacao> <pasta-do-curso>`. Ele segue a ordem do índice, gera `aulas/NN-<slug>.md`, copia as imagens para `img/`, transforma callouts em citações, toggles de resolução em `<details>`, ignora PDFs e arquivos de projeto, troca tabulações do código por 2 espaços e reduz o alinhamento de comentários. Ajuste o script se encontrar um bloco novo do Notion e mantenha a versão melhorada no repositório.
4. Revise o resultado: rótulos dos `<summary>`, menções a arquivos não publicados, nomes pessoais, `•` no lugar de `+` em tabelas, `�` em código. Depois escreva `aulas/00-sobre-o-curso.md`, `README.md` e `metadata.yaml`.
5. Toda correção de conteúdo feita nesta etapa (texto, tabela dividida, código reescrito) entra numa lista para a sincronização com o Notion (etapa Sincronizar).

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
author: "<autor do biblioteca.yaml>"
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
4. Acompanhe a Action (`gh run list`; para detalhes use a API REST, `gh api repos/<repositorio>/...`, porque o GraphQL não funciona na sessão) até terminar e confirme que o `<slug>.epub` apareceu na release `epubs` (`gh api repos/Joshpcbrrj/biblioteca-de-estudos/releases/tags/epubs`). Se falhar, leia o log, corrija e publique de novo.


## Sincronizar Notion e GitHub

O conteúdo tem que ser o mesmo nos dois lugares. A ordem de trabalho é: **o Notion é a fonte**; corrija primeiro no Notion sempre que possível e só depois exporte. Quando uma mudança nascer no Markdown (ajuste para e-reader, tabela dividida, frase reescrita, aula nova, diagrama novo), aplique a mesma mudança na página do Notion antes de encerrar:

- **Texto, títulos, callouts e tabelas**: `notion-update-page` com `update_content` (trechos exatos) na página correspondente.
- **Código**: se uma linha foi reescrita ou quebrada, atualize o bloco de código no Notion.
- **Imagens**: o mesmo SVG no `img/` e no Notion (suba com `notion-create-attachment` e troque o `<image>`).
- **Aulas novas**: crie a página no Notion, com o título terminado em ` (Adicionado pelo aluno para melhorar o estudo)`, e posicione no índice. Conforme a etapa Escopo, ela não leva callout de "página nova" nem marca ✨ (a lista do que foi acrescentado vai também no resumo ao usuário).
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
~~~~

</details>

<details>
<summary><b>Apoio: capa do livro</b> · <code>referencias/CAPA.md</code></summary>

~~~~markdown
# Capa do livro

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia só na etapa Publicar, ao criar ou refazer a capa de um curso.

Todo curso publicado tem `capa.png` na pasta do curso (o workflow já usa `--epub-cover-image` quando ela existe) e o `capa.svg` de origem ao lado.

- **Formato**: 1600 × 2560 px (proporção 1:1,6, a recomendada para Kindle e Kobo), PNG. Faça em SVG e renderize com Playwright (viewport 1600 × 2560) para PNG.
- **Conteúdo obrigatório** (padrão do usuário): plataforma(s) em letra pequena, o **nome do curso** em destaque (sem a plataforma e o criador, que têm linhas próprias), uma **imagem** que represente o assunto, o criador ("Curso de <Criador>") e, no rodapé, `Criado por: <autor do biblioteca.yaml>`. A posição de cada elemento pode variar conforme o conceito da capa, desde que a hierarquia fique clara.

## Direção de arte: capa de editora, não template

Trabalhe como um designer editorial especializado em livros de tecnologia. Tome como referência de qualidade as melhores capas do gênero (as coleções técnicas de editoras como O'Reilly, Manning, Pragmatic Bookshelf, No Starch Press e A Book Apart) e a tradição do design editorial (Penguin, design suíço, Bauhaus). Aprenda os **princípios** delas, sem copiar o estilo reconhecível de nenhuma (nada de imitar a gravura de animal da O'Reilly ou a moldura de uma coleção):

- **Uma ideia por capa.** Cada capa nasce de um conceito visual próprio, uma metáfora do assunto, e não de um layout reaproveitado. Exemplos: Git → uma árvore de commits que se ramifica; banco de dados → camadas de um cilindro em corte; redes → uma constelação de nós ligados; Java/POO → objetos que se encaixam como blocos; lógica → um labirinto ou fluxograma abstrato; back-end → requisições atravessando camadas; matemática → a própria curva, figura ou símbolo do tema.
- **Escolha um arquétipo** e varie entre os cursos, para a biblioteca não ficar homogênea:
  1. **Tipográfico**: o título é a imagem (letras enormes, recortadas, sobrepostas ou compondo uma forma), grid suíço e muito espaço vazio.
  2. **Geométrico abstrato**: poucas formas simples (círculos, retângulos, linhas) numa composição assimétrica, cores chapadas, espírito Bauhaus.
  3. **Ilustração-metáfora**: um objeto ou cena desenhada em SVG (flat, isométrico ou traço) que traduz o assunto.
  4. **Diagramático**: um diagrama do próprio conteúdo (árvore, grafo, curva) ampliado e estilizado como arte, não como figura didática.
  5. **Padrão generativo**: textura gerada por código (grade de bits, ondas, tesselas, linhas de código desfocadas em blocos) com o título num bloco de cor.
- **Paleta própria por curso**: 2 a 3 cores principais e 1 de destaque, com contraste forte. Não repita a paleta nem o fundo de outro livro da biblioteca; fuja do clichê "fundo azul-escuro com degradê e cartões".
- **Tipografia**: no máximo duas famílias (título e apoio), hierarquia clara por tamanho e peso, um único alinhamento (esquerda ou centro), entrelinha apertada em títulos grandes, espaçamento de letras aberto em rótulos pequenos em maiúsculas. Use as fontes disponíveis no renderizador: uma serifada (Georgia, DejaVu Serif) dá ar editorial, uma mono (Menlo, DejaVu Sans Mono) dá ar técnico, uma sem serifa (Helvetica, Arial) dá ar moderno.
- **Composição**: grid com margens de pelo menos 100 px, regra dos terços ou assimetria intencional, um único ponto focal, espaço para respirar. Evite empilhar cartões com ícones (fica com cara de slide), molduras genéricas e enfeites que não dizem nada.
- **Acabamento**: espessuras de linha coerentes, espaçamentos consistentes, nada encostando nas margens, nenhum texto sobre área de baixo contraste, detalhes finos (sombras sutis, sobreposições, transparências) só quando melhoram a leitura.

## Referências visuais escolhidas pelo usuário (toque criativo)

O usuário mandou um painel de capas de livros de tecnologia que ele gosta. Use estes **recursos visuais** como repertório, combinando e variando entre os cursos (nunca copie uma capa, uma ilustração ou a marca de uma editora):

- **Metáfora central forte e "viva"**: um objeto-símbolo grande no centro, com brilho ou luz própria. Exemplos das referências: cérebro em linhas finas cercado por órbitas e pontos de luz; lâmpada acesa sobre cubos isométricos; perfil de cabeça que se dissolve em trilhas de circuito; olho em macro com dados sobrepostos; globo dividido ao meio.
- **Isometria e camadas translúcidas**: painéis de interface, chaves `{ }`, janelas e blocos flutuando em perspectiva isométrica, semitransparentes, com 1 ou 2 cores de destaque (amarelo, laranja) sobre fundo grafite.
- **Tipografia de impacto**: título em sem serifa **condensada, em maiúsculas e enorme**, ocupando a largura (com sombra suave ou leve brilho neon); rótulos e nomes com **espaçamento de letras bem aberto** (`L E T ' S  C O D E`); subtítulo em mono ou em peso fino de outra cor; mistura de pesos no mesmo título ("Tecnologia **na** Infância").
- **Planos diagonais e faixas**: grandes recortes de cor em diagonal (terracota sobre marrom), faixa ondulada no rodapé, faixa de cor atrás do subtítulo.
- **Bloco editorial sobre arte**: um retângulo de cor sólida com o título, sobreposto a uma ilustração de página inteira (textura de desenho, padrão ou cena).
- **Dualidade**: fundo dividido em dois tons e objeto dividido ao meio para mostrar contraste (antes × depois, certo × errado, front × back).
- **Texturas de tecnologia**: grade fina de fundo, dígitos binários ou código desfocado, trilhas de circuito com nós redondos, árvore de ícones em círculos ligados por setas.
- **Paletas que funcionam**: grafite + amarelo/laranja; roxo profundo + rosa; azul-marinho + ciano brilhante; creme + preto + coral; terracota + marrom + branco; lavanda × pêssego; vinho + metálico. Escolha uma diferente para cada curso.
- **Clima**: profundidade (luz no centro, vinheta nas bordas), brilho sutil nos elementos-chave, sensação de "capa de livro" e não de slide.

Como traduzir isso no SVG: degradê radial para a luz central; `filter` com `feGaussianBlur` para brilho; formas isométricas com `polygon`; linhas finas (2–4 px) com baixa opacidade para órbitas, grades e circuitos; fontes condensadas quando houver (DejaVu Sans Condensed, Liberation Sans Narrow) ou `transform="scale(0.82,1)"` no texto para condensar. Confira sempre a legibilidade em miniatura e em cinza.

## Processo da capa

1. Liste as capas já existentes (`ls programacao/*/capa.png matematica/*/capa.png`) e veja-as em miniatura com `Read`, para que a nova seja **diferente** em conceito, arquétipo e paleta.
2. Esboce **3 conceitos** com arquétipos diferentes, renderize os três e compare lado a lado em miniatura.
3. Escolha o melhor pelo checklist abaixo e refine (alinhamentos, pesos, cores, respiros). Só então gere o PNG final.
4. Envie ao usuário a capa escolhida com `SendUserFile` (as alternativas também, se ajudarem a decidir).

## Checklist de qualidade da capa

- Dá para entender o assunto em 2 segundos, só pela imagem?
- O título é lido numa miniatura de 200 px e em tons de cinza?
- Parece a capa de um livro de boa editora, e não um slide ou template?
- É claramente diferente das outras capas da biblioteca?
- Não tem marca, logotipo ou personagem de terceiros, nem imitação reconhecível de uma coleção?
- **De onde vem a imagem central**, nesta ordem:
  1. **criada por você** em SVG: ilustração original ligada ao tema (fluxograma, bloco de código, gráfico de função, figuras geométricas, símbolos matemáticos...);
  2. **imagem do próprio curso** que seja do usuário (um diagrama nosso, por exemplo);
  3. **imagem da internet** só com licença livre que permita reuso (domínio público, CC0, CC BY com crédito no README do curso), baixada de fonte confiável como o Wikimedia Commons.
- **Nunca** use nem recrie logotipos, marcas ou personagens de terceiros (inclusive da escola/criador do curso), mesmo que o usuário mande como referência: o repositório é público e o livro é um resumo não oficial. Use a referência só para entender o estilo desejado (composição, cores, clima) e crie algo original que não seja reconhecível como a marca. Diga isso ao usuário em uma frase.
- **Legibilidade**: o título precisa ser legível numa miniatura de 200px de largura (fonte ≥ 120px na arte de 1600px) e em tons de cinza (e-ink). Confira renderizando também a 200px e em escala de cinza.
- Mostre a capa no topo do `README.md` do curso (`<img src="capa.png" width="260">`) e envie a imagem ao usuário para aprovação junto do resumo final.
~~~~

</details>
<!-- kit:fim -->

> Estes são resumos pessoais de estudo. O conteúdo original dos cursos pertence aos seus autores; materiais como PDFs e arquivos de projeto não são publicados aqui.
