# Visuals: images and reading profiles

## Contents

1. Image families
2. The user's choices
3. Reading profiles
4. Diagrams (SVG)
5. Real images
6. Checking images

## 1. Image families

| Family | Use it for | Goes to Notion |
| --- | --- | --- |
| **SVG diagram** | what the reader cannot see: structure, logic, flow, states, comparison, sequence, timeline, memory and values, chord diagrams, cheat sheets | yes |
| **Real image** (photo or screenshot) | a real thing or scene: a person, a place, an event, a machine, a document, an instrument, an application's screen, files open in an editor, a web page after an action | no: EPUB and website only |

**Choose by what the reader must see.** If the point is how parts relate or how something works inside, draw an SVG diagram. If the point is how something real looks, show the real thing: a diagram would only imitate it. When both could work and the subject is concrete, prefer the real image. Examples from a Git book: the file lifecycle (untracked, staged, committed) is an SVG; two modified files open side by side in VS Code is a screenshot; how a commit points to its parent is an SVG; the GitHub page of a pull request is a screenshot. In a history book, Alan Turing is a photo, never a drawing; the timeline of his work is an SVG.

Before any image, write in one sentence what the reader must understand from it; that sentence is its title. If there is no such sentence, do not make the image. Whatever the reader must reproduce (code, commands, chords) stays as text, even next to a screenshot (`TEACHING.md` §5).

## 2. The user's choices

Asked once, right after approval, and stored in `book.yaml` (`choices`):

- **Images:** `real` (SVG diagrams plus real images where they show it better; the default) · `svg` (SVG diagrams only, for a reader who wants no photos or screenshots).
- **Reading:** `large` (monitors and 10" or larger color e-readers; the default) · `small` (6–7" grayscale e-readers such as Kindle or Kobo).

## 3. Reading profiles

`diagram.py` and `audit.py` read the limits from `choices.reading`:

| Item | `large` | `small` |
| --- | --- | --- |
| Diagram width | ~960 px | 480 px |
| Code line length | ~80 characters | 60 characters |
| Table columns | up to 6 | up to 4 |
| Cheat sheet | 3 columns | 2 columns (taller, same cards) |
| Color | may carry meaning, always with a label too | never the only signal |

## 4. Diagrams (SVG)

**Never write SVG by hand.** Write a short spec (YAML) and run `python scripts/diagram.py <spec.yaml>`. Run `python scripts/diagram.py --help` once to see the diagram types and their fields. Save specs next to the images (`img/_source/`), so translations and fixes only edit the spec.

Pick the type by the idea:

| The idea is... | Type |
| --- | --- |
| steps or decisions | `flow` (top to bottom, diamonds for decisions) |
| something that changes over time | `timeline`; a trace of a loop is a Markdown table, one row per step |
| parts of a whole | `layers` or `tree` |
| how concepts connect | `tree` with verbs in the labels (a free-form concept map is not supported yet) |
| two options | `compare` (same rows on both sides) |
| a common mistake | `compare` with `style: wrong-right` |
| memory, data, positions | `boxes` with names and real values |
| parts talking to each other | `sequence` |
| quantities | `bars` |
| a summary of a part of the book | `cards` (the cheat sheet) |
| a relation between a few things (A → B, A + B = C, wrong → right) | `scene` (icons joined by arrows or signs) |
| a chord shape on a fretted instrument | `chord` (guitar by default; set `tuning` for bass, ukulele, cavaquinho) |
| where notes are on the neck (scales, intervals) | `fretboard` |
| a melody, riff or arpeggio to play | `tab` |

A diagram **adds to** the text: the chapter explains, the image shows the same idea at a glance. SVG is for diagrams only; a real scene or object is a real image (§5), never drawn.

Rules:

- **One focus** per image, highlighted; the rest neutral.
- **At most ~7 main elements**; if more, split into two images or numbered steps.
- **Real values** (`i = 0, 1, 2`), not just abstract labels.
- **Labels next to** what they describe; short (2–5 words).
- **Fixed colors:** blue = input/structure, green = right/output/end, orange = decision/attention, red = error, purple = central concept, gray = neutral. Color is never the only signal: add an icon, a label or a dashed line.
- **Text and note:** each box has a short bold `text` and, when it helps, a `note` with the detail (`Ubuntu` / `bash, apt, git`).
- **Icons** (`icon:`, names from `diagram.py --icons`): one per item when it tells the items apart at a glance (a terminal for the shell, a CPU for the kernel). Pick the icon by meaning; skip it rather than force one. No emoji inside a diagram: they depend on the reader's fonts.
- **Scenes** (`scene:`): only for a relation the reader should see (a folder that holds files, a formula, a wrong window that becomes a right one); a scene that only decorates is left out.
- **Fixed shapes:** rectangle = action/state, diamond = decision, rounded = start/end, cylinder = database, solid arrow = flow, dashed arrow = dependency or return.
- Alt text for every image: what it shows, in one or two sentences.
- File names start with the chapter number: `c06-project-network.svg`.

**Music diagrams** (`chord`, `fretboard`, `tab`): `diagram.py` also prints `text`, the same content as copyable text; put it right under the image, because whatever the reader plays stays as text. Circuit and pinout diagrams are not supported yet: describe them with `layers`, `boxes` or a table.

**Cheat sheets** (`cards`): up to 12 cards (an icon, a numbered short title, 3–5 items of up to ~28 characters, each with its own icon when that helps, optionally a 1–3 line code snippet and a scene), in 3 columns on large screens and 2 in the `small` profile.

## 5. Real images

Only with `choices.images` = `real`. Where they come from (details in `SOURCES.md` §7):

- **Photos** of people, places, events, machines and documents: free-license images from Wikimedia Commons (`images.py search` and `fetch`).
- **Screenshots of a web page** (the book's application, a GitHub page): `images.py screenshot <url>`, taken after the step the reader just did.
- **Screenshots of a desktop application** (an editor, a terminal window, a settings screen) that `images.py` cannot open: ask the user for it, saying exactly what to open, what must be visible and the file name (`img/c03-vscode-diff.png`); then record it in `img/CREDITS.md`. If the user declines, use text or an SVG instead and say so.

Never draw, generate or fake a real image. Each one has its caption with the credit, alt text, and its line in `img/CREDITS.md`. In Notion only the SVG diagrams go in (`notion.py` lists the rest in `left_out`).

## 6. Checking images

- `diagram.py` reports text overflowing boxes, overlaps and size limits: fix the spec until it reports nothing.
- When you need to look, run `python scripts/diagram.py --sheet <chapter>`: one contact sheet with all the chapter's images (a PNG when a converter is available), instead of opening each one.
- Check that every value shown is right (run the code, redo the calculation).
