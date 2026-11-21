# How the tests work

**English** | [Português](testing.pt-BR.md)

This page is for anyone who wants to change the skill or its scripts. It explains what is tested, how, and how to add a test for a change.

## Contents

- [The layers](#the-layers)
- [Running the tests](#running-the-tests)
- [How a test is built](#how-a-test-is-built)
- [What each test file covers](#what-each-test-file-covers)
- [Adding a test](#adding-a-test)
- [What the tests do not cover](#what-the-tests-do-not-cover)
- [Common problems](#common-problems)

## The layers

The skill has two parts: instructions that Claude reads (`SKILL.md`, the modes and the references) and Python scripts that Claude runs (`skills/syllabook/scripts/`). Each part is checked by a different layer.

| Layer | What it checks | Where it runs |
| --- | --- | --- |
| **Lint** | Python style and errors (`ruff`), GitHub workflow files (`actionlint`) | your machine and CI |
| **Script tests** | every rule of every script, with a sample book | your machine and CI |
| **Repository tests** | the skill's structure, the documentation, translations, the library skeleton | your machine and CI |
| **Workflow tests** | the real steps of the library workflows (`epub.yml`, `site.yml`), with fake `gh` and `pip` | Linux and macOS only |
| **Behavior evals** | what the skill does in a real conversation with Claude | your machine only, on your Claude account ([`evals/`](../evals/README.md)) |

The first four are `pytest` tests: 363 of them, with branch coverage of about 97%. The CI ("Kit tests" Action) runs them on every push and pull request, on Windows and Linux, with Python 3.10 and 3.12, because users run the scripts on all of these. It fails if coverage drops below 95%.

## Running the tests

From the repository root:

```bash
pip install -r requirements-dev.txt
ruff check .                 # lint
pytest --cov                 # all tests, with coverage
pytest tests/test_audit.py   # one file
pytest -k credit             # tests whose name contains "credit"
pytest -m "not slow"         # skip the tests that build a real EPUB or website
```

And the workflow lint, the same command the CI uses:

```bash
actionlint .github/workflows/*.yml skills/syllabook/assets/library/.github/workflows/*.yml
```

A full run takes about 20 seconds. Six tests are skipped when a tool is missing (pandoc, Zensical, shellcheck, PowerShell) or on Windows (the workflow tests); the reason shows with `pytest -rs`.

## How a test is built

Everything shared lives in [`tests/conftest.py`](../tests/conftest.py):

- **Isolation (automatic):** each test runs in its own temporary folder, with the skill's state file moved there too. No test touches your home folder, the repository or another test's files.
- **`book`:** a copy of the sample book, [`tests/fixtures/sample-book/`](../tests/fixtures/sample-book/). It has two chapters, the fixed parts, one diagram and its research dossiers, and it passes every check. A test copies it, breaks one thing and checks that the right error appears.
- **`library`:** a user library made from the skeleton in `skills/syllabook/assets/library/`, with the sample book inside.
- **`cli`:** runs a script the way Claude does, `cli('audit', '1', '--book', book)`, and returns the exit code and the JSON the script printed. Scripts run in the same process, so coverage sees them and a failure shows a normal traceback.
- **`edit(path, old, new)`:** replaces text in a file and fails if the text is not there, so a test cannot pass by editing nothing.

A typical test:

```python
def test_a_chapter_without_its_research_dossier_is_a_warning(cli, book):
    os.remove(book / 'research' / 'c01.md')
    code, r = cli('audit', 1, '--book', book)
    assert code == 0 and any('research/c01.md' in w for w in r['warnings'])
```

**No network.** Tests never call a real service. Where a script talks to the internet (Wikimedia Commons in `images.py`, web pages in `ingest.py`) or to an outside program (Docling, Playwright), the test replaces that one function with a fake that returns a known answer.

## What each test file covers

| File | Tests |
| --- | --- |
| `test_common.py` | shared helpers, and the contract that every style file has every label the scripts use |
| `test_book.py` | each `book.yaml` validation rule, the chapter brief and skeleton, progress and status |
| `test_audit.py` | each audit check, per chapter and for the whole book, in both reading profiles |
| `test_facts.py` | which sentences need a fact check |
| `test_build.py` | the EPUB, navigation, map, zips, library lists and the website (built with Zensical) |
| `test_diagram.py` | each diagram type in both reading profiles, each fit problem, the contact sheet |
| `test_icons.py`, `test_build_icons.py` | the embedded Lucide icons and the tool that picks them |
| `test_images.py` | free-license photos from Wikimedia Commons, the credits file and the application screenshots |
| `test_projects.py` | projects assembled from code blocks, evolved across chapters, run and checked; unsafe paths refused |
| `test_ingest.py` | each input type (Markdown, folder, HTML, web address, EPUB, DOCX, PDF), Docling and its fallbacks |
| `test_notion.py` | the conversion to Notion's format (toggles, callouts, uploads), the index page |
| `test_install.py` | the Docling installers (shellcheck, PowerShell syntax) and the helper that edits the Claude app's settings |
| `test_tools.py` | the translation checker and the skill packager |
| `test_sync_template.py` | the library template mirrors the skill's library skeleton |
| `test_repo.py` | the skill's structure, the documentation (links, language switcher) and the library skeleton |
| `test_workflows.py` | the library workflows run step by step, with fake `gh` and `pip` (Linux and macOS only) |

## Adding a test

1. **Write the test first** and watch it fail, so you know it tests the right thing.
2. **New rule in a script?** Most files have a table of cases (`ERRORS`, `WARNINGS` in `test_audit.py`, for example). A new rule is usually one more line: the text to change in the sample book, the new text and the message expected.
3. **New script?** Create `tests/test_<script>.py`, use the `cli` fixture and add the file to the table above.
4. **Change in the sample book?** Keep it passing every check: `test_the_sample_book_is_ready` fails otherwise.
5. Run `pytest --cov` before sending: coverage must stay at 95% or more.

## What the tests do not cover

- **What Claude writes.** The tests check the scripts, not the quality of a chapter. That is the job of the [behavior evals](../evals/README.md) and of real pilot books.
- **Real services.** Publishing to GitHub, Notion and GitHub Pages, the real release and the Pages deploy run in the public demo library, [syllabook-demo](https://github.com/Joshpcbrrj/syllabook-demo).
- **A real browser.** `images.py screenshot` is tested with a fake Playwright.

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| `ModuleNotFoundError` for `yaml`, `pypandoc` or `zensical` | Install the development tools: `pip install -r requirements-dev.txt` |
| `Required test coverage of 95% not reached` | New code without tests. Run `pytest --cov` and look at the missing lines it lists |
| A test passes on your machine but fails in CI on Windows | Paths or line endings. Use `os.path.join` and open text files with `encoding='utf-8'` |
| `test_every_documentation_page_has_the_language_switcher` or a translation test fails | You changed an English page: update the `.pt-BR.md` page and run `python tools/translation.py stamp <page>.pt-BR.md` |
| The workflow tests are always skipped | They need bash and run only on Linux and macOS (or WSL 2, see the [WSL guide](integrations/wsl.md)) |
