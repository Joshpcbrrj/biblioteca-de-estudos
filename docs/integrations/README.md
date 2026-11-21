# Integrations

**English** | [Português](README.pt-BR.md)

Everything that is connected or installed separately from the skill. None of them is required: without them, the skill writes the book just the same and gives you a zip to download. With them, it publishes and finds materials on its own.

## What each one is for

| Integration | What it is for | When the skill uses it | Guide |
| --- | --- | --- | --- |
| **GitHub** | Keep the books in your repository, save progress and publish | start (checkpoints) and end (publishing) | [github.md](github.md) |
| **Notion** | Read a material of yours to improve; create the book copy for your notes | Improve mode and the end | [notion.md](notion.md) |
| **Google Drive** | Find your documents and files to use as sources | when you have materials to use | [google-drive.md](google-drive.md) |
| **Docling** | Convert PDF, DOCX, PPTX and other documents to text, keeping tables and structure | when you send documents | [docling.md](docling.md) |
| **GitHub Pages** | Publish the searchable website with every book | after the first publication | [github-pages.md](github-pages.md) |
| **WSL 2** | A real Linux on Windows, so the skill runs Linux commands and shows their real output | on Windows, whenever a book has code or commands | [wsl.md](wsl.md) |

**On Windows, install WSL 2.** Without it, Linux commands in a book (bash, apt, Docker) cannot be tested: you run them yourself or they are marked "not run". It is also the only way to get Claude Code's sandbox on Windows.

## Where each one works

| Integration | Claude desktop app | Claude in the browser | Claude Code |
| --- | --- | --- | --- |
| GitHub | repository access with write permission | repository access with write permission | `git` + `gh auth login` |
| Notion | connector | connector | Notion's MCP server (`claude mcp add`) |
| Google Drive | connector (any plan) | connector (any plan) | download the files |
| Docling | local MCP server | not available: convert on your computer and attach | command line |
| GitHub Pages | — | — | — |
| WSL 2 | — | — | Claude Code installed inside Ubuntu |

Without any of them, on any plan: the zip to download always works, and GitHub Pages is free for public repositories.

## How the guides are organized

Every guide follows the same outline:

1. **What it is for**
2. **What you need**
3. **Step by step**
4. **How to check that it worked**
5. **Common problems**
