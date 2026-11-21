# Contributing

**English** | [Português](CONTRIBUTING.pt-BR.md)

Thank you for helping. This project is made for people who study on their own, and every fix makes the books better for the next reader.

## Contents

- [I found an error in a book](#i-found-an-error-in-a-book)
- [I want to suggest a topic](#i-want-to-suggest-a-topic)
- [I want to change the skill or the scripts](#i-want-to-change-the-skill-or-the-scripts)
- [Tests](#tests)
- [Translations](#translations)
- [Releases](#releases)
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

Design decisions are recorded in [`plano/PLANO.md`](plano/PLANO.md) (in Portuguese) until they move to `docs/`. If your change goes against one of them, explain why in the pull request.

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
| `test_diagram.py` | each diagram type in both reading profiles, each fit problem, the contact sheet |
| `test_projects.py` | projects assembled from code blocks, evolved across chapters, run and checked; unsafe paths refused |
| `test_ingest.py` | each input type (Markdown, folder, HTML, web address, EPUB, DOCX, PDF), Docling and its fallbacks |
| `test_notion.py` | the conversion to Notion's format (toggles, callouts, uploads), the index page |
| `test_install.py` | the Docling installers (shellcheck, PowerShell syntax) and the helper that edits the Claude app's settings |
| `test_images.py` | free-license photos from Wikimedia Commons, the credits file and the application screenshots |
| `test_icons.py`, `test_build_icons.py` | the embedded Lucide icons and the tool that picks them |
| `test_tools.py` | the translation checker and the skill packager |
| `test_sync_template.py` | the library template mirrors the skill's library skeleton |
| `test_repo.py` | the skill's structure, the documentation and the library skeleton |
| `test_workflows.py` | the library workflows (`epub.yml`, `site.yml`) run step by step, with fake `gh` and `pip` (Linux only) |

`ruff check .` also has a partner for the GitHub workflows: `actionlint .github/workflows/*.yml skills/syllabook/assets/library/.github/workflows/*.yml`. The real release and GitHub Pages deploy run in the public demo library, [syllabook-demo](https://github.com/Joshpcbrrj/syllabook-demo).

**Behavior evals:** besides these tests, [`evals/`](evals/README.md) has cases for `claude plugin eval`, which check what the skill does in a real conversation. They run on your own Claude account, never in CI.

**Adding a rule to a script?** Add one test case for it: most files have a table of cases (`ERRORS`, `WARNINGS`) where a new rule is one more line. The sample book in `tests/fixtures/sample-book/` passes every check; tests copy it and break one thing at a time.

## Translations

The documentation is written in English, with a Portuguese version next to each page (`page.md` and `page.pt-BR.md`). When you change an English page, update the Portuguese one too, then run `python tools/translation.py stamp <page>.pt-BR.md` to record which English version it translates. If you cannot translate it, say so in the pull request: the tests will flag the page as outdated until someone does.

## Releases

1. Move the `[Unreleased]` notes in `CHANGELOG.md` to a new version, and set the same version in `.claude-plugin/plugin.json`.
2. Push to `main` and wait for the tests; then tag it (`git tag vX.Y.Z && git push origin vX.Y.Z`). The "Skill release" Action publishes `syllabook.zip`.
3. If `skills/syllabook/assets/library/` changed, update the [library template](https://github.com/Joshpcbrrj/syllabook-library): clone it, run `python tools/sync_template.py <clone>`, then commit and push the clone.

## General rules

- Follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- Do not submit passages copied from books, courses or third-party documentation, beyond short quotations with their source.
- Do not submit personal data (yours or anyone else's) in issues, commits or files.
- By contributing, you agree that content is licensed under [CC BY-SA 4.0](LICENSE) and code under [MIT](LICENSE-CODIGO).
