#!/usr/bin/env bash
# Installs uv and Docling for Syllabook on macOS or Linux, and optionally adds Docling to the Claude app.
#
# Usage (in this folder):
#   bash install-docling.sh
#   bash install-docling.sh --with-claude-app
#
# Guide: docs/integrations/docling.md
set -euo pipefail

if ! command -v uv >/dev/null 2>&1; then
  echo "Installing uv (it downloads and runs Docling)..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  # the installer adds this folder to PATH for new terminals; add it to this one too
  export PATH="$HOME/.local/bin:$PATH"
fi
uv --version

echo "Installing Docling. The first conversion downloads its models and can take a few minutes."
uv tool install --upgrade docling
docling --version

if [ "${1:-}" = "--with-claude-app" ]; then
  echo "Preparing the Docling server for the Claude app (downloads everything now)..."
  uvx --from "docling-mcp[local]==2.1.0" --with "mcp<2" docling-mcp-server --help >/dev/null
  uv run --no-project python "$(dirname "$0")/add_docling_to_claude.py"
fi

echo
echo "Done. Test it: docling \"some-file.pdf\" --to md --output ."
