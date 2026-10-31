# Estrutura de Decisão Condicional Escolha Caso

> 🗺️ **Nesta aula:** o `escolha`/`caso` como alternativa a longas cadeias de `senao se`, o papel do `pare` e do `caso contrario`, e um menu de letras.

## Para que serve

O `escolha` seleciona uma opção entre várias, comparando **uma variável** com uma lista de valores possíveis. Ele substitui uma sequência longa de `se ... senao se` quando todas as condições são do tipo "a variável é igual a tal valor?".

- Deixa o código mais curto e fácil de ler.
- Facilita a depuração e a inclusão de novas opções.
- Funciona com valores exatos (`inteiro` ou `caracter`), não com faixas como `nota >= 7`. Para faixas, use `se`.

## Sintaxe

```c
escolha (variavel) {
  caso valor_1:
    // comandos para o valor 1
    pare
  caso valor_2:
    // comandos para o valor 2
    pare
  caso valor_3:
    // comandos para o valor 3
    pare
  caso contrario:
    // comandos se nenhum caso combinar
}
```

- `pare` encerra o `escolha`. Sem ele, o programa continua executando os comandos dos casos seguintes, mesmo que não combinem.
- `caso contrario` é o "nenhuma das anteriores", como o `senao` final. É opcional e, por ser o último, não precisa de `pare`.

![Fluxo do escolha / caso com pare](../img/es-escolha.svg)

## Projeto: escolhendo uma letra

**Código**

```c
programa
{
  caracter opcao

  funcao inicio()
  {
    escreva("Digite uma letra (opções válidas: a, b, c): ")
    leia(opcao)

    escolha (opcao) {
      caso 'a':
        escreva("A opção escolhida foi a letra A\n")
        pare
      caso 'b':
        escreva("A opção escolhida foi a letra B\n")
        pare
      caso 'c':
        escreva("A opção escolhida foi a letra C\n")
        pare
      caso contrario:
        escreva("Você digitou uma opção inválida\n")
    }
  }
}
```

> 💡 A comparação diferencia maiúsculas de minúsculas: digitar `A` cai no `caso contrario`, porque `'A'` e `'a'` são caracteres diferentes.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `escolha (variavel)` | Compara uma variável com uma lista de valores exatos |
| `caso valor:` | Bloco executado quando a variável tem esse valor |
| `pare` | Encerra o `escolha`; sem ele, os casos seguintes também rodam |
| `caso contrario` | Nenhum caso combinou (como o `senao` final) |
| Limite | Só valores exatos (inteiro ou caractere); para faixas, use `se` |
