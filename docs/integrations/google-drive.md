# Google Drive: use your files as sources

**English** | [Português](google-drive.pt-BR.md)

## What it is for

When you create or improve a book, Syllabook can search your Google Drive for related material (Google Docs, Slides, Sheets and other files), list what it found, and use the files you choose as sources. It only reads them: nothing in your Drive is changed, copied into the book or published.

## What you need

- A Google account.
- The Claude app or claude.ai on a plan that offers the Google Drive connector (Anthropic lists it for Pro, Max, Team and Enterprise; on Team and Enterprise an admin turns it on first).

## Step by step

1. **Settings → Connectors**, find **Google Drive** and choose **Connect**.
2. Sign in with your Google account and allow access.
3. In a chat, keep Google Drive turned on in the connectors menu.

In **Claude Code**, or without the connector, download the files and attach them, or put them in a folder and give Syllabook its path.

## How to check that it worked

Ask Claude to "search my Google Drive for <a topic>". It should list file names from your Drive.

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| Tables or images of a PDF come out wrong | The connector reads text only. Download the PDF and convert it with Docling ([guide](docling.md)) |
| A large Doc or Sheet is cut off | Exports above about 10 MB are not read whole. Split the file, or download it |
| Google Drive is not in the connectors list | Your plan or your organization does not offer it. Download the files instead |
