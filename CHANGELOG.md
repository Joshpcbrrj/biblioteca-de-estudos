# Changelog

All notable changes to the skill are recorded here. This file is kept in English only.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Rebuild plan in `plano/` (in Portuguese), with the pilot evaluations and a draft of the new skill.
- New repository layout: `created-books/`, `improved-materials/`, `site/` and `docs/`.
- Community files: licenses (CC BY-SA 4.0 and MIT), code of conduct, contributing guide, security policy, issue and pull request templates.
- Documentation in English, with a Portuguese version of each page and a language switcher at the top.
- Docling installation guide in `docs/integrations/docling.md`.
- The new skill in `skills/syllabook/`: `SKILL.md`, the modes (Create, Improve, Translate, Publish), the references (teaching, book parts, sources, syllabus, visuals, examples, cover), the area profiles, the style guides (pt-BR, en) and the library skeleton. The scripts arrive in a later step.
- Kit tests (`tests/run.py`) and the "Kit tests" Action; translation checker (`tools/translation.py`); skill packager (`tools/package_skill.py`) and the "Skill release" Action, triggered by version tags.
- `.gitattributes`, so text files use LF line endings on every system.
- First scripts of the skill: `book.py` (validate `book.yaml` and the concept graph, chapter skeleton and brief, progress, status), `audit.py` (ready criteria per chapter and for the whole book) and `facts.py` (sentences to fact-check), with a sample book in `tests/fixtures/` and tests for each script.
- `build.py`: navigation between chapters, the book map, the concept index, the EPUB with answers moved to an appendix (links both ways), the zip in the repository layout (split above 100 files), a partial checkpoint zip, the library lists and the website source.
- The website is built with [Zensical](https://zensical.org/), the successor of Material for MkDocs: one search across every book, answers as collapsible blocks, code copy button and dark mode.
- Test suite rebuilt with pytest: one file per part of the kit, one case per validation and audit rule, branch coverage measured and required (95% or more), lint with Ruff, and CI on Windows and Linux with Python 3.10 and 3.12. Replaces `tests/run.py`.
- `diagram.py`: SVG diagrams from short YAML specs in the books' theme (flow, timeline, compare, boxes, layers, tree, sequence, bars, cards), sized by the reading profile, with fit checks and a contact sheet rendered to PNG.
- `projects.py`: projects assembled from the book's code blocks, evolved across chapters, run and checked against an expected output; paths that leave the project folder are refused.
- `ingest.py`: study materials (Markdown, folders of pages, HTML, web addresses, EPUB, DOCX, PDF, slides) converted to Markdown sections plus an outline, through Docling when available.
- Plugin layout: the skill moved to `skills/syllabook/`, and `.claude-plugin/plugin.json` and `marketplace.json` make this repository a Claude Code plugin and marketplace (needed for `claude plugin eval`).
- Workflow checks: actionlint in CI, and `tests/test_workflows.py`, which runs the real steps of `epub.yml` and `site.yml` in a test library with fake `gh` and `pip`.
- Library workflows `epub.yml` and `site.yml` (in `assets/library/` and at the root of this template); they do nothing while there are no books.

### Changed

- The project is now called **Syllabook** (repository `syllabook`), and it is a GitHub template.
- `biblioteca.yaml` became `library.yaml`, with keys in English.

### Removed

- The old skills `revisar-curso-biblioteca` and `criar-livro-tecnologia`, the scripts in `ferramentas/` and the tests, to be replaced by the new skill.
- The courses and books published with the old skills (they will be rebuilt with the new one), and the `epubs` and `skill` releases.
