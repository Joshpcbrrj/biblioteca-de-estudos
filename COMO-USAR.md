# Como usar: reformular um curso ou criar um livro do zero

Este repositório é, ao mesmo tempo, a biblioteca de livros e o kit que a produz. Com ele, qualquer pessoa, num chat novo do Claude e sem precisar conhecer a história do projeto, pode:

- **reformular um curso:** transformar as anotações de um curso no Notion num material didático revisado (skill `revisar-curso-biblioteca`);
- **criar um livro do zero:** escrever um livro sobre um tema de tecnologia, com a ementa aprovada por você, e depois livros complementares na mesma trilha (skill `criar-livro-tecnologia`).

Nos dois casos, o resultado é publicado no GitHub e vira um EPUB.

## O que você precisa

- Uma conta do **Claude** com execução de código e a conexão com o **GitHub** (para clonar o repositório e publicar).
- O conector do **Notion** ligado e com acesso à página do curso.
- O **app do Claude no computador**, aberto e com a pasta **Downloads** liberada para o chat. É por ela que o Claude pega a exportação do Notion. Se não der, você pode anexar o `.zip` direto no chat.
- Para reformular: o curso no Notion organizado como **uma página índice** com uma subpágina por aula. Para criar: só uma página do Notion onde os livros vão ficar (o Claude pergunta).

## 1. Escolha a biblioteca

- **Usar esta biblioteca:** nada a fazer.
- **Criar a sua:** no GitHub, clique em **Use this template** → crie o seu repositório. Depois edite o [`biblioteca.yaml`](biblioteca.yaml) com o seu nome (vai na capa), o nome do seu repositório e o nome e e-mail dos commits (use o e-mail *noreply* do GitHub). Apague as pastas de curso de `programacao/` e deixe o catálogo do README e o [`ESTADO.md`](ESTADO.md) só com o cabeçalho. Apague também as pastas de `livros/` e o `progresso/`, e deixe `notion_livros` vazio. Os EPUBs e os zips das skills começam a ser gerados no primeiro push.

## 2. Instale as skills

1. Baixe os zips da release **skill**: [`revisar-curso-biblioteca.zip`](../../releases/download/skill/revisar-curso-biblioteca.zip) e [`criar-livro-tecnologia.zip`](../../releases/download/skill/criar-livro-tecnologia.zip). Instale só a que for usar, ou as duas.
2. No Claude, abra a tela de **Skills** e envie o zip.

Prefere não instalar? Abra o bloco **Skill completa** da skill desejada no [README](README.md#-kit-de-reformulação-e-criação-skills--arquivos-de-apoio), copie o conteúdo e cole na primeira mensagem do chat. Funciona igual: a skill busca sozinha os arquivos de apoio no repositório.

## Opcional: ler os PDFs do curso com o Docling

Se o curso tiver PDFs de aula ou de listas de exercícios, o Claude pode convertê-los para conferir os enunciados exatos e a ementa. Os PDFs não são publicados. Para isso:

1. Instale o `uv`, o programa que baixa e roda o Docling (confira antes com `uv --version`):
   - **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
   - **macOS ou Linux** (terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

   Depois feche e abra o terminal e rode `uv --version` de novo para confirmar.
2. Quando o Claude pedir, baixe os PDFs para a pasta Downloads e rode o comando que ele passar, algo como `uvx --from docling docling "lista-1.pdf" --to md --output .`.
3. Na primeira vez, o Docling baixa os modelos e demora alguns minutos.

Quer o Docling também como servidor MCP no app? A configuração que funciona e a solução para os erros comuns ("Connection closed", modo remoto, antivírus) estão no apoio **PDFs do curso com o Docling** do [README](README.md#-kit-de-reformulação-e-criação-skills--arquivos-de-apoio).

## 3. Comece um chat novo

**Para reformular um curso**, cole esta mensagem (troque o link):

```text
Quero reformular um curso com a skill revisar-curso-biblioteca.
Link do índice no Notion: https://www.notion.so/...
Repositório: Joshpcbrrj/biblioteca-de-estudos
```

**Para criar um livro do zero**:

```text
Quero criar um livro com a skill criar-livro-tecnologia.
Tema: Docker
Repositório: Joshpcbrrj/biblioteca-de-estudos
```

O Claude confere as conexões, lê o `biblioteca.yaml` e o `ESTADO.md` e começa a trabalhar. Um curso ou livro por chat deixa tudo mais leve e mais barato.

## 4. O que acontece ao reformular um curso

1. **Remodelação no Notion**, página por página. O chat principal coordena e dispara um agente novo para cada página, para não acumular contexto. Em cada página, o Claude:
   - corrige fatos e código;
   - completa o que falta no escopo do curso;
   - reescreve cada aula no padrão (analogias, revisão rápida, próximo passo, código comentado);
   - troca as imagens por diagramas no design system;
   - fecha cada seção com um cheat sheet.
2. **Parada para exportar.** O Claude para e pede a exportação. Na página índice do curso, no Notion:
   - clique em **•••** → **Exportar**;
   - formato **HTML**;
   - **Incluir subpáginas** ligado;
   - **Incluir conteúdo: tudo**;
   - salve o `.zip` na pasta Downloads e avise no chat.
3. **Publicação.** O Claude converte para Markdown, confere tudo, gera o EPUB, faz o commit e espera a GitHub Action. No fim você recebe o link do curso e do livro.

Se o chat ficar longo demais ou cair, abra outro e diga "continue o curso X": o andamento fica no `ESTADO.md` do repositório.

## 5. O que acontece ao criar um livro

1. **Perguntas rápidas** (no máximo 3): para quem é, nível e tamanho. Antes, o Claude olha os livros que já existem na mesma trilha.
2. **Ementa proposta:** capítulos, objetivo de cada um, pré-requisitos, projeto final, o que fica para livros futuros e a versão da ferramenta usada como referência.
3. **Você ajusta à vontade**, em linguagem normal: "aumenta", "diminui", "tira o capítulo 5", "adiciona volumes", "junta o 3 e o 4", "mais prático". A cada pedido, a ementa volta inteira e atualizada. **Nada é escrito antes de você dizer "aprovado".**
4. **Escrita no Notion**, um capítulo por agente. Cada capítulo tem:
   - o padrão de aula;
   - um laboratório com os comandos executados de verdade;
   - exercícios com a resolução recolhida;
   - as fontes oficiais com a data em que foram conferidas.
5. **Parada para exportar e publicação**, como na reformulação. O livro vai para `livros/<slug>/`, com o aviso "criado com IA a partir de fontes públicas".
6. **Próximo livro da trilha:** no fim, o Claude sugere o livro complementar (ex.: *Docker do zero* → *Docker Compose* → *Docker em produção*). O livro novo começa de onde o anterior parou e aponta para ele em vez de repetir o conteúdo. O mapa das trilhas fica em [`livros/`](livros/).

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| O zip tem poucos KB ou só uma página | A exportação foi feita a partir de uma aula. Exporte de novo, a partir da **página índice**. |
| O Claude não acha a pasta Downloads | Abra o app do Claude no computador e libere a pasta para o chat, ou anexe o zip. |
| O Claude não consegue publicar no GitHub | Confira se o repositório está conectado com permissão de escrita. |
| A Action "Kit das skills" falhou | Alguém editou uma skill sem atualizar o README: rode `python3 ferramentas/montar_kit.py` e faça commit. |
| O servidor Docling mostra "Connection closed" | Veja a tabela de problemas no apoio **PDFs do curso com o Docling** (normalmente falta `--with "mcp<2"`). |
| Uma imagem não aparece no Notion | O upload expirou (vale ~1 h). Peça para o Claude refazer a página. |

## Para mexer no kit

- As skills ficam em [`skill/`](skill/): uma pasta por skill e os arquivos comuns às duas em [`skill/_comum/`](skill/_comum/). Os scripts ficam em [`ferramentas/`](ferramentas/).
- Depois de editar a skill, rode `python3 ferramentas/montar_kit.py`. Ele atualiza o README, e a Action publica o zip novo.
- Antes de commitar, rode `python3 testes/rodar.py`. Ele confere que o curso de exemplo continua passando no critério de pronto, que o curso quebrado é recusado, que todo caminho citado na skill existe e que o README está em dia. A Action "Testes do kit" roda o mesmo a cada push.
- O critério de pronto de um curso de verdade é `python3 -I ferramentas/auditar_curso.py <area>/<slug> --criterios`: sem erros, e os avisos registrados no `ESTADO.md`.
- Os scripts leem a configuração do `biblioteca.yaml` (`ferramentas/config.py`).
