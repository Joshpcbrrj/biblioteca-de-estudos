<!-- translation-of: SECURITY.md sha256:6e873c3d4bf7 -->
# Segurança

[English](SECURITY.md) | **Português**

## Como relatar um problema

Se você encontrar um problema de segurança na skill ou nos scripts (por exemplo, algo que exponha tokens, senhas ou arquivos do usuário), **não abra uma issue pública**.

Use o relato privado do GitHub: aba **Security** do repositório → **Report a vulnerability**. Descreva o problema, como reproduzi-lo e o impacto.

A resposta inicial vem em até 7 dias. Quando houver correção, ela entra no [CHANGELOG](CHANGELOG.md) e no aviso de segurança do repositório.

## Boas práticas que a skill segue

- Nunca pede que você cole tokens, senhas ou chaves no chat. As conexões são feitas pelos conectores do Claude (Notion, Google Drive e GitHub no app do Claude) ou pelo seu próprio login no Claude Code (`gh auth login` para o GitHub).
- Não baixa instruções da internet durante o uso: tudo o que a skill segue vem no pacote instalado.
- Materiais que você envia servem só de fonte: os arquivos originais nunca são publicados. No modo Aprimorar, o livro aprimorado vai para a sua biblioteca como qualquer outro livro.

## Versões com suporte

Só a versão mais recente da skill recebe correções.
