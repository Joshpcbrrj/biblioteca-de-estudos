# GitHub, pull requests e boas mensagens de commit

> 🗺️ **Nesta aula:** a diferença entre Git e GitHub, o fluxo de trabalho em equipe com branches e pull requests, forks e como escrever mensagens de commit que ajudam o time.

## De onde paramos

Você já sabe enviar e receber commits com `push` e `pull`. Agora vamos ver como uma equipe usa isso no dia a dia sem pisar no trabalho uns dos outros.

## Git ≠ GitHub

**Git** é o programa que controla versões no seu computador. **GitHub** é um site que hospeda repositórios Git na nuvem e adiciona ferramentas de colaboração: pull requests, revisão de código, issues e Actions. GitLab e Bitbucket são alternativas.

## O fluxo de pull request

Em equipe, ninguém envia direto para a `main`. Cada mudança nasce numa branch e passa por revisão antes de entrar:

```bash
# 1. parte da main atualizada
git switch main
git pull
# 2. cria a branch da tarefa
git switch -c feat/formulario-contato
# ... edita e testa ...
git add .
git commit -m "feat: adiciona formulário de contato"
# 3. envia a branch
git push -u origin feat/formulario-contato
```

4. No GitHub, clique em **Compare & pull request**. Descreva **o que** mudou e **por quê**, e peça revisão.
5. Os colegas comentam. Você ajusta com novos commits na mesma branch, e o PR se atualiza sozinho.
6. Aprovado, clique em **Merge** e apague a branch remota.
7. Localmente, volte para a `main` e atualize: `git switch main` e depois `git pull`.

> 💡 **Fork:** para contribuir com um projeto em que você não tem permissão de escrita, faça um *fork* (uma cópia do repositório na sua conta), trabalhe nele e abra o PR para o original.

## Boas mensagens de commit

Um histórico legível vale ouro quando algo quebra. O padrão **Conventional Commits** é muito usado:

```
tipo(escopo opcional): descrição curta
```

| Tipo | Quando usar |
| --- | --- |
| `feat` | nova funcionalidade |
| `fix` | correção de bug |
| `docs` | só documentação |
| `style` | formatação, sem mudar a lógica |
| `refactor` | reorganização sem mudar o comportamento |
| `test` | testes |
| `chore` | configuração, dependências, build |

```
❌ "ajustes"
❌ "agora vai"
❌ "commit final 2"
✅ fix(login): exibe erro quando a senha está vazia
✅ feat: adiciona modo escuro
```

Regras práticas: primeira linha com até cerca de **50 caracteres**, verbo no imperativo ("adiciona", "corrige"), **um assunto por commit**. Se precisar explicar, pule uma linha e escreva o corpo.

## Outros recursos do GitHub

- **README.md**: a vitrine do repositório. Explique o que é o projeto, como rodar e mostre um print.
- **Issues**: lista de bugs e tarefas. Escrever `Closes #12` na descrição do PR fecha a issue 12 quando ele for mesclado.
- **GitHub Pages**: publica um site estático de graça (*Settings → Pages*), ótimo para os projetos de HTML e CSS deste curso.
- **Actions**: automações que rodam a cada push (testes, build, deploy).

> ⚠️ Nunca suba `node_modules/`, `.env` ou senhas (veja a aula de **Gitignore**). Um segredo que foi para o GitHub deve ser considerado **vazado** e trocado, mesmo que você apague o commit depois.

## Exercício

Escreva mensagens no padrão Conventional Commits para: (a) você corrigiu o cálculo do frete; (b) você atualizou o README com instruções de instalação; (c) você criou a página de perfil do usuário.

<details>
<summary>Ver resposta</summary>

```
fix(frete): corrige cálculo para pedidos acima de 10 kg
docs: adiciona instruções de instalação ao README
feat(perfil): cria página de perfil do usuário
```

O escopo entre parênteses é opcional; o importante é o tipo certo e uma descrição curta e específica.

</details>

## 🧠 Revisão rápida

**Qual a diferença entre Git e GitHub?**

Git é a ferramenta de versionamento local; GitHub é o serviço que hospeda os repositórios e adiciona colaboração.

**Por que trabalhar numa branch e abrir um PR em vez de enviar direto para a main?**

Para que a mudança seja revisada e testada antes de entrar no código que todo mundo usa.

**O que é um fork?**

Uma cópia de um repositório na sua conta, usada para contribuir com projetos em que você não pode escrever.

> ➡️ **Próximo passo:** quando o PR é aprovado, as branches precisam ser unidas. Duas formas de fazer isso: **Merge e rebase**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Git × GitHub | ferramenta local × serviço de hospedagem e colaboração |
| Pull request | pedido para mesclar uma branch, com revisão |
| Fork | sua cópia de um repositório alheio |
| Conventional Commits | `tipo(escopo): descrição` |
| Issues | lista de bugs e tarefas do projeto |
| GitHub Pages | hospedagem grátis de sites estáticos |
