# Design: diagramas mais coloridos e explícitos (diagram.py)

Aprovado pelo usuário em 2026-11-20 (abordagem A). Parte da fase de acabamento antes da v1.0.

## 1. Intenção

Os SVGs do Syllabook **somam ao texto**: o capítulo explica, e a imagem mostra a mesma ideia de um jeito que se entende batendo o olho (o que vem antes do quê, o que se compara com o quê, quais são as partes de um todo). Hoje o `diagram.py` gera diagramas corretos, porém pálidos e econômicos: uma linha por caixa, tons pastel quase brancos, emojis que dependem da fonte do leitor e cards sem ícones por item.

Referências de qualidade, pela ordem:

1. Infográfico "O manual do Claude" que o usuário mostrou: card com cor de fundo própria, **ícone em cada item**, uma **pequena cena** que demonstra a ideia (pasta → arquivos, janela errada → janela certa, "Papel + Tarefa + Contexto + Formato = Melhor saída"), título grande com subtítulo. Usamos o estilo, não copiamos o conteúdo nem os desenhos.
2. Livros antigos do usuário no Notion (WSL do zero, cap. 1; cheat sheets do curso Dio Java): caixa com título em negrito e linha de nota, selo de ícone no card, ✔ em círculo, sublinhado em degradê, sombra suave, setas grossas.

## 2. Metas

- Paleta mais forte: fundos com cor de verdade, borda e texto escuros da mesma família.
- Cabeçalho: título grande, subtítulo opcional, sublinhado em degradê.
- Toda caixa aceita `text` (negrito) + `note` (linha menor), em todos os tipos onde houver caixa.
- **Biblioteca de ícones embutida** (~80 ícones Lucide, licença ISC), pedidos pelo nome no YAML: `icon: folder`. Funciona sem internet, no claude.ai, no EPUB e no Notion.
- Ícone por item em `cards`, por passo em `flow`, por camada em `layers`, por linha em `compare`, por participante em `sequence`, por nó em `tree`, por evento em `timeline`.
- Emojis dentro do SVG substituídos por ícones desenhados (✅/❌ do `compare` viram `check-circle`/`x-circle`).
- Campo `scene` nos `cards` (e como tipo próprio, ver §5.4): uma sequência curta de ícones ligados por setas que demonstra a ideia do card.
- Perfil `small` (Kindle em cinza) continua legível: o ícone e o rótulo carregam o sentido, nunca só a cor.

## 3. Não metas

- Não é um editor livre de SVG: quem escreve o livro não posiciona nada à mão (abordagem C descartada).
- Não gera ilustrações (PNG) nem usa API de imagem; isso continua com `illustrate.py`, adiado.
- **Regra confirmada pelo usuário (2026-11-20):** SVG é só para diagramas. Imagens "normais", que explicam outros temas (cenas, objetos, processos ilustrados), são um trabalho à parte, desenvolvido depois. A `scene` deste design é um diagrama de ícones e setas, não uma ilustração.
- Não muda o formato dos tipos existentes de forma incompatível: specs antigos continuam desenhando (campos novos são opcionais).

## 4. Anti-metas (falha mesmo funcionando)

- Diagrama bonito que não explica: ícone ou cena decorativa, sem relação com o conceito (VISUALS proíbe cenas decorativas).
- Texto que não cabe e ninguém avisa: a checagem de estouro do `diagram.py` precisa cobrir os elementos novos (ícone ao lado do texto reduz a largura útil).
- Ilegível no `small` ou em cinza.
- Depender de fonte, emoji ou rede para desenhar.
- Spec ficar longo: um card com cena não deve passar de ~10 linhas de YAML.

## 5. Como (decidido)

### 5.1 Abordagens consideradas

| | Abordagem | Troca | Decisão |
|---|---|---|---|
| A | Tema novo + ícones embutidos + `scene` montada por ícones | Mais trabalho (ícones, testes, regras); SVG um pouco maior | **Escolhida**: ganho do infográfico, mantendo YAML curto, desenho pelo script e checagem de estouro |
| B | Só tema novo, sem ícones | Barato; fica no nível dos livros antigos | Perde a âncora visual por item e a cena |
| C | Tipo livre com grade de ícones e formas | Flexível | Volta a ser SVG à mão; difícil de testar; gasta tokens (seção 20 do plano) |

### 5.2 Tema

- `PALETTE` ganha uma quarta cor por família (`fill`, `border`, `strong`, `tint`): `tint` é o fundo mais saturado do card/selo; `fill` continua para caixas internas. Os valores ficam como chamada do construtor, com duas restrições: contraste do `strong` sobre `fill` ≥ 4,5:1, e as 7 famílias distinguíveis em cinza pelo menos pela borda + ícone.
- Cabeçalho: `title` (maior, peso 800), `subtitle` opcional (novo campo de todo spec), sublinhado com `linearGradient` azul → lilás → salmão → amarelo.
- Sombra suave já existe; manter. Cantos 14–16 px.
- Fonte: continua `system-ui` (nada de fonte embutida).

### 5.3 Ícones

- Arquivo `skills/syllabook/assets/icons.json`: `{nome: "<conteúdo interno do svg Lucide>"}` (paths, circles, lines; viewBox 24, stroke-based). Desenhado com `<g transform=... stroke=strong fill=none stroke-width=2>`.
- Licença: Lucide é ISC; incluir o aviso em `skills/syllabook/assets/ICONS-LICENSE.txt` e citar no README/créditos.
- Lista inicial (~80) cobrindo programação, matemática, idiomas, música e estudo em geral: arquivos e pastas, código, terminal, banco, servidor, nuvem, rede, cadeado, chave, engrenagem, usuário/pessoas, balão de fala, livro, lupa, lâmpada, alvo, gráfico, calculadora, sigma, função, relógio, calendário, check/x em círculo, alerta, play, música/nota, microfone, globo/idioma, lápis, lista, camadas, setas, repetir, filtro, caixa/pacote, contêiner, chip, janela, celular, link, nuvem de upload/download etc. A lista final é do construtor, com o critério "ícone que aparece em pelo menos dois perfis de área".
- Nome desconhecido → problema reportado (como o texto que não cabe), com até 3 sugestões de nomes parecidos (difflib).
- `diagram.py --icons` lista os nomes disponíveis (para a skill consultar uma vez, sem gastar tokens lendo o JSON).

### 5.4 Campos novos por tipo (todos opcionais)

- Todo spec: `subtitle`.
- `flow`: passo ganha `note` e `icon`; a decisão desenha o texto numa linha (fonte menor se precisar) com `note` abaixo; `side` ganha `side_note`, `side_icon`, `side_color` (padrão continua vermelho só quando o spec não disser).
- `layers`: `icon` por camada; `text` e `note` em duas linhas (hoje juntas com "·").
- `compare`: `left.icon`/`right.icon`; com `style: wrong-right` os emojis viram ícones desenhados.
- `boxes`: `name` e índices mais visíveis (selo para o índice); `highlight` com borda forte.
- `tree`, `timeline`, `sequence`: `icon` por nó/evento/participante.
- `bars`: sem ícone; só tema.
- `cards`: o `icon` de hoje (texto ASCII) passa a aceitar nome de ícone; se não for nome conhecido e tiver até 4 caracteres, continua como selo de texto (compatível). Itens com ✔ em círculo da cor do card; `items` aceita `{text, icon}` para trocar o ✔ por ícone. Novo `scene`.
- **`scene`** (dentro de card, e também como tipo `scene` de imagem inteira para o texto do capítulo):
  ```yaml
  scene:
    - [folder]                 # um passo = um ou mais ícones empilhados
    - [file-text, database]    # setas ligam cada passo ao seguinte
    label: Memória compartilhada   # legenda curta embaixo (opcional)
  ```
  Formas aceitas: lista de passos (cada passo uma lista de 1–3 ícones), `op` opcional entre passos (`+`, `=`, `→` padrão, `↔`), e `label`. No card, a cena ocupa uma coluna à direita (large) ou uma faixa abaixo dos itens (small). Limite: 4 passos, 3 ícones por passo.
  Isso cobre: pasta → arquivos, A + B + C = D, janela errada → janela certa, ícones em ciclo simples (o último passo com `→` de volta ao primeiro fica para depois, se os pilotos pedirem).

### 5.5 Checagens

- Estouro: largura útil desconta o ícone (e a coluna da cena) antes de `wrap`.
- Ícone desconhecido e cena acima dos limites → `problems` (saída 1).
- Contraste mínimo verificado em teste sobre a paleta.
- `MAX_ELEMENTS` continua valendo (ícones dentro de uma caixa não contam).

### 5.6 Documentação e exemplos

- `--help` do `diagram.py` e `references/VISUALS.md` (seção 4, regras e cheat sheets) atualizados: ícone por item, quando usar `scene`, "a cena demonstra, não enfeita".
- Livro de exemplo (`tests/fixtures/sample-book`) e vitrine (`syllabook-demo`): trocar o `c01-lista.svg` provisório por um spec real em `img/_source/` (tipo `boxes` com índices) e incluir uma cheat sheet com cena. A vitrine é atualizada depois do commit do kit.
- Conferir no Notion (copia o SVG) e no EPUB (o pandoc embute o SVG; ícones são paths, então não dependem de fonte).

## 6. Restrições

- Python puro + PyYAML (o que a skill já usa); sem dependência nova em tempo de execução. Baixar os ícones do Lucide é tarefa única de desenvolvimento, não da skill.
- Cobertura de testes ≥ 95% (pyproject); um teste por regra nova em `tests/test_diagram.py`; Ruff.
- Revisar olhando o PNG (resvg-py) cada tipo nos dois perfis: foi isso que pegou defeitos na 3c.
- Commits com o e-mail noreply; textos da skill em inglês, docs EN + pt-BR com o hash de tradução.

## 7. Fica com o construtor

- Valores exatos das cores, tamanhos e espaçamentos (dentro das restrições de contraste e de leitura).
- Lista final de ícones e seus nomes (preferir os nomes do Lucide).
- Layout fino da cena dentro do card nos dois perfis.

## 8. Melhoria pequena junto

- YAML com erro (por exemplo, `?` sem aspas) hoje mostra traceback; passar a mostrar `fail("spec.yaml line N: <mensagem>")` em `common.load_yaml`.
