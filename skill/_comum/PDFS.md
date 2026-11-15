# PDFs do curso com o Docling (opcional)

> Arquivo comum às skills da biblioteca. Leia na etapa Levantar, só se o curso tiver PDFs de aula, de lista de exercícios ou de ementa.

**Para que serve:** os PDFs do curso costumam trazer o que as anotações não trazem: o **enunciado exato** de cada exercício e a **ementa**. Convertidos para Markdown, eles permitem conferir se cada resolução responde ao que foi pedido e se o curso cobre o que promete (etapa Escopo). Os PDFs e os `.md` gerados servem **só de fonte**: nunca são publicados nem colados nas aulas.

**Se não houver Docling:** siga sem este passo e registre no resumo final que os PDFs não foram conferidos.

## Como pedir ao usuário

1. Liste os PDFs do curso (blocos `<pdf>` das páginas) com o nome da aula de cada um.
2. Peça que baixe esses PDFs para a pasta **Downloads**, com nomes simples (`lista-1.pdf`, `lista-2.pdf`, `ementa.pdf`).
3. Passe o comando pronto, já com os nomes. No Windows, no PowerShell:

   ```powershell
   cd $env:USERPROFILE\Downloads
   foreach ($f in "lista-1.pdf","lista-2.pdf") {
     uvx --from docling docling $f --to md --output .
   }
   ```

   No macOS ou no Linux: `cd ~/Downloads && for f in lista-1.pdf lista-2.pdf; do uvx --from docling docling "$f" --to md --output .; done`.

4. Quando o usuário avisar, leia os `.md` gerados ao lado de cada PDF (`device_list_dir` e `device_stage_files`, ou peça que anexe os arquivos).

**Na primeira vez**, o Docling baixa os modelos de layout e de OCR e pode levar alguns minutos. Depois, uma lista leva segundos.

## O que esperar do resultado

| Parte do PDF | Qualidade |
| --- | --- |
| Títulos, parágrafos e listas | Boa: estrutura e acentos preservados |
| Tabelas | Boa: linhas e colunas certas |
| Imagens escaneadas | Texto por OCR; confira números e símbolos |
| Código | Às vezes vem numa linha só. A opção `--enrich-code` só ajuda quando o trecho está visualmente marcado como código. Refaça as quebras pela lógica, ou use o código do Notion e dos arquivos `.por` |

## Pelo servidor MCP (só para PDFs pequenos)

Se o Docling estiver conectado como servidor MCP no app do computador (ferramentas `docling__convert_document_into_docling_document` e `docling__export_docling_document_to_markdown`), dá para converter sem o terminal. Mas a ponte com o computador espera **no máximo ~80 s** por resposta. PDF grande, ou a primeira conversão (que baixa os modelos), estoura esse limite. Se der tempo esgotado, **não repita a chamada**: use o terminal.

## Instalar e configurar (para o usuário)

1. Instale o `uv` (o gerenciador que baixa e roda o Docling), se ainda não tiver:
   - confira com `uv --version`; se mostrar a versão, pule este passo;
   - **Windows** (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`;
   - **macOS ou Linux** (terminal): `curl -LsSf https://astral.sh/uv/install.sh | sh`;
   - feche e abra o terminal de novo e confira com `uv --version`. Se o comando não for encontrado, o instalador mostra no fim a pasta que precisa entrar no PATH (normalmente `~/.local/bin`).
2. O comando do terminal acima já basta para converter. Para ter também o servidor MCP no app do Claude:
   - desinstale a extensão "Docling MCP", se houver;
   - baixe tudo antes: `uvx --from "docling-mcp[local]==2.1.0" --with "mcp<2" docling-mcp-server --help`;
   - em **Configurações → Desenvolvedor → Editar configuração**, ponha no **nível principal** do arquivo (ao lado de `"preferences"`, nunca dentro dele):

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

   O caminho do `uvx` sai de `(Get-Command uvx).Source`. Depois, feche o Claude por completo (inclusive na bandeja) e abra de novo. A primeira inicialização leva cerca de 1 minuto.

## Problemas conhecidos

| Sintoma no log ou na tela | Causa e correção |
| --- | --- |
| `No module named 'mcp.server.fastmcp'`; o app só mostra "Connection closed" | O `docling-mcp` 2.x puxa a biblioteca `mcp` 2.x, que mudou de API. Fixe `--with "mcp<2"` |
| `DOCLING_SERVICE_URL must be set for remote mode` | O padrão é o modo remoto. Use o extra `[local]` e o `env` de modo local mostrados acima |
| O servidor não conecta, sem erro claro | O padrão do transporte é `streamable-http`; o app precisa de `--transport stdio` |
| O app ignora o servidor | O bloco `mcpServers` está dentro de `preferences` ou o JSON ficou inválido (chave sobrando). Ele vai no nível principal |
| Tempo esgotado na conversão pelo chat | Limite de ~80 s da ponte. Use o terminal |
| Aviso do antivírus durante a instalação | Veja o nome da ameaça e o caminho no histórico de proteção **antes** de liberar qualquer coisa. Arquivos do cache do `uv`/`torch` costumam ser falso positivo, mas confirme |

**Onde ficam os logs** (Windows): `%APPDATA%\Claude\logs`; na instalação pela Microsoft Store, em `%LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude\logs`. O arquivo é `mcp-server-<nome>.log`. Para achar e copiar para Downloads:

```powershell
Get-ChildItem $env:APPDATA, $env:LOCALAPPDATA -Recurse -Filter "*.log" -ErrorAction SilentlyContinue |
  Where-Object { $_.Name -like "*ocling*" } |
  ForEach-Object { Copy-Item $_.FullName "$env:USERPROFILE\Downloads\" -Force }
```
