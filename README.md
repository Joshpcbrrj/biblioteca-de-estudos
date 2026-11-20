# 📚 Syllabook

**English** | [Português](README.pt-BR.md)

**Turn any topic or study material into a book you can actually learn from.**

Syllabook is a Claude skill for self-learners. It writes course-books on any topic and improves the study materials you already have. Everything it produces is yours: Markdown in your GitHub repository, an EPUB for any e-reader, a searchable website and, if you want, a copy in Notion.

> 🚧 **Being rebuilt.** The skill is being rewritten from scratch. The roadmap and decisions are in [`plano/PLANO.md`](plano/PLANO.md) (in Portuguese). There is no version to install yet.

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

This repository is a **template**: click **Use this template** to get the skill and the empty folders, and keep your own books in your own GitHub account.

## Contributing

Found an error or want to suggest a topic? Open an [issue](../../issues/new/choose). To contribute to the skill, see [CONTRIBUTING.md](CONTRIBUTING.md). This project follows a [Code of Conduct](CODE_OF_CONDUCT.md).

## License

- Content (books and documentation): [CC BY-SA 4.0](LICENSE).
- Code (skill and scripts): [MIT](LICENSE-CODIGO).
