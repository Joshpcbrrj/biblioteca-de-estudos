# Docling: converter documentos no seu computador

## Para que serve

O [Docling](https://github.com/docling-project/docling) converte PDF, DOCX, PPTX, HTML e imagens em Markdown, mantendo títulos, listas e tabelas. A skill usa o resultado como fonte para criar ou aprimorar um livro. Os documentos e os arquivos convertidos **não são publicados**.

Sem o Docling, a skill continua funcionando: lê o PDF anexado direto ou usa uma extração mais simples, que perde parte das tabelas e da estrutura.

## O que você precisa

- Windows, macOS ou Linux.
- O `uv`, programa que baixa e roda o Docling.
- Na primeira conversão, alguns minutos e espaço em disco: o Docling baixa os modelos de layout e de leitura de texto (OCR).
- Para usar **dentro do chat**: o app do Claude no computador. O Docling instalado no seu computador **não aparece** no Claude pelo navegador.

## Passo a passo

### 1. Instalar o `uv`

Confira se já tem: `uv --version`. Se mostrar a versão, pule para o passo 2.

- **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
- **macOS ou Linux** (terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`

Feche e abra o terminal e rode `uv --version` de novo. Se o comando não for encontrado, o instalador mostra no fim a pasta que precisa entrar no PATH (normalmente `~/.local/bin`).

### 2. Converter pelo terminal

Funciona em qualquer caso, e é o caminho mais confiável para documentos grandes:

```powershell
cd $env:USERPROFILE\Downloads
uvx --from docling docling "material.pdf" --to md --output .
```

No macOS ou no Linux:

```bash
cd ~/Downloads
uvx --from docling docling "material.pdf" --to md --output .
```

O `.md` aparece ao lado do PDF. Anexe esse arquivo no chat, ou deixe a skill ler pela pasta Downloads, se ela estiver liberada no app.

### 3. (Opcional) Usar dentro do chat, pelo app do Claude

1. Baixe tudo antes, para a primeira inicialização não demorar:

   ```text
   uvx --from "docling-mcp[local]==2.1.0" --with "mcp<2" docling-mcp-server --help
   ```

2. No app do Claude: **Configurações → Desenvolvedor → Editar configuração**. No arquivo, ponha o bloco abaixo no **nível principal** (ao lado de `"preferences"`, nunca dentro dele). Troque o caminho do `uvx` pelo seu: no Windows, ele aparece com `(Get-Command uvx).Source`; no macOS e no Linux, com `which uvx`.

   ```json
   "mcpServers": {
     "docling": {
       "command": "C:\\Users\\<usuario>\\.local\\bin\\uvx.exe",
       "args": ["--from", "docling-mcp[local]==2.1.0", "--with", "mcp<2",
                "docling-mcp-server", "--transport", "stdio"],
       "env": {"DOCLING_CONVERSION_MODE": "local",
               "DOCLING_MCP_CONVERSION_MODE": "local"}
     }
   }
   ```

3. Feche o Claude por completo (inclusive na bandeja do sistema) e abra de novo. A primeira inicialização leva cerca de 1 minuto.

## Como conferir que funcionou

- **Terminal:** o comando do passo 2 cria o arquivo `.md` sem erro.
- **App do Claude:** em **Configurações → Desenvolvedor**, o servidor `docling` aparece como conectado. Num chat, peça para listar as ferramentas do Docling.

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| `No module named 'mcp.server.fastmcp'`; o app mostra "Connection closed" | O `docling-mcp` 2.x puxa a biblioteca `mcp` 2.x, que mudou. Mantenha `--with "mcp<2"` |
| `DOCLING_SERVICE_URL must be set for remote mode` | O padrão é o modo remoto. Use o extra `[local]` e o `env` de modo local do passo 3 |
| O servidor não conecta, sem erro claro | Falta `--transport stdio` |
| O app ignora o servidor | O bloco `mcpServers` ficou dentro de `preferences`, ou o JSON ficou inválido |
| A conversão pelo chat estoura o tempo | A ponte do app espera cerca de 80 s por chamada. Documento grande ou primeira conversão: use o terminal (passo 2) e não repita a chamada |
| Código vem numa linha só | Limitação do Docling com código em PDF. Peça à skill para refazer as quebras pela lógica ou use o código original |
| Aviso do antivírus na instalação | Veja o nome da ameaça e o caminho no histórico de proteção **antes** de liberar. Arquivos do cache do `uv` costumam ser falso positivo, mas confirme |

**Onde ficam os logs do app** (Windows): `%LOCALAPPDATA%\Claude\logs` ou `%APPDATA%\Claude\logs`, no arquivo `mcp-server-docling.log`.
