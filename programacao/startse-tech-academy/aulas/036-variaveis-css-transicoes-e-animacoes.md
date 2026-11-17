# Variáveis CSS, transições e animações (Adicionado pelo aluno para melhorar o estudo)

> 🗺️ **Nesta aula:** variáveis CSS para reaproveitar valores, transições para suavizar mudanças de estado e animações com `@keyframes`, respeitando quem prefere menos movimento.

## De onde paramos

A aula de cores mostrou uma variável `--cor-primaria` de passagem, e a de pseudo-classes usou `transition` no sublinhado animado. Esta aula explica as duas ferramentas a fundo e fecha o módulo IV.

## Variáveis CSS (custom properties)

Num site grande, a mesma cor azul aparece em dezenas de regras. Se o designer pedir um azul diferente, você teria de achar e trocar todas, e é fácil esquecer alguma. Com uma variável, você define o azul uma vez e o usa em todo lugar com `var(--cor-primaria)`. Trocar o valor no `:root` muda o site inteiro. É a forma mais simples de manter o visual consistente, e é a base do modo escuro.

**Variáveis guardam um valor para reutilizar no CSS inteiro.** Mude em um lugar, e o site todo muda.

```css
/* :root = o <html>: valem para a página toda */
:root {
  --cor-primaria: #1a73e8;
  --cor-texto: #222;
  --raio: 8px;
  --espaco: 1rem;
}

.botao {
  background: var(--cor-primaria);
  border-radius: var(--raio);
  padding: var(--espaco) calc(var(--espaco) * 2);
}

/* valor padrão se a variável não existir */
.alerta { color: var(--cor-alerta, crimson); }
```

Elas seguem a **cascata**: dá para redefinir em um trecho da página.

```css
.tema-escuro {
  --cor-texto: #eee;
  --cor-fundo: #121212;
}
```

E dá para trocar pelo JavaScript (módulo VII):

```jsx
document.documentElement.style
  .setProperty("--cor-primaria", "tomato");
```

## Transições: suavizar mudanças

Sem transição, um botão muda de cor de uma vez ao passar o mouse, e o olho percebe um "pulo". Com `transition`, a mudança leva um tempo curto, como 0,2 segundo, e parece natural. Você declara a transição no estado **normal** do elemento, e não no `:hover`. Assim ela vale na ida e na volta: o botão suaviza ao receber o mouse e também ao perdê-lo.

Uma **transição** anima a passagem entre dois estados, como normal → `:hover`.

```css
/* transition: anima a cor e a posição */
.botao {
  background: var(--cor-primaria);
  transition: background-color .2s ease,
              transform .2s ease;
}
.botao:hover {
  background: #1558b0;
  transform: translateY(-2px);
}
```

Formato: `transition: propriedade duração curva atraso`. Curvas comuns: `ease` (padrão), `linear`, `ease-in`, `ease-out` e `cubic-bezier(...)`.

> 💡 Prefira animar `transform` e `opacity`: o navegador faz isso na GPU, sem recalcular o layout. Animar `width`, `height`, `top` ou `margin` pode deixar a página travando. Evite também `transition: all`, que anima coisas que você não pretendia.

### As transformações mais usadas

| Função | Faz |
| --- | --- |
| `translate(x, y)` | move |
| `scale(1.1)` | aumenta ou diminui |
| `rotate(45deg)` | gira |
| `skew(10deg)` | inclina |

## Animações com `@keyframes`

A transição só vai de um estado a outro quando algo a dispara. A animação roda por conta própria e pode ter várias etapas. Primeiro você descreve os quadros no `@keyframes`, com `from` e `to` ou com porcentagens, e depois aplica a animação ao elemento com `animation`. Um bom uso é o efeito de aparecer ao carregar a página: o elemento começa invisível e deslocado, e termina visível no lugar. O valor `infinite` repete sem parar, útil para indicadores de carregamento.

Para movimentos que rodam sozinhos ou têm várias etapas:

```css
/* @keyframes: quadros de início e fim */
@keyframes aparecer {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes girar {
  to { transform: rotate(360deg); }
}

.card    { animation: aparecer .4s ease-out both; }
.loading { animation: girar 1s linear infinite; }
```

Propriedades de `animation`:

| Propriedade | Exemplo | Faz |
| --- | --- | --- |
| `animation-name` | `aparecer` | qual `@keyframes` usar |
| `animation-duration` | `.4s` | duração |
| `animation-timing-function` | `ease-out` | curva |
| `animation-delay` | `.1s` | espera antes de começar |
| `animation-iteration-count` | `infinite` | quantas vezes |
| `animation-direction` | `alternate` | ida e volta |
| `animation-fill-mode` | `both` | mantém o primeiro/último quadro |

![Transição × animação](../img/st-transicao-2.svg)

> 💡 **Analogia:** uma transição é como um dimmer de luz: você gira o botão e a lâmpada passa suavemente de apagada para acesa, só quando alguém mexe. Uma animação com `@keyframes` é como o pisca-pisca de Natal: segue uma sequência programada sozinha, quantas vezes você mandar.

## Respeite quem prefere menos movimento

Movimento excessivo pode causar tontura e náusea em algumas pessoas, e o sistema operacional permite que elas peçam menos animação. O bloco acima lê esse pedido e reduz as durações a quase zero, mantendo o site funcional e sem efeitos. Incluir isso é um gesto simples de cuidado, e vale ser parte do seu CSS padrão desde o começo.

Algumas pessoas sentem tontura com animações. O sistema operacional permite pedir "reduzir movimento", e o CSS consegue ler isso:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: .01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: .01ms !important;
  }
}
```

## Exercício

Crie um botão que, ao passar o mouse, cresça 5% e escureça a cor em 0,2 s, usando uma variável para a cor.

<details>
<summary>Ver resposta</summary>

```css
/* :root: variável reutilizável no CSS */
:root { --cor-botao: hsl(220 90% 50%); }

.botao {
  background: var(--cor-botao);
  color: white;
  transition: transform .2s, background .2s;
}
.botao:hover {
  transform: scale(1.05);
  background: hsl(220 90% 40%);
}
```

</details>

## 🧠 Revisão rápida

**Onde declarar variáveis que valem para a página toda?**

Em `:root`.

**Qual a diferença entre transição e animação?**

A transição anima a mudança entre dois estados (como o `:hover`); a animação com `@keyframes` roda sozinha e pode ter várias etapas.

**Quais propriedades animam com melhor desempenho?**

`transform` e `opacity`.

> ➡️ **Próximo passo:** fim do módulo IV. O módulo V organiza os elementos na tela, começando por **Media queries**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Variável | `--nome` em `:root`, usada com `var()` |
| Transição | anima a mudança entre estados |
| `transform` | move, escala, gira e inclina |
| `@keyframes` | animação com etapas |
| `animation` | nome, duração, curva, repetição |
| Movimento reduzido | `prefers-reduced-motion` |
