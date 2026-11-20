# Mode 1: Create, from topic to approved syllabus

The sections below follow this checklist, step by step. Copy it into your reply and tick it off:

```text
- [ ] 1. Understand the request (up to 3 questions)
- [ ] 2. Pick the area profile
- [ ] 3. Research
- [ ] 4. Assessment + syllabus (in the same message)
- [ ] 5. Adjust until "approved"
- [ ] 6. Save book.yaml and follow the flow in SKILL.md
```

**No chapter before "approved".** A wrong syllabus costs the whole book; adjusting it costs one message.

## 1. Understand the request

One message, at most 3 questions, and only what the request did not say:

| Question | Default if the user does not answer |
| --- | --- |
| What is your level in this topic today? | never studied it |
| Why do you want to learn it? (e.g. work, travel, hobby, exam) | general use |
| Size: short guide (5–6 ch.), book (8–12) or complete (13–16)? | book |

Do not ask how much time per day: chapter 0 offers schedules at three paces.

In the same message, offer (not a required question): "If you have books, PDFs, EPUBs or a Google Drive folder on this topic, send them: I'll use them as sources." If the user sends any, run each file through `ingest.py` and use only its outline until step 3. In Google Drive, list the files found and let the user choose before opening any. Usage rules are in `references/SOURCES.md` (understand and check, never copy).

If the user has a library on GitHub, check `created-books/` and `improved-materials/` for a book on the same topic. If there is one, show what it covers and ask: expand it, write the next book in the track, or take another angle.

## 2. Area profile

Pick the profile from the topic and read only that one (at most 2 when the topic combines areas, e.g. electronics = `skills.md` + `stem.md`):

| Profile | Topics |
| --- | --- |
| `stem.md` | programming, math, statistics, technology |
| `languages.md` | English and other languages |
| `skills.md` | music, electronics, drawing, cooking, hands-on work |
| `knowledge.md` | history, sciences, concepts, reading topics |

## 3. Research

Follow `references/SOURCES.md`. The goal of the research, and nothing beyond it:

- the **usual curriculum** for the topic (university syllabi, textbooks, official documentation);
- the **prerequisites** and the **common mistakes and myths** of beginners;
- the **current version**, when the topic changes over time (tools, laws);
- 4 to 8 reliable **sources**, each with the date it was checked.

Start with the user's materials, if any (only the useful sections, by the outline). Search with specific questions and stop when you have the above. The sources go into `book.yaml`; chapters reuse them and do not research the topic again.

## 4. Assessment + syllabus

Before showing it, save the draft **outside the repository** (`/tmp/book-<slug>.yaml`, with `approved_on: ""`, the `sources` and the concept graph; the model is in `references/SYLLABUS.md`) and run `python scripts/book.py validate /tmp/book-<slug>.yaml`. Fix it until it passes.

Show it in one message, in this format. Labels go in the conversation language; titles in the book language.

```text
🔎 Assessment: <topic>
What it is and what it is for: <1–2 sentences>
Helps to know first: <prerequisites, or "nothing">
How people usually learn it: <the usual path, in 1–2 sentences>
Common mistakes and myths: <2–3 items>
Main sources: <2–4 names>

📘 <Title> · <start level> → <end level> · <n> chapters · ~<h> h
For whom: <one sentence>
When you finish, you will: <the book's goal, checkable>
Prerequisites: <knowledge or books>

0. How to study this book
1. <Title>                     → <goal with an action verb>
2. ...
n. <Final project or challenge> → <what the reader delivers>
   Final mock exam

Next steps: <2–4 topics for later books>
Reference version: <only if the topic changes over time, with the date>

Adjust freely: "longer", "shorter", "drop 5", "add X",
"merge 3 and 4", "swap the order", "more hands-on".
When it looks right, say "approved".
```

Syllabus rules:

- **Beginner to intermediate**, unless the user asks otherwise.
- **Progression:** each chapter uses only concepts from earlier ones (`book.py validate` checks the concept graph).
- **One goal per chapter**, with a verb that can be checked ("build", "translate", "play at 80 bpm"), never "understand" or "know".
- **Chapter 1 delivers a concrete win** (something that works, is said or is played on day one).
- **Practice in every chapter**, of the kind defined by the profile.
- **Explicit scope:** what does not fit goes to "Next steps".

## 5. Adjust until "approved"

Read requests in plain language. Always reply with **the whole updated syllabus** and, above it, one line `Changed: ...`. Run `book.py validate` after every change.

| Request | What to do |
| --- | --- |
| "longer" / "more complete" | add or deepen chapters without breaking the progression; state the new total |
| "shorter" | merge nearby chapters; the rest goes to Next steps |
| "drop X" | remove it; if a later chapter depends on it, move the minimum it needs there and say so in `Changed:` |
| "add Y" | fit it where the progression allows; if Y is too advanced for the level, suggest leaving it for another book |
| "more hands-on" | turn explanation goals into tasks; make the final project measurable |
| "merge", "split", "swap the order" | do it and check that no chapter now uses a concept not yet taught |
| a request that conflicts with the level or size | do it, and state the effect in one sentence |

## 6. Save and continue

When you hear "approved" (or a clear equivalent in any language), and only then:

1. Fill in `approved_on` and save to `created-books/<slug>/book.yaml` (with GitHub connected, on the `draft/<slug>` branch).
2. Follow "Flow after approval" in `SKILL.md`, from step 1.

**Changes after approval:** show the impact ("dropping ch. 5 affects the examples in ch. 6 and 8"), ask approval for that change only, and update `book.yaml` as described in `references/SYLLABUS.md`.
