# Docling: convert documents on your computer

**English** | [Português](docling.pt-BR.md)

## What it is for

[Docling](https://github.com/docling-project/docling) converts PDF, DOCX, PPTX, HTML and images into Markdown, keeping headings, lists and tables. The skill uses the result as a source to create or improve a book. The documents and the converted files are **never published**.

Without Docling the skill still works: it reads an attached PDF directly or uses a simpler extraction, which loses part of the tables and structure.

## What you need

- Windows, macOS or Linux.
- `uv`, the program that downloads and runs Docling.
- For the first conversion, a few minutes and some disk space: Docling downloads its layout and text recognition (OCR) models.
- To use it **inside the chat**: the Claude desktop app. Docling installed on your computer **does not show up** in Claude in the browser.

## Step by step

**Shortcut:** the installers in [`install/`](../../install/) do steps 1 and 3 for you. On Windows: `powershell -ExecutionPolicy Bypass -File install-docling.ps1 -WithClaudeApp`; on macOS or Linux: `bash install-docling.sh --with-claude-app`. Leave the last option out if you only want the command line. They keep a backup of the Claude app's settings (`.bak`) before changing them.

### 1. Install `uv`

Check whether you already have it: `uv --version`. If it shows a version, skip to step 2.

- **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS or Linux** (terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

Close and reopen the terminal and run `uv --version` again. If the command is not found, the installer prints at the end the folder that must be added to PATH (usually `~/.local/bin`).

### 2. Convert from the terminal

This works in every case, and it is the most reliable path for large documents:

```powershell
cd $env:USERPROFILE\Downloads
uvx --from docling docling "material.pdf" --to md --output .
```

On macOS or Linux:

```bash
cd ~/Downloads
uvx --from docling docling "material.pdf" --to md --output .
```

The `.md` file appears next to the PDF. Attach it to the chat, or let the skill read it from the Downloads folder if that folder is shared with the app.

### 3. (Optional) Use it inside the chat, through the Claude app

1. Download everything first, so the first start does not take long:

   ```text
   uvx --from "docling-mcp[local]==2.1.0" --with "mcp<2" docling-mcp-server --help
   ```

2. In the Claude app: **Settings → Developer → Edit config**. In the file, put the block below at the **top level** (next to `"preferences"`, never inside it). Replace the `uvx` path with yours: on Windows it is shown by `(Get-Command uvx).Source`; on macOS and Linux, by `which uvx`.

   ```json
   "mcpServers": {
     "docling": {
       "command": "C:\\Users\\<user>\\.local\\bin\\uvx.exe",
       "args": ["--from", "docling-mcp[local]==2.1.0", "--with", "mcp<2",
                "docling-mcp-server", "--transport", "stdio"],
       "env": {"DOCLING_CONVERSION_MODE": "local",
               "DOCLING_MCP_CONVERSION_MODE": "local"}
     }
   }
   ```

3. Quit Claude completely (including the system tray) and open it again. The first start takes about 1 minute.

## How to check that it worked

- **Terminal:** the command in step 2 creates the `.md` file without errors.
- **Claude app:** in **Settings → Developer**, the `docling` server shows as connected. In a chat, ask it to list the Docling tools.

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| `No module named 'mcp.server.fastmcp'`; the app shows "Connection closed" | `docling-mcp` 2.x pulls version 2.x of the `mcp` library, whose API changed. Keep `--with "mcp<2"` |
| `DOCLING_SERVICE_URL must be set for remote mode` | Remote mode is the default. Use the `[local]` extra and the local-mode `env` from step 3 |
| The server does not connect, with no clear error | `--transport stdio` is missing |
| The app ignores the server | The `mcpServers` block ended up inside `preferences`, or the JSON became invalid |
| Conversion through the chat times out | The app bridge waits about 80 s per call. For a large document or the first conversion, use the terminal (step 2) and do not repeat the call |
| Code comes out on a single line | A Docling limitation with code in PDFs. Ask the skill to restore the line breaks from the logic, or use the original code |
| Antivirus warning during installation | Check the threat name and path in the protection history **before** allowing anything. Files in the `uv` cache are often false positives, but confirm |

**Where the app logs are** (Windows): `%LOCALAPPDATA%\Claude\logs` or `%APPDATA%\Claude\logs`, in the file `mcp-server-docling.log`.
