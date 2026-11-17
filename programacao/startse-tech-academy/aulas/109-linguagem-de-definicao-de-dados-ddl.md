# Linguagem de definição de dados (DDL)

> 🗺️ **Nesta aula:** os comandos DDL (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`), como criar, alterar e apagar estruturas com segurança e a diferença entre `DELETE`, `TRUNCATE` e `DROP`.

## De onde paramos

Com as tabelas normalizadas no papel, é hora de criá-las no banco e saber alterá-las quando o sistema evoluir.

## O que é a DDL

Um banco de dados só guarda informação depois que alguém decidiu o formato dela: que tabelas existem, que colunas cada uma tem e que tipo de valor cabe em cada coluna. Essa decisão é feita com a DDL, e costuma ser feita poucas vezes, no começo do projeto e a cada mudança importante. Já guardar e consultar registros acontece milhares de vezes por dia. Por isso a DDL é rara, mas pesada: errar um `DROP` custa muito mais que errar um `INSERT`.

![DDL mexe na estrutura; DML, nos dados](../img/st-ddl-2.svg)

> 💡 **Analogia:** pense numa estante de livros. A DDL cuida da **estante**: montar (`CREATE`), pôr ou tirar prateleiras (`ALTER`) e jogar a estante fora (`DROP`). A DML cuida dos **livros**: guardar, trocar e tirar alguns escolhidos (`DELETE ... WHERE`). O `TRUNCATE` fica no meio: esvazia todas as prateleiras de uma vez, mas a estante continua lá.

**DDL (Data Definition Language) é a parte do SQL que define a estrutura do banco: bancos, tabelas, colunas, índices, views e restrições.** Ela mexe no "esqueleto"; quem mexe nos dados é a DML.

| Comando | O que faz |
| --- | --- |
| `CREATE` | cria banco, tabela, índice, view, trigger |
| `ALTER` | altera a estrutura (colunas e restrições) |
| `DROP` | apaga o objeto inteiro (estrutura **e** dados) |
| `TRUNCATE` | esvazia a tabela e mantém a estrutura |
| `RENAME` | renomeia (MySQL: `RENAME TABLE a TO b`) |

## Criando

Repare no que o `CREATE TABLE` abaixo declara. Cada coluna tem nome, tipo e, quando preciso, uma regra: `NOT NULL` impede o campo vazio, `UNIQUE` impede dois clientes com o mesmo e-mail e `DEFAULT CURRENT_TIMESTAMP` preenche a data sozinha. O banco passa a recusar dados inválidos, sem depender de o programa lembrar de checar. Com `IF NOT EXISTS`, rodar o script duas vezes não dá erro, o que é útil quando você refaz o ambiente. O índice do final não muda os dados: ele só ajuda a achar produtos pelo nome mais rápido, como o índice remissivo de um livro.

```sql
CREATE DATABASE loja;
-- MySQL (no PostgreSQL: \c loja)
USE loja;

CREATE TABLE clientes (
  id        INT PRIMARY KEY AUTO_INCREMENT,
  nome      VARCHAR(100) NOT NULL,
  email     VARCHAR(100) NOT NULL UNIQUE,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- não dá erro se já existir
CREATE TABLE IF NOT EXISTS produtos (
  id    INT PRIMARY KEY AUTO_INCREMENT,
  nome  VARCHAR(100) NOT NULL,
  preco DECIMAL(10, 2) NOT NULL
);

CREATE INDEX idx_produtos_nome ON produtos(nome);
```

## Alterando

Sistemas evoluem. Um dia o cadastro precisa da data de nascimento, outro dia o nome ganha mais caracteres. Em vez de apagar a tabela e perder os clientes, o `ALTER TABLE` muda a estrutura com os dados no lugar. Cada linha abaixo faz uma mudança só, e você pode combiná-las conforme a necessidade. Ao adicionar uma coluna `NOT NULL` numa tabela que já tem linhas, informe um `DEFAULT`; senão o banco não sabe o que colocar nas linhas antigas e recusa o comando.

```sql
-- nova coluna
ALTER TABLE clientes ADD COLUMN data_nascimento DATE;
-- muda o tipo (MySQL)
ALTER TABLE clientes
  MODIFY COLUMN nome VARCHAR(150) NOT NULL;
-- renomeia
ALTER TABLE clientes
  RENAME COLUMN nome TO nome_completo;
-- remove
ALTER TABLE clientes DROP COLUMN data_nascimento;
-- nova restrição
ALTER TABLE clientes
  ADD CONSTRAINT ck_email CHECK (email LIKE '%@%');
```

## Apagando

São três níveis de estrago, do menor ao maior. `TRUNCATE` apaga todas as linhas e mantém a tabela pronta para receber novos dados, o que serve para limpar uma tabela de logs. `DROP TABLE` remove a tabela inteira, com estrutura e dados. `DROP DATABASE` leva junto todas as tabelas do banco. O `IF EXISTS` evita erro se o objeto já foi removido, mas não protege você de apagar o objeto errado. Antes de rodar qualquer um dos três em produção, confirme em qual banco você está conectado.

![DELETE, TRUNCATE e DROP lado a lado.](../img/st-delete-truncate-drop.svg)

> 💡 **Analogia:** é como limpar uma sala: tirar alguns objetos (`DELETE`), esvaziar tudo e manter a sala (`TRUNCATE`) ou demolir a própria sala (`DROP`).

```sql
-- apaga todas as linhas, rápido; a estrutura fica
TRUNCATE TABLE logs;
-- apaga a tabela inteira
DROP TABLE IF EXISTS logs;
-- apaga o banco inteiro!
DROP DATABASE loja;
```

> ⚠️ `DROP` e `TRUNCATE` **não têm "desfazer"** na maioria dos bancos (no MySQL, causam *commit* implícito e não entram em transação). Em produção, faça **backup** antes e prefira **migrations** versionadas (Flyway, Liquibase, Prisma, Knex) em vez de rodar DDL na mão.

## `DELETE` × `TRUNCATE` × `DROP`

|  | `DELETE FROM t` | `TRUNCATE TABLE t` | `DROP TABLE t` |
| --- | --- | --- | --- |
| Tipo | DML | DDL | DDL |
| Apaga | linhas (aceita `WHERE`) | todas as linhas | a tabela inteira |
| Estrutura | mantém | mantém | apaga |
| Reinicia o `AUTO_INCREMENT` | não | sim | — |
| Velocidade | linha a linha | muito rápido | muito rápido |

> ⚠️ **Correções:** `COMMIT` e `ROLLBACK` **não são DDL**: pertencem à **TCL**. E os exemplos originais usavam `//` como comentário, o que não existe em SQL; o correto é `--` ou `/* */`.

## Exercício

A tabela `produtos` precisa de: uma coluna `estoque` inteira com valor padrão 0, a garantia de que o estoque nunca seja negativo e a renomeação da tabela para `itens_catalogo`. Escreva os comandos.

<details>
<summary>Ver resposta</summary>

```sql
ALTER TABLE produtos
  ADD COLUMN estoque INT NOT NULL DEFAULT 0;

ALTER TABLE produtos
  ADD CONSTRAINT ck_estoque CHECK (estoque >= 0);

RENAME TABLE produtos TO itens_catalogo;
-- PostgreSQL:
-- ALTER TABLE produtos RENAME TO itens_catalogo;
```

</details>

## 🧠 Revisão rápida

**Qual a diferença entre `TRUNCATE` e `DROP`?**

`TRUNCATE` esvazia e mantém a tabela; `DROP` apaga a tabela.

**`DELETE` é DDL ou DML?**

DML: mexe nos dados, não na estrutura.

**Para que serve `IF NOT EXISTS`?**

Para não dar erro se o objeto já existir.

> ➡️ **Próximo passo:** com as tabelas criadas, vamos inserir, alterar e consultar dados: **Linguagem de Manipulação de Dados (DML)**.

## 📌 Resumo

| Comando | Em uma frase |
| --- | --- |
| `CREATE` | cria um objeto |
| `ALTER` | muda a estrutura |
| `DROP` | apaga o objeto e os dados |
| `TRUNCATE` | esvazia a tabela |
| `IF [NOT] EXISTS` | evita erro se (não) existir |
| Migrations | DDL versionada e revisável |
