# Syllabus: the `book.yaml` file

`book.yaml` is the book's contract and its memory: the approved syllabus, the user's choices and the progress. Scripts read it; you keep it up to date only through the steps that say so. Run `python scripts/book.py validate <book.yaml>` after every change.

## Model

```yaml
title: "Docker Compose na prática"
subtitle: "Do primeiro compose.yaml a uma stack completa"
slug: docker-compose-na-pratica      # lowercase ASCII and hyphens; folder name
origin: created                      # created | improved
language: pt-BR                      # book language
conversation_language: pt-BR
profiles: [stem]                     # stem | languages | skills | knowledge (at most 2)
level: {start: beginner, end: intermediate}
audience: "Who already runs containers with docker run"
goal: "Describe an app with API, database and proxy in one compose.yaml and run it with one command"
prerequisites: ["docker-do-zero"]    # slugs of other books, or plain text
track: {name: devops, order: 1}
reference_version: "Docker Compose v5.6, Docker Engine 29.9"   # only if the topic changes over time
review_by: "2027-11"                 # only if the topic changes over time
sources:
  - {title: "How Compose works", url: "https://docs.docker.com/compose/intro/compose-application-model/", checked: "2026-11-17"}
approved_on: ""                      # empty while it is a draft
edition: "1.0"
human_review: false
choices: {images: svg, reading: large}   # images: svg | illustrations | paid-api; reading: large | small
concepts:                            # the concept graph
  - {id: service, name: "serviço", chapter: 1, depends: []}
  - {id: project-network, name: "rede do projeto", chapter: 6, depends: [service]}
chapters:
  - n: 1
    title: "Por que um arquivo para o projeto"
    goal: "Rebuild a long docker run as a compose.yaml"
    topics: ["declarative vs imperative", "services"]
    minutes: 35
    sources_original: []             # mode 2: sections of the original this chapter comes from
next_steps: ["Docker Swarm do zero", "Kubernetes do zero"]
covers: [compose, compose-yaml]      # short stable labels, used to compare books in a track
progress: []                         # filled by book.py: {n, done, summary}
changes: []                          # changes after approval: {date, what, why}
```

Mode-specific fields:

- **Improve (mode 2):** `origin: improved`; `original: {title, kind, where}` (where it came from, never published); `promise: {goal, audience, level, sequence}`; `sources_original` in each chapter; `new_content_pct`.
- **Translate (mode 3):** `translation_of: <slug>`; `glossary: [{source, target}]`; the original gets `translations: [<slug>-<lang>]`.

## Concept graph rules

- Every concept that a chapter teaches is listed once, with the chapter that teaches it.
- `depends` lists the concepts it needs. `book.py validate` refuses a concept that depends on one taught in a later chapter.
- Keep it short: the 3–8 key concepts of each chapter, not every term. `build.py` uses it for the map, the glossary links and the index.

## Labels

`covers` and the ids in `concepts` are short, stable, lowercase, ASCII and hyphenated (`compose-yaml`), whatever the book language. `name` and the titles are in the book language.

## Changes after approval

1. Show the impact first ("dropping ch. 5 affects the examples in ch. 6 and 8").
2. Ask approval for that change only.
3. Update the chapters and concepts, add an entry to `changes` (date, what, why), and run `book.py validate`.
4. If chapters already written are affected, list them and fix them before continuing.

Do not change `approved_on`: the original approval date stays; `changes` holds the history (and git holds the rest).
