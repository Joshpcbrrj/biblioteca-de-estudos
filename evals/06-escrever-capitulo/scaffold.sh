#!/usr/bin/env bash
# Prepares a library with an approved book whose chapters 0 and 1 are written and chapter 2 is not.
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
root="${CLAUDE_PLUGIN_ROOT:-$here/../..}"
book=created-books/python-do-zero-teste
mkdir -p created-books
cp -r "$root/tests/fixtures/sample-book" "$book"
cp "$root/skills/syllabook/assets/library/library.yaml" library.yaml
rm -f "$book/chapters/02-o-laco-for.md" "$book/chapters/03-simulado-final.md" "$book/chapters/glossario.md"
py="$(command -v python3 || command -v python)"
"$py" - "$book/book.yaml" <<'PY'
import sys, yaml
path = sys.argv[1]
data = yaml.safe_load(open(path, encoding='utf-8'))
data['progress'] = [{'n': 1, 'done': '2026-11-20',
                     'summary': 'Listas: criar uma lista de notas, len conta os itens, o índice começa em 0.'}]
yaml.safe_dump(data, open(path, 'w', encoding='utf-8'), allow_unicode=True, sort_keys=False)
PY
