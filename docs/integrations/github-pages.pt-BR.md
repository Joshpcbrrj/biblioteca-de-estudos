<!-- translation-of: github-pages.md sha256:cf38f8b26d70 -->
# GitHub Pages: o site com todos os livros

[English](github-pages.md) | **Português**

## Para que serve

Um site com todos os seus livros: busca instantânea em todos eles, capítulos num menu lateral, código com botão de copiar, respostas que abrem ao clicar, modo escuro e link para cada EPUB. Ele funciona bem no computador, no celular e no navegador do leitor digital. Veja o [site de demonstração](https://joshpcbrrj.github.io/syllabook-demo/).

## O que você precisa

- O repositório da sua biblioteca no GitHub ([guia](github.pt-BR.md)), **público**: o GitHub Pages é grátis para repositórios públicos; nos privados, exige um plano pago do GitHub.
- O workflow `.github/workflows/site.yml`, que o Syllabook acrescenta junto com a biblioteca.

## Passo a passo

1. No seu repositório em github.com: **Settings → Pages**.
2. Em **Build and deployment → Source**, escolha **GitHub Actions**. É só isso: não há mais nada para preencher.
3. Publique um livro (ou abra **Actions → Website → Run workflow**). O workflow monta o site com o [Zensical](https://zensical.org/) e o publica.

O seu endereço é `https://<seu-usuario>.github.io/<nome-do-repositorio>/`.

## Como conferir que funcionou

- **Actions → Website**: a última execução está verde, com duas etapas, *build* e *deploy*.
- **Settings → Pages** mostra "Your site is live at ..." com o endereço.
- Abra o endereço e busque uma palavra de um dos seus livros.

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| O endereço mostra uma página 404 | A primeira publicação ainda não rodou. Rode **Actions → Website → Run workflow** e espere terminar |
| A etapa *deploy* falha com erro do Pages | O Pages não está em **GitHub Actions** (passo 2), ou o repositório é privado num plano gratuito |
| O workflow do site roda, mas não publica nada | A biblioteca ainda não tem livros: o workflow espera o primeiro `book.yaml` |
| Um livro novo não aparece | O workflow só roda quando muda um livro, a pasta `site/` ou o `library.yaml`. Rode-o à mão em **Actions** |
