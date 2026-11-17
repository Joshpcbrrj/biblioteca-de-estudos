# Teste de mesa: simulando o programa no papel (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** o que é o teste de mesa, como montar a tabela passo a passo e como usá-lo para achar um erro num laço.

## De onde paramos

Com laços e decisões, os programas ficaram longos o bastante para errar sem perceber: uma volta a mais, uma condição trocada. O teste de mesa é a ferramenta para enxergar o que acontece por dentro.

## O que é

O **teste de mesa** é simular a execução de um algoritmo à mão, anotando numa tabela o valor de cada variável a cada passo. Você faz o papel do computador: lê uma instrução, executa, atualiza a tabela e passa para a próxima.

Serve para:

- entender o que um código faz antes de rodá-lo;
- conferir se o algoritmo dá o resultado esperado;
- encontrar erros de lógica, principalmente em laços e decisões.

## Como montar

1. Crie uma coluna para cada variável, uma para as condições importantes e uma para a saída (o que aparece na tela).
2. Escolha valores de entrada para testar.
3. Siga o código linha a linha, sem pular nada. A cada atribuição, anote o novo valor numa nova linha da tabela.
4. Em cada condição, anote se ela deu V ou F e siga o caminho correspondente.
5. No final, compare a saída com o resultado que você esperava.

![Teste de mesa de um laço que soma de 1 a 4](../img/tm-tabela.svg)

> 💡 **Analogia:** é o extrato bancário do programa. Cada linha registra uma movimentação e o saldo logo depois dela. Se o saldo final não bate, você volta linha por linha até achar a movimentação errada.

## Projeto: achando um erro com o teste de mesa

O programa abaixo deveria ler 3 notas e mostrar a média, mas o resultado sai errado.

```c
programa
{
  real nota, soma = 0.0
  inteiro cont = 1

  funcao inicio()
  {
    // o erro está escondido aqui: com cont
    // começando em 1, "< 3" dá só 2 voltas
    enquanto (cont < 3) {
      escreva("Nota: ")
      leia(nota)
      soma += nota
      cont++
    }
    escreva("Média: ", soma / 3, "\n")
  }
}
```

Teste de mesa digitando as notas 6, 8 e 10 (média esperada: 8):

| Passo | cont | cont < 3? | nota e soma |
| --- | --- | --- | --- |
| início | 1 | – | soma = 0 |
| 1ª volta | 1 → 2 | V | lê 6, soma = 6 |
| 2ª volta | 2 → 3 | V | lê 8, soma = 14 |
| teste | 3 | F | sai e mostra 14 / 3 = 4.67 |

A tabela mostra o problema: com `cont` começando em 1 e a condição `cont < 3`, o laço dá só **duas** voltas. A terceira nota nunca é lida, e a soma de duas notas é dividida por 3.

> 🛠️ **Correção:** usar `cont <= 3` (ou começar `cont` em 0 e manter `cont < 3`). Refazendo o teste de mesa, são três voltas, a soma chega a 24 e a média sai 8.

> 💡 Teste sempre os **limites**: a primeira e a última volta de cada laço e os valores exatos das condições (como 7 em `media >= 7`). A maioria dos erros de laço é de "uma volta a mais ou a menos". Para programas maiores, a depuração do Portugol Studio faz o mesmo trabalho automaticamente.

## 🧠 Revisão rápida

**Quantas voltas dá `para (i = 2; i <= 6; i += 2)`? Monte o teste de mesa.**

3 voltas: i = 2, 4 e 6. Depois i vira 8 e a condição dá falso.

**Por que anotar o resultado da condição (V ou F) em cada passo?**

Porque é ali que o programa decide se continua ou sai; a maioria dos erros de laço aparece nesse ponto.

**Quais valores de entrada vale a pena testar primeiro?**

Os limites: o primeiro e o último valor aceitos e os valores exatos das condições.

> ➡️ **Próximo passo:** use o teste de mesa para conferir suas soluções na **3ª Lista de exercícios**, toda sobre repetição.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Teste de mesa | Simular o programa à mão, anotando as variáveis a cada passo |
| Colunas | Uma por variável, uma por condição importante e uma para a saída |
| Linhas | Uma por passo ou volta do laço |
| Para que serve | Entender o código e achar erros de lógica |
| Onde olhar | Primeira e última volta, valores exatos das condições |
