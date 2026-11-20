# Installs uv and Docling for Syllabook on Windows, and optionally adds Docling to the Claude app.
#
# Usage (PowerShell, in this folder):
#   powershell -ExecutionPolicy Bypass -File install-docling.ps1
#   powershell -ExecutionPolicy Bypass -File install-docling.ps1 -WithClaudeApp
#
# Guide: docs/integrations/docling.md
param([switch]$WithClaudeApp)
$ErrorActionPreference = 'Stop'

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host 'Installing uv (it downloads and runs Docling)...'
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    # the installer adds this folder to PATH for new terminals; add it to this one too
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}
uv --version

Write-Host 'Installing Docling. The first conversion downloads its models and can take a few minutes.'
uv tool install --upgrade docling
docling --version

if ($WithClaudeApp) {
    Write-Host 'Preparing the Docling server for the Claude app (downloads everything now)...'
    uvx --from "docling-mcp[local]==2.1.0" --with "mcp<2" docling-mcp-server --help | Out-Null
    $helper = Join-Path $PSScriptRoot 'add_docling_to_claude.py'
    uv run --no-project python "$helper"
}

Write-Host ''
Write-Host 'Done. Test it: docling "some-file.pdf" --to md --output .'
