# Exercícios I

> 🗺️ **Nesta lista:** cinco questões sobre escolha de tipos de dados e relacionamentos entre tabelas, no contexto de pagamentos, supermercado e pronto-socorro.

## De onde paramos

As questões revisam tipos de dados, modelagem e cardinalidade.

## Questão 1

Você está modelando uma tabela de transações de cartão de crédito de um sistema de pagamentos. Para o campo "horário da transação", qual tipo de dado usar?

<details>
<summary>Ver resposta</summary>

Um tipo de **data e hora**. No PostgreSQL, `timestamptz` (timestamp com fuso): transações acontecem em fusos diferentes e precisam ser comparadas no mesmo instante.

</details>

> ⚠️ **Ajuste:** a resposta original era `datetime`, nome usado no MySQL e no SQL Server. O PostgreSQL não tem esse tipo; os equivalentes são `timestamp` e `timestamptz`.

## Questão 2

Na mesma tabela, qual o tipo mais adequado para o campo "id", que será a chave primária da transação?

<details>
<summary>Ver resposta</summary>

`bigint`. Um sistema de pagamentos pode passar dos 2,1 bilhões de registros, limite do `integer`. O `bigint` vai até cerca de 9,2 × 10¹⁸.

</details>

## Questão 3

O estado de aprovação de um pedido de reembolso é guardado num campo booleano. Sobre esse tipo, qual a alternativa correta?

<details>
<summary>Ver resposta</summary>

Ocupa **1 byte** por registro e aceita `true`, `false` ou `null`.

</details>

## Questão 4

Num supermercado, a tabela de marcas tem registros como Nestlé e Lacta, e a de produtos tem Nescau e Diamante Negro. Qual o relacionamento de marca com produto, nessa ordem?

<details>
<summary>Ver resposta</summary>

**1 para N**: uma marca tem vários produtos, e cada produto pertence a uma marca. A chave estrangeira `marca_id` fica em produtos.

</details>

## Questão 5

Num pronto-socorro, cada paciente tem um médico responsável e cada médico atende pelo menos dez pacientes por dia. Qual alternativa está correta?

<details>
<summary>Ver resposta</summary>

A tabela de médicos se relaciona com a de pacientes pela chave estrangeira `id_medico`, que fica na tabela de **pacientes**. É um 1:N: a FK vai para o lado N.

</details>

> ➡️ **Próximo passo:** a segunda lista, sobre comandos SQL, LGPD e índices.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 e 2 | Tipos para data/hora e chaves |
| 3 | Tamanho do boolean |
| 4 e 5 | Cardinalidade 1:N e posição da FK |
