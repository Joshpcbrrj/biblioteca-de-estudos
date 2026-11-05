# Como tirar dúvidas de programação no Google e no Stack Overflow

> 🗺️ **Nesta aula:** como ler uma mensagem de erro, pesquisar com eficiência no Google, perguntar bem no Stack Overflow e usar assistentes de IA e a documentação oficial.

## De onde paramos

Com o ambiente instalado, você vai escrever código, e código dá erro. Isso é normal: todo programador passa boa parte do dia lendo mensagens de erro e pesquisando. A diferença entre travar uma hora e resolver em cinco minutos está no método.

## Antes de pesquisar

1. **Leia a mensagem de erro inteira.** Ela costuma dizer *o quê* (tipo do erro), *onde* (arquivo e linha) e *por quê*. A primeira linha do *stack trace* que aponta para o **seu** código é a pista mais valiosa.
2. **Classifique o erro:**
  - **sintático**: o código não segue a gramática da linguagem (parêntese faltando, vírgula sobrando). Geralmente o editor já sublinha;
  - **semântico ou de lógica**: o código roda, mas faz a coisa errada (resultado errado, `undefined`, laço infinito).
3. **Faça a pergunta certa.** Descreva o que você *esperava* e o que *aconteceu*.

### Lendo um erro real

```
Uncaught TypeError: Cannot read properties
  of undefined (reading 'nome')
    at mostrarUsuario (app.js:12:23)
    at app.js:20:1
```

- **Tipo:** `TypeError`, uma operação num valor do tipo errado.
- **O quê:** tentou ler `.nome` de algo que é `undefined`.
- **Onde:** arquivo `app.js`, linha 12, coluna 23, dentro da função `mostrarUsuario`.
- **Próximo passo:** abrir a linha 12 e descobrir por que a variável antes do `.nome` está vazia.

## Dicas de busca no Google

- **Comece pela tecnologia**: `javascript array remove duplicates`.
- **Tire os nomes do seu projeto** (suas variáveis, arquivos, nome da empresa). Ninguém mais usa esses termos.
- **Pesquise em inglês**: há muito mais conteúdo.
- **Cole a mensagem de erro entre aspas** para buscar a frase exata: `"Cannot read properties of undefined"`.

### Operadores úteis

| Operador | Exemplo | O que faz |
| --- | --- | --- |
| `"..."` | `"unexpected token"` | frase exata |
| `site:` | `site:stackoverflow.com flexbox center` | busca só em um site |
| `-` | `manipulate DOM -jquery` | exclui um termo |
| `before:` | `java streams before:2018` | resultados anteriores a uma data |
| `after:` | `react hooks after:2023` | resultados mais recentes |
| `..` | `python 2021..2023` | intervalo de números ou anos |
| `OR` | `react OR vue OR angular` | qualquer um dos termos |
| `filetype:` | `refactoring filetype:pdf` | tipo de arquivo |

> ⚠️ **Correção:** o operador `related:` foi **descontinuado pelo Google** em 2023 e não funciona mais. A sintaxe certa é `site:dominio.com termo`, com `site` em minúsculas e sem espaço depois dos dois-pontos.

## Como perguntar no Stack Overflow

Antes de perguntar, **pesquise**: a maioria das dúvidas já tem resposta. Se não tiver:

- **Título específico**: "Por que meu `fetch` retorna `Promise { <pending> }`?" é melhor que "Ajuda com JavaScript".
- **Sem cumprimentos nem agradecimentos** no texto: vá direto ao ponto.
- **Exemplo mínimo reproduzível**: o menor trecho de código que mostra o problema, em **texto** (nunca print).
- **O que você esperava × o que aconteceu**, com a mensagem de erro completa.
- **O que você já tentou.**
- **Versões** (linguagem, biblioteca, navegador).

### Exemplo de boa pergunta

```
Título: Por que console.log mostra
"Promise { <pending> }" em vez dos dados?

Estou buscando dados de uma API, mas o log
mostra uma Promise:

  const url = "https://api.exemplo.com/produtos";
  const dados = fetch(url).then(r => r.json());
  console.log(dados); // Promise { <pending> }

Esperava ver o array de produtos. Já tentei
colocar o console.log depois do fetch,
sem sucesso. Node 20.
```

### Exemplo de boa resposta

```
O fetch é assíncrono: devolve uma Promise na
hora, e os dados chegam depois. Use await
(dentro de uma função async) ou um .then():

  async function carregar() {
    const resposta = await fetch(url);
    const dados = await resposta.json();
    console.log(dados); // agora sim, o array
  }
  carregar();

Veja mais em: MDN, "Using the Fetch API".
```

Uma boa resposta **explica o porquê**, mostra o código corrigido e aponta a documentação.

## Assistentes de IA

Ferramentas como Claude, ChatGPT e GitHub Copilot ajudam a entender erros e conceitos. Use bem:

- Cole o erro **e** o trecho de código relevante.
- Peça para **explicar** o problema, não só para corrigir: você precisa aprender o porquê.
- **Teste e confira** a resposta. A IA pode errar com muita confiança, principalmente sobre versões recentes de bibliotecas.

## Documentação

A documentação oficial é sempre a fonte mais confiável. O DevDocs reúne a documentação de várias linguagens num só lugar:

🔗 [DevDocs API Documentation](https://devdocs.io/)

Para HTML, CSS e JavaScript, a referência é a **MDN Web Docs** (developer.mozilla.org).

## 🧠 Revisão rápida

**Num stack trace, qual linha costuma ser a pista mais útil?**

A primeira que aponta para um arquivo do seu próprio código.

**Como buscar a frase exata de um erro no Google?**

Colocando a mensagem entre aspas.

**Por que enviar código como texto, e não como print, numa pergunta?**

Para que quem responde possa copiar, rodar e testar o exemplo.

> ➡️ **Próximo passo:** antes de qualquer linguagem, vem o raciocínio. A próxima aula treina o pensamento algorítmico: **Lógica de programação e algoritmos**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Mensagem de erro | diz o tipo, o local e a causa |
| Sintático × lógica | não roda × roda errado |
| Busca | tecnologia, em inglês, erro entre aspas |
| `site:` | busca dentro de um site |
| Boa pergunta | título específico, exemplo mínimo, esperado × obtido |
| IA | peça explicação e confira a resposta |
| Documentação | MDN para web; DevDocs para várias linguagens |
