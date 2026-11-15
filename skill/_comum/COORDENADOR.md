# Modo coordenador: um agente por página

> Arquivo comum às skills da biblioteca. Leia antes da etapa "Por página".

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
Você vai <reformular | escrever> UMA página de um <curso | livro> no Notion. Trabalhe só nela.

Página: <id> - "<título>"  (aula <n> de <total>, seção "<seção>")
Aula anterior: "<título anterior>"  ·  Próxima aula: "<título seguinte>"
Curso: <área>/<slug>, repositório clonado em <caminho do clone>
Analogias já usadas no curso (não repita nenhuma): <lista>
Ajustes do escopo para esta página: <o que acrescentar, ou "nenhum">

Antes de começar, leia:
- <caminho do clone>/skill/_comum/PADRAO_AULA.md (padrão, imagens,
  armadilhas);
- <caminho do clone>/skill/<skill em uso>/SKILL.md (regras da skill);
- .../skill/_comum/EXEMPLOS.md (imite a aula de exemplo);
- .../skill/_comum/NOTION.md;
- .../skill/_comum/DIDATICA_VISUAL.md, só se for criar ou trocar uma imagem.

Faça, nesta ordem:
1. notion-fetch da página.
2. Corrija fatos (ou, num livro novo, pesquise e cite as fontes do
   briefing), rode o código ou faça teste de mesa, refaça as contas.
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
