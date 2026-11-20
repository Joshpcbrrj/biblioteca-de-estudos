---
type: llm
---

The user wants to publish a finished book without connecting GitHub or Notion. No book files were provided in the conversation, so asking for the book (its zip or folder) first is correct.
Pass if the reply, in Portuguese, explains a working path without connections: the skill generates the EPUB and a zip of the book, and the user uploads the zip contents to their GitHub library through the website ("Add file → Upload files") or GitHub Desktop. Mentioning the 100-file limit, turning on GitHub Pages, or leaving Notion for later are pluses.
Template placeholders such as https://<seu-usuário>.github.io/<repositório>/ are not invented links.
Fail if it invents a concrete link to a repository or site, asks for tokens or passwords, or says publishing is impossible without connecting.
