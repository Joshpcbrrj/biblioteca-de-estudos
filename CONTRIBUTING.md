# Contributing

**English** | [Português](CONTRIBUTING.pt-BR.md)

Thank you for helping. This project is made for people who study on their own, and every fix makes the books better for the next reader.

## Contents

- [I found an error in a book](#i-found-an-error-in-a-book)
- [I want to suggest a topic](#i-want-to-suggest-a-topic)
- [I want to change the skill or the scripts](#i-want-to-change-the-skill-or-the-scripts)
- [Tests](#tests)
- [Translations](#translations)
- [General rules](#general-rules)

## I found an error in a book

Open an issue with the **Report an error** form. Give the book, the chapter, the passage and what is wrong. If you know the fix, include it, with a source when it is a fact.

## I want to suggest a topic

Open an issue with the **Suggest a topic** form. Tell us what you want to learn and why.

## I want to change the skill or the scripts

1. Open an issue first, describing the change, so we can agree on the approach.
2. Fork the repository and create a branch with a short name (e.g. `fix-audit-tables`).
3. Follow the project style: the skill and code in English, short sentences, one term per concept.
4. Run the checks before sending (see [Tests](#tests)). The "Kit tests" Action runs the same on every pull request, on Windows and Linux.
5. Open the pull request and fill in the checklist that appears.

Design decisions are recorded in `docs/decisions/`. If your change goes against one of them, explain why in the pull request.

## Tests

```bash
pip install -r requirements-dev.txt
ruff check .              # lint
pytest --cov              # all tests, with coverage (must stay at 95% or more)
pytest tests/test_build.py   # only one part
pytest -m "not slow"      # skip the tests that build a real EPUB or website
```

There is one test file per part of the kit:

| File | Tests |
| --- | --- |
| `test_common.py` | shared helpers, and the contract that every style file has every label the scripts use |
| `test_book.py` | each `book.yaml` validation rule, the chapter brief and skeleton, progress and status |
| `test_audit.py` | each audit check, per chapter and for the whole book, in both reading profiles |
| `test_facts.py` | which sentences need a fact check |
| `test_build.py` | the EPUB, navigation, map, zips, library lists and the website (built with Zensical) |
| `test_tools.py` | the translation checker and the skill packager |
| `test_repo.py` | the skill's structure, the documentation and the library skeleton |

**Adding a rule to a script?** Add one test case for it: most files have a table of cases (`ERRORS`, `WARNINGS`) where a new rule is one more line. The sample book in `tests/fixtures/sample-book/` passes every check; tests copy it and break one thing at a time.

## Translations

The documentation is written in English, with a Portuguese version next to each page (`page.md` and `page.pt-BR.md`). When you change an English page, update the Portuguese one too, then run `python tools/translation.py stamp <page>.pt-BR.md` to record which English version it translates. If you cannot translate it, say so in the pull request: the tests will flag the page as outdated until someone does.

## General rules

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Do not submit passages copied from books, courses or third-party documentation, beyond short quotations with their source.
- Do not submit personal data (yours or anyone else's) in issues, commits or files.
- By contributing, you agree that content is licensed under [CC BY-SA 4.0](LICENSE) and code under [MIT](LICENSE-CODIGO).
