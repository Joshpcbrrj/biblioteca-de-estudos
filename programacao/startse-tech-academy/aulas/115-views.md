# Views

> 🗺️ **Nesta aula:** o que é uma view, como criar, usar, alterar e apagar, para que serve (simplificar, proteger e padronizar), quando dá para alterar dados por ela e o que é uma view materializada.

## De onde paramos

Algumas consultas, como "quanto cada cliente já gastou", se repetem em vários relatórios e envolvem JOIN e agregação. Em vez de reescrevê-las toda vez, dá para salvá-las no banco.

## O que é uma view

**Uma view é uma consulta** `SELECT` **salva no banco com um nome, que pode ser usada como se fosse uma tabela.** Ela não armazena dados: cada vez que você consulta a view, o banco executa a consulta por trás dela.

![A view junta clientes e pedidos e expõe só as colunas necessárias.](../img/view-sql.svg)

> 💡 **Analogia:** uma view é uma **janela** para dentro do depósito. Quem olha por ela vê só a parte que a janela enquadra (as colunas e linhas escolhidas), sem entrar no depósito nem mexer nas prateleiras escondidas. E a janela mostra a cena **ao vivo**: se algo muda lá dentro, você vê na hora. A view materializada é diferente: é uma **foto** tirada pela janela, rápida de olhar, mas que precisa ser tirada de novo para ficar atualizada.

## Criando e usando

```sql
CREATE VIEW vw_resumo_clientes AS
SELECT c.nome,
       COUNT(p.id)  AS pedidos,
       SUM(p.total) AS gasto
FROM clientes c
JOIN pedidos p ON p.cliente_id = c.id
GROUP BY c.id, c.nome;

-- usa como uma tabela
SELECT * FROM vw_resumo_clientes
WHERE gasto > 100
ORDER BY gasto DESC;

-- altera ou apaga
CREATE OR REPLACE VIEW vw_resumo_clientes AS ...;
DROP VIEW vw_resumo_clientes;
```

## Para que servem

Uma view é uma consulta com nome, e isso traz três ganhos práticos. O primeiro é a **simplicidade**: uma consulta com cinco `JOIN`s e filtros complicados vira `SELECT * FROM v_pedidos_completos`, e todo o time passa a usar a mesma lógica, sem copiar e colar. O segundo é a **segurança**: você pode dar acesso a uma view que mostra só algumas colunas (por exemplo, sem o salário) e negar o acesso à tabela original. O terceiro é a **estabilidade**: se a estrutura das tabelas mudar, você ajusta a view e os relatórios que a usam continuam funcionando sem alteração.

- **Simplificar**: um JOIN complicado é escrito uma vez e reaproveitado em vários relatórios.
- **Segurança**: o usuário recebe permissão só na view (`GRANT SELECT ON vw_... TO analista`), sem ver colunas sensíveis como `cpf` ou `senha_hash`.
- **Abstração**: se a estrutura das tabelas mudar, basta ajustar a view, e quem a usa não percebe.
- **Padronização**: todo mundo calcula "gasto do cliente" do mesmo jeito.

## Dá para alterar dados por uma view?

Só em **views simples** (uma tabela, sem `GROUP BY`, `DISTINCT`, agregações ou `UNION`). Nesse caso, `INSERT`/`UPDATE`/`DELETE` na view vão para a tabela original. Views com JOIN e agregação, como a do exemplo, são **somente leitura**.

`WITH CHECK OPTION` impede inserir pela view uma linha que ela própria não mostraria:

```sql
CREATE VIEW vw_produtos_ativos AS
SELECT * FROM produtos WHERE ativo = TRUE
-- bloqueia INSERT de produto inativo por esta view
WITH CHECK OPTION;
```

## View × view materializada

Uma view comum **não guarda dados**: toda vez que é consultada, o banco executa a consulta de novo, e o resultado está sempre atualizado. Isso é ótimo para consultas leves, mas pode ser lento se a consulta for pesada. A **view materializada** guarda o **resultado** em disco, como uma foto tirada num momento; consultá-la é muito rápido, mas os dados podem ficar defasados até que ela seja atualizada (`REFRESH MATERIALIZED VIEW`, no PostgreSQL). Escolha pela necessidade: se precisa do dado em tempo real, view comum; se precisa de velocidade e aceita alguns minutos de atraso, como em relatórios e painéis, view materializada.

Uma view comum roda a consulta **toda vez**. Em consultas pesadas, o **PostgreSQL** e o **Oracle** oferecem a **view materializada** (`CREATE MATERIALIZED VIEW`), que **guarda o resultado** e é atualizada sob demanda (`REFRESH MATERIALIZED VIEW`). O MySQL não tem esse recurso nativo.

> ⚠️ **Correção:** a aula dizia que "as alterações feitas nos dados através de uma view são refletidas nas tabelas", como se isso valesse sempre. Só vale para views **atualizáveis** (simples, de uma tabela, sem agregação).

## Exercício

Crie uma view `vw_produtos_baratos` com nome e preço dos produtos abaixo de R$ 20 e consulte-a ordenando pelo preço.

<details>
<summary>Ver resposta</summary>

```sql
-- a view guarda a consulta, não os dados
CREATE VIEW vw_produtos_baratos AS
SELECT nome, preco
FROM produtos
WHERE preco < 20;

SELECT * FROM vw_produtos_baratos
ORDER BY preco;
```

Como é uma view simples, de uma tabela só, ela também é atualizável.

</details>

## 🧠 Revisão rápida

**Uma view guarda dados?**

Não. Ela executa a consulta a cada uso (exceto a materializada).

**Como uma view ajuda na segurança?**

Dando acesso só à view, que esconde colunas sensíveis.

**Dá para fazer `UPDATE` numa view com `GROUP BY`?**

Não. Ela é somente leitura.

> ➡️ **Próximo passo:** regras que o próprio banco garante: **Restrições de atributo e de tabela**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| View | consulta salva usada como tabela |
| `CREATE OR REPLACE VIEW` | cria ou altera |
| Segurança | expõe só as colunas permitidas |
| View atualizável | simples, de uma tabela |
| `WITH CHECK OPTION` | barra linhas fora do filtro |
| Materializada | guarda o resultado; precisa de refresh |
