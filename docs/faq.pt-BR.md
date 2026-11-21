<!-- translation-of: faq.md sha256:5a0b8e39b6a1 -->
# Perguntas frequentes

[English](faq.md) | **Português**

## Conteúdo

- [Qual plano do Claude eu preciso?](#qual-plano-do-claude-eu-preciso)
- [App do Claude ou Claude Code?](#app-do-claude-ou-claude-code)
- [Como atualizo ou removo o Syllabook?](#como-atualizo-ou-removo-o-syllabook)
- [Quanto custa um livro?](#quanto-custa-um-livro)
- [Posso parar e continuar depois?](#posso-parar-e-continuar-depois)
- [Dá para usar sem GitHub?](#dá-para-usar-sem-github)
- [Meus materiais ficam privados?](#meus-materiais-ficam-privados)
- [Posso editar um livro à mão?](#posso-editar-um-livro-à-mão)
- [Que temas e idiomas funcionam?](#que-temas-e-idiomas-funcionam)
- [O código dos livros é testado?](#o-código-dos-livros-é-testado)
- [De onde vêm as imagens?](#de-onde-vêm-as-imagens)
- [Achei um erro num livro. E agora?](#achei-um-erro-num-livro-e-agora)

## Qual plano do Claude eu preciso?

- **App do Claude** (claude.ai, desktop): qualquer plano, inclusive o grátis, com a execução de código ligada: **Configurações → Capacidades → Execução de código e criação de arquivos** (no app em inglês: *Settings → Capabilities → Code execution and file creation*). Nos planos Team e Enterprise, um administrador pode ter desligado o envio de skills.
- **Claude Code:** uma conta Pro, Max, Ultra, Team, Enterprise ou Console. O plano grátis não inclui o Claude Code.

## App do Claude ou Claude Code?

Os dois escrevem o mesmo livro. A diferença é o que o Claude consegue executar enquanto escreve:

| | App do Claude | Claude Code |
| --- | --- | --- |
| Instalação | enviar o `syllabook.zip` uma vez | dois comandos no terminal |
| Código e comandos do livro | rodam na sandbox do Claude; o que precisa da sua máquina (Docker, servidores, hardware) você roda e cola a saída | rodam no seu computador, com a saída real |
| Melhor para | idiomas, habilidades práticas, conhecimento geral | livros de tecnologia |

No Windows, use o Claude Code dentro do [WSL 2](integrations/wsl.pt-BR.md), para que os comandos de Linux também rodem.

## Como atualizo ou removo o Syllabook?

- **Claude Code:** atualize com `claude plugin marketplace update syllabook` e depois `claude plugin update syllabook@syllabook`, e reinicie o Claude Code. Para remover: `claude plugin uninstall syllabook@syllabook`.
- **App do Claude:** baixe o `syllabook.zip` novo da [versão mais recente](https://github.com/Joshpcbrrj/syllabook/releases/latest) e envie na seção de Skills das configurações, no lugar do antigo. Para remover, apague a skill nessa mesma seção.

Os seus livros não são afetados: eles ficam na sua biblioteca, não na skill. O que mudou em cada versão está no [CHANGELOG](../CHANGELOG.md) (em inglês).

## Quanto custa um livro?

Num plano por assinatura (Pro, Max...), o livro não custa nada além do plano: ele gasta os seus limites de uso. Um livro longo costuma levar mais de uma sessão; quando um limite acaba, continue depois que ele renovar.

Como referência: no livro-piloto de Docker Compose (escrito com o Claude Code em novembro de 2026), cada capítulo gastou o equivalente a uns US$ 2 a 2,50 em preço de API, contando a pesquisa, o teste de cada comando e as checagens.

## Posso parar e continuar depois?

Sim. O progresso de cada livro fica salvo no `book.yaml` dele, capítulo por capítulo. Numa conversa nova, peça para continuar o livro (por exemplo, "continue o meu livro de Docker Compose") e o Syllabook retoma do próximo capítulo.

## Dá para usar sem GitHub?

Dá. Sem conexão, o Syllabook entrega um zip com o livro, com as pastas no mesmo formato de uma biblioteca. Você pode guardar o zip, ler o Markdown ou enviá-lo para um repositório depois ([guia do GitHub](integrations/github.pt-BR.md)).

## Meus materiais ficam privados?

- **Os seus arquivos** (PDFs, documentos, páginas do Notion que você manda para aprimorar) servem só de fonte. Eles nunca são publicados.
- **Os livros** vão para a sua biblioteca. O [modelo de biblioteca](https://github.com/Joshpcbrrj/syllabook-library) é um repositório público, porque o GitHub Pages e as releases são grátis assim. Você pode deixá-lo privado, mas aí o site exige um plano pago do GitHub.
- **A conversa** segue as configurações de privacidade da sua conta do Claude.

## Posso editar um livro à mão?

Pode. Os capítulos são arquivos Markdown comuns, em `chapters/`. Depois de editar, peça ao Syllabook para conferir e publicar o livro: ele roda a auditoria de novo, refaz o EPUB e o site e aponta o que a sua edição quebrou (uma seção faltando, um link quebrado).

## Que temas e idiomas funcionam?

- **Temas:** qualquer um. O Syllabook adapta a didática a quatro perfis: programação e matemática, idiomas, habilidades práticas (música, eletrônica...) e conhecimento geral (como história). Para um tema que não se encaixa em nenhum, ele monta um método próprio e o explica no parecer.
- **Idiomas:** a conversa e o livro podem ser em qualquer idioma. Português do Brasil e inglês têm guias de estilo próprios; nos outros idiomas, ele escreve com naturalidade e avisa que ainda não há guia de estilo.

## O código dos livros é testado?

É. Cada comando e cada trecho de código é executado enquanto o capítulo é escrito, e o livro mostra a saída real. O que não dá para rodar (um comando de outro sistema operacional, por exemplo) sai marcado como "não executado" no texto. Por isso o Claude Code, e o WSL 2 no Windows, rendem livros de tecnologia melhores.

## De onde vêm as imagens?

- **Diagramas:** desenhados em SVG pelos scripts da skill, a partir de uma descrição da estrutura (blocos, fluxos, linhas do tempo, acordes...).
- **Fotos:** só com licença livre (domínio público, CC0, CC BY, CC BY-SA), do Wikimedia Commons, com o autor e a licença embaixo da imagem.
- **Capturas de tela:** da aplicação do livro rodando de verdade.

Por enquanto, o Syllabook não gera imagens com IA.

## Achei um erro num livro. E agora?

- **No seu próprio livro:** peça ao Syllabook para corrigir ("no capítulo 3 do meu livro de Docker, a porta está errada"). Ele muda o capítulo, confere de novo e registra a mudança.
- **No funcionamento da skill:** abra uma [issue](https://github.com/Joshpcbrrj/syllabook/issues/new/choose) no repositório do Syllabook.
