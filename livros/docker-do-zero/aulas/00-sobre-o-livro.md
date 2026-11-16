# Sobre o livro

> 🤖 Livro criado com IA a partir de fontes públicas, citadas em cada capítulo. Conferido em 2026-11-15, com Docker Desktop 4.96 e Docker Engine 29.9.

Este livro é para quem programa e nunca usou contêineres. Começa pela instalação no Windows (Docker Desktop com WSL 2), no Linux e no Mac, compara a interface com a linha de comando e segue por imagens, Dockerfile, builds enxutos, volumes, redes e publicação, até uma API com banco PostgreSQL rodando em contêineres.

Vai usar no Windows? O livro *WSL do zero*, da mesma biblioteca, prepara o Linux no Windows que o Docker Desktop usa por baixo.

## Como o livro está organizado

| Parte | Capítulos | O que você faz |
| --- | --- | --- |
| Começar | 1 a 3 | Entende o que é um contêiner e instala o Docker no Windows, no Linux ou no Mac |
| Usar contêineres | 4 e 5 | Roda e observa contêineres pela linha de comando e pelo Docker Desktop |
| Construir imagens | 6 a 8 | Entende imagens, escreve o primeiro Dockerfile e deixa o build rápido e enxuto |
| Dados, redes e publicação | 9 a 11 | Guarda dados em volumes, liga contêineres numa rede e publica a imagem |
| Projeto final | 12 e 13 | Sobe uma API com PostgreSQL e vê os próximos livros da trilha |

## Legenda

- 🗺️ **Neste capítulo**: o que a página cobre, logo no início
- 💡 analogia ou dica importante
- ⚠️ cuidado, correção ou comando que não foi executado na produção do livro
- 🧪 **Laboratório**: passo a passo para fazer no seu computador
- 🏋️ **Pratique**: exercícios; as respostas ficam recolhidas em **Ver resposta**
- 📚 **Fontes**: de onde veio cada informação, com a data da conferência
- 📌 **Resumo**: tabela de revisão, no final
- 🧭 **Cheat sheet**: o livro inteiro em 12 cards (capítulo 13)

## Resumo do livro

| Parte | Ideia central | Comandos-chave |
| --- | --- | --- |
| Começar | Contêiner é um processo isolado que divide o kernel | `docker version` |
| Usar contêineres | A CLI repete e automatiza; a interface ajuda a observar | `docker run -d -p`, `logs`, `exec` |
| Construir imagens | A ordem do Dockerfile decide o cache | `docker build`, multi-stage |
| Dados, redes e publicação | Volume guarda; rede própria resolve nomes; push publica | `volume`, `network`, `push` |
| Projeto final | API e banco separados, ligados pela rede | `tarefas-net`, `compose.yaml` |
