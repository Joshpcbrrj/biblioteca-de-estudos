# Laço de Repetição “Faça-Enquanto”

> ✨ **Página nova.** O `faca-enquanto` é o terceiro laço do Portugol e só aparecia de passagem na aula de vetores.

> 🗺️ **Nesta aula:** o laço que executa o bloco antes de testar a condição, a diferença para o `enquanto`, e os dois usos mais comuns: menus e validação de entrada.

## O laço faca-enquanto

No `enquanto`, a condição é testada **antes** de cada volta, e o bloco pode nem ser executado. No `faca-enquanto`, o bloco vem **primeiro** e a condição é testada **depois**. Por isso ele sempre executa o bloco **pelo menos uma vez**.

```c
faca {
  // executado uma vez, e de novo enquanto a condição for verdadeira
} enquanto (condicao)
```

![enquanto x faca-enquanto](../img/fe-comp.svg)

> 💡 O `faca-enquanto` é a escolha natural quando o bloco **produz** o valor que a condição vai testar: ler um dado e repetir se ele for inválido, mostrar um menu e repetir até escolherem "sair". Com o `enquanto`, seria preciso ler uma vez antes do laço e outra dentro dele.

## Os três laços lado a lado

| Laço | Testa a condição | Mínimo de voltas | Use quando |
| --- | --- | --- | --- |
| `para` | Antes de cada volta | 0 | Se sabe quantas voltas serão |
| `enquanto` | Antes de cada volta | 0 | Não se sabe quantas voltas, e talvez nenhuma |
| `faca-enquanto` | Depois de cada volta | 1 | O bloco precisa rodar pelo menos uma vez |

## Projeto: validando uma nota

A nota deve estar entre 0 e 10. Enquanto o usuário digitar um valor fora disso, o programa pergunta de novo.

```c
programa
{
  real nota

  funcao inicio()
  {
    faca {
      escreva("Digite a nota (0 a 10): ")
      leia(nota)

      se (nota < 0 ou nota > 10) {
        escreva("Nota inválida! Tente de novo.\n")
      }
    } enquanto (nota < 0 ou nota > 10)

    escreva("Nota registrada: ", nota, "\n")
  }
}
```

Compare com a versão em `enquanto`: seria preciso um `leia` antes do laço e outro dentro dele.

## Projeto: menu que repete até sair

```c
programa
{
  inteiro opcao, num

  funcao inicio()
  {
    faca {
      escreva("\n1 - Ver o dobro | 2 - Ver o quadrado | 0 - Sair\n")
      escreva("Opção: ")
      leia(opcao)

      escolha (opcao) {
        caso 1:
          escreva("Número: ")
          leia(num)
          escreva("Dobro: ", num * 2, "\n")
          pare
        caso 2:
          escreva("Número: ")
          leia(num)
          escreva("Quadrado: ", num * num, "\n")
          pare
        caso 0:
          escreva("Até logo!\n")
          pare
        caso contrario:
          escreva("Opção inválida.\n")
      }
    } enquanto (opcao != 0)
  }
}
```

> ⚠️ Não confunda o `enquanto (condicao)` que fecha o `faca` com o início de um novo laço `enquanto`. Ele não tem bloco próprio: termina ali mesmo, logo depois do `}`.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `faca { } enquanto (cond)` | Executa o bloco e só depois testa a condição |
| Garantia | O bloco roda pelo menos uma vez |
| Repete quando | A condição é verdadeira, como no `enquanto` |
| Uso típico | Validar entradas e repetir menus |
| Diferença para o `enquanto` | Dispensa a leitura antes do laço |
