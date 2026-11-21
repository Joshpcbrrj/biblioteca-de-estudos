# Notion: read your materials and keep a copy of each book

**English** | [Português](notion.pt-BR.md)

## What it is for

- **Improve mode:** Syllabook reads your course notes straight from Notion, page by page.
- **At the end of every book:** it creates a copy of the book in Notion, under a page you choose, so you can take notes on it. The copy has the text, the answers as toggles and the images (SVG diagrams and photos).

## What you need

- A Notion account with access to the pages you want to use.
- The Notion page where your books should go (copy its link: **••• → Copy link**).

## Step by step

### Claude app or claude.ai

1. **Settings → Connectors**, find **Notion** and choose **Connect**.
2. Sign in to Notion and allow access to the pages Syllabook should read and write (at least the page where books go).
3. In a chat, the Notion tools now appear in the connectors menu; keep Notion turned on for that chat.

### Claude Code

In a terminal, add Notion's official MCP server once, for every project:

```bash
claude mcp add --scope user --transport http notion https://mcp.notion.com/mcp
```

Then, inside Claude Code, type `/mcp`, choose **notion** and sign in. Start a new Claude Code session afterwards, so it loads the Notion tools.

## How to check that it worked

Ask Claude to "fetch my Notion page <link>". It should show the page's title and content. The first time Syllabook publishes, it asks for the link of the page where books go and saves it in `library.yaml` (`notion_page`).

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| Claude says it cannot see the page | The page was not shared when you connected. Reconnect and select it, or share its parent page |
| A diagram is missing in the Notion copy | Image uploads expire after about an hour. Ask Claude to redo that chapter's page |
| Answers appear as plain `<details>` text | The page was not made by Syllabook's converter. Ask Claude to redo it with `notion.py` |
| `/mcp` shows "Needs authentication" or "Invalid redirect_uri" | Run `/mcp` again and repeat the sign-in; update Claude Code if it keeps failing |
