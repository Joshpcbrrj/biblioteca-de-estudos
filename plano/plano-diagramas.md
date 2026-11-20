# Diagramas coloridos e explícitos — plano de implementação

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** o `diagram.py` passa a desenhar diagramas com cores fortes, título + nota em cada caixa, ícones Lucide embutidos por item e `scene` (ícones ligados por setas), sem quebrar specs antigos.

**Architecture:** ícones ficam em `assets/icons.json` (gerado uma vez por `tools/build_icons.py` a partir do `lucide-static`) e são lidos por um módulo pequeno, `scripts/icons.py`. O `diagram.py` ganha o tema novo no `Canvas`, um `box_with_text` com `note`/`icon`, a função `scene` e os campos novos em cada tipo. Checagens de estouro descontam o espaço do ícone e da cena.

**Tech Stack:** Python 3.10+, PyYAML, pytest, Ruff, resvg-py (só para revisar PNG), npm (só para baixar o `lucide-static` uma vez).

**Spec:** `plano/design-diagramas.md`

## Global Constraints

- Só Python puro + PyYAML em tempo de execução; nada de rede nem fonte embutida para desenhar.
- SVG é só para diagramas; ilustrações ficam fora (design §3).
- Campos novos são opcionais: todo spec que desenha hoje continua desenhando sem `problems` novos.
- Contraste do `strong` sobre `fill` e sobre `tint` ≥ 4,5:1 (WCAG).
- Limites: `scene` com até 4 passos, até 3 ícones por passo; `cards` até 12; `MAX_ELEMENTS = 7` (ícones dentro de caixa não contam).
- Cobertura ≥ 95% com ramificações; Ruff (linha 120); um teste por regra nova.
- Textos da skill em inglês; mensagens de erro em inglês no estilo das atuais.
- Commits: `git -c user.name="Josue" -c user.email="<noreply do GitHub do usuário>" commit -F arquivo` (ver memória), mensagem em português, terminando com `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`.

## Review Focus

1. Spec antigo com `icon` ASCII de card que coincide com nome de ícone (ex.: `lock`, `code`): desenha o ícone, sem erro (teste na Task 5).
2. Ícone desconhecido em qualquer tipo: vira `problem` com sugestões, nunca `KeyError`/traceback (teste na Task 2 e na Task 4).
3. Perfil `small` com ícone + texto longo: a largura útil desconta o ícone e o estouro é reportado (teste na Task 3).
4. YAML com erro de sintaxe: mensagem `spec.yaml line N: ...` e saída 1 (teste na Task 1).
5. `scene` com passo vazio, mais de 3 ícones ou `op` inválido: `problem` claro (teste na Task 5).

---

### Task 1: erro de YAML legível

**Files:**
- Modify: `skills/syllabook/scripts/common.py` (`load_yaml`)
- Test: `tests/test_common.py`

**Interfaces:**
- Produces: `load_yaml(path)` chama `fail(f'{os.path.basename(path)} line {n}: {problem}')` em `yaml.YAMLError` com `problem_mark`; sem `problem_mark`, `fail(f'{basename}: {e}')`.

- [ ] **Step 1: teste que falha**

```python
def test_load_yaml_reports_the_line_of_a_syntax_error(tmp_path, capsys):
    p = tmp_path / 'spec.yaml'
    p.write_text('steps:\n  - {text: Precisa isolar?, kind: decision}\n', encoding='utf-8')
    with pytest.raises(SystemExit) as e:
        common.load_yaml(str(p))
    assert e.value.code == 1
    assert 'spec.yaml line 2' in capsys.readouterr().out
```
(Confirmar em `common.fail` se a mensagem vai para stdout ou stderr e ajustar o `readouterr`.)

- [ ] **Step 2:** `pytest tests/test_common.py -k syntax_error` → FAIL (traceback do yaml).
- [ ] **Step 3:** implementar em `load_yaml`; linha = `problem_mark.line + 1`, problema = `e.problem`.
- [ ] **Step 4:** `pytest tests/test_common.py` → PASS.
- [ ] **Step 5:** commit "diagram: erro de YAML com a linha".

### Task 2: biblioteca de ícones

**Files:**
- Create: `tools/build_icons.py`, `tests/test_build_icons.py`
- Create: `skills/syllabook/assets/icons.json`, `skills/syllabook/assets/ICONS-LICENSE.txt`
- Create: `skills/syllabook/scripts/icons.py`, `tests/test_icons.py`
- Modify: `skills/syllabook/scripts/diagram.py` (`main`: opção `--icons`)

**Interfaces:**
- Produces `tools/build_icons.py`: `build(svg_dir: str, names: list[str]) -> tuple[dict[str, str], list[str]]` (ícones encontrados `{nome: conteúdo interno do <svg>}`, nomes ausentes); CLI `python tools/build_icons.py <pasta lucide-static/icons> [--out PATH]` usa a lista `NAMES` do próprio arquivo e grava JSON ordenado por nome, uma entrada por linha.
- Produces `scripts/icons.py`:
  - `names() -> list[str]` (ordenada)
  - `known(name: str) -> bool`
  - `suggest(name: str) -> list[str]` (até 3, `difflib.get_close_matches`, cutoff 0.6)
  - `draw(name: str, x: float, y: float, size: float, color: str, width: float = 2) -> str`: `<g transform="translate(x,y) scale(size/24)" fill="none" stroke="color" stroke-width="width" stroke-linecap="round" stroke-linejoin="round">…</g>`; `KeyError` se desconhecido.
  - JSON lido uma vez (cache em módulo), de `../assets/icons.json` relativo ao script.

- [ ] **Step 1: testes que falham** (`tests/test_build_icons.py`, com pasta falsa de 2 SVGs):

```python
def test_build_keeps_the_inner_markup_and_reports_missing(tmp_path):
    (tmp_path / 'folder.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" '
                                         'class="lucide"><path d="M1 1h2"/></svg>')
    icons, missing = build_icons.build(str(tmp_path), ['folder', 'nope'])
    assert icons == {'folder': '<path d="M1 1h2"/>'} and missing == ['nope']
```
(`tests/test_icons.py`):
```python
def test_every_icon_is_valid_svg_markup():
    for n in icons.names():
        ET.fromstring(f'<svg xmlns="http://www.w3.org/2000/svg">{icons.draw(n, 0, 0, 24, "#000")}</svg>')

def test_suggestions_for_a_typo():
    assert 'folder' in icons.suggest('foldr')

def test_draw_scales_to_the_size_and_colors_the_stroke():
    g = icons.draw('folder', 10, 20, 48, '#123456')
    assert 'translate(10,20) scale(2' in g and 'stroke="#123456"' in g

def test_unknown_icon_raises_key_error():
    with pytest.raises(KeyError):
        icons.draw('nope', 0, 0, 24, '#000')

def test_the_library_has_the_planned_size():
    assert 70 <= len(icons.names()) <= 110

def test_command_lists_icons(cli):  # diagram.py --icons
    result = cli('diagram', '--icons')
    assert 'folder' in result['icons']
```
(Seguir o padrão do fixture `cli` de `tests/conftest.py` para o retorno.)

- [ ] **Step 2:** `pytest tests/test_build_icons.py tests/test_icons.py` → FAIL (módulos não existem).
- [ ] **Step 3:** implementar `tools/build_icons.py` com `NAMES` = lista abaixo; o conteúdo interno é tudo entre a tag `<svg …>` e `</svg>`, sem quebras de linha extras.
  `NAMES`: folder, folder-open, file, file-text, file-code, files, code, code-xml, braces, terminal, square-terminal, database, server, cloud, cloud-upload, cloud-download, network, globe, wifi, link, lock, lock-open, key, shield, shield-check, settings, wrench, user, users, message-circle, message-square, mail, bell, book, book-open, notebook-pen, graduation-cap, search, lightbulb, target, brain, puzzle, chart-bar, chart-line, chart-pie, calculator, sigma, percent, hash, binary, variable, table, clock, calendar, timer, circle-check, circle-x, triangle-alert, info, circle-help, play, pause, repeat, refresh-cw, rotate-ccw, music, mic, headphones, guitar, languages, pencil, list, list-checks, list-ordered, layers, arrow-right, arrow-left-right, filter, package, box, container, cpu, monitor, app-window, smartphone, git-branch, git-merge, git-pull-request, bug, rocket, zap, flask-conical, atom, sparkles, star, house, map, compass, eye, download, upload, copy, save, workflow.
- [ ] **Step 4:** gerar os ícones: `npm pack lucide-static` no scratchpad, extrair, `python tools/build_icons.py <pasta>/package/icons --out skills/syllabook/assets/icons.json`. Nomes ausentes são impressos: tirar da lista (não inventar). Copiar o `LICENSE` do pacote para `ICONS-LICENSE.txt`, com uma linha no topo: `Icons from Lucide (https://lucide.dev), version <versão do pacote>, ISC license.`
- [ ] **Step 5:** implementar `scripts/icons.py` e `--icons` no `diagram.py` (`out({'icons': icons.names()})`); no `--help`, uma linha: `--icons lists the icon names for the "icon" fields`.
- [ ] **Step 6:** `pytest tests/test_build_icons.py tests/test_icons.py tests/test_repo.py` → PASS.
- [ ] **Step 7:** commit "diagram: biblioteca de ícones Lucide embutida".

### Task 3: tema novo e caixas com nota e ícone

**Files:**
- Modify: `skills/syllabook/scripts/diagram.py` (`PALETTE`, `Canvas`, `header`, `box_with_text`)
- Test: `tests/test_diagram.py`

**Interfaces:**
- Consumes: `icons.known`, `icons.suggest`, `icons.draw` (Task 2).
- Produces:
  - `PALETTE[cor] = (fill, border, strong, tint)` para as 7 cores atuais.
  - `Canvas.icon(name, x, y, size, color) -> bool`: desenha com `PALETTE[color][2]`; se desconhecido, adiciona a `problems` `f'unknown icon "{name}"' + (f' (did you mean {", ".join(sugestões)}?)' if sugestões else '')` e retorna False.
  - `Canvas.svg` passa a incluir `<linearGradient id="underline">` (azul → lilás → salmão → amarelo, os `border` de blue, purple, red, orange).
  - `header(c, spec)` desenha `subtitle` (opcional, tamanho `small`, cor `SOFT`) abaixo do título e o sublinhado com `fill="url(#underline)"`.
  - `box_with_text(c, x, y, w, text, color, size=None, weight=500, dashed=False, note=None, icon=None) -> float` (altura). Com `icon`: ícone de `size*1.3` à esquerda, texto alinhado à esquerda depois dele, largura útil = `w - 2*14 - size*1.3 - 10`. Com `note`: segunda linha(s) em `small`, cor `SOFT`. Sem `icon` e sem `note`: mesmo desenho centralizado de hoje (só com a paleta nova).

- [ ] **Step 1: testes que falham**

```python
def contrast(a, b): ...  # luminância relativa WCAG; helper no teste

@pytest.mark.parametrize('color', sorted(diagram.PALETTE))
def test_strong_text_is_readable_on_fill_and_tint(color):
    fill, _, strong, tint = diagram.PALETTE[color]
    assert contrast(strong, fill) >= 4.5 and contrast(strong, tint) >= 4.5

def test_subtitle_and_gradient_underline():
    text, *_ = diagram.render(spec('bars', subtitle='Seção 4 · classes'))
    assert 'Seção 4 · classes' in text and 'url(#underline)' in text

def test_box_with_note_and_icon_draws_both():
    s = spec('layers'); s['layers'][0].update(icon='layers', note='COPY . .')
    text, _, problems, _ = diagram.render(s)
    assert 'COPY . .' in text and 'scale(' in text and not problems

def test_icon_takes_width_from_the_text_in_the_small_profile():
    s = spec('layers'); s['layers'][0] = {'text': 'x' * 30, 'icon': 'layers'}
    assert not diagram.render(dict(s, layers=[{'text': 'x' * 30}]), 'small')[2]
    assert any('does not fit' in p for p in diagram.render(s, 'small')[2])

def test_unknown_icon_is_a_problem_with_suggestions():
    s = spec('layers'); s['layers'][0]['icon'] = 'foldr'
    assert any('unknown icon "foldr"' in p and 'folder' in p for p in diagram.render(s)[2])
```
(Ajustar o tamanho do texto `x * 30` até o primeiro caso caber e o segundo não, no perfil `small`; o objetivo do teste é exatamente essa fronteira.)

- [ ] **Step 2:** `pytest tests/test_diagram.py` → os novos FAIL.
- [ ] **Step 3:** implementar. Paleta: tons mais saturados que os de hoje, na linha das referências (fundos como `#DCE8FF`, `#D6F2E4`, `#FFF0C2`, `#FFE0D6`, `#EBE0FB`, `#D5F0F0`, `#EEEBE4` para `tint`; `fill` um passo mais claro); valores finais a critério do construtor, passando no teste de contraste.
- [ ] **Step 4:** `pytest tests/test_diagram.py` → PASS (os testes antigos inclusive).
- [ ] **Step 5:** commit "diagram: tema novo, subtítulo e caixas com nota e ícone".

### Task 4: campos novos nos tipos (menos cards)

**Files:**
- Modify: `skills/syllabook/scripts/diagram.py` (`flow`, `layers`, `compare`, `boxes`, `tree`, `timeline`, `sequence`)
- Test: `tests/test_diagram.py`

**Interfaces:**
- Consumes: `box_with_text(..., note=, icon=)`, `Canvas.icon` (Task 3).
- Produces (campos de spec, todos opcionais):
  - `flow` passo: `note`, `icon`; decisão: texto numa linha se couber em `dw*0.75` com fonte `body`, senão tenta `small` antes de quebrar; `note` abaixo; `side_note`, `side_icon`, `side_color` (padrão `'red'`).
  - `layers`: `icon`; `text` e `note` em linhas separadas (sem o "·").
  - `compare`: `left.icon`, `right.icon`; `wrong-right` desenha `circle-x`/`circle-check` em vez de ❌/✅ (sem emoji no SVG); `rows` aceita `[left, right]` como hoje.
  - `boxes`: índice (`label`) num selo arredondado `gray`; `highlight` com borda `strong` de 3 px.
  - `tree`: `icon` por nó. `timeline`: `icon` por evento, dentro do círculo. `sequence`: `participants` aceita `str` ou `{name, icon}`; `messages.from/to` usam o `name`.

- [ ] **Step 1: testes que falham**

```python
@pytest.mark.parametrize('kind, change, expect', [
    ('flow', lambda s: s['steps'][0].update(icon='play', note='lê as notas'), 'lê as notas'),
    ('flow', lambda s: s['steps'][1].update(side_note='nada a fazer', side_color='teal'), 'nada a fazer'),
    ('tree', lambda s: s['root'].update(icon='file-code'), 'scale('),
    ('timeline', lambda s: s['events'][0].update(icon='bug'), 'scale('),
    ('sequence', lambda s: s.update(participants=[{'name': 'api', 'icon': 'server'}, 'db']), 'scale('),
])
def test_new_optional_fields(kind, change, expect):
    s = spec(kind); change(s)
    text, _, problems, _ = diagram.render(s)
    assert expect in text and not problems

def test_compare_wrong_right_uses_drawn_icons_not_emoji():
    text, *_ = diagram.render(spec('compare'))
    assert '✅' not in text and '❌' not in text and 'scale(' in text

def test_no_emoji_left_in_any_type():
    for kind in SPECS:
        text, *_ = diagram.render(spec(kind))
        assert not re.search('[✀-➿\U0001F300-\U0001FAFF]', text), kind
```
E atualizar `TEXTS['compare']` de `'✅ Certo'` para `'Certo'`.

- [ ] **Step 2:** rodar → FAIL.
- [ ] **Step 3:** implementar tipo a tipo; o ✓ de texto dos cards sai na Task 5 (o teste "no emoji" só passa por completo depois dela: marcar `cards` como `xfail` aqui e tirar na Task 5).
- [ ] **Step 4:** `pytest tests/test_diagram.py` → PASS.
- [ ] **Step 5:** commit "diagram: ícones e notas em flow, layers, compare, boxes, tree, timeline e sequence".

### Task 5: `scene` e cards no estilo novo

**Files:**
- Modify: `skills/syllabook/scripts/diagram.py` (nova `scene_block`, `scene` como tipo, `cards`, `TYPES`, `LAYOUTS`, `REQUIRED`)
- Test: `tests/test_diagram.py`

**Interfaces:**
- Consumes: `Canvas.icon`, `icons.known` (Tasks 2–3).
- Produces:
  - `scene_block(c, x, y, w, scene, color) -> float` (altura). `scene` = `{steps: [[ícone, ...], ...], ops: [op, ...] (opcional, len = passos-1, cada um em '→','+','=','↔'; padrão '→'), label: str (opcional)}`. Passos espaçados igualmente em `w`; ícones de um passo empilhados (até 3) dentro de um quadrado `tint` com borda; `→`/`↔` desenhados como setas (marker), `+`/`=` como texto grande `strong`; `label` em `small` abaixo.
  - Problemas: `'a scene holds at most 4 steps'`, `'a scene step holds 1 to 3 icons'`, `f'scene op "{op}" must be one of → + = ↔'`, ícone desconhecido via `Canvas.icon`.
  - Tipo `scene`: `REQUIRED['scene'] = 'steps'`; spec `{type: scene, title, steps, ops, label}`; desenha `scene_block` na largura toda; conta `len(steps)` elementos.
  - `cards`: card com `tint`; selo do ícone (quadrado arredondado de `size*2.2`, `fill`, borda `border`) à esquerda do título: se `icons.known(icon)` desenha o ícone, senão texto mono até 4 caracteres (compatível); itens com círculo + check desenhados (ícone `circle-check` em `strong`) ou o `icon` do item quando `items` tiver `{text, icon}`; `scene` opcional: coluna à direita com 40% da largura no `large`, faixa abaixo dos itens no `small`; `code` como hoje.

- [ ] **Step 1: testes que falham**

```python
def test_scene_type_draws_steps_ops_and_label():
    s = {'type': 'scene', 'title': 'Prompt', 'steps': [['user'], ['list'], ['sparkles']],
         'ops': ['+', '='], 'label': 'Melhor saída'}
    text, _, problems, _ = diagram.render(s)
    assert 'Melhor saída' in text and '+' in text and not problems

@pytest.mark.parametrize('scene, problem', [
    ({'steps': [['file']] * 5}, 'at most 4 steps'),
    ({'steps': [[]]}, '1 to 3 icons'),
    ({'steps': [['file'] * 4]}, '1 to 3 icons'),
    ({'steps': [['file'], ['file']], 'ops': ['*']}, 'must be one of'),
])
def test_scene_limits(scene, problem):
    assert any(problem in p for p in diagram.render({'type': 'scene', 'title': 'x', **scene})[2])

def test_card_with_icon_name_items_with_icons_and_a_scene():
    s = spec('cards')
    s['cards'][0].update(icon='folder', items=[{'text': 'juntos', 'icon': 'files'}, 'instruções'],
                         scene={'steps': [['folder'], ['file', 'file']], 'label': 'Memória'})
    for profile in ('large', 'small'):
        text, _, problems, _ = diagram.render(s, profile)
        assert 'Memória' in text and 'instruções' in text and not problems

def test_card_ascii_icon_still_works():
    text, _, problems, _ = diagram.render(spec('cards'))   # icons '[]' and 'for'
    assert 'for' in text and not problems
```
Tirar o `xfail` de `cards` do teste "no emoji" (Task 4). Acrescentar `'scene'` ao `SPECS`/`TEXTS` para entrar no teste dos dois perfis.

- [ ] **Step 2:** rodar → FAIL.
- [ ] **Step 3:** implementar.
- [ ] **Step 4:** `pytest` completo + `ruff check .` → PASS, cobertura ≥ 95%.
- [ ] **Step 5:** commit "diagram: scene e cheat sheet no estilo novo".

### Task 6: revisão visual, documentação e exemplos

**Files:**
- Modify: `skills/syllabook/scripts/diagram.py` (docstring/`--help`)
- Modify: `skills/syllabook/references/VISUALS.md` (§4 regras, cheat sheets; §5 linha "no decorative scenes" → diferenciar `scene` de diagrama vs ilustração)
- Modify: `skills/syllabook/SKILL.md` (linha do `diagram.py`: citar `--icons`)
- Create: `tests/fixtures/sample-book/img/_source/c01-lista.yaml`; regenerar `tests/fixtures/sample-book/img/c01-lista.svg`
- Test: `tests/test_diagram.py` (`test_help_lists_every_type` cobre `scene`)

**Interfaces:**
- Consumes: tudo das Tasks 2–5.

- [ ] **Step 1:** atualizar `--help`: tipos com os campos novos (`note`, `icon`, `subtitle`, `side_note/side_icon/side_color`, `scene`), uma linha "icons: names from `--icons`; a scene demonstrates the idea, never decorates". Rodar `pytest tests/test_diagram.py -k help` → PASS.
- [ ] **Step 2:** VISUALS.md: ícone por item quando ajuda a distinguir conceitos; `scene` quando o card tem uma relação (A → B, A + B = C); "SVG is for diagrams only; illustrations are a separate, later step"; ✅/❌ desenhados. Rodar `python tools/translation.py check` se VISUALS tiver tradução (hoje não tem; confirmar).
- [ ] **Step 3:** spec do fixture `c01-lista.yaml` (tipo `boxes`, `name: notas`, valores 7.5/8.0/6.5, índices 0/1/2, primeiro destacado, caption "O primeiro item tem índice 0."); `python skills/syllabook/scripts/diagram.py tests/fixtures/sample-book/img/_source/c01-lista.yaml` → `fits: true`. O texto alternativo do capítulo 1 já descreve esse desenho.
- [ ] **Step 4: revisão olhando o PNG.** Gerar no scratchpad um spec de cada tipo (os da conversa: fluxo do WSL, camadas do WSL, compare, sequence, cards com 6 cards e 2 cenas, scene "Papel + Tarefa + Contexto + Formato = Melhor saída") nos perfis `large` e `small`, converter com resvg-py e olhar cada PNG. Comparar com as referências em `scratchpad/ref/` (WSL c01 e cheat sheets Dio). Corrigir sobreposição, desalinhamento e texto colado; rodar `pytest` de novo após cada ajuste.
- [ ] **Step 5:** `pytest` + `ruff check .` → PASS; commit "diagram: documentação, exemplo do livro de teste e ajustes da revisão visual"; push; conferir o CI verde (`gh run watch`).
- [ ] **Step 6:** vitrine `Joshpcbrrj/syllabook-demo`: copiar `skills/` atualizada e o `c01-lista` (spec + svg) para `created-books/python-do-zero-demo/img/`, commit com o e-mail noreply, push, conferir os workflows de EPUB e site verdes.
- [ ] **Step 7:** republicar no Notion só a página "1. Listas" (id `41e345e2044381b09e07fe0bf060b856`) com o SVG novo: `notion.py 1 --book <demo>`, upload, `replace_content`; conferir com fetch.
