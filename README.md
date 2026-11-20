# 📚 Criador de Estudos e Aprimorador de Materiais

Uma skill do Claude para **aprender sozinho**: ela cria livros-curso sobre qualquer tema e aprimora os materiais de estudo que você já tem. O resultado é seu: Markdown no seu GitHub, EPUB para ler em qualquer leitor, um site com busca e, se você quiser, uma cópia no Notion.

> 🚧 **Em reformulação.** A skill está sendo refeita do zero. O roteiro e as decisões estão em [`plano/PLANO.md`](plano/PLANO.md). Ainda não há versão para instalar.

## O que ela faz

- **Cria um livro a partir de um tema.** Você diz o que quer aprender; a skill pesquisa, apresenta um parecer e uma ementa, e você ajusta até aprovar. Depois ela escreve o livro inteiro, do básico ao intermediário.
- **Aprimora um material seu.** Notion, PDF, EPUB, DOCX, Google Drive, texto ou link. A skill mantém a proposta do original, corrige, completa o que falta e reescreve para facilitar o estudo, a revisão e a pesquisa.
- **Funciona para áreas diferentes:** programação e matemática, idiomas, habilidades práticas (música, eletrônica...) e temas de conhecimento geral (como a história da computação).

Cada livro traz mapa com links, teste de nivelamento, exercícios com gabarito comentado, revisões, simulado final e glossário.

## Como o repositório está organizado

| Pasta | O que tem |
| --- | --- |
| [`livros-criados/`](livros-criados/) | Livros feitos a partir de uma ementa |
| [`materiais-aprimorados/`](materiais-aprimorados/) | Materiais de estudo aprimorados |
| [`site/`](site/) | Fonte do site com busca (GitHub Pages) que mostra todos os livros |
| [`docs/`](docs/) | Documentação: como usar, complementos (GitHub, Notion, Google Drive, Docling), referência |
| [`plano/`](plano/) | Plano da reformulação (temporário) |

Este repositório é um **template**: quem usar "Use this template" recebe a skill e as pastas vazias, e guarda os próprios livros no próprio GitHub.

## Contribuir

Achou um erro ou quer sugerir um tema? Abra uma [issue](../../issues/new/choose). Para contribuir com a skill, veja o [CONTRIBUTING.md](CONTRIBUTING.md). Este projeto segue um [Código de Conduta](CODE_OF_CONDUCT.md).

## Licença

- Conteúdo (livros e documentação): [CC BY-SA 4.0](LICENSE).
- Código (skill e scripts): [MIT](LICENSE-CODIGO).
