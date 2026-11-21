<!-- translation-of: wsl.md sha256:b07e0a956980 -->
# WSL 2: um Linux para testar código no Windows

[English](wsl.md) | **Português**

## Para que serve

No Windows, a skill só consegue rodar o que o Windows roda. A maioria dos livros de tecnologia usa comandos de Linux (`bash`, `apt`, Docker, servidores), e um comando que não foi executado entra no livro marcado como "não executado". O [WSL 2](https://learn.microsoft.com/pt-br/windows/wsl/) (Subsistema do Windows para Linux) dá a você um Linux de verdade dentro do Windows, sem dual boot. Com o Claude Code instalado nele, a skill executa cada exemplo e copia a saída real para o livro.

Ele também ajuda no desenvolvimento da própria skill:

- **Sandbox:** o Claude Code roda os comandos numa sandbox isolada no Linux e no WSL 2. No Windows nativo, roda sem ela.
- **Avaliações:** o caso 6 das [avaliações](../../evals/README.md) precisa de um shell, e o eval recusa o Bash no Windows.
- **Docker:** com a integração WSL do Docker Desktop, os mesmos `docker` e `docker compose` funcionam dentro do Ubuntu.

O WSL é opcional. Sem ele, a skill escreve o livro do mesmo jeito: testa o que dá no PowerShell ou no Git Bash, pede que você rode o resto (execução guiada) ou marca como "não executado".

## O que você precisa

- Windows 11, ou Windows 10 versão 2004 ou mais nova (build 19041 ou maior).
- A virtualização do processador ligada. Confira no **Gerenciador de Tarefas → Desempenho → CPU**, na linha **Virtualização**.
- Um PowerShell aberto como administrador, só para a instalação.
- Para o Claude Code: um plano Pro, Max, Team, Enterprise ou Console.

## Passo a passo

### 1. Instalar o WSL e o Ubuntu

No PowerShell como administrador (botão direito no menu Iniciar → **Terminal (Admin)**):

```powershell
# o nome vem da coluna NAME desta lista
wsl --list --online
wsl --install -d Ubuntu-26.04
```

Quando terminar, **reinicie o Windows**. Na volta, o Ubuntu termina de se instalar (abra **Ubuntu** pelo menu Iniciar se ele não abrir sozinho) e pede um nome de usuário e uma senha:

- em minúsculas, sem espaço nem acento (por exemplo, `ana`);
- a senha não aparece enquanto você digita: digite e aperte Enter.

Essa conta é só do Linux e não tem relação com o seu usuário do Windows.

### 2. Atualizar o Ubuntu e instalar o que a sandbox usa

No terminal do Ubuntu:

```bash
sudo apt update && sudo apt upgrade -y
# bubblewrap e socat: o que a sandbox do Claude Code usa no Linux
sudo apt install -y bubblewrap socat git
```

### 3. Instalar o Claude Code como o seu usuário

Sem `sudo`: o instalador põe tudo na sua pasta pessoal (`~/.local`).

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Feche e abra o terminal e confira:

```bash
claude --version
```

Se aparecer `claude: command not found`, falta o `~/.local/bin` no PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### 4. Trazer a sua biblioteca e instalar a skill

Guarde os projetos no disco do Linux (`~/projetos`), não em `/mnt/c/...`: é mais rápido e evita problemas de permissão e de quebra de linha.

```bash
mkdir -p ~/projetos && cd ~/projetos
git clone https://github.com/<você>/<sua-biblioteca>.git
cd <sua-biblioteca>
claude plugin marketplace add Joshpcbrrj/syllabook
claude plugin install syllabook@syllabook
claude
```

Na primeira vez, o Claude Code abre o login no navegador. Se ele não abrir, copie o link do terminal e abra no navegador do Windows. Depois, confie na pasta da biblioteca (**Yes, I trust this folder**).

### 5. (Opcional) Docker dentro do Ubuntu

Para livros que usam Docker: no Docker Desktop, abra **Settings → Resources → WSL Integration**, ligue o **Ubuntu-26.04** e clique em **Apply**. O Docker continua rodando no Docker Desktop, e o Ubuntu só recebe os comandos.

## Como conferir que funcionou

No PowerShell:

```powershell
wsl -l -v
```

A linha do `Ubuntu-26.04` precisa mostrar `2` na coluna `VERSION`. No Ubuntu:

```bash
uname -r                       # termina em -microsoft-standard-WSL2
claude --version               # uma versão seguida de (Claude Code)
claude plugin list             # lista o syllabook@syllabook
docker compose version         # só se você fez o passo 5
```

Saída na máquina em que este guia foi testado (WSL 3.0.5, Ubuntu 26.04.1, novembro de 2026):

```text
6.18.58.1-microsoft-standard-WSL2
2.1.330 (Claude Code)
Docker Compose version v5.7.0
```

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| Erro `0x80370102` na instalação | A virtualização está desligada. Ligue Intel VT-x ou AMD-V/SVM na BIOS/UEFI, salve, reinicie e instale de novo |
| O WSL diz que o nome da distribuição não é válido | Você digitou o nome amigável (`Ubuntu 26.04 LTS`). Use o da coluna `NAME`: `Ubuntu-26.04` |
| `wsl --install` só mostra o texto de ajuda | O WSL já está instalado. Use `wsl --install -d Ubuntu-26.04` |
| `wsl -l -v` mostra `VERSION 1` | Rode `wsl --set-version Ubuntu-26.04 2` |
| `claude: command not found` | Falta o `~/.local/bin` no PATH (passo 3), ou o Claude Code foi instalado com `sudo`, em `/root`. Apague `/root/.local/bin/claude` e `/root/.local/share/claude` e instale de novo como o seu usuário |
| O login, os MCPs ou os plugins do Windows não aparecem no Ubuntu | As duas instalações são independentes. Entre e configure de novo dentro do Ubuntu |
| Tudo fica lento, ou os arquivos aparecem com permissões trocadas | O projeto está em `/mnt/c/...`. Mova para `~/projetos` |
| `docker: command not found` no Ubuntu | Ligue a integração WSL no Docker Desktop (passo 5) e abra um terminal novo |

Fontes, conferidas em 2026-11-21: [Instalar o WSL](https://learn.microsoft.com/pt-br/windows/wsl/install) e [Solução de problemas do WSL](https://learn.microsoft.com/pt-br/windows/wsl/troubleshooting) (Microsoft Learn), [Claude Code setup](https://code.claude.com/docs/en/setup), [Sandboxing](https://code.claude.com/docs/en/sandboxing) e [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).
