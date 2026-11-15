# Ementa: propor, ajustar com o aluno e aprovar

> Arquivo de apoio da skill `criar-livro-tecnologia`. Leia nas etapas Entender e Ementa.

A ementa é o contrato do livro. **Nada é escrito antes de o aluno aprovar.** Errar aqui custa o livro inteiro; ajustar aqui custa uma mensagem.

## 1. Entender o pedido (no máximo 3 perguntas, numa mensagem)

Pergunte só o que o pedido não disse. Use `AskUserQuestion` se houver; senão, texto.

| Pergunta | Opções sugeridas (padrão em negrito) |
| --- | --- |
| Para quem é? | **quem nunca usou o tema**, quem já usa e quer se aprofundar, uso no trabalho |
| Qual nível? | **iniciante**, intermediário, avançado |
| Qual tamanho? | guia curto (4–5 capítulos), **livro (8–10)**, completo (12–15) |

Antes de perguntar, rode `python3 ferramentas/mapa_livros.py`. Se já houver livros na mesma trilha, diga quais são e proponha a posição do novo ("o básico já existe; este pode começar do Compose"). Isso costuma substituir a pergunta de nível.

## 2. Propor a ementa

Pesquise antes (veja `referencias/PESQUISA.md`): documentação oficial, guia de primeiros passos, versão atual da ferramenta. A ementa segue estas regras:

- **Progressão:** cada capítulo usa só o que os anteriores ensinaram. O primeiro responde "por que isso existe"; o último é um **projeto final** que junta tudo.
- **Um objetivo por capítulo**, com verbo de ação que dá para conferir: "construir uma imagem própria", e não "entender imagens".
- **Prática em todo capítulo:** um laboratório com comandos ou código executáveis e 2–3 exercícios.
- **Escopo explícito:** a lista "Fica para livros futuros" diz o que o livro **não** cobre, e é ela que alimenta os próximos livros da trilha.

Mostre no chat neste formato, e em nenhum outro:

```text
📘 <Título do livro>  ·  <nível>  ·  <n> capítulos  ·  trilha: <trilha> (<posição>)
Para quem: <uma frase>
Ao terminar, você vai: <objetivo do livro>
Pré-requisitos: <livros da trilha ou conhecimentos>

1. <Título do capítulo>      → <objetivo com verbo de ação>
2. ...
n. Projeto final: <nome>     → <o que o leitor entrega>

Fica para livros futuros: <tema>, <tema>, <tema>
Versão de referência: <ferramenta x.y, conferida em AAAA-MM-DD>

Ajuste à vontade: "aumenta", "diminui", "tira o 5", "adiciona X",
"junta o 3 e o 4", "troca a ordem", "mais prático", "nível intermediário".
Quando estiver bom, diga "aprovado".
```

## 3. Ajustar (quantas rodadas o aluno quiser)

Interprete pedidos em linguagem natural e responda sempre com **a ementa inteira atualizada** e, acima dela, uma linha "Mudou:" listando as alterações.

| Pedido | O que fazer |
| --- | --- |
| "aumenta" / "mais completo" | Acrescente capítulos ou aprofunde os existentes, sem quebrar a progressão; diga o novo total |
| "diminui" / "mais curto" | Junte capítulos próximos e mande o excedente para "Fica para livros futuros" |
| "tira o X" | Remova; se algo depois dependia dele, mova esse conteúdo ou avise |
| "adiciona Y" | Encaixe onde a progressão permitir; se Y for avançado demais para o nível, sugira deixar para outro livro |
| "junta", "separa", "troca a ordem" | Faça e confira se nenhum capítulo passa a usar algo ainda não ensinado |
| Pedido que contradiz o nível ou o tamanho | Faça, mas avise em uma frase o efeito ("com Kubernetes, o livro deixa de ser iniciante") |

Se a sobreposição com um livro existente passar de ~40% (`mapa_livros.py --checar`), pergunte se é melhor ampliar o livro antigo ou mudar o enfoque do novo.

## 4. Aprovar e registrar

Ao ouvir "aprovado" (ou equivalente claro), e só então:

1. Grave `livros/<slug>/ementa.yaml` com `aprovada_em` preenchido, faça commit e push. A partir daí o livro aparece no mapa da trilha.
2. Crie no Notion a página índice do livro (dentro da página de livros do `biblioteca.yaml`) e uma subpágina vazia por capítulo, na ordem.
3. Cadastre os ids com `progresso.py <slug> init`.

**Mudanças depois da aprovação:** mostre o impacto ("tirar o capítulo 5 afeta os exemplos dos capítulos 6 e 8"), peça aprovação só da mudança, atualize o `ementa.yaml` (o histórico fica no git) e as páginas do Notion.

## Modelo do `ementa.yaml`

```yaml
titulo: "Docker do zero"
slug: docker-do-zero            # minúsculas, hífens, sem acento
trilha: docker                  # agrupa os livros complementares
ordem_na_trilha: 1
nivel: iniciante                # iniciante | intermediário | avançado
publico: "Quem programa, mas nunca usou contêineres"
objetivo: "Empacotar e publicar uma aplicação com banco de dados em contêineres"
pre_requisitos: []              # slugs de outros livros desta biblioteca
versao_referencia: "Docker Engine 29.x (conferido em 2026-11-15)"
aprovada_em: "2026-11-15"       # vazio enquanto for rascunho
capitulos:
  - n: 1
    titulo: "Por que contêineres existem"
    objetivo: "Explicar que problema o Docker resolve e quando não usar"
    topicos: [isolamento, "imagem x contêiner", "contêiner x máquina virtual"]
  - n: 2
    titulo: "Instalação e primeiro contêiner"
    objetivo: "Rodar, listar, parar e remover um contêiner"
    topicos: [docker run, docker ps, ciclo de vida]
cobre: [conteiner, imagem, dockerfile, volumes, redes-basicas, docker-hub]
fica_para_depois: [compose-avancado, swarm, kubernetes, seguranca-de-imagens]
```

`cobre` e `fica_para_depois` usam rótulos curtos e estáveis (minúsculas, hífens): são eles que o mapa compara entre livros.
