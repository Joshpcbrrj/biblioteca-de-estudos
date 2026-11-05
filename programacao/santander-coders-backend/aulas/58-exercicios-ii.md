# Exercícios II

> 🗺️ **Nesta lista:** sete questões sobre CREATE, INSERT, UPDATE e DELETE, aspas em SQL, LGPD e senhas, e índices, mais um bônus de consulta.

## De onde paramos

Esta lista fecha o módulo de banco de dados e o curso.

## Questão 1

Qual comando cria tabelas no PostgreSQL?

<details>
<summary>Ver resposta</summary>

`CREATE TABLE nome (colunas...);`

</details>

## Questão 2

Você vai cadastrar 5 jogos no catálogo de uma loja de games usando uma única query. Como fazer?

<details>
<summary>Ver resposta</summary>

Um `INSERT INTO` com vários grupos de valores separados por vírgula:

```sql
INSERT INTO jogos (nome, preco)
VALUES ('Jogo A', 199.90),
       ('Jogo B', 149.90),
       ('Jogo C', 99.90),
       ('Jogo D', 59.90),
       ('Jogo E', 29.90);
```

</details>

## Questão 3

Um registro vai guardar o nome de uma pessoa, a idade e a data do cadastro. Quais valores vão entre aspas?

<details>
<summary>Ver resposta</summary>

O **nome** e a **data do cadastro**: textos e datas vão entre aspas simples. A idade, que é número, não.

```sql
INSERT INTO pessoas (nome, idade, cadastro)
VALUES ('Ana', 30, '2026-01-10');
```

</details>

> ⚠️ **Ajuste:** a resposta original dizia "nome e data de nascimento", mas o enunciado fala em data do cadastro. A regra é a mesma para qualquer data. E em SQL as aspas são sempre **simples** e retas: `'Carlos'`. Aspas curvas (‘ ’), comuns ao copiar de editores de texto, dão erro.

## Questão 4

Para corrigir o nome de um aluno de "Carlo" para "Carlos", você rodou:

```sql
UPDATE alunos SET nome = 'Carlos';
```

O que deu errado?

<details>
<summary>Ver resposta</summary>

Faltou o `WHERE`: **todos** os alunos passaram a se chamar Carlos. O certo seria filtrar pela chave primária:

```sql
UPDATE alunos SET nome = 'Carlos'
WHERE id = 15;
```

</details>

## Questão 5

Um erro gerou cadastros errados, todos no dia 2026-01-10, e todos os dados desse dia podem ser descartados. Qual query remove esses registros?

<details>
<summary>Ver resposta</summary>

```sql
DELETE FROM cadastro
WHERE data = '2026-01-10';
```

Se a coluna for `timestamp` (com hora), a igualdade só pega a meia-noite. Use uma faixa: `WHERE data >= '2026-01-10' AND data < '2026-01-11'`.

</details>

## Questão 6

Num aplicativo de receitas, você percebe que as senhas dos clientes estão salvas abertas na tabela e qualquer desenvolvedor consegue lê-las. O que dizer sobre isso?

<details>
<summary>Ver resposta</summary>

É uma falha grave de segurança, e a empresa pode ser punida pela **LGPD** (Lei Geral de Proteção de Dados) por não proteger dados pessoais. Senhas nunca devem ser guardadas abertas, nem criptografadas de forma reversível: o certo é guardar só um **hash** próprio para senhas, como bcrypt ou Argon2, e comparar hashes no login.

</details>

## Questão 7

Um colega criou índices de árvore B numa tabela com 100 registros e o tempo das consultas quase não mudou. Ele acha que errou algo. O que você diz?

<details>
<summary>Ver resposta</summary>

Que não há erro: índices reduzem muito o tempo de consulta, mas a diferença só aparece em tabelas com **muitos** registros. Com 100 linhas, ler a tabela inteira já é instantâneo, e o próprio PostgreSQL costuma preferir o seq scan.

</details>

> ⚠️ O enunciado original falava em "árvore binária". O índice padrão é a **árvore B** (B-tree), em que cada nó tem muitos filhos.

## Bônus

Mostre o nome e o total gasto de cada cliente, do que mais gastou para o que menos gastou, sabendo que `pedidos` tem `cliente_id` e `total`.

<details>
<summary>Ver resposta</summary>

```sql
SELECT c.nome, SUM(p.total) AS gasto
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.nome
ORDER BY gasto DESC;
```

</details>

> ➡️ **Fim do curso.** Volte ao índice para ver o resumo de todos os módulos.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 a 3 | CREATE, INSERT e aspas |
| 4 e 5 | UPDATE e DELETE com WHERE |
| 6 | LGPD e armazenamento de senhas |
| 7 | Índices |
| Bônus | JOIN com agregação |
