# Teaching: how every chapter teaches

## Contents

1. Foundations
2. Chapter pattern
3. Practice ladder
4. Explanations
5. Code and other reproducible content
6. Analogies
7. Review and feedback
8. Chapter checklist

## 1. Foundations

Every rule below comes from research on how people learn. Apply the principle, not just the format.

| Principle | What it means in a chapter |
| --- | --- |
| **First principles of instruction** (Merrill) | start from a real problem; activate what the reader already knows; demonstrate; let them apply it; help them use it in their own context |
| **Cognitive load** (Sweller) | one new idea at a time; worked examples before problems; cut anything that does not help understanding |
| **Multimedia** (Mayer) | words and picture together; labels next to what they describe; one focus per image; no decoration |
| **Retrieval practice** | questions answered without looking; answers hidden until the reader tries |
| **Spacing and interleaving** | reviews come back to earlier chapters; question types are mixed |
| **Elaboration and self-explanation** | ask "why?" and "how?"; ask the reader to explain in their own words |
| **Prediction** | "predict the result before you see it", then show it |
| **Concrete examples** | real values first, the general rule after |
| **Misconceptions** | name the common mistake and correct it explicitly |
| **Constructive alignment** (Biggs) and backward design | the chapter goal decides the practice, and the review questions measure that goal |

Do not use: "learning styles" (no evidence), mind maps as the review tool, or analogy quotas.

## 2. Chapter pattern

`book.py brief` creates this skeleton; headings are written in the book language.

```text
# <n>. <Title>
> 🗺️ In this chapter: <1–2 sentences> · ⏱️ ~<minutes> min
> 🔥 Warm-up: 1–2 quick questions on earlier chapters (answers hidden; from chapter 2 on)
## Where we left off        2–3 sentences linking to the previous chapter (not in chapter 1)
## <Topic>                  one section per topic, in this order:
                            why it exists → definition (one bold sentence) → concrete example
                            → code or procedure with its real output → diagram, if it helps
                            → analogy, if the idea is abstract → the common mistake
## 🏋️ Practice              the ladder in §3
## 🧠 Quick review          3–5 questions, at least one from an earlier chapter; answers hidden
## 🤖 Study with an AI tutor  2 ready-to-copy prompts (§7)
> ➡️ Next: what comes next and why
## 📌 Summary               table: Item | In one sentence
## 📚 Sources               links with the date they were checked
> 🔁 Review today: chapters <x> and <y> (from the brief)
```

The area profile may change the order of a topic's steps. Optional material goes under a heading that starts with `🔎` and the word for "Going deeper" in the book language; everything else is essential, so a reader in a hurry can skip only the `🔎` parts.

## 3. Practice ladder

Every chapter climbs these four steps, using the kind of practice set by the area profile:

1. **Worked example:** a fully solved problem, each step explained.
2. **Complete it:** a similar problem with parts left blank.
3. **On your own:** a new problem, same skill.
4. **Challenge:** the same skill in a different context (transfer).

Each answer is hidden and **commented**: why the answer is right and which wrong answers are common and why. For open answers (a text, a recording, a design), give a short rubric with 3–4 criteria the reader can check alone.

Hidden answers always use this exact format, with the summary text in the book language and blank lines where shown:

```text
<details>
<summary>See answer</summary>

<answer>

</details>
```

## 4. Explanations (the most important part)

- Start from the problem the idea solves.
- One idea per paragraph; short sentences; active voice; talk to the reader directly.
- Define every term the first time it appears. In technology and language books, add the English term in parentheses on first use when that is what people use.
- Use an `A × B` table for ideas that are easily confused.
- Show first, then name: the example before the formal definition when possible.
- Explain **why**, not only how.
- No filler, no hype, and never "simply", "just" or "obviously": they make the reader feel stupid when it is not simple for them.
- Test each chapter: does it answer why this exists, how it works with a real example, and what the most common mistake is? If not, complete it.

## 5. Code and other reproducible content

- Code goes in a block with its language, complete enough to run, followed by its **real output**.
- Comments go on the line above the code and explain **why**, not what ("keeps the total to divide at the end", not "adds the grade").
- Line length and indentation follow the reading profile in `VISUALS.md`.
- Anything the reader must reproduce (code, formulas, commands, chords, tabs, steps) is text, never only an image.
- **Projects:** start each block with its file path in bold (`**app/main.py**`) so `projects.py` can assemble and run the project. Final-project code goes inside `<details>`.
- **Mistakes on purpose:** mark the block as failing and show the real error message.
- Formulas in LaTeX (`$...$`, `$$...$$`); procedures as numbered steps.

## 6. Analogies

Use an analogy only for a concept that is both **abstract and new**. Map each part of the concept to a part of the analogy, and end with one line saying **where the analogy breaks**. A single metaphor carried through the book is better than a new one in every chapter. Never force one.

## 7. Review and feedback

- **Warm-up and quick review:** retrieval questions; the brief tells you which earlier chapters to revisit.
- **Review today:** the chapters the brief suggests, for spaced review.
- **AI tutor prompts:** two per chapter, ready to copy, for example (in the book language):
  - "Ask me 5 questions about <topic>, one at a time. Wait for my answer before giving feedback, and do not give me the answers first."
  - "Here is my answer to exercise <x>: <answer>. Point out my mistakes without giving me the solution."
- **Summary:** a table of the chapter's key items, one sentence each.

## 8. Chapter checklist (before `book.py done`)

- The chapter goal is practiced in the ladder and checked in the review.
- Every topic has why, definition, example and common mistake.
- Every piece of code and every command was run (or is marked "not run").
- Facts were checked (`facts.py`).
- No concept is used before it is taught (the brief lists which you may use).
- `audit.py` passes.
