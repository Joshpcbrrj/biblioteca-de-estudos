# Como usar: reformular um curso do zero

Este repositório é, ao mesmo tempo, a biblioteca de livros e o kit que a produz. Com ele, qualquer pessoa transforma anotações de um curso no Notion num material didático revisado, publica no GitHub e recebe um EPUB, num chat novo do Claude, sem precisar conhecer a história do projeto.

## O que você precisa

- Uma conta do **Claude** com execução de código e a conexão com o **GitHub** (para clonar o repositório e publicar).
- O conector do **Notion** ligado e com acesso à página do curso.
- O **app do Claude no computador**, aberto e com a pasta **Downloads** liberada para o chat. É por ela que o Claude pega a exportação do Notion. Se não der, você pode anexar o `.zip` direto no chat.
- O curso no Notion organizado assim: **uma página índice** com uma subpágina por aula.

## 1. Escolha a biblioteca

- **Usar esta biblioteca:** nada a fazer.
- **Criar a sua:** no GitHub, clique em **Use this template** → crie o seu repositório. Depois edite o [`biblioteca.yaml`](biblioteca.yaml) com o seu nome (vai na capa), o nome do seu repositório e o nome e e-mail dos commits (use o e-mail *noreply* do GitHub). Apague as pastas de curso de `programacao/` e deixe o catálogo do README e o [`ESTADO.md`](ESTADO.md) só com o cabeçalho. Os EPUBs e o zip da skill começam a ser gerados no primeiro push.

## 2. Instale a skill

1. Baixe o [`revisar-curso-biblioteca.zip`](../../releases/download/skill/revisar-curso-biblioteca.zip) (fica na release **skill**).
2. No Claude, abra a tela de **Skills** e envie o zip.

Prefere não instalar? Abra o bloco **Skill completa** no [README](README.md#-kit-de-reformulação-skill--arquivos-de-apoio), copie o conteúdo e cole na primeira mensagem do chat. Funciona igual: a skill busca sozinha os arquivos de apoio no repositório.

## 3. Comece um chat novo

Cole esta mensagem (troque o link):

```text
Quero reformular um curso com a skill revisar-curso-biblioteca.
Link do índice no Notion: https://www.notion.so/...
Repositório: Joshpcbrrj/biblioteca-de-estudos
```

O Claude confere as conexões, lê o `biblioteca.yaml` e o `ESTADO.md` e começa a trabalhar. Um curso por chat deixa tudo mais leve e mais barato.

## 4. O que acontece

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

## Problemas comuns

| Sintoma | O que fazer |
| --- | --- |
| O zip tem poucos KB ou só uma página | A exportação foi feita a partir de uma aula. Exporte de novo, a partir da **página índice**. |
| O Claude não acha a pasta Downloads | Abra o app do Claude no computador e libere a pasta para o chat, ou anexe o zip. |
| O Claude não consegue publicar no GitHub | Confira se o repositório está conectado com permissão de escrita. |
| A Action "Kit da skill" falhou | Alguém editou a skill sem atualizar o README: rode `python3 ferramentas/montar_kit.py` e faça commit. |
| Uma imagem não aparece no Notion | O upload expirou (vale ~1 h). Peça para o Claude refazer a página. |

## Para mexer no kit

- A skill e os arquivos de apoio ficam em [`skill/revisar-curso-biblioteca/`](skill/revisar-curso-biblioteca/); os scripts, em [`ferramentas/`](ferramentas/).
- Depois de editar a skill, rode `python3 ferramentas/montar_kit.py`. Ele atualiza o README, e a Action publica o zip novo.
- Antes de commitar, rode `python3 testes/rodar.py`. Ele confere que o curso de exemplo continua passando no critério de pronto, que o curso quebrado é recusado, que todo caminho citado na skill existe e que o README está em dia. A Action "Testes do kit" roda o mesmo a cada push.
- O critério de pronto de um curso de verdade é `python3 -I ferramentas/auditar_curso.py <area>/<slug> --criterios`: sem erros, e os avisos registrados no `ESTADO.md`.
- Os scripts leem a configuração do `biblioteca.yaml` (`ferramentas/config.py`).
