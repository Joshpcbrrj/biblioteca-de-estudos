# Cover

A book cover, not a template: original, clean and readable as a small thumbnail.

## Content

- Title and subtitle, in the book language.
- "by <author>" with `author` from `library.yaml` (in the book language, e.g. "por <author>").
- For improved materials, a small line under the subtitle: the kind of original ("based on course notes").
- No third-party logos, brands, mascots or characters, ever. Represent a technology with an original abstract shape, never its logo.

## Format

- Source in SVG (`cover.svg`), exported to PNG at **1600 × 2560** (`cover.png`) for the EPUB. Text as real text, not paths.
- One idea in the artwork: an abstract shape or a simple scene that hints at the topic (stacked blocks for containers, sound waves for music, a timeline for history).
- Two typefaces at most; the title fills about a third of the width and stays readable at 160 px wide.
- High contrast between text and background; works in grayscale.
- A consistent series look per library: same layout grid and type, a different accent color per track.

## Process

1. Write in one sentence the visual idea and the accent color.
2. Build the SVG (from the cover template in `assets/` when available).
3. Render the PNG and look at it at two sizes: full and 160 px wide.
4. Check: title readable at 160 px; nothing touching the edges; no third-party marks; author and edition correct.
