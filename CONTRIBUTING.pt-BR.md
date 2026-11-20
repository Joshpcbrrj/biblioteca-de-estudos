<!-- translation-of: CONTRIBUTING.md sha256:e8d97fff5053 -->
# Como contribuir

[English](CONTRIBUTING.md) | **Português**

Obrigado por querer ajudar. Este projeto é feito para quem estuda sozinho, e toda correção deixa os livros melhores para a próxima pessoa.

## Conteúdo

- [Achei um erro num livro](#achei-um-erro-num-livro)
- [Quero sugerir um tema](#quero-sugerir-um-tema)
- [Quero mudar a skill ou os scripts](#quero-mudar-a-skill-ou-os-scripts)
- [Regras gerais](#regras-gerais)

## Achei um erro num livro

Abra uma issue com o formulário **Report an error (Reportar erro)**. Diga o livro, o capítulo, o trecho e o que está errado. Se souber a correção, mande junto, com a fonte quando for um fato.

## Quero sugerir um tema

Abra uma issue com o formulário **Suggest a topic (Sugerir tema)**. Conte o que você quer aprender e para quê.

## Quero mudar a skill ou os scripts

1. Abra uma issue antes, explicando a mudança, para combinarmos o caminho.
2. Faça um fork e uma branch com nome curto (ex.: `fix-audit-tables`).
3. Siga o padrão do projeto: a skill e o código em inglês, frases curtas, um termo por conceito.
4. Rode os testes do kit antes de enviar: `pip install pyyaml` e depois `python tests/run.py`. A Action "Kit tests" roda o mesmo em todo pull request.
5. Abra o pull request preenchendo o roteiro que aparece.

As decisões de projeto ficam registradas em `docs/decisions/`. Se a sua mudança contraria uma delas, explique por quê no pull request.

## Traduções

A documentação é escrita em inglês, com a versão em português ao lado de cada página (`pagina.md` e `pagina.pt-BR.md`). Quando mudar uma página em inglês, atualize também a em português e rode `python tools/translation.py stamp <pagina>.pt-BR.md` para registrar de qual versão em inglês ela é a tradução. Se não puder traduzir, diga no pull request: os testes vão apontar a página como desatualizada até alguém traduzir.

## Regras gerais

- Respeite o [Código de Conduta](CODE_OF_CONDUCT.pt-BR.md).
- Não envie trechos copiados de livros, cursos ou documentação de terceiros, além de citações curtas com a fonte.
- Não envie dados pessoais (seus ou de outras pessoas) em issues, commits ou arquivos.
- Ao contribuir, você concorda que o conteúdo é licenciado sob [CC BY-SA 4.0](LICENSE) e o código sob [MIT](LICENSE-CODIGO).
