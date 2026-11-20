# Library skeleton

The skill copies these files into the user's library repository when it does not have them yet (`modes/PUBLISH.md` §2). Never overwrite a file that already exists there, and never copy this note (`SKELETON.md`).

| File | Where it goes |
| --- | --- |
| `README.md`, `README.pt-BR.md` | repository root: the library's front page; replace `<user>` and `<repository>` in the site address |
| `LICENSE`, `LICENSE-CODIGO` | repository root: CC BY-SA 4.0 for the content, MIT for code; the user may choose others |
| `library.yaml` | repository root; the skill fills `author`, `repository`, `commit_name` and `commit_email` |
| `created-books/`, `improved-materials/`, `site/` | repository root, with their READMEs in English and Portuguese |
| `.github/workflows/epub.yml` | builds one EPUB per book on every push and publishes it on the `epub_release` release |
| `.github/workflows/site.yml` | builds the website with Zensical and publishes it on GitHub Pages (the user turns Pages on once: Settings → Pages → Source: GitHub Actions) |

Both workflows do nothing while the library has no books. They use the scripts in the repository when it has a copy of the skill, and otherwise download the latest Syllabook release.
