# Security

**English** | [Português](SECURITY.pt-BR.md)

## Reporting a problem

If you find a security problem in the skill or the scripts (for example, something that exposes the user's tokens, passwords or files), **do not open a public issue**.

Use GitHub's private reporting: the repository's **Security** tab → **Report a vulnerability**. Describe the problem, how to reproduce it and its impact.

You will get a first answer within 7 days. When there is a fix, it goes into the [CHANGELOG](CHANGELOG.md) and the repository's security advisory.

## Practices the skill follows

- It never asks you to paste tokens, passwords or keys into the chat. Connections (GitHub, Notion, Google Drive) go through Claude's connectors.
- It does not download instructions from the internet while running: everything it follows comes in the installed package.
- Materials you send are used only as sources and are never published.

## Supported versions

Only the latest version of the skill receives fixes.
