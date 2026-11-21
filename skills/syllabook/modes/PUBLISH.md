# Connections, checkpoints and publishing (also mode 4)

## Contents

1. Connections at the start
2. Checkpoints during the book
3. Publishing to GitHub
4. Copying to Notion
5. Mode 4: publish a finished book

Integration guides live in the kit repository: `https://github.com/Joshpcbrrj/syllabook/tree/main/docs/integrations` (one page per integration, in English and Portuguese). When a connection is missing, explain in up to 3 lines and send the guide link; never reproduce the guide in the chat.

## 1. Connections at the start

Check the available tools without asking the user:

| Integration | How to tell it is available | Used for |
| --- | --- | --- |
| GitHub | tools to read and write repository files, or `git` with access to the user's repository | checkpoints and publishing |
| Notion | Notion tools (fetch, create and update pages) | reading materials (mode 2) and the copy at the end |
| Google Drive | Drive search and read tools | the user's materials, only when they have some |
| Docling | Docling tools (local MCP in the desktop app) or the `docling` command | converting documents, only when there are documents |

If **GitHub** or **Notion** is missing:

1. Say in one or two lines what it is for (GitHub: save progress and publish the book and site; Notion: a copy of the book to take notes in).
2. Send the guide link and wait for "done" or "skip".
3. After "done", check again. If it still fails, say what you saw and offer to continue without it.
4. After "skip", continue: the book is made the same way, and you ask again at the end.

Never ask for tokens or passwords in the chat: connections go through Claude's connectors.

## 2. Checkpoints during the book

- **GitHub connected:** work on the `draft/<slug>` branch of the user's library repository. `book.py done` saves each chapter; commit it right away with the message `<slug>: chapter <n>`. Use `commit_name` and `commit_email` from `library.yaml`.
- **No GitHub:** at the end of each part of the book (or every 4 chapters), offer a partial zip from `build.py --partial`, written outside the library repository (see `--out` in SKILL.md), so it is never committed with the book.
- If the user has no library repository yet, suggest creating one from the template (https://github.com/Joshpcbrrj/syllabook-library, **Use this template**, public): each user keeps their books in a repository of their own.
- If the library repository has no `library.yaml` or book folders yet, copy `assets/library/` into it before the first commit (everything except `SKELETON.md`, which explains each file), and fill in `library.yaml` and the site address in the README.
- "GitHub connected" means write access to the repository: repository access with push permission in the Claude app, or `git` in Claude Code. GitHub's own MCP server as a custom connector needs an OAuth app set up by hand; do not suggest it to beginners.

## 3. Publishing to GitHub

At the end, ask once: "Publish the book to GitHub and create the copy in Notion?" (the default answer is yes for both). Then, for GitHub, use the first option that works:

1. **Write access available:** run `build.py lists --library <repo>` so the folder lists include the book, then merge `draft/<slug>` into `branch` (from `library.yaml`), or commit straight to it if there was no draft branch. The Actions build the EPUB and the site (they come with the library skeleton in `assets/library/`).
2. **Not connected, and the user wants to connect now:** send the GitHub guide link, wait, check again, then do option 1.
3. **The user declines or cannot connect:** run `build.py --out <outputs>` with the downloadable outputs folder (on claude.ai, `/mnt/user-data/outputs`) and deliver the EPUB and the zip. Tell them: extract it at the root of their library repository (the zip already holds `created-books/<slug>/` or `improved-materials/<slug>/`), then upload with GitHub's website (**Add file → Upload files**, dragging the folder) or GitHub Desktop. GitHub's website takes up to 100 files per upload: if the book has more, `build.py` splits the zip into parts and you say which part goes first.

**First publication in a repository:** remind the user to turn on the site once: **Settings → Pages → Source: GitHub Actions** (link to the GitHub Pages guide). The site address is `https://<user>.github.io/<repository>/`.

## 4. Copying to Notion

1. If `notion_page` in `library.yaml` is empty, ask for the link of the Notion page where books should go, and save it (commit with the book when GitHub is connected).
2. **Index page:** `python scripts/notion.py index` prints its title and content (the subtitle, a 📚 callout with the links to the site, the GitHub folder and the EPUB, and the chapter list). Create it under that page.
3. **Pages, in reading order, under the index:** chapter 0 (`notion.py 0`), each chapter (`notion.py <n>`), the mock exam (`notion.py <its number>`) and the glossary (`notion.py <its file name>`). Each command prints `title`, `content` and `uploads`:
   - upload each file in `uploads` with the Notion file tools, then replace its `placeholder` in `content` with what the upload returns (an upload is valid for about an hour, so upload right before creating the page);
   - create the page with that `title` and `content`, sending the content as printed: it is already in Notion's format (toggles, callouts, images);
   - `left_out` lists the photos, screenshots and illustrations that stay out of Notion on purpose: Notion keeps only the SVG diagrams, and the other images stay in the EPUB and the site.
4. If a Notion call fails, retry once with a smaller piece (half of the content, then append the rest); if it fails again, report which chapter and continue with the next.

## 5. Mode 4: publish a finished book

For a book made earlier with this skill and never published (or published only in part):

1. Ask for the zip the skill delivered (or the folder, if it is already in a repository). It must contain `book.yaml`; without it, the material goes to mode 2 (Improve).
2. Run `book.py validate`, then `audit.py`. If there are errors, list them and ask whether to fix them now (this costs a little) or publish as it is with a warning.
3. Run `build.py`, then §3 and §4 above. The folder comes from `origin` in `book.yaml`.
