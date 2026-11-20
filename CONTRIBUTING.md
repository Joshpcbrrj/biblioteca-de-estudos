# Contributing

**English** | [Português](CONTRIBUTING.pt-BR.md)

Thank you for helping. This project is made for people who study on their own, and every fix makes the books better for the next reader.

## Contents

- [I found an error in a book](#i-found-an-error-in-a-book)
- [I want to suggest a topic](#i-want-to-suggest-a-topic)
- [I want to change the skill or the scripts](#i-want-to-change-the-skill-or-the-scripts)
- [General rules](#general-rules)

## I found an error in a book

Open an issue with the **Report an error** form. Give the book, the chapter, the passage and what is wrong. If you know the fix, include it, with a source when it is a fact.

## I want to suggest a topic

Open an issue with the **Suggest a topic** form. Tell us what you want to learn and why.

## I want to change the skill or the scripts

1. Open an issue first, describing the change, so we can agree on the approach.
2. Fork the repository and create a branch with a short name (e.g. `fix-audit-tables`).
3. Follow the project style: the skill and code in English, short sentences, one term per concept.
4. Run the kit tests before sending: `pip install pyyaml`, then `python tests/run.py`. The "Kit tests" Action runs the same on every pull request.
5. Open the pull request and fill in the checklist that appears.

Design decisions are recorded in `docs/decisions/`. If your change goes against one of them, explain why in the pull request.

## Translations

The documentation is written in English, with a Portuguese version next to each page (`page.md` and `page.pt-BR.md`). When you change an English page, update the Portuguese one too, then run `python tools/translation.py stamp <page>.pt-BR.md` to record which English version it translates. If you cannot translate it, say so in the pull request: the tests will flag the page as outdated until someone does.

## General rules

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Do not submit passages copied from books, courses or third-party documentation, beyond short quotations with their source.
- Do not submit personal data (yours or anyone else's) in issues, commits or files.
- By contributing, you agree that content is licensed under [CC BY-SA 4.0](LICENSE) and code under [MIT](LICENSE-CODIGO).
