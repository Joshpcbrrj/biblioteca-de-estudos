# Transações e ACID (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** o que é uma transação, os comandos `START TRANSACTION`, `COMMIT`, `ROLLBACK` e `SAVEPOINT`, as garantias ACID, os níveis de isolamento e como usar transações numa aplicação Node.js.

## De onde paramos

Os índices deixam as consultas rápidas. Falta garantir que operações que precisam acontecer **juntas** nunca fiquem pela metade, mesmo que o servidor caia no meio.

## O que é uma transação

Pense numa transferência de R$ 100 entre duas contas. Por baixo são dois comandos: tirar 100 de uma conta e pôr 100 na outra. Se o servidor cair entre os dois, o dinheiro some: saiu de uma conta e não chegou na outra. A transação existe para impedir isso. Tudo dentro dela vale como um bloco só: se qualquer parte falhar, o banco desfaz o que já tinha feito e as contas voltam ao estado original.

**Uma transação agrupa vários comandos em uma unidade: ou todos são gravados, ou nenhum é.** O exemplo clássico é uma transferência bancária: tirar o dinheiro de uma conta e colocar na outra precisa acontecer **junto**. Se o sistema cair no meio, o dinheiro não pode sumir.

![COMMIT confirma tudo; ROLLBACK desfaz tudo.](../img/transacao.svg)

> 💡 **Analogia:** é o caixa do supermercado. Ele passa todos os produtos (os comandos), mas a compra só vale quando o pagamento é aprovado e a nota sai (`COMMIT`). Se o cartão for recusado, o caixa cancela a compra **inteira** (`ROLLBACK`): você não sai com metade das sacolas. E, depois de a nota sair, a compra está registrada mesmo que falte luz no minuto seguinte (durabilidade).

## Comandos (TCL)

O ciclo tem sempre três movimentos. `START TRANSACTION` abre o bloco. Dentro dele você roda os comandos normalmente, mas as mudanças ainda são provisórias: só você as vê. No fim, `COMMIT` confirma e torna tudo definitivo para todo mundo, ou `ROLLBACK` descarta tudo como se nada tivesse acontecido. A decisão costuma ser tomada pelo programa: se todos os comandos deram certo, `COMMIT`; se algum falhou, `ROLLBACK`.

```sql
-- ou BEGIN
START TRANSACTION;

UPDATE contas SET saldo = saldo - 100 WHERE id = 1;
UPDATE contas SET saldo = saldo + 100 WHERE id = 2;

-- conferiu e está tudo certo? grava
COMMIT;

-- deu algo errado? desfaz tudo desde o início
ROLLBACK;
```

`SAVEPOINT nome` cria um ponto intermediário, e `ROLLBACK TO nome` volta só até ele.

> 💡 Por padrão, os clientes (como o psql e o MySQL Workbench) vêm com **autocommit** ligado: cada comando solto é uma transação que se confirma sozinha. O `START TRANSACTION` desliga isso até o próximo `COMMIT` ou `ROLLBACK`. No MySQL, comandos DDL (`CREATE`, `DROP`, `ALTER`) fazem **commit implícito** e não podem ser desfeitos.

## ACID: as quatro garantias

A sigla ACID resume o que se espera de um banco confiável, e cada letra responde a um medo real. **Atomicidade**: "e se cair no meio?" Tudo ou nada. **Consistência**: "e se violar uma regra?" O banco recusa e mantém as chaves e restrições valendo. **Isolamento**: "e se dois clientes comprarem o último item ao mesmo tempo?" Cada transação age como se estivesse sozinha. **Durabilidade**: "e se faltar luz depois de confirmar?" O que foi confirmado sobrevive.

| Letra | Propriedade | Significa |
| --- | --- | --- |
| **A** | Atomicidade | tudo ou nada: sem transferência pela metade |
| **C** | Consistência | vai de um estado válido a outro, respeitando PK, FK e CHECK |
| **I** | Isolamento | transações simultâneas não veem dados pela metade |
| **D** | Durabilidade | depois do `COMMIT`, o dado sobrevive a uma queda |

## Níveis de isolamento

Isolamento total é seguro, mas obriga as transações a esperarem umas pelas outras, e isso deixa o sistema lento. Por isso os bancos deixam você escolher quanto isolamento quer. O padrão de cada banco já serve para a maioria dos casos. Os níveis mais altos entram em cena em operações delicadas, como fechar o caixa do dia, em que ler um valor que muda no meio do cálculo daria um resultado errado.

Isolamento total custa desempenho, então os bancos oferecem níveis:

| Nível | Evita |
| --- | --- |
| `READ UNCOMMITTED` | nada (pode ler dados não confirmados, o *dirty read*) |
| `READ COMMITTED` | leitura suja (padrão do PostgreSQL e do SQL Server) |
| `REPEATABLE READ` | leitura suja e leituras que mudam no meio da transação (padrão do MySQL/InnoDB) |
| `SERIALIZABLE` | tudo: como se as transações rodassem uma depois da outra |

## Na aplicação (Node.js com mysql2)

```jsx
const conn = await pool.getConnection();
try {
  await conn.beginTransaction();
  await conn.query(
    "UPDATE contas SET saldo = saldo - ? WHERE id = ?",
    [100, 1]
  );
  await conn.query(
    "UPDATE contas SET saldo = saldo + ? WHERE id = ?",
    [100, 2]
  );
  await conn.commit();
} catch (erro) {
  // qualquer erro desfaz as duas operações
  await conn.rollback();
  throw erro;
} finally {
  conn.release();
}
```

> ⚠️ Repare nos `?`: são **parâmetros**. Nunca monte SQL concatenando texto digitado pelo usuário (`"... WHERE nome = '" + nome + "'"`), porque isso abre brecha para **SQL Injection**: alguém pode digitar um trecho de SQL e apagar ou vazar dados.

## Exercício

Escreva em SQL uma compra que: (1) cria o pedido 50 para o cliente 7; (2) insere o item (produto 3, quantidade 2, preço 39.90); (3) baixa o estoque do produto. Tudo deve ser desfeito se algo falhar.

<details>
<summary>Ver resposta</summary>

```sql
START TRANSACTION;

INSERT INTO pedidos (id, cliente_id, data_pedido)
VALUES (50, 7, CURRENT_DATE);

INSERT INTO itens_pedido
  (pedido_id, produto_id, quantidade, preco_unit)
VALUES (50, 3, 2, 39.90);

UPDATE produtos
SET estoque = estoque - 2
WHERE id = 3 AND estoque >= 2;

-- se o UPDATE não afetou nenhuma linha
-- (estoque insuficiente), a aplicação faz ROLLBACK;
-- senão:
COMMIT;
```

A condição `estoque >= 2` evita estoque negativo; a aplicação confere quantas linhas o `UPDATE` afetou para decidir entre `COMMIT` e `ROLLBACK`.

</details>

## 🧠 Revisão rápida

**O que garante a atomicidade?**

Que todos os comandos da transação sejam gravados, ou nenhum.

**O que é autocommit?**

Cada comando solto é confirmado automaticamente.

**Como evitar SQL Injection?**

Usando consultas parametrizadas (`?`) em vez de concatenar texto.

> ➡️ **Próximo passo:** juntar tudo, ligando a API do Express a um banco SQL: **Integrando Node.js e SQL: API com banco de dados**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Transação | tudo ou nada |
| `COMMIT` | confirma |
| `ROLLBACK` | desfaz |
| `SAVEPOINT` | ponto de retorno parcial |
| ACID | atomicidade, consistência, isolamento, durabilidade |
| Isolamento | níveis trocam segurança por desempenho |
| Parâmetros `?` | evitam SQL Injection |
