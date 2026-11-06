# Teste prático com o Node JS

> 🗺️ **Nesta aula:** o primeiro projeto Node do zero: criar o `package.json` com `npm init`, escrever o arquivo principal, executar, criar scripts e ler e gravar um arquivo com o módulo `fs`.

## De onde paramos

Você conhece o Node e o npm. Agora vamos juntar os dois num projeto mínimo, passo a passo.

![Projeto Node em 4 passos](../img/st-node.svg)

## 1. Iniciar o projeto

Crie uma pasta, abra o terminal nela e rode:

```bash
npm init
```

O npm faz algumas perguntas e gera o arquivo `package.json`:

| Pergunta | O que é |
| --- | --- |
| package name | nome do projeto (minúsculas, sem espaços) |
| version | versão inicial (sugere `1.0.0`) |
| description | descrição curta |
| entry point | arquivo principal (sugere `index.js`) |
| test command | comando executado por `npm test` |
| git repository | URL do repositório (pode ficar vazio) |
| keywords | palavras-chave para busca no npm |
| author | seu nome |
| license | licença (sugere `ISC`; `MIT` é muito comum) |

Para aceitar tudo no padrão e editar depois:

```bash
npm init -y
```

## 2. Criar o arquivo principal

Crie `index.js` (o mesmo nome que está em `"main"` no `package.json`):

```jsx
console.log("Uma vez Flamengo, sempre Flamengo!!!");
```

## 3. Executar

```bash
# executa o arquivo indicado
node index.js
# executa o "main" do package.json
node .
```

## 4. Criar scripts no package.json

```json
{
  "name": "meu-projeto",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "node --watch index.js"
  }
}
```

```bash
# roda "node index.js"
npm start
# reinicia sozinho a cada alteração (Node 18+)
npm run dev
```

## 5. Um passo além: ler e gravar arquivos

O que o navegador não deixa fazer, o Node faz: acessar arquivos do computador.

```jsx
// index.js (com "type": "module" no package.json)
import { readFile, writeFile } from "node:fs/promises";

await writeFile("nota.txt", "Primeira nota\n");
const texto = await readFile("nota.txt", "utf8");
console.log(texto);  // Primeira nota
```

`fs/promises` devolve Promises, por isso usamos `await`: o assunto das próximas aulas.

> ⚠️ **Correção:** o arquivo foi criado como `main.js`, mas o `npm init` sugere `index.js` como entry point. Nesse caso, `node .` procura `index.js` e falha com **Cannot find module**. O arquivo e o `"main"` precisam ter o mesmo nome.

## Exercício

Crie um script que conte quantas linhas tem um arquivo `lista.txt` e mostre o resultado. Adicione o atalho `npm run contar`.

<details>
<summary>Ver resposta</summary>

```jsx
// contar.js
import { readFile } from "node:fs/promises";

const texto = await readFile("lista.txt", "utf8");
const linhas = texto.split("\n").filter(l => l.trim());
console.log(`${linhas.length} linhas`);
```

```json
"scripts": {
  "contar": "node contar.js"
}
```

O `filter` descarta linhas vazias, como a do fim do arquivo.

</details>

## 🧠 Revisão rápida

**O que `node .` executa?**

O arquivo indicado em `"main"` no `package.json`.

**Qual script pode ser chamado sem `run`?**

`start` (e `test`).

> ➡️ **Próximo passo:** a primeira forma de lidar com operações assíncronas: **Callback**.

## 📌 Resumo

| Passo | Em uma frase |
| --- | --- |
| `npm init` | cria o `package.json` |
| `"main"` | arquivo principal do projeto |
| `node index.js` | executa um arquivo |
| `npm start` | roda o script `start` |
| `node --watch` | reinicia a cada alteração |
| `fs/promises` | lê e grava arquivos |
