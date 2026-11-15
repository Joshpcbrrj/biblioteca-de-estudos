# Pesquisa, fontes e verificação

> Arquivo de apoio da skill `criar-livro-tecnologia`. Leia antes de propor a ementa e passe as regras no briefing de cada capítulo.

Um livro criado do zero não tem um original para corrigir. O risco é **inventar** (comando, opção ou recurso que não existe) ou **desatualizar** (algo que mudou de versão). Estas regras existem para isso.

## Fontes, em ordem de confiança

1. **Documentação oficial** e guias do próprio projeto (ex.: docs.docker.com), notas de versão (*release notes*), especificações e RFCs.
2. **Repositório oficial** (README, exemplos, issues dos mantenedores).
3. Livros e cursos reconhecidos, blogs técnicos dos mantenedores ou de empresas com autoridade no tema.
4. Fóruns (Stack Overflow e afins) **só** para entender armadilhas comuns, nunca como fonte de fato.

Toda afirmação que pode mudar com o tempo (comandos, opções, valores padrão, limites, versões, preços, licenças) precisa vir de 1 ou 2, **conferida nesta sessão** com WebSearch/WebFetch. Conceitos estáveis (o que é um processo, o que é uma porta de rede) não precisam de fonte.

## Como citar no capítulo

- No fim de cada capítulo, antes do Resumo, uma seção `## 📚 Fontes` com 2 a 6 links no formato `[Título](URL)`, e "conferido em AAAA-MM-DD".
- Comportamento que depende de versão vem com a versão no texto: "a partir do Docker Engine 25, ...".
- No índice do livro e no `00-sobre-o-livro.md`, o aviso: **"Livro criado com IA a partir de fontes públicas, citadas em cada capítulo. Conferido em <data>, com <ferramenta x.y>."**

## Direitos autorais

- **Explique com as suas palavras.** Não copie parágrafos da documentação nem de outros livros; paráfrase não é trocar sinônimos, é reescrever a explicação.
- No máximo **uma citação curta** (menos de 15 palavras) por fonte, entre aspas e com o link, só quando a frase exata importar.
- Exemplos de código: escreva os seus. Um trecho curto da documentação, quando inevitável, vai com a fonte. Respeite a licença de qualquer código reaproveitado.
- Nada de logotipos, marcas ou mascotes de terceiros, nem na capa nem nos diagramas (veja `_comum/CAPA.md`).

## Verificação prática (laboratórios)

Todo comando e todo código do livro precisa ter sido **executado** e ter a saída mostrada. Onde rodar, nesta ordem:

1. **Neste ambiente da sessão:** linguagens, bibliotecas e ferramentas de linha de comando que instalam com pip, npm ou apt.
2. **No computador do aluno** (`device_bash`, a VM Linux ligada ao app do computador), quando a ferramenta precisar de algo que a sessão não tem, como um serviço (Docker, bancos de dados). Confira antes com `which` se está instalado.
3. Se não der para executar em lugar nenhum: marque o bloco com um callout `⚠️` yellow_bg, "Este comando não foi executado na produção do livro; confira a saída no seu ambiente", e liste o caso nas `pendencias` do capítulo.

Nunca invente uma saída. Se a saída real tiver dados variáveis (ids, horários), mostre a real e explique o que muda.

## Ao fechar o livro

- Revise a lista de fontes de todos os capítulos: link quebrado ou página que mudou volta para conferência.
- Registre no `ESTADO.md` a data e a versão de referência. Um livro com mais de ~12 meses entra na lista de "revisar versão".
