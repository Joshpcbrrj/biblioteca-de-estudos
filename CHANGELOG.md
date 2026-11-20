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
- The new skill in `skill/syllabook/`: `SKILL.md`, the modes (Create, Improve, Translate, Publish), the references (teaching, book parts, sources, syllabus, visuals, examples, cover), the area profiles, the style guides (pt-BR, en) and the library skeleton. The scripts arrive in a later step.
- Kit tests (`tests/run.py`) and the "Kit tests" Action; translation checker (`tools/translation.py`); skill packager (`tools/package_skill.py`) and the "Skill release" Action, triggered by version tags.
- `.gitattributes`, so text files use LF line endings on every system.

### Changed

- The project is now called **Syllabook** (repository `syllabook`), and it is a GitHub template.
- `biblioteca.yaml` became `library.yaml`, with keys in English.

### Removed

- The old skills `revisar-curso-biblioteca` and `criar-livro-tecnologia`, the scripts in `ferramentas/` and the tests, to be replaced by the new skill.
- The courses and books published with the old skills (they will be rebuilt with the new one), and the `epubs` and `skill` releases.
