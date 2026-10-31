# Regra para construção de algoritmos

> 🗺️ **Nesta aula:** 17 regras para escrever algoritmos corretos e claros, divididas em escrita, estrutura e qualidade, e um exemplo de antes e depois aplicando as regras.

As regras para construção de algoritmos são orientações para que o algoritmo seja **correto**, **claro** e **fácil de transformar em programa**. Elas se dividem em dois grupos: como **escrever** as instruções e como **estruturar** a solução.

## Regras de escrita das instruções

Estas regras valem principalmente para algoritmos em linguagem natural ou pseudocódigo:

1. **Use apenas um verbo por instrução.** Cada linha deve ser uma única ação.
  - ❌ "Pegue a lâmpada e troque-a."
  - ✅ "Pegue a lâmpada nova." / "Retire a lâmpada queimada." / "Coloque a lâmpada nova."
2. **Escreva para quem não conhece o assunto.** Imagine que o algoritmo será seguido por alguém (ou algo, como o computador) que não sabe nada além do que está escrito.
3. **Use frases curtas e simples.**
4. **Seja objetivo.** Evite passos desnecessários ou rodeios.
5. **Evite palavras com duplo sentido** e termos vagos ("um pouco", "até ficar bom", "algumas vezes"). Cada instrução deve ter uma só interpretação.

## Regras de estrutura

6. **Ordem lógica.** Organize as instruções de forma que cada uma possa usar o resultado das anteriores.
7. **Entrada, processamento e saída.** Deixe claro o que o algoritmo recebe, o que faz com isso e o que entrega (veja **Fases de um algoritmo**).
8. **Variáveis com nomes significativos.** Declare as variáveis antes de usar e dê nomes que digam o que guardam: `mediaFinal` em vez de `m`.
9. **Indentação.** Recue as instruções que estão dentro de um `Se` ou de um laço. Isso deixa visível o que pertence a cada bloco.
10. **Comentários quando ajudarem.** Use-os para explicar o **porquê** de um trecho que não é óbvio, não para repetir o que o código já diz.
11. **Estruturas de controle adequadas.** Use `Se...então...senão` para decisões e laços (`Enquanto...faça`, `Para...faça`) para repetições, em vez de copiar a mesma instrução várias vezes.
12. **Divida em partes (modularidade).** Problemas grandes ficam mais fáceis quando quebrados em subproblemas menores, cada um resolvido separadamente (em programas, cada parte costuma virar uma função).
13. **Garanta que termina.** Todo laço precisa de uma condição que em algum momento se torne falsa.

## Regras de qualidade

14. **Teste com várias entradas**, inclusive casos-limite: zero, números negativos, valores iguais, a nota exatamente no limite (7,0).
15. **Pense na eficiência.** Entre duas soluções corretas, prefira a que faz menos passos ou usa menos memória.
16. **Documente** o problema resolvido, a entrada esperada e a saída produzida.
17. **Revise e ajuste.** Um algoritmo melhora com testes e feedback.

## Exemplo: aplicando as regras

**Antes** (ambíguo, várias ações por linha, nomes ruins):

```
Leia os números e some e veja se é grande
Se for, mostre
```

**Depois:**

```
Algoritmo SomaMaiorQueCem
Início
  Declare numero1, numero2, soma: Real

  // Entrada
  Leia numero1
  Leia numero2

  // Processamento
  soma <- numero1 + numero2

  // Saída
  Se soma > 100 então
    Escreva "A soma ", soma, " é maior que 100"
  Senão
    Escreva "A soma ", soma, " não é maior que 100"
  FimSe
Fim
```

Mudanças aplicadas: um verbo por linha, critério objetivo ("maior que 100" em vez de "grande"), nomes significativos, fases separadas por comentários, indentação dentro do `Se` e uma resposta também para o caso negativo.

## 📌 Resumo da aula

| Grupo | Regras principais |
| --- | --- |
| Escrita | um verbo por instrução · frases curtas · nada de termos vagos ("um pouco", "até ficar bom") |
| Estrutura | ordem lógica · entrada → processamento → saída · nomes significativos · indentação · laços em vez de repetir linhas · dividir em partes · garantir que termina |
| Qualidade | testar casos-limite · preferir a solução mais simples e eficiente · documentar · revisar |

**Checklist rápido antes de dar o algoritmo por pronto:** cada linha faz uma coisa só? Alguém de fora entenderia? Todo laço termina? Testei com zero, negativos e valores iguais?
