<!-- translation-of: README.md sha256:16f9ce594175 -->
# <img src="docs/img/syllabook-icon.svg" alt="" height="40"> Syllabook

[English](README.md) | **Português**

![Syllabook: um livro aberto cujas páginas mostram a estrutura de um curso, com módulos, capítulos e gráficos](docs/img/syllabook-banner.pt-BR.jpg)

**Transforme qualquer tema ou material de estudo num livro com que dá para aprender de verdade.**

![Primeira mensagem do Syllabook no Claude Code: ele confirma o idioma e oferece criar um livro, aprimorar um material de estudo, traduzir um livro, publicar um ou continuar um em andamento](docs/img/syllabook-start.pt-BR.svg)

Syllabook é uma skill do Claude para quem estuda sozinho. Ela cria livros-curso sobre qualquer tema e aprimora os materiais de estudo que você já tem. Tudo o que ela produz é seu: Markdown no seu repositório do GitHub, EPUB para qualquer leitor digital, um site com busca e, se você quiser, uma cópia no Notion.

> 🧪 **Versão inicial (0.x).** Funciona de ponta a ponta e vai melhorando em versões pequenas até a 1.0. O roteiro e as decisões estão em [`plano/PLANO.md`](plano/PLANO.md); as mudanças, no [CHANGELOG](CHANGELOG.md) (em inglês).

## Instalar

- **App do Claude (claude.ai, desktop):** baixe o `syllabook.zip` da [versão mais recente](https://github.com/Joshpcbrrj/syllabook/releases/latest) e envie na seção de Skills das configurações do Claude.
- **Claude Code:** `claude plugin marketplace add Joshpcbrrj/syllabook` e depois `claude plugin install syllabook@syllabook`.
- **No Windows, use também o WSL 2** ([guia de instalação](docs/integrations/wsl.pt-BR.md)): com o Claude Code rodando dentro do Ubuntu, a skill testa cada comando de Linux e cada exemplo de código e põe a saída real no livro.

🔌 **Integrações** (nenhuma é obrigatória; cada uma tem um guia de instalação passo a passo):

- **[GitHub](docs/integrations/github.pt-BR.md)**, conector do Claude: guarda os livros no seu repositório, salva o progresso e publica.
- **[Notion](docs/integrations/notion.pt-BR.md)**, conector do Claude: lê um material seu para aprimorar e cria uma cópia do livro para você anotar.
- **[Google Drive](docs/integrations/google-drive.pt-BR.md)**, conector do Claude: busca documentos e arquivos seus para usar como fonte.
- **[Docling](docs/integrations/docling.pt-BR.md)**: converte PDF, DOCX, PPTX e outros documentos em texto, mantendo tabelas e estrutura.
- **[WSL 2](docs/integrations/wsl.pt-BR.md)**: um Linux de verdade no Windows, para a skill testar os comandos e o código dos livros.

Todas, mais o GitHub Pages (site com busca), estão na [página de integrações](docs/integrations/README.pt-BR.md).

👀 **Veja funcionando:** a [biblioteca de demonstração](https://github.com/Joshpcbrrj/syllabook-demo) e o [site com busca](https://joshpcbrrj.github.io/syllabook-demo/) dela, gerados pelos mesmos workflows que toda biblioteca recebe.

## O que ela faz

- **Cria um livro a partir de um tema.** Você diz o que quer aprender. Ela pesquisa, apresenta um parecer e uma ementa, e você ajusta até aprovar. Depois ela escreve o livro inteiro, do básico ao intermediário.
- **Aprimora um material seu.** Notion, PDF, EPUB, DOCX, Google Drive, texto ou link. Ela mantém a proposta do original, corrige, completa o que falta e reescreve para facilitar o estudo, a revisão e a pesquisa.
- **Traduz um livro** para outro idioma, adaptando exemplos e termos para os novos leitores.
- **Funciona para áreas diferentes:** programação e matemática, idiomas, habilidades práticas (música, eletrônica...) e conhecimento geral (como a história da computação).
- **Fala o seu idioma:** ela deduz ou pergunta o idioma da conversa e o do livro.

Cada livro traz mapa com links, teste de nivelamento, exercícios com gabarito comentado, revisões espaçadas, simulado final e glossário.

## Como o repositório está organizado

| Pasta | O que tem |
| --- | --- |
| [`created-books/`](created-books/README.pt-BR.md) | Livros feitos a partir de uma ementa |
| [`improved-materials/`](improved-materials/README.pt-BR.md) | Materiais de estudo aprimorados |
| [`site/`](site/README.pt-BR.md) | Fonte do site com busca (GitHub Pages) que mostra todos os livros |
| [`docs/`](docs/README.pt-BR.md) | Documentação: como usar, integrações (GitHub, Notion, Google Drive, Docling, WSL 2), referência |
| [`plano/`](plano/) | Plano da reformulação (temporário) |

**A sua própria biblioteca:** cada pessoa guarda os livros num repositório só seu. Crie o seu a partir do [modelo de biblioteca](https://github.com/Joshpcbrrj/syllabook-library) (**Use this template → Create a new repository**, público) ou comece com um repositório vazio e deixe o Syllabook prepará-lo no primeiro livro. Este repositório guarda a skill e os arquivos de desenvolvimento dela, não livros.

## Apoie o Syllabook

O Syllabook é gratuito e aberto. Se ele ajuda você a aprender, você pode apoiar o desenvolvimento:

| Pix (chave aleatória) | Bitcoin (BlueWallet) | Outras criptomoedas (HiddenSwap) |
| :---: | :---: | :---: |
| <a href="https://nubank.com.br/cobrar/1i7whc/6b00f69e-18fc-4ede-8251-9aa5ab30882a"><img src="docs/img/donate-pix.png" alt="QR code do Pix" width="180"></a> | <img src="docs/img/donate-bitcoin.png" alt="QR code de Bitcoin" width="180"> | <a href="https://hiddenswap.com/pay/U5SUjiUR"><img src="docs/img/donate-hiddenswap.png" alt="QR code do HiddenSwap" width="180"></a> |
| [Pagar com Pix](https://nubank.com.br/cobrar/1i7whc/6b00f69e-18fc-4ede-8251-9aa5ab30882a) | `bc1qpavyz63u90f5y8mawj0lydn55hr3f9l9kum7mq` | [Pagar pelo HiddenSwap](https://hiddenswap.com/pay/U5SUjiUR) |

## Contribuir

Achou um erro ou quer sugerir um tema? Abra uma [issue](../../issues/new/choose). Para contribuir com a skill, veja o [CONTRIBUTING.pt-BR.md](CONTRIBUTING.pt-BR.md). Este projeto segue um [Código de Conduta](CODE_OF_CONDUCT.pt-BR.md).

## Licença

- Conteúdo (livros e documentação): [CC BY-SA 4.0](LICENSE).
- Código (skill e scripts): [MIT](LICENSE-CODIGO).
