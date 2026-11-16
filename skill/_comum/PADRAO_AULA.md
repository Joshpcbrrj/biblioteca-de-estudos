# Padrão de aula e de imagens

> Arquivo comum às skills da biblioteca (`revisar-curso-biblioteca` e `criar-livro-tecnologia`). Leia antes de escrever a primeira página e imite o `_comum/EXEMPLOS.md`. Onde se lê "aula", vale também "capítulo"; onde se lê "curso", vale também "livro".

## Cada aula (no Notion)

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
- **Correções** (ao reformular material existente): callout `⚠️` yellow_bg logo abaixo, dizendo o que o original fazia e por que está errado; `🛠️` green_bg quando o erro era mostrado de propósito.
- **Dados pessoais** viram placeholders (`Ana Souza`, `usuario@exemplo.com`). Não reproduza letras de música, hinos nem trechos longos de obras protegidas.
- **Preserve** (ao reformular) pdf, file, bookmark, vídeo, breadcrumb e child pages exatamente como vieram.

**Índice do curso ou livro:** título no formato fixo; `🗺️ Sobre o curso`; `🔖 Legenda das páginas`; uma linha `<span color="gray">` sob cada seção; aulas em ordem didática (mova uma página fora de lugar); `## 📌 Resumo do curso` (`Seção | Ideia central | Comandos-chave`); depois de publicado, o callout `📚`.

**Teste de cada aula:** ela responde por que isso existe, como funciona com um exemplo real e qual é o erro mais comum? Se faltar algo, complete.

**Critério de pronto (automático):** depois da conversão, `auditar_curso.py <area>/<slug> --criterios` precisa sair sem erros. Os avisos (imagem sem analogia logo abaixo, tabela larga, saída real de terminal ou linha com URL acima de 60 caracteres, que não se quebram sem falsificar o comando) são aceitáveis só se estiverem registrados no `ESTADO.md` com o motivo.

## Imagens (detalhes em _comum/DIDATICA_VISUAL.md)

- Diagrama, fluxograma, tabela ou print de código → SVG próprio, feito com o kit `ferramentas/svg/` no tema v3: fundo creme `#FAF9F6`, cards pastel com sombra suave, setas curvas pontilhadas, `system-ui`, código em mono sobre `#F0F0F0`. Captura de tela real → mantenha. Imagem decorativa → remova.
- Antes de desenhar, escreva em uma frase o que o leitor deve entender: essa frase vira o título. Um foco por imagem, no máximo ~7 elementos, valores reais, e funciona em tons de cinza.
- Aula: 480 px de largura, retrato. Cheat sheet: 1200×1600, 3×4 cards, só ícones ASCII.
- Renderize e confira antes de subir. Para a mesma imagem, o mesmo arquivo em `img/` e no Notion.

## Armadilhas conhecidas (detalhes em _comum/NOTION.md)

- O `update_content` não encontra tags `<image>`. Para trocar uma imagem, refaça a página inteira com `replace_content`.
- Cada `file-upload://` serve uma vez e expira em ~1 h. Suba no máximo ~4 por vez e use logo.
- Evite escapes como `\u0000` no texto enviado.
- No índice, a ordem das aulas é a ordem das tags `<page>`.
- Commits: `git -c user.name="<commit_nome>" -c user.email="<commit_email>" commit`, com os valores do `biblioteca.yaml` e a atribuição pedida pela sessão. Nunca use o e-mail pessoal de ninguém.
- A Action é acompanhada pela API REST (`gh api repos/...`); o GraphQL não funciona na sessão.
