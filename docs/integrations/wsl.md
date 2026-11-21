# WSL 2: a Linux to test code on Windows

**English** | [Português](wsl.pt-BR.md)

## What it is for

On Windows, the skill can only run what Windows runs. Most technology books use Linux commands (`bash`, `apt`, Docker, servers), and a command that was never run goes into the book marked "not run". The [WSL 2](https://learn.microsoft.com/en-us/windows/wsl/) (Windows Subsystem for Linux) gives you a real Linux inside Windows, without dual boot. With Claude Code installed in it, the skill runs every example and copies the real output into the book.

It also helps with the skill's own development:

- **Sandbox:** Claude Code runs commands in an isolated sandbox on Linux and WSL 2. On native Windows it runs them without one.
- **Evals:** case 6 of the [evals](../../evals/README.md) needs a shell, and the eval refuses Bash on Windows.
- **Docker:** with Docker Desktop's WSL integration, the same `docker` and `docker compose` work inside Ubuntu.

WSL is optional. Without it, the skill still writes the book: it tests what it can in PowerShell or Git Bash, asks you to run the rest (guided run) or marks it "not run".

## What you need

- Windows 11, or Windows 10 version 2004 or newer (build 19041 or higher).
- CPU virtualization turned on. Check it in **Task Manager → Performance → CPU**, on the **Virtualization** line.
- A PowerShell opened as administrator, for the install only.
- For Claude Code: a Pro, Max, Team, Enterprise or Console plan.

## Step by step

### 1. Install WSL and Ubuntu

In PowerShell as administrator (right-click the Start menu → **Terminal (Admin)**):

```powershell
# the name comes from the NAME column of this list
wsl --list --online
wsl --install -d Ubuntu-26.04
```

When it finishes, **restart Windows**. On the way back, Ubuntu finishes installing (open **Ubuntu** from the Start menu if it does not open by itself) and asks for a user name and a password:

- lowercase, no spaces or accents (for example, `ana`);
- the password does not show while you type: type it and press Enter.

This account belongs to Linux only. It has nothing to do with your Windows user.

### 2. Update Ubuntu and install the sandbox tools

In the Ubuntu terminal:

```bash
sudo apt update && sudo apt upgrade -y
# bubblewrap and socat: what Claude Code's sandbox needs on Linux
sudo apt install -y bubblewrap socat git
```

### 3. Install Claude Code as your user

Without `sudo`: the installer puts everything in your home folder (`~/.local`).

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Close and open the terminal, then check:

```bash
claude --version
```

If you get `claude: command not found`, `~/.local/bin` is not in the PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 4. Bring your library and install the skill

Keep your projects on the Linux disk (`~/projects`), not in `/mnt/c/...`: it is faster and avoids permission and line-ending problems.

```bash
mkdir -p ~/projects && cd ~/projects
git clone https://github.com/<you>/<your-library>.git
cd <your-library>
claude plugin marketplace add Joshpcbrrj/syllabook
claude plugin install syllabook@syllabook
claude
```

On the first run, Claude Code opens the login in the browser. If it does not open, copy the link from the terminal into the Windows browser. Then trust the library folder (**Yes, I trust this folder**).

### 5. (Optional) Docker inside Ubuntu

For books that use Docker: in Docker Desktop, open **Settings → Resources → WSL Integration**, turn on **Ubuntu-26.04** and click **Apply**. Docker keeps running in Docker Desktop. Ubuntu only gets the commands.

## How to check that it worked

In PowerShell:

```powershell
wsl -l -v
```

The `Ubuntu-26.04` line must show `2` in the `VERSION` column. In Ubuntu:

```bash
uname -r                       # ends in -microsoft-standard-WSL2
claude --version               # a version followed by (Claude Code)
claude plugin list             # lists syllabook@syllabook
docker compose version         # only if you did step 5
```

Output on the machine where this guide was tested (WSL 3.0.5, Ubuntu 26.04.1, November 2026):

```text
6.18.58.1-microsoft-standard-WSL2
2.1.330 (Claude Code)
Docker Compose version v5.7.0
```

## Common problems

| Symptom | Cause and fix |
| --- | --- |
| Error `0x80370102` when installing | Virtualization is off. Turn on Intel VT-x or AMD-V/SVM in the BIOS/UEFI, save, restart and install again |
| WSL says the distribution name is not valid | You typed the friendly name (`Ubuntu 26.04 LTS`). Use the `NAME` column: `Ubuntu-26.04` |
| `wsl --install` only shows the help text | WSL is already installed. Use `wsl --install -d Ubuntu-26.04` |
| `wsl -l -v` shows `VERSION 1` | Run `wsl --set-version Ubuntu-26.04 2` |
| `claude: command not found` | `~/.local/bin` missing from the PATH (step 3), or Claude Code was installed with `sudo`, in `/root`. Remove `/root/.local/bin/claude` and `/root/.local/share/claude` and install again as your user |
| The login, MCPs or plugins from Windows are missing in Ubuntu | The two installations are independent. Log in and configure again inside Ubuntu |
| Everything is slow, or files show up with changed permissions | The project is in `/mnt/c/...`. Move it to `~/projects` |
| `docker: command not found` in Ubuntu | Turn on the WSL integration in Docker Desktop (step 5) and open a new terminal |

Sources, checked on 2026-11-21: [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) and [Troubleshooting WSL](https://learn.microsoft.com/en-us/windows/wsl/troubleshooting) (Microsoft Learn), [Claude Code setup](https://code.claude.com/docs/en/setup), [Sandboxing](https://code.claude.com/docs/en/sandboxing) and [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).
