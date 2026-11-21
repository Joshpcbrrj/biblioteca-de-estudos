# <img src="docs/img/syllabook-icon.svg" alt="" height="40"> Syllabook

**English** | [Português](README.pt-BR.md)

![Syllabook: create your course on any topic. An open book whose pages show the course structure and the dynamic content structure](docs/img/syllabook-banner.jpg)

**Turn any topic or study material into a book you can actually learn from.**

![Syllabook's first message in Claude Code: it confirms the language and offers to create a book, improve a study material, translate a book, publish one or continue one in progress](docs/img/syllabook-start.svg)

Syllabook is a Claude skill for self-learners. It writes course-books on any topic and improves the study materials you already have. Everything it produces is yours: Markdown in your GitHub repository, an EPUB for any e-reader, a searchable website and, if you want, a copy in Notion.

> 🧪 **Early version (0.x).** It works end to end, and it keeps improving in small releases until 1.0. The roadmap and decisions are in [`plano/PLANO.md`](plano/PLANO.md) (in Portuguese); changes are in the [CHANGELOG](CHANGELOG.md).

## Install

- **Claude app (claude.ai, desktop):** download `syllabook.zip` from the [latest release](https://github.com/Joshpcbrrj/syllabook/releases/latest) and upload it in the Skills section of Claude's settings.
- **Claude Code:** `claude plugin marketplace add Joshpcbrrj/syllabook`, then `claude plugin install syllabook@syllabook`.

👀 **See it working:** the [demo library](https://github.com/Joshpcbrrj/syllabook-demo) and its [searchable website](https://joshpcbrrj.github.io/syllabook-demo/), built by the same workflows every library gets.

## What it does

- **Creates a book from a topic.** Tell it what you want to learn. It researches, shows a short assessment and a syllabus, and you adjust until you approve. Then it writes the whole book, from beginner to intermediate.
- **Improves your study material.** Notion, PDF, EPUB, DOCX, Google Drive, plain text or a link. It keeps the purpose of the original, fixes errors, fills gaps and rewrites it for study, review and research.
- **Translates a book** into another language, adapting examples and terms to the new readers.
- **Works across fields:** programming and math, languages, practical skills (music, electronics...) and general knowledge (such as the history of computing).
- **Speaks your language:** it detects or asks the language of the conversation and of the book.

Every book includes a map with links, a placement test, exercises with commented answers, spaced reviews, a final mock exam and a glossary.

## Repository layout

| Folder | Contents |
| --- | --- |
| [`created-books/`](created-books/) | Books written from a syllabus |
| [`improved-materials/`](improved-materials/) | Improved study materials |
| [`site/`](site/) | Source of the searchable website (GitHub Pages) that shows every book |
| [`docs/`](docs/) | Documentation: how to use, integrations (GitHub, Notion, Google Drive, Docling), reference |
| [`plano/`](plano/) | Rebuild plan (temporary, in Portuguese) |

**Your own library:** every user keeps their books in a repository of their own. Create yours from the [library template](https://github.com/Joshpcbrrj/syllabook-library) (**Use this template → Create a new repository**, public), or start with an empty repository and let Syllabook set it up on the first book. This repository holds the skill and its development files, not books.

## Support Syllabook

Syllabook is free and open. If it helps you learn, you can support its development:

| Bitcoin | Other cryptocurrencies |
| :---: | :---: |
| <img src="docs/img/donate-bitcoin.png" alt="Bitcoin QR code" width="180"> | <a href="https://hiddenswap.com/pay/U5SUjiUR"><img src="docs/img/donate-hiddenswap.png" alt="HiddenSwap QR code" width="180"></a> |
| `bc1qpavyz63u90f5y8mawj0lydn55hr3f9l9kum7mq` | [Pay with HiddenSwap](https://hiddenswap.com/pay/U5SUjiUR) |

## Contributing

Found an error or want to suggest a topic? Open an [issue](../../issues/new/choose). To contribute to the skill, see [CONTRIBUTING.md](CONTRIBUTING.md). This project follows a [Code of Conduct](CODE_OF_CONDUCT.md).

## License

- Content (books and documentation): [CC BY-SA 4.0](LICENSE).
- Code (skill and scripts): [MIT](LICENSE-CODIGO).
