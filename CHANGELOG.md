# Changelog

All notable changes to the skill are recorded here. This file is kept in English only.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [0.2.0] - 2026-11-20

Colorful, explicit diagrams.

### Added

- 104 Lucide icons (ISC license) embedded in the skill (`assets/icons.json`), drawn by name with `icon:`; `diagram.py --icons` lists them, and a misspelled name is reported with suggestions.
- `icon` and `note` (a smaller line under the bold text) in flow, layers, tree, timeline, sequence and compare boxes; `side_note`, `side_icon` and `side_color` for a flow decision's other way out.
- `scene`: a short row of icons joined by arrows, `+` or `=` (folder → files, A + B = C), as its own diagram type or inside a cheat-sheet card.
- `subtitle` for every diagram.
- README: the Syllabook icon, a banner in each language and a picture of the skill's first message in Claude Code.

### Changed

- Stronger theme: colored box backgrounds, a gradient underline under the title, contrast of at least 4.5:1 checked by the tests.
- Cheat sheets: an icon badge per card, drawn check marks (or an icon per item) and an optional scene under the items.
- `compare` with `style: wrong-right` draws its marks as icons instead of emoji, which depended on the reader's fonts; no diagram contains emoji now.
- A YAML syntax error in a spec shows the file and line instead of a Python traceback.
- The sample book's chapter 1 diagram is drawn from a spec (`img/_source/c01-lista.yaml`).

## [0.1.0] - 2026-11-20

First release of the rebuilt skill.

### Added

- Install instructions in the README (Claude app and Claude Code).

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
- `notion.py`: chapters, chapter 0, the mock exam, the glossary and the index page converted to Notion's format (answers as toggles, notes as callouts, SVG diagrams and real photos as uploads, illustrations left out).
- Integration guides for GitHub, Notion, Google Drive and GitHub Pages, in English and Portuguese, with the compatibility table checked against current documentation.
- Docling installers for Windows (`install/install-docling.ps1`) and macOS/Linux (`install/install-docling.sh`), with a tested helper that adds Docling to the Claude app's settings and keeps a backup.
- Plugin layout: the skill moved to `skills/syllabook/`, and `.claude-plugin/plugin.json` and `marketplace.json` make this repository a Claude Code plugin and marketplace (needed for `claude plugin eval`).
- Workflow checks: actionlint in CI, and `tests/test_workflows.py`, which runs the real steps of `epub.yml` and `site.yml` in a test library with fake `gh` and `pip`.
- Library workflows `epub.yml` and `site.yml` (in `assets/library/` and at the root of this template); they do nothing while there are no books.

### Changed

- The project is now called **Syllabook** (repository `syllabook`), and it is a GitHub template.
- `biblioteca.yaml` became `library.yaml`, with keys in English.

### Fixed

- `notion.py`: the chapter list on the index page was read by Notion as a numbered list inside each bullet and renumbered from 1 (chapter 0 showed as "1."); the numbers are now escaped and blocks are separated by blank lines. Found by publishing the sample book to a real Notion page.
- `projects.py`: on Windows with Python 3.13 or later, a path such as `/etc/passwd.py` was no longer refused, because `os.path.isabs` returns `False` for a rooted path without a drive.

### Removed

- The old skills `revisar-curso-biblioteca` and `criar-livro-tecnologia`, the scripts in `ferramentas/` and the tests, to be replaced by the new skill.
- The courses and books published with the old skills (they will be rebuilt with the new one), and the `epubs` and `skill` releases.
