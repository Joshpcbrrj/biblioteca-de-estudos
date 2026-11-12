# Imagens e diagramas (Fase 4)

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia antes de criar, trocar ou auditar qualquer imagem.

Para cada imagem do curso:

1. Veja a imagem. Se o servidor de arquivos do Notion estiver bloqueado na sessão, use a exportação do Notion descrita na Fase 6 (ela traz todas as imagens).
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
- Guarde cópia local de todos os SVGs criados: eles vão para o repositório na Fase 6.

