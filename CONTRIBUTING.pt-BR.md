<!-- translation-of: CONTRIBUTING.md sha256:2b659b064c9f -->
# Como contribuir

[English](CONTRIBUTING.md) | **Português**

Obrigado por querer ajudar. Este projeto é feito para quem estuda sozinho, e toda correção deixa os livros melhores para a próxima pessoa.

## Conteúdo

- [Achei um erro num livro](#achei-um-erro-num-livro)
- [Quero sugerir um tema](#quero-sugerir-um-tema)
- [Quero mudar a skill ou os scripts](#quero-mudar-a-skill-ou-os-scripts)
- [Testes](#testes)
- [Traduções](#traduções)
- [Versões](#versões)
- [Regras gerais](#regras-gerais)

## Achei um erro num livro

Abra uma issue com o formulário **Report an error (Reportar erro)**. Diga o livro, o capítulo, o trecho e o que está errado. Se souber a correção, mande junto, com a fonte quando for um fato.

## Quero sugerir um tema

Abra uma issue com o formulário **Suggest a topic (Sugerir tema)**. Conte o que você quer aprender e para quê.

## Quero mudar a skill ou os scripts

1. Abra uma issue antes, explicando a mudança, para combinarmos o caminho.
2. Faça um fork e uma branch com nome curto (ex.: `fix-audit-tables`).
3. Siga o padrão do projeto: a skill e o código em inglês, frases curtas, um termo por conceito.
4. Rode as verificações antes de enviar (veja [Testes](#testes)). A Action "Kit tests" roda o mesmo em todo pull request, no Windows e no Linux.
5. Abra o pull request preenchendo o roteiro que aparece.

As decisões de projeto ficam registradas em [`plano/PLANO.md`](plano/PLANO.md) até irem para `docs/`. Se a sua mudança contraria uma delas, explique por quê no pull request.

## Testes

```bash
pip install -r requirements-dev.txt
ruff check .              # verificação de estilo do código
pytest --cov              # todos os testes, com cobertura (precisa ficar em 95% ou mais)
pytest tests/test_build.py   # só uma parte
pytest -m "not slow"      # pula os testes que geram um EPUB ou um site de verdade
```

Há um arquivo de teste para cada parte do kit. [Como os testes funcionam](docs/testing.pt-BR.md) explica cada arquivo, as fixtures compartilhadas, o que os testes não cobrem e como acrescentar um teste.

O `ruff check .` tem um parceiro para os workflows do GitHub: `actionlint .github/workflows/*.yml skills/syllabook/assets/library/.github/workflows/*.yml`. A release e a publicação no GitHub Pages de verdade rodam na biblioteca pública de demonstração, [syllabook-demo](https://github.com/Joshpcbrrj/syllabook-demo).

**Avaliações de comportamento:** além desses testes, a pasta [`evals/`](evals/README.md) tem casos para o `claude plugin eval`, que conferem o que a skill faz numa conversa de verdade. Eles rodam na sua própria conta do Claude, nunca no CI.

**Vai acrescentar uma regra a um script?** Acrescente um caso de teste para ela: a maioria dos arquivos tem uma tabela de casos (`ERRORS`, `WARNINGS`) em que uma regra nova é uma linha a mais. O livro de exemplo em `tests/fixtures/sample-book/` passa em todas as checagens; os testes o copiam e quebram uma coisa de cada vez.

## Traduções

A documentação é escrita em inglês, com a versão em português ao lado de cada página (`pagina.md` e `pagina.pt-BR.md`). Quando mudar uma página em inglês, atualize também a em português e rode `python tools/translation.py stamp <pagina>.pt-BR.md` para registrar de qual versão em inglês ela é a tradução. Se não puder traduzir, diga no pull request: os testes vão apontar a página como desatualizada até alguém traduzir.

## Versões

1. Passe as notas de `[Unreleased]` do `CHANGELOG.md` para uma versão nova e ponha a mesma versão no `.claude-plugin/plugin.json`.
2. Envie para a `main` e espere os testes; depois crie a tag (`git tag vX.Y.Z && git push origin vX.Y.Z`). A Action "Skill release" publica o `syllabook.zip`.
3. Se `skills/syllabook/assets/library/` mudou, atualize o [modelo de biblioteca](https://github.com/Joshpcbrrj/syllabook-library): clone-o, rode `python tools/sync_template.py <clone>` e depois faça o commit e envie o clone.

## Regras gerais

- Respeite o [Código de Conduta](CODE_OF_CONDUCT.pt-BR.md).
- Não envie trechos copiados de livros, cursos ou documentação de terceiros, além de citações curtas com a fonte.
- Não envie dados pessoais (seus ou de outras pessoas) em issues, commits ou arquivos.
- Ao contribuir, você concorda que o conteúdo é licenciado sob [CC BY-SA 4.0](LICENSE) e o código sob [MIT](LICENSE-CODIGO).
