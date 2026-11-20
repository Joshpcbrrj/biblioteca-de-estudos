# Mode 3: Translate a book into another language

Copy this checklist into your reply and tick it off:

```text
- [ ] 1. Identify the book and the target language
- [ ] 2. Glossary and adaptation notes (approved by the user)
- [ ] 3. Create the sibling book
- [ ] 4. Chapter loop (translate and adapt)
- [ ] 5. Fixed parts and images in the new language
- [ ] 6. Link both versions and publish
```

Translating here means **adapting**: the reader of the new version must feel the book was written for them.

## 1. Identify the book

- Accept a book made by this skill: its folder in the user's repository, or the zip it delivered (it carries `book.yaml`). Any other material goes to mode 2 (Improve), with the target language as the book language.
- Read only `book.yaml` and the glossary. Confirm the target language and the conversation language.
- **Language-learning books are adapted, not translated.** A book teaching English to Portuguese speakers cannot simply become a book for Spanish speakers: false friends, pronunciation traps and grammar contrasts change. Say so in one sentence and treat the examples about the learner's native language as content to rewrite.

## 2. Glossary and adaptation notes

Before chapter 1, build a term table from the concept graph and the book's glossary: `original term → term in the target language`, using the terms people in that language actually use (for technology, often the English term). List also what will be adapted: names in examples, currencies, units, dates, cultural references, sources available in the target language.

Show both in one message and wait for "approved". The table goes into the new `book.yaml` (`glossary`) and every chapter follows it.

## 3. Create the sibling book

- Folder: next to the original, with the language suffix (`created-books/<slug>-<lang>/` or `improved-materials/<slug>-<lang>/`).
- `book.yaml`: copy the original's, then set `language`, `translation_of: <slug>`, the translated titles and concept names, and an empty progress list. Add `translations: [<slug>-<lang>]` to the original.
- Run `book.py validate`.

## 4. Chapter loop

Use the loop in `SKILL.md`, with these differences:

- `book.py brief <n>` also gives the path of the original chapter: read it, translate and adapt it into the new file. Do not add or remove content.
- **Code:** stays identical; translate only comments and user-facing strings when they are part of the lesson. `projects.py` runs everything again.
- **Commands and outputs:** keep the real outputs; translate only the explanation around them.
- **Sources:** keep the originals; add a source in the target language when one exists and says the same.
- **Facts:** `facts.py` is still run, because adapted examples can introduce new numbers or names.

## 5. Fixed parts and images

- Chapter 0, placement test, mock exam, glossary and map: regenerate with `build.py` in the new language; translate their texts like a chapter.
- **SVG diagrams:** translate the text in each spec and redraw with `diagram.py`; never edit an SVG by hand.
- **Illustrations:** regenerate from their HTML source in `img/_source/` with the translated text.
- **Real images:** keep them; translate captions and alt text; keep the credits.

## 6. Link and publish

- Each version's README links to the other ("Also available in: ...").
- Run `audit.py` on the whole book, then `build.py`, then publish as in `modes/PUBLISH.md` §3–4.
