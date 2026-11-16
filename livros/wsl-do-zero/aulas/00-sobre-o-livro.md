# Sobre o livro

> 🤖 Livro criado com IA a partir de fontes públicas, citadas em cada capítulo, e do guia pessoal do autor. Conferido em 2026-11-15, com WSL 3.0 e Ubuntu 26.04 LTS.

Este livro é para quem usa Windows e quer um Linux de verdade para programar, sem dual boot e sem montar uma máquina virtual à mão. O caminho vai da instalação do WSL e do Ubuntu à personalização do terminal, às ferramentas de desenvolvimento, ao backup do ambiente e ao Claude Code, e termina com um projeto criado com o Spec Kit.

## Como o livro está organizado

| Parte | Capítulos | O que você faz |
| --- | --- | --- |
| Instalar e conhecer | 1 a 3 | Entende o WSL, instala o Ubuntu e usa os primeiros comandos sem trabalhar como root |
| Montar o ambiente | 4 a 6 | Escolhe onde guardar os arquivos, personaliza o terminal e instala as ferramentas |
| Cuidar do ambiente | 7 e 8 | Limita recursos, resolve problemas e faz backup que volta |
| Programar com IA | 9 a 11 | Usa o Claude Code, cria um projeto com o Spec Kit e vê os próximos livros |

## Legenda

- 🗺️ **Neste capítulo**: o que a página cobre, logo no início
- 💡 analogia ou dica importante
- ⚠️ cuidado, correção ou comando que não foi executado na produção do livro
- 🧪 **Laboratório**: passo a passo para fazer no seu computador
- 🏋️ **Pratique**: exercícios; as respostas ficam recolhidas em **Ver resposta**
- 📚 **Fontes**: de onde veio cada informação, com a data da conferência
- 📌 **Resumo**: tabela de revisão, no final
- 🧭 **Cheat sheet**: o livro inteiro em 12 cards (capítulo 11)

## Resumo do livro

| Parte | Ideia central | Comandos-chave |
| --- | --- | --- |
| Instalar e conhecer | O WSL 2 roda um kernel Linux real numa VM leve | `wsl --install -d Ubuntu-26.04`, `wsl -l -v` |
| Montar o ambiente | Projetos e ferramentas ficam do lado Linux | `~/projetos`, `nvm`, `sdk`, `uv` |
| Cuidar do ambiente | Ajustes no .wslconfig e no wsl.conf; backup é export e import | `wsl --shutdown`, `wsl --export` |
| Programar com IA | Claude Code como usuário; spec diz o quê, plan diz como | `claude`, `/speckit-specify` |
