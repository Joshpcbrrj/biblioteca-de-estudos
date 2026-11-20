# Esboço da skill (para revisão)

Primeira versão para o dono ler e comentar antes da fase 1. Nada aqui está instalado nem é usado ainda.

| Arquivo | Estado |
| --- | --- |
| `SKILL.md` | esboço completo |
| `modos/CRIAR.md` | esboço completo |
| `modos/APRIMORAR.md`, `modos/PUBLICAR.md` | a escrever depois da revisão destes dois |
| `referencias/*`, `referencias/areas/*` | a escrever na fase 2 |
| `scripts/*` | citados pelo nome; a escrever nas fases 2 e 3 |

## O que conferir na leitura

1. A primeira mensagem (menu) e as perguntas do modo Criar estão como você imagina?
2. O formato do **parecer + ementa** (`modos/CRIAR.md` §4) mostra o que você quer ver antes de aprovar?
3. O laço de cada capítulo (`SKILL.md`) está claro? É o coração da economia de tokens.
4. Falta alguma regra em "Nunca"?

## Decisões tomadas no esboço (diferenças em relação ao plano)

- O antigo `ESCRITA.md` não existe: o laço de cada capítulo é curto e ficou no próprio `SKILL.md`.
- O antigo `PUBLICACAO.md` virou parte de `modos/PUBLICAR.md` (conexões, GitHub, Notion, modo "Publicar livro pronto").
- Os scripts foram agrupados para o Claude chamar menos comandos: `livro.py` (validar, briefing, feito, status — substitui o `progresso.py`), `gerar.py` (mapa, navegação, glossário, apêndice de respostas, EPUB, pacote), `diagrama.py` (SVG a partir de especificação), `fatos.py` (frases a conferir) e `notion.py`.
- Parecer e ementa saem **na mesma mensagem**, para economizar uma rodada.
- O modo Continuar é tão curto que ficou dentro do `SKILL.md`.
