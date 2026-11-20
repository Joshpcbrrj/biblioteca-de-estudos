<!-- translation-of: google-drive.md sha256:2717bf01f932 -->
# Google Drive: usar os seus arquivos como fonte

[English](google-drive.md) | **Português**

## Para que serve

Ao criar ou aprimorar um livro, o Syllabook pode buscar no seu Google Drive materiais sobre o tema (Documentos, Apresentações e Planilhas Google e outros arquivos), listar o que encontrou e usar como fonte os arquivos que você escolher. Ele só lê: nada no seu Drive é alterado, copiado para o livro ou publicado.

## O que você precisa

- Uma conta Google.
- O app do Claude ou o claude.ai num plano que ofereça o conector do Google Drive (a Anthropic o lista para Pro, Max, Team e Enterprise; no Team e no Enterprise, um administrador o ativa antes).

## Passo a passo

1. **Configurações → Conectores**, procure o **Google Drive** e escolha **Conectar**.
2. Entre com a sua conta Google e libere o acesso.
3. Num chat, deixe o Google Drive ligado no menu de conectores.

No **Claude Code**, ou sem o conector, baixe os arquivos e anexe no chat, ou coloque-os numa pasta e passe o caminho dela ao Syllabook.

## Como conferir que funcionou

Peça ao Claude para "buscar no meu Google Drive sobre <um tema>". Devem aparecer nomes de arquivos do seu Drive.

## Problemas comuns

| Sintoma | Causa e correção |
| --- | --- |
| Tabelas ou imagens de um PDF saem erradas | O conector lê só o texto. Baixe o PDF e converta com o Docling ([guia](docling.pt-BR.md)) |
| Um Documento ou Planilha grande vem cortado | Exportações acima de cerca de 10 MB não são lidas inteiras. Divida o arquivo ou baixe-o |
| O Google Drive não aparece na lista de conectores | O seu plano ou a sua organização não o oferece. Baixe os arquivos |
