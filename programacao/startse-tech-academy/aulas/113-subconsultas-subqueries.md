# Subconsultas (subqueries)

> 🗺️ **Nesta aula:** subconsultas que devolvem um valor, uma lista ou uma tabela, `IN`, `EXISTS`, subconsultas correlacionadas, CTEs com `WITH` e quando preferir subconsulta ou JOIN.

## De onde paramos

Com agregação você calcula a média de preços. Mas e para listar "os produtos mais caros que a média"? É preciso calcular a média primeiro e usá-la num filtro. Para isso servem as subconsultas.

## O que é uma subconsulta

**Uma subconsulta é um** `SELECT` **dentro de outro comando SQL.** O resultado da consulta de dentro é usado pela de fora, como um valor, uma lista ou uma tabela temporária.

## 1. Subconsulta que devolve um valor (escalar)

```sql
-- produtos mais caros que a média
SELECT nome, preco
FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos);
```

O banco calcula primeiro a média e depois a usa no filtro.

## 2. Subconsulta que devolve uma lista: `IN` e `NOT IN`

```sql
-- clientes que já compraram
SELECT nome FROM clientes
WHERE id IN (SELECT cliente_id FROM pedidos);

-- clientes que nunca compraram
SELECT nome FROM clientes
WHERE id NOT IN (
  SELECT cliente_id FROM pedidos
  WHERE cliente_id IS NOT NULL
);
```

> ⚠️ Se a subconsulta de um `NOT IN` devolver **algum** `NULL`, o resultado fica **vazio**, porque qualquer comparação com NULL é "desconhecida". Por isso o filtro `IS NOT NULL` acima, ou prefira `NOT EXISTS`.

## 3. `EXISTS` e `NOT EXISTS`

Testa se a subconsulta devolve **alguma linha**. Costuma ser a forma mais clara e eficiente de perguntar "tem ou não tem".

```sql
SELECT c.nome
FROM clientes c
WHERE NOT EXISTS (
  SELECT 1 FROM pedidos p WHERE p.cliente_id = c.id
);
```

## 4. Subconsulta correlacionada

Usa colunas da consulta de fora e, por isso, é avaliada **para cada linha**.

```sql
-- o pedido mais caro de cada cliente
SELECT p.cliente_id, p.id, p.total
FROM pedidos p
WHERE p.total = (
  SELECT MAX(p2.total)
  FROM pedidos p2
  WHERE p2.cliente_id = p.cliente_id
);
```

## 5. Subconsulta no `FROM` (tabela derivada)

```sql
SELECT AVG(gasto) AS ticket_medio_por_cliente
FROM (
  SELECT cliente_id, SUM(total) AS gasto
  FROM pedidos
  GROUP BY cliente_id
) AS gastos;  -- o apelido é obrigatório
```

## CTE: `WITH`, a forma mais legível

Uma **CTE** (Common Table Expression) dá nome a uma subconsulta antes do `SELECT` principal. Ela está disponível no MySQL 8+, PostgreSQL e SQL Server.

```sql
WITH gastos AS (
  SELECT cliente_id, SUM(total) AS gasto
  FROM pedidos
  GROUP BY cliente_id
)
SELECT c.nome, g.gasto
FROM gastos g
JOIN clientes c ON c.id = g.cliente_id
WHERE g.gasto > (SELECT AVG(gasto) FROM gastos);
```

## Subconsulta ou JOIN?

Muitas subconsultas podem ser reescritas como JOIN, e o resultado é o mesmo. Use o que ficar **mais legível**: `EXISTS` para "tem ou não tem", JOIN quando precisar de colunas das duas tabelas e CTE quando a consulta tiver várias etapas. Na dúvida sobre desempenho, compare com `EXPLAIN`.

## Exercício

Liste os produtos que **nunca** foram vendidos (não aparecem em `itens_pedido`), de duas formas: com `NOT EXISTS` e com `LEFT JOIN`.

<details>
<summary>Ver resposta</summary>

```sql
-- com NOT EXISTS
SELECT pr.nome
FROM produtos pr
WHERE NOT EXISTS (
  SELECT 1 FROM itens_pedido ip
  WHERE ip.produto_id = pr.id
);

-- com LEFT JOIN
SELECT pr.nome
FROM produtos pr
LEFT JOIN itens_pedido ip ON ip.produto_id = pr.id
WHERE ip.id IS NULL;
```

</details>

## 🧠 Revisão rápida

**Por que `NOT IN` pode devolver vazio inesperadamente?**

Porque um `NULL` na lista torna todas as comparações desconhecidas.

**O que é uma subconsulta correlacionada?**

Uma subconsulta que usa colunas da consulta de fora e roda para cada linha.

**Qual a vantagem de uma CTE?**

Dar nome às etapas, deixando consultas complexas mais legíveis.

> ➡️ **Próximo passo:** escolher o tipo certo para cada coluna: **Tipos de dados**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Subconsulta | SELECT dentro de outro comando |
| Escalar | devolve um único valor |
| `IN` | compara com uma lista |
| `EXISTS` | testa se existe alguma linha |
| Correlacionada | roda para cada linha de fora |
| Tabela derivada | subconsulta no FROM, com apelido |
| CTE (`WITH`) | subconsulta nomeada e legível |
