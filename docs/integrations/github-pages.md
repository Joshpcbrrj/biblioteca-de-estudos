# GitHub Pages: the website with every book

**English** | [Português](github-pages.pt-BR.md)

## What it is for

A website with all your books: instant search across every book, chapters in a side menu, code with a copy button, answers that open on click, dark mode and a link to each EPUB. It reads well on a computer, a phone and an e-reader's browser. See the [demo website](https://joshpcbrrj.github.io/syllabook-demo/).

## What you need

- Your library repository on GitHub ([guide](github.md)), **public**: GitHub Pages is free for public repositories; private ones need a paid GitHub plan.
- The workflow `.github/workflows/site.yml`, which Syllabook adds with the library.

## Step by step

1. In your repository on github.com: **Settings → Pages**.
2. Under **Build and deployment → Source**, choose **GitHub Actions**. That is all: there is nothing else to fill in.
3. Publish a book (or open **Actions → Website → Run workflow**). The workflow builds the site with [Zensical](https://zensical.org/) and publishes it.

Your address is `https://<your-username>.github.io/<repository-name>/`.

## How to check that it worked

- **Actions → Website**: the latest run is green, with two jobs, *build* and *deploy*.
- **Settings → Pages** shows "Your site is live at ..." with the address.
- Open the address and search for a word from one of your books.

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| The address shows a 404 page | The first deploy has not run yet. Run **Actions → Website → Run workflow** and wait for it to finish |
| The *deploy* job fails with a Pages error | Pages is not set to **GitHub Actions** (step 2), or the repository is private on a free plan |
| The website workflow runs but publishes nothing | The library has no books yet: the workflow waits for the first `book.yaml` |
| A new book does not show up | The workflow runs only when a book, `site/` or `library.yaml` changes. Run it by hand from **Actions** |
