# Estado dos cursos

Diário de bordo da reformulação. As skills leem este arquivo no início de cada chat e o atualiza sempre que para (antes de pedir exportação) e ao publicar. Assim, qualquer chat novo continua do ponto certo.

**Padrão atual:** skill `revisar-curso-biblioteca` (pasta `skill/`), com imagens no tema v3 (creme, cards pastel, setas pontilhadas), analogia abaixo de cada diagrama, "De onde paramos", "🧠 Revisão rápida", "➡️ Próximo passo", código comentado com linhas de até 60 caracteres e cheat sheet 3×4 por seção.

**Situação:** ✅ publicado no padrão atual · 🟡 em andamento · ⬜ publicado no padrão anterior (falta reformular)

| Curso (pasta) | Índice no Notion (id) | Situação | Onde parou / o que falta |
| --- | --- | --- | --- |
| Bóson: Lógica com Portugol (`boson-logica-portugol`) | `8b772bba9b614b229a9b95bdb781b736` | ✅ | Publicado em 15/11/2026, com o índice e as 41 aulas no padrão atual (progresso em `progresso/boson-logica-portugol.json`). Avisos aceitos: 9 imagens que dividem a analogia com a imagem ao lado e 1 tabela de 3 colunas com célula longa (aula 40). |
| StartSe: Tech Academy (`startse-tech-academy`) | `e6830a2b39514b5d8ed12ba3b11be1bf` | 🟡 | No Notion, as aulas 001, 002, 003, 004, 006, 007, 008, 009, 012, 013, 015, 016, 017, 018 e 020 já têm as imagens novas (e os cheat sheets 01 e 02). Faltam as demais aulas. A aula 002 repete a analogia da URL da aula 020: troque a da 002. |
| Capgemini: Programa Start (`capgemini-start`) | `1dba10cd207c4d98ac533fd0541a5432` | 🟡 | No Notion, os cheat sheets dos módulos (lógica, web, CSS, JS, Angular e Java) já estão no padrão novo. Faltam as imagens das aulas e as analogias do módulo 16 (streams, JPA/ORM, exceções, camadas do Spring e fullstack). |
| Santander Coders: Back-End (`santander-coders-backend`) | `b577cdd2eafd4d0bad2823787bd8957e` | ⬜ | Imagens do GitHub já no tema v3; texto e Notion ainda no padrão anterior. |
| Dio: Banco Pan Java (`dio-banco-pan-java`) | `a2aea06fdb2b456e9f22e65ca0e466a9` | ⬜ | Igual ao Santander. |
| Cod3r: Lógica com JS (`cod3r-logica-javascript`) | `4d6a1b710876489eb5c1f704f952361b` | ⬜ | Igual ao Santander. |
| Geek University: Lógica (`geek-university-logica`) | `adfd8948157a43f3a455b48b3055a489` | ⬜ | Igual ao Santander; só 6 imagens: precisa de diagramas novos. |
| Intellectuale: Lógica com Flowgorithm (`intellectuale-logica-flowgorithm`) | `e31cead3c72648cf93b69c365ac21edd` | ⬜ | Igual ao Santander. |

O id é o código de 32 caracteres no fim do link do índice no Notion; um curso novo entra aqui com o seu.

**Ordem combinada com o dono:** um curso por vez; o próximo é escolhido por ele.

## Livros criados do zero

Skill `criar-livro-tecnologia`. A ementa aprovada de cada livro fica em `livros/<slug>/ementa.yaml`; o mapa das trilhas, em `livros/README.md` (gerado por `ferramentas/mapa_livros.py --md`).

| Livro (pasta) | Trilha | Índice no Notion (id) | Situação | Onde parou / o que falta |
| --- | --- | --- | --- | --- |
| — | — | — | — | Nenhum livro ainda. |

Página do Notion onde os livros são criados: `notion_livros` do `biblioteca.yaml` (vazio até o primeiro livro).

## Como atualizar este arquivo

- Páginas concluídas ficam em `progresso/<slug>.json` (script `ferramentas/progresso.py`); aqui vai só o resumo.
- Ao parar para pedir exportação: mude a situação para 🟡 (ou mantenha) e liste as páginas feitas e as que faltam.
- Ao publicar: mude para ✅, com a data e os "avisos aceitos" da auditoria, para o próximo chat não tratá-los como erro.
- Frases curtas, uma linha por curso. Faça commit junto com o trabalho.
