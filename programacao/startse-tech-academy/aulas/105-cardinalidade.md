# Cardinalidade

> 🗺️ **Nesta aula:** o que é cardinalidade, os relacionamentos 1:1, 1:N e N:M, como cada um vira tabela no banco e a notação de mínimo e máximo.

## De onde paramos

Na introdução, a coluna `cliente_id` ligava pedidos a clientes. Mas como saber de que lado colocar a chave estrangeira, ou se é preciso uma tabela extra? A resposta está na cardinalidade.

## O que é cardinalidade

**Cardinalidade diz quantos registros de uma entidade podem se relacionar com quantos registros da outra.** Ela define **onde fica a chave estrangeira** e se é preciso criar uma tabela extra.

![Os três tipos de relacionamento e como cada um vira tabela.](../img/cardinalidade.svg)

> 💡 **Analogia:** pense numa escola. Cada aluno tem **uma** carteirinha e cada carteirinha é de **um** aluno (1:1). Uma turma tem **muitos** alunos, mas cada aluno está em **uma** turma (1:N): basta anotar a turma na ficha do aluno. Já alunos e disciplinas são **muitos para muitos** (N:M): ninguém consegue anotar tudo numa ficha só, então a escola mantém uma **lista de matrículas**, que é exatamente a tabela associativa.

## Um para um (1:1)

Cada registro de A se liga a **no máximo um** de B, e vice-versa.

- Exemplos: pessoa ↔ passaporte; usuário ↔ perfil detalhado.
- **No banco:** a chave estrangeira fica em um dos lados, com `UNIQUE` para garantir que não se repita.

```sql
CREATE TABLE passaportes (
  id        INT PRIMARY KEY,
  numero    VARCHAR(20) NOT NULL,
  -- UNIQUE garante o 1:1
  pessoa_id INT UNIQUE NOT NULL,
  FOREIGN KEY (pessoa_id) REFERENCES pessoas(id)
);
```

Relações 1:1 são raras. Muitas vezes os dados poderiam estar na mesma tabela; separe quando parte deles for opcional, sensível ou pouco usada.

## Um para muitos (1:N)

Um registro de A se liga a **vários** de B, mas cada B pertence a **um** A. É o tipo **mais comum**.

- Exemplos: cliente → pedidos; categoria → produtos; post → comentários.
- **No banco:** a chave estrangeira fica no lado **N** (o "muitos").

```sql
CREATE TABLE pedidos (
  id         INT PRIMARY KEY,
  cliente_id INT NOT NULL,
  FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
```

## Muitos para muitos (N:M)

Vários A se ligam a vários B.

- Exemplos: alunos ↔ disciplinas; pedidos ↔ produtos; filmes ↔ atores.
- **No banco:** **não dá** para resolver com uma coluna só. É preciso uma **tabela associativa** (tabela de junção), com uma chave estrangeira para cada lado.

```sql
CREATE TABLE matriculas (
  aluno_id       INT,
  disciplina_id  INT,
  -- pode guardar dados da própria relação
  data_matricula DATE,
  -- impede matrícula duplicada
  PRIMARY KEY (aluno_id, disciplina_id),
  FOREIGN KEY (aluno_id) REFERENCES alunos(id),
  FOREIGN KEY (disciplina_id)
    REFERENCES disciplinas(id)
);
```

## Mínimo e máximo

A notação completa indica **mínimo e máximo** de cada lado: `(0,N)` = opcional, pode ter vários; `(1,1)` = obrigatório, exatamente um. Por exemplo, um cliente tem `(0,N)` pedidos (pode não ter nenhum), e um pedido tem `(1,1)` cliente.

No banco, o **mínimo 1** vira `NOT NULL` na chave estrangeira.

> ⚠️ **Correção:** o exemplo original de 1:1 ("um cliente tem apenas um endereço de entrega") não é realista, pois clientes costumam ter vários endereços. Foi trocado por pessoa ↔ passaporte.

## Exercício

Classifique cada relacionamento e diga onde fica a chave estrangeira: (a) país e capital; (b) autor e livro, considerando que um livro pode ter vários autores; (c) departamento e funcionário, em que cada funcionário trabalha em um só departamento.

<details>
<summary>Ver resposta</summary>

| Relação | Cardinalidade | Onde fica a FK |
| --- | --- | --- |
| país e capital | 1:1 | em um dos lados, com `UNIQUE` |
| autor e livro | N:M | tabela associativa `autores_livros` |
| departamento e funcionário | 1:N | em `funcionarios.departamento_id` |

</details>

## 🧠 Revisão rápida

**Num 1:N, em qual tabela fica a chave estrangeira?**

No lado N (o "muitos").

**Como implementar um N:M?**

Com uma tabela associativa que tem uma chave estrangeira para cada lado.

**O que garante o 1:1 no banco?**

Uma chave estrangeira com `UNIQUE`.

> ➡️ **Próximo passo:** desenhar todas as entidades e relacionamentos de um sistema: **Modelo entidade relacionamento (ER)**.

## 📌 Resumo

| Tipo | Em uma frase |
| --- | --- |
| 1:1 | FK em um lado, com `UNIQUE` |
| 1:N | FK no lado N; o mais comum |
| N:M | tabela associativa com duas FKs |
| (0,N) | opcional, pode ter vários |
| (1,1) | obrigatório, exatamente um |
| Mínimo 1 | vira `NOT NULL` |
