# Linguagem de Manipulação de Dados (DML)

> 🗺️ **Nesta aula:** inserir, atualizar, apagar e consultar dados com `INSERT`, `UPDATE`, `DELETE` e `SELECT`, os filtros do `WHERE`, hábitos de segurança e a ordem em que o banco executa uma consulta.

## De onde paramos

A DDL criou as tabelas vazias. Agora vamos preenchê-las e consultá-las: é aqui que o banco passa a ser útil.

## O que é a DML

**DML (Data Manipulation Language) são os comandos que mexem nos dados: inserir, atualizar, apagar e consultar.** A DDL define as tabelas; a DML preenche e usa.

## INSERT: inserir

```sql
-- uma linha (sempre liste as colunas:
-- é mais seguro se a tabela mudar)
INSERT INTO clientes (nome, email)
VALUES ('Ana', 'ana@ex.com');

-- várias linhas de uma vez
INSERT INTO clientes (nome, email) VALUES
  ('Beto',  'beto@ex.com'),
  ('Carla', 'carla@ex.com');

-- a partir de outra consulta
INSERT INTO clientes_arquivados (id, nome)
SELECT id, nome FROM clientes WHERE ativo = FALSE;
```

Colunas omitidas recebem o `DEFAULT` (ou `NULL`); o `id AUTO_INCREMENT` é gerado sozinho.

## UPDATE: atualizar

```sql
UPDATE clientes
SET cidade = 'Recife', ativo = TRUE
WHERE id = 1;

-- aumento de 10%
UPDATE produtos
SET preco = preco * 1.10
WHERE categoria = 'livros';
```

## DELETE: apagar

```sql
DELETE FROM clientes WHERE id = 3;
```

> ⚠️ **Sem** `WHERE`**,** `UPDATE` **e** `DELETE` **atingem TODAS as linhas.** Dois hábitos que salvam: (1) escreva primeiro um `SELECT * FROM tabela WHERE ...` com o mesmo filtro e confira as linhas; (2) rode dentro de uma transação (`BEGIN;`), confira e só então dê `COMMIT` (ou `ROLLBACK`). O MySQL Workbench já vem com o *safe update mode*, que bloqueia esses comandos sem `WHERE` com chave.

## SELECT: consultar

```sql
SELECT nome, email
FROM clientes
WHERE cidade = 'Recife' AND ativo = TRUE
ORDER BY nome
LIMIT 10;
```

### Filtros do WHERE

| Operador | Exemplo |
| --- | --- |
| `=`, `<>`, `>`, `<`, `>=`, `<=` | `preco > 100` |
| `AND`, `OR`, `NOT` | `cidade = 'Recife' OR cidade = 'Natal'` |
| `IN` | `cidade IN ('Recife', 'Natal')` |
| `BETWEEN` | `preco BETWEEN 10 AND 50` (inclui as pontas) |
| `LIKE` | `nome LIKE 'A%'` (começa com A) · `'%silva%'` (contém) |
| `IS NULL` / `IS NOT NULL` | `email IS NULL` (**nunca** `= NULL`) |

Outros recursos: `SELECT DISTINCT cidade` (sem repetir), `AS` para apelidos (`preco * 0.9 AS preco_promo`) e `*` para todas as colunas (bom para explorar; evite em código de produção).

### A ordem real de execução

![Você escreve SELECT primeiro, mas o banco o executa quase no fim.](../img/sql-ordem.svg)

## Exercício

Com a tabela `produtos(id, nome, preco, categoria, estoque)`, escreva: (a) os produtos sem estoque da categoria "bebidas"; (b) um aumento de 5% nos preços de quem custa menos de 10; (c) a remoção dos produtos com nome começando por "TESTE".

<details>
<summary>Ver resposta</summary>

```sql
-- a)
SELECT nome
FROM produtos
WHERE categoria = 'bebidas' AND estoque = 0;

-- b)
UPDATE produtos
SET preco = preco * 1.05
WHERE preco < 10;

-- c) confira antes com SELECT!
SELECT * FROM produtos WHERE nome LIKE 'TESTE%';
DELETE FROM produtos WHERE nome LIKE 'TESTE%';
```

</details>

## 🧠 Revisão rápida

**Como testar se uma coluna está vazia?**

`coluna IS NULL`, nunca `= NULL`.

**O que `LIKE '%silva%'` encontra?**

Textos que contêm "silva" em qualquer posição.

**Por que um apelido do SELECT não funciona no WHERE?**

Porque o WHERE é executado antes do SELECT.

> ➡️ **Próximo passo:** buscar dados de várias tabelas ao mesmo tempo: **Junção de tabelas (JOIN)**.

## 📌 Resumo

| Comando | Em uma frase |
| --- | --- |
| `INSERT` | insere linhas |
| `UPDATE ... WHERE` | altera as linhas filtradas |
| `DELETE ... WHERE` | apaga as linhas filtradas |
| `SELECT` | consulta |
| `WHERE` | filtra linhas |
| `LIKE`, `IN`, `BETWEEN` | filtros comuns |
| `IS NULL` | testa ausência de valor |
