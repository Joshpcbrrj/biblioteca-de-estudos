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

**Ordem da trilha devops (combinada com o dono):** 1. Docker Compose na prática → 2. Docker Swarm do zero → 3. Kubernetes do zero. Cada livro só é escrito depois do anterior estar publicado.

| Livro (pasta) | Trilha | Índice no Notion (id) | Situação | Onde parou / o que falta |
| --- | --- | --- | --- | --- |
| `livros/wsl-do-zero` | wsl (1º) | 419345e2044381a2b27edff0235f85f2 | ✅ publicado 2026-11-15 | 11 capítulos, capa e EPUB. Avisos aceitos: saida_longa (saídas reais de terminal e linhas com URL; o EPUB quebra a linha). Revisar versões em nov/2027. |
| `livros/docker-do-zero` | docker (1º) | 419345e2044381a8a4aac8e2a8ddd1d1 | ✅ publicado 2026-11-16 | 13 capítulos, capa e EPUB. Labs no Docker Engine 29.9.2 com imagem ubuntu:24.04 local (Hub bloqueado). Avisos aceitos: saida_longa. Revisar versões em nov/2027. |
| `livros/docker-compose-na-pratica` | devops (1º) | 41b345e2044381c19feecbab08c8b211 | 🟡 ementa aprovada 2026-11-17, 1 de 14 capítulos escritos | Cap. 1 escrito com laboratório executado (saídas reais). Próximo: cap. 2 ("Instalar e conferir o Compose"). Faltam: índice e cheat sheet da 1ª parte (definir as partes antes), publicação. |
| `livros/docker-swarm-do-zero` | devops (2º) | 41b345e2044381458a26d98bb8aef5c2 | 🟡 ementa aprovada 2026-11-17, 14 capítulos no Notion vazios | Escrita só depois do Compose (ordem da trilha). Quando chegar a vez: cap. 1 ("Por que orquestrar"). Laboratório multi-nó com contêineres `docker:dind` a validar antes do cap. 3. |
| `livros/kubernetes-do-zero` | devops (3º) | 41b345e2044381c29fabd02d23dc2bb5 | 🟡 ementa aprovada 2026-11-17, 15 capítulos no Notion vazios | Escrita só depois do Swarm (ordem da trilha). Quando chegar a vez: cap. 1 ("Por que o Kubernetes existe"). Cluster com kind (vários nós) no Docker Desktop, versão 1.37.1. Ingress (cap. 13) e Gateway API (cap. 14) separados. A conferir antes de escrever: instalação das CRDs e de um controlador da Gateway API no kind, e um controlador de Ingress que não seja o Ingress NGINX (aposentado). |

Página do Notion onde os livros são criados: `notion_livros` do `biblioteca.yaml` (página "📗 Cursos criados a partir de ementa", dentro de Estudos).

## Como atualizar este arquivo

- Páginas concluídas ficam em `progresso/<slug>.json` (script `ferramentas/progresso.py`); aqui vai só o resumo.
- Ao parar para pedir exportação: mude a situação para 🟡 (ou mantenha) e liste as páginas feitas e as que faltam.
- Ao publicar: mude para ✅, com a data e os "avisos aceitos" da auditoria, para o próximo chat não tratá-los como erro.
- Frases curtas, uma linha por curso. Faça commit junto com o trabalho.
