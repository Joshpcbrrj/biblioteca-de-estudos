# Estado dos cursos

Diário de bordo da reformulação. A skill lê este arquivo no início de cada chat e o atualiza sempre que para (antes de pedir exportação) e ao publicar. Assim, qualquer chat novo continua do ponto certo.

**Padrão atual:** skill `revisar-curso-biblioteca` (pasta `skill/`), com imagens no tema v3 (creme, cards pastel, setas pontilhadas), analogia abaixo de cada diagrama, "De onde paramos", "🧠 Revisão rápida", "➡️ Próximo passo", código comentado com linhas de até 60 caracteres e cheat sheet 3×4 por seção.

**Situação:** ✅ publicado no padrão atual · 🟡 em andamento · ⬜ publicado no padrão anterior (falta reformular)

| Curso (pasta) | Situação | Onde parou / o que falta |
| --- | --- | --- |
| Bóson: Lógica com Portugol (`boson-logica-portugol`) | ✅ | Publicado em 15/11/2026. As 42 páginas no padrão atual. Nenhuma pendência. |
| StartSe: Tech Academy (`startse-tech-academy`) | 🟡 | No Notion, as aulas 001, 002, 003, 004, 006, 007, 008, 009, 012, 013, 015, 016, 017, 018 e 020 já têm as imagens novas (e os cheat sheets 01 e 02). Faltam as demais aulas. A aula 002 repete a analogia da URL da aula 020: troque a da 002. |
| Capgemini: Programa Start (`capgemini-start`) | 🟡 | No Notion, os cheat sheets dos módulos (lógica, web, CSS, JS, Angular e Java) já estão no padrão novo. Faltam as imagens das aulas e as analogias do módulo 16 (streams, JPA/ORM, exceções, camadas do Spring e fullstack). |
| Santander Coders: Back-End (`santander-coders-backend`) | ⬜ | Imagens do GitHub já no tema v3; texto e Notion ainda no padrão anterior. |
| Dio: Banco Pan Java (`dio-banco-pan-java`) | ⬜ | Igual ao Santander. |
| Cod3r: Lógica com JS (`cod3r-logica-javascript`) | ⬜ | Igual ao Santander. |
| Geek University: Lógica (`geek-university-logica`) | ⬜ | Igual ao Santander; só 6 imagens: precisa de diagramas novos. |
| Intellectuale: Lógica com Flowgorithm (`intellectuale-logica-flowgorithm`) | ⬜ | Igual ao Santander. |

**Ordem combinada com o dono:** um curso por vez; o próximo é escolhido por ele.

## Como atualizar este arquivo

- Ao parar para pedir exportação: mude a situação para 🟡 (ou mantenha) e liste as páginas feitas e as que faltam.
- Ao publicar: mude para ✅, com a data e as pendências que sobraram (avisos da auditoria, por exemplo).
- Frases curtas, uma linha por curso. Faça commit junto com o trabalho.
