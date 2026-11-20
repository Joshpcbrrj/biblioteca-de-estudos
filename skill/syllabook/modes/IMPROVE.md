# Mode 2: Improve, from material to approved plan

Copy this checklist into your reply and tick it off:

```text
- [ ] 1. Receive the material (and related sources, if any)
- [ ] 2. Ingest: Markdown per section + outline
- [ ] 3. Write down the material's promise
- [ ] 4. Map and diagnosis
- [ ] 5. Improvement plan (with the fidelity contract)
- [ ] 6. Adjust until "approved"
- [ ] 7. Save book.yaml and follow the flow in SKILL.md
```

**The original's purpose rules.** The goal is to make *this* material teach better, not to write a different book. No chapter before "approved".

## 1. Receive the material

Accept any of these, alone or combined:

| Material | How to get it |
| --- | --- |
| Notion page | the user's link; open the index page and **every** subpage with the Notion tools |
| PDF, DOCX, PPTX, EPUB, text | attached to the chat, or from the Downloads folder if the app shares it |
| Google Drive | search by topic, list the files found, and open only those the user picks |
| Web link | fetch the page |

Also offer, once: "If you have related books or PDFs, send them: I'll use them only to fill gaps and check facts." Ask the profile questions only if the material does not answer them (level of the reader, purpose).

## 2. Ingest

Run `python scripts/ingest.py <material> --out /tmp/sources/<slug>` for each file or page set. It writes one Markdown file per section and prints the outline. From now on, **read sections, not whole files**: the outline tells you where each topic is.

Pick the area profile from the content (see `modes/CREATE.md` §2) and read it.

## 3. The material's promise

Write it down from the material itself, in four lines: **goal**, **audience**, **level**, **sequence** (the order of its parts). If the material does not state one of them, infer it and mark it "(inferred)". This is the contract: the plan cannot break it.

## 4. Map and diagnosis

For each section of the original, note in a few words:

- what it teaches and whether it is **complete, shallow or missing** compared with the promise;
- **suspected errors** (facts, code, calculations), to confirm with sources or by running them;
- what is **already good** and must stay.

Then classify everything you would add:

| Class | Rule |
| --- | --- |
| **Essential gap:** a prerequisite used but never taught, something promised but absent, a step whose absence breaks the practice | goes into the book |
| **Useful deepening** | a short box inside an existing chapter, not a new chapter |
| **Outside the promise** | only in "Next steps" |

Limits: new content up to about **20%** of the total; a new chapter only if the plan lists it; the original order stays unless it has a teaching error, which you explain.

## 5. Improvement plan

Save the draft outside the repository (`/tmp/book-<slug>.yaml`, `origin: improved`, `approved_on: ""`, with the concept graph and the mapping from original sections to chapters) and run `book.py validate` until it passes. Show it in one message, in this format (labels in the conversation language, titles in the book language):

```text
🔎 What I found: <material name>
Promise: <goal> · for <audience> · <level> · <n> parts
Already good (stays): <2–3 items>
Corrections: <errors found, one line each, or "none so far">
Gaps to fill (essential): <items, each with where it goes>
Short deepening boxes: <items, or "none">
Outside the promise (only in Next steps): <items>

📘 <Title> · <n> chapters · new content ~<p>% · ~<h> h
0. How to study this book
1. <Title>   ← original: <section(s)>   → <goal>
2. ...
   Final mock exam

The original is never published: only its structure, topics and goals are used,
with explanations written from scratch.

Adjust freely: "keep the original order", "fewer additions", "split 3", "add X".
When it looks right, say "approved".
```

## 6. Adjust until "approved"

Same rules as `modes/CREATE.md` §5, plus two:

- "fewer additions" → move items from essential to deepening or to Next steps, and update the percentage;
- a request that breaks the promise (a different audience, a much higher level) → do it only after saying in one sentence that the book will no longer follow the original.

## 7. Save and continue

When you hear "approved":

1. Fill in `approved_on` and save to `improved-materials/<slug>/book.yaml` (on the `draft/<slug>` branch when GitHub is connected).
2. Follow "Flow after approval" in `SKILL.md`. In each chapter, `book.py brief` also lists the original sections it maps to: read only those.
3. At the end, the audit checks that every chapter points to where it came from.

**Copyright:** rewrite every explanation in your own words; quote at most a short passage with its source; never copy exercises verbatim from third-party material (write new ones that train the same skill). The user's own notes are theirs and can be reused freely.
