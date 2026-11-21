# Frequently asked questions

**English** | [Português](faq.pt-BR.md)

## Contents

- [Which Claude plan do I need?](#which-claude-plan-do-i-need)
- [Claude app or Claude Code?](#claude-app-or-claude-code)
- [How do I update or remove Syllabook?](#how-do-i-update-or-remove-syllabook)
- [How much does a book cost?](#how-much-does-a-book-cost)
- [Can I stop and continue later?](#can-i-stop-and-continue-later)
- [Can I use it without GitHub?](#can-i-use-it-without-github)
- [Are my materials private?](#are-my-materials-private)
- [Can I edit a book by hand?](#can-i-edit-a-book-by-hand)
- [Which topics and languages work?](#which-topics-and-languages-work)
- [Is the code in the books tested?](#is-the-code-in-the-books-tested)
- [Where do the images come from?](#where-do-the-images-come-from)
- [I found an error in a book. What now?](#i-found-an-error-in-a-book-what-now)

## Which Claude plan do I need?

- **Claude app** (claude.ai, desktop): any plan, including Free, with code execution turned on: **Settings → Capabilities → Code execution and file creation**. On Team and Enterprise, an owner may have turned off uploading skills.
- **Claude Code:** a Pro, Max, Ultra, Team, Enterprise or Console account. The Free plan does not include Claude Code.

## Claude app or Claude Code?

Both write the same book. The difference is what Claude can run while writing:

| | Claude app | Claude Code |
| --- | --- | --- |
| Install | upload `syllabook.zip` once | two commands in the terminal |
| Code and commands in the book | run in Claude's sandbox; what needs your machine (Docker, servers, hardware) you run yourself and paste the output | run on your computer, with the real output |
| Best for | languages, practical skills, general knowledge | technology books |

On Windows, use Claude Code inside [WSL 2](integrations/wsl.md), so Linux commands run too.

## How do I update or remove Syllabook?

- **Claude Code:** update with `claude plugin marketplace update syllabook`, then `claude plugin update syllabook@syllabook`, and restart Claude Code. Remove it with `claude plugin uninstall syllabook@syllabook`.
- **Claude app:** download the new `syllabook.zip` from the [latest release](https://github.com/Joshpcbrrj/syllabook/releases/latest) and upload it in the Skills section of the settings, in place of the old one. To remove it, delete it in the same section.

Your books are not touched: they live in your library, not in the skill. What changed in each version is in the [CHANGELOG](../CHANGELOG.md).

## How much does a book cost?

On a subscription plan (Pro, Max...), a book costs nothing beyond your plan: it uses your usage limits. A long book usually takes more than one session; when a limit is reached, continue after it resets.

As a reference: in the Docker Compose pilot book (written with Claude Code, November 2026), each chapter used about US$ 2 to 2.50 at API prices, including the research, the tests of every command and the checks.

## Can I stop and continue later?

Yes. The progress of each book is saved in its `book.yaml`, chapter by chapter. In a new conversation, ask to continue the book (for example, "continue my Docker Compose book") and Syllabook picks up from the next chapter.

## Can I use it without GitHub?

Yes. Without a connection, Syllabook gives you a zip with the book, in the same folder layout as a library. You can keep the zip, read the Markdown, or upload it to a repository later ([GitHub guide](integrations/github.md)).

## Are my materials private?

- **Your files** (PDF, documents, Notion pages you send to improve) are used only as sources. They are never published.
- **The books** go to your library. The [library template](https://github.com/Joshpcbrrj/syllabook-library) is a public repository, because GitHub Pages and releases are free there. You can make it private, but then the website needs a paid GitHub plan.
- **The conversation** follows the privacy settings of your Claude account.

## Can I edit a book by hand?

Yes. Chapters are plain Markdown files in `chapters/`. After editing, ask Syllabook to check and publish the book: it runs the audit again, rebuilds the EPUB and the website, and points out anything your edit broke (a missing section, a broken link).

## Which topics and languages work?

- **Topics:** any. Syllabook adapts its teaching to four profiles: programming and math, languages, practical skills (music, electronics...) and general knowledge (such as history). For a topic that fits none, it builds a method of its own and explains it in the assessment.
- **Languages:** the conversation and the book can be in any language. Portuguese (Brazil) and English have their own style guides; in other languages it writes naturally and tells you there is no style guide yet.

## Is the code in the books tested?

Yes. Every command and every piece of code is run while the chapter is written, and the book shows the real output. What cannot run (a command for another operating system, for example) is marked "not run" in the text. That is why Claude Code, and WSL 2 on Windows, give better technology books.

## Where do the images come from?

- **Diagrams:** drawn by the skill's scripts as SVG, from a description of the structure (blocks, flows, timelines, chords...).
- **Photos:** only with a free license (public domain, CC0, CC BY, CC BY-SA), from Wikimedia Commons, with the author and license under the image.
- **Screenshots:** of the book's application actually running.

For now, Syllabook does not generate pictures with AI.

## I found an error in a book. What now?

- **In your own book:** ask Syllabook to fix it ("in chapter 3 of my Docker book, the port is wrong"). It changes the chapter, checks it again and records the change.
- **In how the skill works:** open an [issue](https://github.com/Joshpcbrrj/syllabook/issues/new/choose) in the Syllabook repository.
