# Normalização de dados (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** o que é normalização, as anomalias que ela evita, a 1ª, 2ª e 3ª Formas Normais aplicadas passo a passo a uma tabela de pedidos, e quando desnormalizar de propósito.

## De onde paramos

Você sabe criar tabelas e ligá-las por chaves. Mas como decidir **quais** tabelas criar? A normalização é o método para chegar a um bom desenho.

## O que é normalização

Imagine uma planilha de pedidos em que o nome e o endereço do cliente se repetem em toda linha. Se ele mudar de endereço, você precisa corrigir dezenas de linhas, e basta esquecer uma para o banco passar a contar duas verdades. Essas falhas têm nomes: anomalia de **atualização** (mudar em um lugar e esquecer outro), de **inserção** (não poder cadastrar um cliente sem pedido) e de **exclusão** (apagar o único pedido e perder os dados do cliente). A **normalização** é o processo de organizar as tabelas, por etapas chamadas formas normais, para que cada informação fique guardada **em um único lugar**.

**Normalização é o processo de organizar as tabelas para que cada informação fique guardada em um lugar só.** Isso evita **redundância** e as chamadas **anomalias**:

- **de atualização**: a cidade da Ana muda, mas está repetida em 50 pedidos, e um deles fica desatualizado;
- **de inserção**: não dá para cadastrar um produto que ainda não foi vendido;
- **de exclusão**: apagar o único pedido de um cliente apaga também os dados do cliente.

![Antes, a cidade da Ana se repete; depois, ela fica num lugar só.](../img/normalizacao.svg)

> 💡 **Analogia:** é a diferença entre um caderno de recados e uma agenda de contatos. No caderno, você escreve o endereço da Ana em todo recado sobre ela; quando ela se muda, precisa caçar e corrigir cada página, e sempre escapa uma. Na agenda, o endereço fica **uma vez** no contato da Ana, e os recados só dizem "Ana". Normalizar é passar do caderno para a agenda.

## Ponto de partida: uma tabela "planilha"

| pedido | cliente (cidade) | produtos | precos |
| --- | --- | --- | --- |
| 1 | Ana (Recife) | café, chá | 39.90, 19.90 |
| 2 | Ana (Recife) | café | 39.90 |
| 3 | Beto (Natal) | bolo | 25.00 |

Problemas: listas dentro da célula, Ana e Recife repetidos e o preço do café repetido.

## 1ª Forma Normal (1FN): valores atômicos

Cada célula guarda **um único valor**, sem listas nem grupos repetidos. A lista de produtos vira uma linha por item:

| pedido | cliente (cidade) | produto | preco |
| --- | --- | --- | --- |
| 1 | Ana (Recife) | café | 39.90 |
| 1 | Ana (Recife) | chá | 19.90 |
| 2 | Ana (Recife) | café | 39.90 |
| 3 | Beto (Natal) | bolo | 25.00 |

## 2ª Forma Normal (2FN): depender da chave inteira

Está na 1FN e **nenhuma coluna depende só de parte da chave**. Aqui a chave é `(pedido, produto)`, mas `preco` depende só de `produto`, e `cliente` só de `pedido`. Separamos:

- `pedidos(id, cliente, cidade_cliente)`
- `produtos(id, nome, preco)`
- `itens_pedido(pedido_id, produto_id, quantidade)`

## 3ª Forma Normal (3FN): sem dependência entre colunas comuns

Está na 2FN e **nenhuma coluna depende de outra coluna que não seja a chave**. `cidade_cliente` depende do **cliente**, e não do pedido, então o cliente ganha a própria tabela:

- `clientes(id, nome, cidade)`
- `pedidos(id, cliente_id, data)`
- `produtos(id, nome, preco)`
- `itens_pedido(pedido_id, produto_id, quantidade, preco_unit)`

Resumo fácil de lembrar: cada coluna deve depender **"da chave, da chave inteira e de nada além da chave"**.

## Desnormalizar de propósito

Normalizar evita repetição e inconsistência, mas tem um custo: os dados ficam espalhados em várias tabelas, e consultá-los exige `JOIN`s. Em alguns cenários, vale **quebrar a regra de propósito** e repetir um dado para ganhar velocidade. Exemplos: guardar o nome do cliente dentro do pedido para o relatório não precisar juntar tabelas, ou manter um campo `total` calculado em vez de somar os itens a cada consulta. A diferença entre desnormalizar e bagunçar está na intenção: você só desnormaliza **depois** de modelar corretamente, com um ganho de desempenho medido e sabendo que precisará manter as cópias sincronizadas.

Às vezes **repetir dados é a escolha certa**:

- `itens_pedido.preco_unit` guarda o preço **da época da compra**, porque, se o preço do produto mudar, o pedido antigo não pode mudar junto;
- relatórios e dashboards muito acessados podem usar tabelas resumo para evitar JOINs pesados.

A regra: **normalize primeiro**, até a 3FN, e desnormalize só com um motivo claro.

## Exercício

Normalize até a 3FN a tabela `matriculas(aluno, email_aluno, disciplina, professor, sala_professor)`, sabendo que cada disciplina tem um único professor e cada professor tem uma sala.

<details>
<summary>Ver resposta</summary>

- `alunos(id, nome, email)`
- `professores(id, nome, sala)`
- `disciplinas(id, nome, professor_id)`
- `matriculas(aluno_id, disciplina_id)`

O e-mail depende do aluno (parte da chave), por isso sai na 2FN. A sala depende do professor, que depende da disciplina: dependência transitiva, resolvida na 3FN.

</details>

## 🧠 Revisão rápida

**O que a 1FN exige?**

Valores atômicos: um valor por célula, sem listas.

**Qual problema a 3FN resolve?**

Colunas que dependem de outra coluna comum, e não da chave.

**Por que `preco_unit` fica repetido em `itens_pedido`?**

Para guardar o preço da época da compra, mesmo que o produto mude de preço.

> ➡️ **Próximo passo:** os comandos que criam e alteram essas estruturas: **Linguagem de definição de dados (DDL)**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Normalização | cada informação num lugar só |
| Anomalias | atualização, inserção e exclusão |
| 1FN | valores atômicos |
| 2FN | dependência da chave inteira |
| 3FN | nada além da chave |
| Desnormalizar | só com motivo claro (histórico, desempenho) |
