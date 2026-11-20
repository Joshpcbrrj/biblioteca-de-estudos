# Library skeleton

The skill copies these files into the user's library repository when it does not have them yet (`modes/PUBLISH.md` §2). Never overwrite a file that already exists there.

| File | Where it goes |
| --- | --- |
| `library.yaml` | repository root; the skill fills `author`, `repository`, `commit_name` and `commit_email` |
| `created-books/`, `improved-materials/`, `site/` | repository root, with their READMEs in English and Portuguese |

The workflows that build the EPUB and the website are added in phase 3 of the rebuild.
