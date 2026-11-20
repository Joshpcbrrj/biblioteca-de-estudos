# Modo Criar: do tema à ementa aprovada

Copie este checklist na resposta e vá marcando:

```text
- [ ] 1. Entender o pedido (até 3 perguntas)
- [ ] 2. Escolher o perfil de área
- [ ] 3. Pesquisar
- [ ] 4. Parecer + ementa (na mesma mensagem)
- [ ] 5. Ajustar até "aprovado"
- [ ] 6. Gravar o livro.yaml e seguir o fluxo do SKILL.md
```

**Nada de capítulo antes do "aprovado".** Errar na ementa custa o livro inteiro; ajustar custa uma mensagem.

## 1. Entender o pedido

Uma mensagem só, com no máximo 3 perguntas, e só o que o pedido não disse:

| Pergunta | Padrão se o usuário não responder |
| --- | --- |
| Qual o seu nível hoje no tema? | nunca estudou |
| Para que você quer aprender? (ex.: trabalho, viagem, hobby, prova) | uso geral |
| Tamanho: guia curto (5–6 cap.), livro (8–12) ou completo (13–16)? | livro |

Não pergunte tempo por dia: o cap. 0 traz cronogramas em três ritmos.

Na mesma mensagem, ofereça (não é pergunta obrigatória): "Se tiver livros, PDFs, EPUBs ou uma pasta no Google Drive sobre o tema, pode mandar: uso como fonte." Se o usuário mandar, passe cada arquivo pelo `ingerir.py` e use só o sumário até a etapa 3; no Drive, liste os arquivos encontrados e deixe o usuário escolher antes de abrir. Regras de uso em `referencias/FONTES.md` (entender e conferir, nunca copiar).

Se o usuário tiver uma biblioteca no GitHub, confira em `livros-criados/` e `materiais-aprimorados/` se já existe livro do mesmo tema. Se existir, mostre o que ele cobre e pergunte: ampliar esse, criar o próximo da trilha ou outro enfoque.

## 2. Perfil de área

Escolha o perfil pelo tema e leia só ele (no máximo 2, quando o tema combinar áreas, ex.: eletrônica = `habilidades.md` + `exatas.md`):

| Perfil | Temas |
| --- | --- |
| `exatas.md` | programação, matemática, estatística, tecnologia |
| `idiomas.md` | inglês e outras línguas |
| `habilidades.md` | música, eletrônica, desenho, culinária, prática manual |
| `conhecimento.md` | história, ciências, conceitos, temas de leitura |

## 3. Pesquisar

Siga `referencias/FONTES.md`. Objetivo da pesquisa, e nada além dele:

- o **currículo usual** do tema (ementas de universidades, livros-texto, documentação oficial);
- os **pré-requisitos** e os **erros e mitos comuns** de quem começa;
- a **versão atual**, quando o tema muda com o tempo (ferramentas, leis);
- 4 a 8 **fontes** confiáveis, com a data de conferência.

Comece pelos materiais do usuário, se houver (só as seções úteis, pelo sumário). Faça buscas com pergunta específica e pare quando tiver isso. As fontes vão para o `livro.yaml`; os capítulos reaproveitam e não pesquisam o tema de novo.

## 4. Parecer + ementa

Antes de mostrar, grave o rascunho **fora do repositório** (`/tmp/livro-<slug>.yaml`, com `aprovada_em: ""`, as `fontes` e o grafo de conceitos; modelo em `referencias/EMENTA.md`) e rode `python scripts/livro.py validar /tmp/livro-<slug>.yaml`. Corrija até passar.

Mostre numa mensagem só, neste formato:

```text
🔎 Parecer: <tema>
O que é e para que serve: <1–2 frases>
Ajuda saber antes: <pré-requisitos, ou "nada">
Como se aprende: <o caminho usual, em 1–2 frases>
Erros e mitos comuns: <2–3 itens>
Fontes principais: <2–4 nomes>

📘 <Título> · <nível inicial> → <nível final> · <n> capítulos · ~<h> h
Para quem: <uma frase>
Ao terminar, você vai: <objetivo do livro, verificável>
Pré-requisitos: <conhecimentos ou livros>

0. Como estudar este livro
1. <Título>                    → <objetivo com verbo de ação>
2. ...
n. <Projeto ou desafio final>  → <o que o leitor entrega>
   Simulado final

Próximos caminhos: <2–4 temas para livros seguintes>
Versão de referência: <só se o tema muda com o tempo, com a data>

Ajuste à vontade: "aumenta", "diminui", "tira o 5", "adiciona X",
"junta o 3 e o 4", "troca a ordem", "mais prático".
Quando estiver bom, diga "aprovado".
```

Regras da ementa:

- **Do básico ao intermediário**, salvo pedido diferente.
- **Progressão:** cada capítulo usa só conceitos dos anteriores (o `livro.py validar` confere pelo grafo de conceitos).
- **Um objetivo por capítulo**, com verbo que dá para conferir ("montar", "traduzir", "tocar a 80 bpm"), nunca "entender" ou "conhecer".
- **Capítulo 1 com uma vitória concreta** (algo que funciona, se fala ou se toca já no primeiro dia).
- **Prática em todo capítulo**, do tipo definido no perfil.
- **Escopo explícito:** o que não cabe vai para "Próximos caminhos".

## 5. Ajustar até "aprovado"

Interprete pedidos em linguagem natural. Responda sempre com **a ementa inteira atualizada** e, acima dela, uma linha `Mudou: ...`. Rode o `livro.py validar` a cada mudança.

| Pedido | O que fazer |
| --- | --- |
| "aumenta" / "mais completo" | acrescente ou aprofunde capítulos sem quebrar a progressão; diga o novo total |
| "diminui" / "mais curto" | junte capítulos próximos; o excedente vai para Próximos caminhos |
| "tira o X" | remova; se outro capítulo depende dele, leve o mínimo necessário para lá e diga no `Mudou:` |
| "adiciona Y" | encaixe onde a progressão permitir; se Y for avançado para o nível, sugira deixar para outro livro |
| "mais prático" | troque objetivos de explicar por tarefas; projeto final mensurável |
| "junta", "separa", "troca a ordem" | faça e confira se nenhum capítulo passou a usar conceito ainda não ensinado |
| pedido que contradiz nível ou tamanho | faça, e avise o efeito em uma frase |

## 6. Gravar e seguir

Ao ouvir "aprovado" (ou equivalente claro), e só então:

1. Preencha `aprovada_em` e grave em `livros-criados/<slug>/livro.yaml` (com GitHub conectado, na branch `rascunho/<slug>`).
2. Siga o "Fluxo depois do aprovado" do `SKILL.md`, a partir do passo 1.

**Mudança depois de aprovado:** mostre o impacto ("tirar o cap. 5 afeta os exemplos dos caps. 6 e 8"), peça aprovação só da mudança e atualize o `livro.yaml` conforme `referencias/EMENTA.md`.
