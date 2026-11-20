# Visuals: images and reading profiles

## Contents

1. Image families
2. The user's choices
3. Reading profiles
4. Diagrams (SVG)
5. Illustrations (PNG)
6. Real images
7. Checking images

## 1. Image families

| Family | Use it for | Goes to Notion |
| --- | --- | --- |
| **SVG diagram** | structure, flow, comparison, sequence, timeline, memory and values, chord or circuit diagrams, cheat sheets | yes |
| **Illustration (PNG)** | a process or an overview that an image explains better than text | no |
| **Real image** | what something looks like: historical photos, instruments, components (see `SOURCES.md` §7) | yes |

Before any image, write in one sentence what the reader must understand from it; that sentence is its title. If there is no such sentence, do not make the image. Whatever the reader must reproduce stays as text (`TEACHING.md` §5).

## 2. The user's choices

Asked once, right after approval, and stored in `book.yaml` (`choices`):

- **Images:** `svg` (SVG diagrams only; the default on the free plan) · `illustrations` (SVG + illustrations from HTML templates) · `paid-api` (SVG + illustrations from a paid image API; needs the user's key set up outside the chat and network access to the provider; never text generated inside the image).
- **Reading:** `large` (monitors and 10" or larger color e-readers; the default) · `small` (6–7" grayscale e-readers such as Kindle or Kobo).

## 3. Reading profiles

`diagram.py` and `audit.py` read the limits from `choices.reading`:

| Item | `large` | `small` |
| --- | --- | --- |
| Diagram width | ~960 px | 480 px |
| Code line length | ~80 characters | 60 characters |
| Table columns | up to 6 | up to 4 |
| Cheat sheet in the EPUB | whole sheet | split in 2 parts |
| Color | may carry meaning, always with a label too | never the only signal |

## 4. Diagrams (SVG)

**Never write SVG by hand.** Write a short spec (YAML) and run `python scripts/diagram.py <spec.yaml>`. Run `python scripts/diagram.py --help` once to see the diagram types and their fields. Save specs next to the images (`img/_source/`), so translations and fixes only edit the spec.

Pick the type by the idea:

| The idea is... | Type |
| --- | --- |
| steps or decisions | flowchart (top to bottom) |
| something that changes over time | timeline, or a trace table (one row per step) |
| parts of a whole | blocks, layers, tree |
| how concepts connect | concept map (arrows labeled with verbs) |
| two options | side by side, same rows on both sides |
| a common mistake | wrong × right |
| memory, data, positions | boxes with names and real values |
| parts talking to each other | sequence diagram |
| quantities | simple bar or line chart |

Rules:

- **One focus** per image, highlighted; the rest neutral.
- **At most ~7 main elements**; if more, split into two images or numbered steps.
- **Real values** (`i = 0, 1, 2`), not just abstract labels.
- **Labels next to** what they describe; short (2–5 words).
- **Fixed colors:** blue = input/structure, green = right/output/end, orange = decision/attention, red = error, purple = central concept, gray = neutral. Color is never the only signal: add ✅/❌, a label or a dashed line.
- **Fixed shapes:** rectangle = action/state, diamond = decision, rounded = start/end, cylinder = database, solid arrow = flow, dashed arrow = dependency or return.
- Alt text for every image: what it shows, in one or two sentences.
- File names start with the chapter number: `c06-project-network.svg`.

**Cheat sheets:** a 3 × 4 grid of cards (icon in ASCII, numbered short title, 3–5 items of up to ~28 characters, optionally a 1–3 line code snippet), read column by column; in the `small` profile, `build.py` also makes the 2-part version for the EPUB.

## 5. Illustrations (PNG)

Only with `choices.images` = `illustrations` or `paid-api`.

- **HTML templates:** `python scripts/illustrate.py <spec.yaml>` fills an HTML template from `assets/` and renders a PNG at 2×. Text in the image is always correct because it is real text. The spec goes to `img/_source/`.
- **Paid API:** only for imagery without text (a scene, an object); any labels are added by the template on top. Never send the user's materials to the API.
- Color and icons always carry meaning; no decorative scenes.

## 6. Real images

See `SOURCES.md` §7: free licenses only, credits in `img/CREDITS.md` and in the caption.

## 7. Checking images

- `diagram.py` and `illustrate.py` report text overflowing boxes, overlaps and size limits: fix the spec until they report nothing.
- When you need to look, run `python scripts/diagram.py --sheet <chapter>`: one contact sheet with all the chapter's images, instead of opening each one.
- Check that every value shown is right (run the code, redo the calculation).
