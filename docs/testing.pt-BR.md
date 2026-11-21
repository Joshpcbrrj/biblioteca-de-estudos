<!-- translation-of: testing.md sha256:bd8044bad280 -->
# Como os testes funcionam

[English](testing.md) | **Português**

Esta página é para quem quer mudar a skill ou os scripts dela. Ela explica o que é testado, como, e como acrescentar um teste para uma mudança.

## Conteúdo

- [As camadas](#as-camadas)
- [Rodar os testes](#rodar-os-testes)
- [Como um teste é montado](#como-um-teste-é-montado)
- [O que cada arquivo de teste cobre](#o-que-cada-arquivo-de-teste-cobre)
- [Acrescentar um teste](#acrescentar-um-teste)
- [O que os testes não cobrem](#o-que-os-testes-não-cobrem)
- [Problemas comuns](#problemas-comuns)

## As camadas

A skill tem duas partes: as instruções que o Claude lê (`SKILL.md`, os modos e as referências) e os scripts em Python que o Claude executa (`skills/syllabook/scripts/`). Cada parte é conferida por uma camada diferente.

| Camada | O que confere | Onde roda |
| --- | --- | --- |
| **Lint** | estilo e erros do Python (`ruff`) e os arquivos de workflow do GitHub (`actionlint`) | no seu computador e no CI |
| **Testes dos scripts** | cada regra de cada script, com um livro de exemplo | no seu computador e no CI |
| **Testes do repositório** | a estrutura da skill, a documentação, as traduções e o esqueleto da biblioteca | no seu computador e no CI |
| **Testes dos workflows** | os passos reais dos workflows da biblioteca (`epub.yml`, `site.yml`), com `gh` e `pip` falsos | só no Linux e no macOS |
| **Avaliações de comportamento** | o que a skill faz numa conversa de verdade com o Claude | só no seu computador, na sua conta do Claude ([`evals/`](../evals/README.md)) |

As quatro primeiras são testes do `pytest`: 363 ao todo, com cobertura de ramos de cerca de 97%. O CI (a Action "Kit tests") roda todos a cada push e pull request, no Windows e no Linux, com Python 3.10 e 3.12, porque os usuários rodam os scripts em todos eles. Ele falha se a cobertura cair abaixo de 95%.

## Rodar os testes

Na raiz do repositório:

```bash
pip install -r requirements-dev.txt
ruff check .                 # lint
pytest --cov                 # todos os testes, com cobertura
pytest tests/test_audit.py   # um arquivo
pytest -k credit             # testes cujo nome contém "credit"
pytest -m "not slow"         # pula os testes que geram um EPUB ou um site de verdade
```

E o lint dos workflows, o mesmo comando que o CI usa:

```bash
actionlint .github/workflows/*.yml skills/syllabook/assets/library/.github/workflows/*.yml
```

Uma rodada completa leva uns 20 segundos. Seis testes são pulados quando falta uma ferramenta (pandoc, Zensical, shellcheck, PowerShell) ou no Windows (os testes dos workflows); o motivo aparece com `pytest -rs`.

## Como um teste é montado

Tudo o que é compartilhado fica em [`tests/conftest.py`](../tests/conftest.py):

- **Isolamento (automático):** cada teste roda numa pasta temporária própria, e o arquivo de estado da skill vai junto para lá. Nenhum teste mexe na sua pasta pessoal, no repositório ou nos arquivos de outro teste.
- **`book`:** uma cópia do livro de exemplo, [`tests/fixtures/sample-book/`](../tests/fixtures/sample-book/). Ele tem dois capítulos, as partes fixas, um diagrama e os dossiês de pesquisa, e passa em todas as checagens. O teste copia o livro, quebra uma coisa e confere se aparece o erro certo.
- **`library`:** uma biblioteca de usuário montada a partir do esqueleto em `skills/syllabook/assets/library/`, com o livro de exemplo dentro.
- **`cli`:** roda um script como o Claude roda, `cli('audit', '1', '--book', book)`, e devolve o código de saída e o JSON que o script imprimiu. Os scripts rodam no mesmo processo, então a cobertura os enxerga e uma falha mostra um traceback normal.
- **`edit(path, old, new)`:** troca um texto num arquivo e falha se o texto não estiver lá, para que um teste não passe sem ter mudado nada.

Um teste típico:

```python
def test_a_chapter_without_its_research_dossier_is_a_warning(cli, book):
    os.remove(book / 'research' / 'c01.md')
    code, r = cli('audit', 1, '--book', book)
    assert code == 0 and any('research/c01.md' in w for w in r['warnings'])
```

**Sem rede.** Os testes nunca chamam um serviço de verdade. Quando um script fala com a internet (o Wikimedia Commons no `images.py`, páginas da web no `ingest.py`) ou com um programa de fora (Docling, Playwright), o teste troca só essa função por uma falsa, que devolve uma resposta conhecida.

## O que cada arquivo de teste cobre

| Arquivo | Testa |
| --- | --- |
| `test_common.py` | as funções compartilhadas e o contrato de que todo arquivo de estilo tem todos os rótulos que os scripts usam |
| `test_book.py` | cada regra de validação do `book.yaml`, o resumo e o esqueleto do capítulo, o progresso e o status |
| `test_audit.py` | cada checagem da auditoria, por capítulo e no livro inteiro, nos dois perfis de leitura |
| `test_facts.py` | quais frases precisam de checagem de fatos |
| `test_build.py` | o EPUB, a navegação, o mapa, os zips, as listas da biblioteca e o site (gerado com o Zensical) |
| `test_diagram.py` | cada tipo de diagrama nos dois perfis de leitura, cada problema de encaixe, a folha de contatos |
| `test_icons.py`, `test_build_icons.py` | os ícones do Lucide embutidos e a ferramenta que os escolhe |
| `test_images.py` | as fotos com licença livre do Wikimedia Commons, o arquivo de créditos e as capturas da aplicação |
| `test_projects.py` | projetos montados a partir dos blocos de código, evoluídos entre capítulos, executados e conferidos; caminhos inseguros recusados |
| `test_ingest.py` | cada tipo de entrada (Markdown, pasta, HTML, endereço da web, EPUB, DOCX, PDF), o Docling e as alternativas a ele |
| `test_notion.py` | a conversão para o formato do Notion (toggles, callouts, uploads) e a página de índice |
| `test_install.py` | os instaladores do Docling (shellcheck, sintaxe do PowerShell) e o ajudante que edita as configurações do app do Claude |
| `test_tools.py` | o verificador de traduções e o empacotador da skill |
| `test_sync_template.py` | o modelo de biblioteca espelha o esqueleto da biblioteca da skill |
| `test_repo.py` | a estrutura da skill, a documentação (links, seletor de idioma) e o esqueleto da biblioteca |
| `test_workflows.py` | os workflows da biblioteca rodando passo a passo, com `gh` e `pip` falsos (só no Linux e no macOS) |

## Acrescentar um teste

1. **Escreva o teste primeiro** e veja-o falhar: assim você sabe que ele testa a coisa certa.
2. **Regra nova num script?** A maioria dos arquivos tem uma tabela de casos (por exemplo, `ERRORS` e `WARNINGS` no `test_audit.py`). Uma regra nova costuma ser uma linha a mais: o texto a trocar no livro de exemplo, o texto novo e a mensagem esperada.
3. **Script novo?** Crie `tests/test_<script>.py`, use a fixture `cli` e acrescente o arquivo à tabela acima.
4. **Mudou o livro de exemplo?** Ele precisa continuar passando em todas as checagens; senão, o `test_the_sample_book_is_ready` falha.
5. Rode `pytest --cov` antes de enviar: a cobertura precisa ficar em 95% ou mais.

## O que os testes não cobrem

- **O que o Claude escreve.** Os testes conferem os scripts, não a qualidade de um capítulo. Isso é trabalho das [avaliações de comportamento](../evals/README.md) e dos livros-piloto de verdade.
- **Serviços de verdade.** A publicação no GitHub, no Notion e no GitHub Pages, a release real e o deploy do Pages rodam na biblioteca pública de demonstração, a [syllabook-demo](https://github.com/Joshpcbrrj/syllabook-demo).
- **Um navegador de verdade.** O `images.py screenshot` é testado com um Playwright falso.

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| `ModuleNotFoundError` para `yaml`, `pypandoc` ou `zensical` | Instale as ferramentas de desenvolvimento: `pip install -r requirements-dev.txt` |
| `Required test coverage of 95% not reached` | Código novo sem teste. Rode `pytest --cov` e veja as linhas que faltam na lista |
| Um teste passa no seu computador e falha no CI do Windows | Caminhos ou quebras de linha. Use `os.path.join` e abra arquivos de texto com `encoding='utf-8'` |
| `test_every_documentation_page_has_the_language_switcher` ou um teste de tradução falha | Você mudou uma página em inglês: atualize a página `.pt-BR.md` e rode `python tools/translation.py stamp <página>.pt-BR.md` |
| Os testes dos workflows são sempre pulados | Eles precisam do bash e só rodam no Linux e no macOS (ou no WSL 2, veja o [guia do WSL](integrations/wsl.pt-BR.md)) |
