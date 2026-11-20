# GitHub: keep your books in your own repository

**English** | [Português](github.pt-BR.md)

## What it is for

Your library lives in a GitHub repository of yours: the books in Markdown, the EPUBs in its releases and the website on GitHub Pages. With access to it, Syllabook saves your progress after every chapter (on a `draft/<book>` branch) and publishes the book at the end. Without access, it gives you a zip and tells you where to upload it.

## What you need

- A GitHub account.
- A **public** repository for your library (GitHub Pages is free for public repositories). The easiest way: open the [demo library](https://github.com/Joshpcbrrj/syllabook-demo) to see what one looks like, then create an empty repository and let Syllabook set it up on the first book.

## Step by step

Use the first option that fits where you use Claude.

### Option 1: Claude app with repository access

When Syllabook asks for your library repository, give Claude access to it **with write permission**. Claude then clones it, commits each chapter and publishes. The exact screen depends on your Claude app version; always allow access to that one repository only.

### Option 2: Claude Code

Claude Code uses `git` on your computer. Sign in once with the GitHub command line:

```bash
gh auth login
```

Choose GitHub.com, HTTPS and "Login with a web browser": copy the 8-character code that the terminal shows, paste it on the page that opens and authorize.

### Option 3: no connection

Say "no" when Syllabook offers to connect. At the end it gives you a zip whose folders already match the repository (`created-books/<book>/...`). In your repository on github.com: **Add file → Upload files**, drag the folder in and commit. GitHub's website takes up to 100 files per upload; for bigger books Syllabook splits the zip and tells you the order.

### Advanced: GitHub's MCP server as a custom connector

GitHub hosts an MCP server at `https://api.githubcopilot.com/mcp/`. Adding it to Claude as a custom connector currently requires your own GitHub OAuth app (or a personal access token in Claude Code), so it is not the recommended path. Never paste a token into a chat.

## How to check that it worked

- Option 1 or 2: ask Claude to "list the files of my library repository". It should show `library.yaml` and the book folders.
- Option 2: `gh auth status` shows `Logged in to github.com`.
- After the first publication, the repository's **Actions** tab shows "Build EPUBs" and "Website" in green.

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| Claude can read but not push | Access was given read-only. Give write permission to that repository |
| `gh` asks for a code, and the browser page is empty | Copy the code from the terminal line "First copy your one-time code" |
| "Build EPUBs" or "Website" fails on the first push | Open the failed run in **Actions** and read the last lines; for the website, turn on GitHub Pages first ([guide](github-pages.md)) |
| Upload on the website stops at 100 files | Use the parts Syllabook made, in order, or GitHub Desktop |
