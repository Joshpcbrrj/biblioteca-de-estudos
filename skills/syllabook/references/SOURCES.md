# Sources: research, user materials, fact checks and copyright

## Contents

1. Trust order
2. Research
3. The user's materials
4. Citing in the book
5. Fact checks
6. Copyright
7. Real images
8. Sensitive topics

## 1. Trust order

1. Official documentation, standards, specifications, release notes; primary sources (original documents, data, papers).
2. The project's official repository; museums, archives and universities.
3. Recognized textbooks and courses; peer-reviewed reviews; blogs by maintainers or institutions with authority on the topic.
4. Forums and Q&A sites **only** to learn which mistakes are common, never as the source of a fact.

Anything that can change over time (commands, options, defaults, limits, versions, prices, laws) must come from levels 1–2 and be **checked in this session**. Stable concepts (what a variable is, what a verb tense is) need no source.

## 2. Research

- Search with a specific question; read only the part of a page that answers it.
- Stop as soon as you have what the step asks for (`modes/CREATE.md` §3).
- Record every source in `book.yaml` (`sources`: title, URL, checked date). Chapters reuse them and do not research the topic again; a chapter searches only to confirm a specific fact that is missing.

## 3. The user's materials

Books, PDFs, EPUBs, Notion pages or Drive files the user sends:

- Run `ingest.py` and work from the outline; read only the sections a step needs.
- Use them to **understand, structure and check**. Never copy their text, examples or exercises.
- Cite them like any source ("<Title>, ch. 3"). They are never published or attached to the book.
- In Google Drive, list what the search found and open only what the user chooses.

## 4. Citing in the book

- Each chapter ends with `## 📚 Sources`: 2–6 links with their checked date.
- Version-dependent behavior names the version in the text ("since version 25, ...").
- Quotations: at most one short quotation (under 15 words) per source, in quotation marks, with the link, and only when the exact words matter.

## 5. Fact checks

For each chapter, `facts.py <n>` lists the sentences with dates, numbers, names and quotations. For each one:

1. Find it in the recorded sources (or confirm it with one new search).
2. If it holds, keep it; if it does not, fix it; if it cannot be checked, remove it or say clearly that it is uncertain.

Separate **fact**, **interpretation** and **legend** in the text whenever a topic has popular stories or debate ("The popular version says...; the records show..."). This is mandatory in the `knowledge` profile.

## 6. Copyright

- Explain in your own words. Paraphrasing means rewriting the explanation, not swapping synonyms.
- Write your own examples, exercises and code. A short snippet from documentation, when unavoidable, carries its source; respect the license of any reused code.
- Never reproduce song lyrics, poems or long passages of protected works. In music books, use public-domain songs or exercises written for the book.
- Third-party material in mode 2: only its structure, topics and goals; the original is never published.
- No third-party logos, brands or mascots, in images or on the cover.

## 7. Real images

Photos of people, machines, instruments, components or historical documents:

- only public domain or free licenses (e.g. from Wikimedia Commons or museum open-access collections);
- record author, source, license and link in `img/CREDITS.md`, and give the credit in the caption;
- prefer an SVG diagram when the point is a structure, not what the thing looks like.

## 8. Sensitive topics

- Health, law, finance, safety: official sources only, and a short note that the book does not replace a professional.
- Electronics, tools, chemistry or anything with physical risk: a safety box before the first hands-on step (see the `skills` profile).
- Topics that change fast (technology, laws): set `review_by` in `book.yaml`, usually 12 months after the check.
