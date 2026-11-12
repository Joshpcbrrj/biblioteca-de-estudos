# Capa do livro

> Arquivo auxiliar da skill `revisar-curso-biblioteca`. Leia só na Fase 6, ao criar ou refazer a capa de um curso.

Todo curso publicado tem `capa.png` na pasta do curso (o workflow já usa `--epub-cover-image` quando ela existe) e o `capa.svg` de origem ao lado.

- **Formato**: 1600 × 2560 px (proporção 1:1,6, a recomendada para Kindle e Kobo), PNG. Faça em SVG e renderize com Playwright (viewport 1600 × 2560) para PNG.
- **Conteúdo obrigatório** (padrão do usuário): plataforma(s) em letra pequena, o **nome do curso** em destaque (sem a plataforma e o criador, que têm linhas próprias), uma **imagem** que represente o assunto, o criador ("Curso de <Criador>") e, no rodapé, `Criado por: Josué B. Almeida`. A posição de cada elemento pode variar conforme o conceito da capa, desde que a hierarquia fique clara.

## Direção de arte: capa de editora, não template

Trabalhe como um designer editorial especializado em livros de tecnologia. Tome como referência de qualidade as melhores capas do gênero (as coleções técnicas de editoras como O'Reilly, Manning, Pragmatic Bookshelf, No Starch Press e A Book Apart) e a tradição do design editorial (Penguin, design suíço, Bauhaus). Aprenda os **princípios** delas, sem copiar o estilo reconhecível de nenhuma (nada de imitar a gravura de animal da O'Reilly ou a moldura de uma coleção):

- **Uma ideia por capa.** Cada capa nasce de um conceito visual próprio, uma metáfora do assunto, e não de um layout reaproveitado. Exemplos: Git → uma árvore de commits que se ramifica; banco de dados → camadas de um cilindro em corte; redes → uma constelação de nós ligados; Java/POO → objetos que se encaixam como blocos; lógica → um labirinto ou fluxograma abstrato; back-end → requisições atravessando camadas; matemática → a própria curva, figura ou símbolo do tema.
- **Escolha um arquétipo** e varie entre os cursos, para a biblioteca não ficar homogênea:
  1. **Tipográfico**: o título é a imagem (letras enormes, recortadas, sobrepostas ou compondo uma forma), grid suíço e muito espaço vazio.
  2. **Geométrico abstrato**: poucas formas simples (círculos, retângulos, linhas) numa composição assimétrica, cores chapadas, espírito Bauhaus.
  3. **Ilustração-metáfora**: um objeto ou cena desenhada em SVG (flat, isométrico ou traço) que traduz o assunto.
  4. **Diagramático**: um diagrama do próprio conteúdo (árvore, grafo, curva) ampliado e estilizado como arte, não como figura didática.
  5. **Padrão generativo**: textura gerada por código (grade de bits, ondas, tesselas, linhas de código desfocadas em blocos) com o título num bloco de cor.
- **Paleta própria por curso**: 2 a 3 cores principais e 1 de destaque, com contraste forte. Não repita a paleta nem o fundo de outro livro da biblioteca; fuja do clichê "fundo azul-escuro com degradê e cartões".
- **Tipografia**: no máximo duas famílias (título e apoio), hierarquia clara por tamanho e peso, um único alinhamento (esquerda ou centro), entrelinha apertada em títulos grandes, espaçamento de letras aberto em rótulos pequenos em maiúsculas. Use as fontes disponíveis no renderizador: uma serifada (Georgia, DejaVu Serif) dá ar editorial, uma mono (Menlo, DejaVu Sans Mono) dá ar técnico, uma sem serifa (Helvetica, Arial) dá ar moderno.
- **Composição**: grid com margens de pelo menos 100 px, regra dos terços ou assimetria intencional, um único ponto focal, espaço para respirar. Evite empilhar cartões com ícones (fica com cara de slide), molduras genéricas e enfeites que não dizem nada.
- **Acabamento**: espessuras de linha coerentes, espaçamentos consistentes, nada encostando nas margens, nenhum texto sobre área de baixo contraste, detalhes finos (sombras sutis, sobreposições, transparências) só quando melhoram a leitura.

## Referências visuais escolhidas pelo usuário (toque criativo)

O usuário mandou um painel de capas de livros de tecnologia que ele gosta. Use estes **recursos visuais** como repertório, combinando e variando entre os cursos (nunca copie uma capa, uma ilustração ou a marca de uma editora):

- **Metáfora central forte e "viva"**: um objeto-símbolo grande no centro, com brilho ou luz própria. Exemplos das referências: cérebro em linhas finas cercado por órbitas e pontos de luz; lâmpada acesa sobre cubos isométricos; perfil de cabeça que se dissolve em trilhas de circuito; olho em macro com dados sobrepostos; globo dividido ao meio.
- **Isometria e camadas translúcidas**: painéis de interface, chaves `{ }`, janelas e blocos flutuando em perspectiva isométrica, semitransparentes, com 1 ou 2 cores de destaque (amarelo, laranja) sobre fundo grafite.
- **Tipografia de impacto**: título em sem serifa **condensada, em maiúsculas e enorme**, ocupando a largura (com sombra suave ou leve brilho neon); rótulos e nomes com **espaçamento de letras bem aberto** (`L E T ' S  C O D E`); subtítulo em mono ou em peso fino de outra cor; mistura de pesos no mesmo título ("Tecnologia **na** Infância").
- **Planos diagonais e faixas**: grandes recortes de cor em diagonal (terracota sobre marrom), faixa ondulada no rodapé, faixa de cor atrás do subtítulo.
- **Bloco editorial sobre arte**: um retângulo de cor sólida com o título, sobreposto a uma ilustração de página inteira (textura de desenho, padrão ou cena).
- **Dualidade**: fundo dividido em dois tons e objeto dividido ao meio para mostrar contraste (antes × depois, certo × errado, front × back).
- **Texturas de tecnologia**: grade fina de fundo, dígitos binários ou código desfocado, trilhas de circuito com nós redondos, árvore de ícones em círculos ligados por setas.
- **Paletas que funcionam**: grafite + amarelo/laranja; roxo profundo + rosa; azul-marinho + ciano brilhante; creme + preto + coral; terracota + marrom + branco; lavanda × pêssego; vinho + metálico. Escolha uma diferente para cada curso.
- **Clima**: profundidade (luz no centro, vinheta nas bordas), brilho sutil nos elementos-chave, sensação de "capa de livro" e não de slide.

Como traduzir isso no SVG: degradê radial para a luz central; `filter` com `feGaussianBlur` para brilho; formas isométricas com `polygon`; linhas finas (2–4 px) com baixa opacidade para órbitas, grades e circuitos; fontes condensadas quando houver (DejaVu Sans Condensed, Liberation Sans Narrow) ou `transform="scale(0.82,1)"` no texto para condensar. Confira sempre a legibilidade em miniatura e em cinza.

## Processo da capa

1. Liste as capas já existentes (`ls programacao/*/capa.png matematica/*/capa.png`) e veja-as em miniatura com `Read`, para que a nova seja **diferente** em conceito, arquétipo e paleta.
2. Esboce **3 conceitos** com arquétipos diferentes, renderize os três e compare lado a lado em miniatura.
3. Escolha o melhor pelo checklist abaixo e refine (alinhamentos, pesos, cores, respiros). Só então gere o PNG final.
4. Envie ao usuário a capa escolhida com `SendUserFile` (as alternativas também, se ajudarem a decidir).

## Checklist de qualidade da capa

- Dá para entender o assunto em 2 segundos, só pela imagem?
- O título é lido numa miniatura de 200 px e em tons de cinza?
- Parece a capa de um livro de boa editora, e não um slide ou template?
- É claramente diferente das outras capas da biblioteca?
- Não tem marca, logotipo ou personagem de terceiros, nem imitação reconhecível de uma coleção?
- **De onde vem a imagem central**, nesta ordem:
  1. **criada por você** em SVG: ilustração original ligada ao tema (fluxograma, bloco de código, gráfico de função, figuras geométricas, símbolos matemáticos...);
  2. **imagem do próprio curso** que seja do usuário (um diagrama nosso, por exemplo);
  3. **imagem da internet** só com licença livre que permita reuso (domínio público, CC0, CC BY com crédito no README do curso), baixada de fonte confiável como o Wikimedia Commons.
- **Nunca** use nem recrie logotipos, marcas ou personagens de terceiros (inclusive da escola/criador do curso), mesmo que o usuário mande como referência: o repositório é público e o livro é um resumo não oficial. Use a referência só para entender o estilo desejado (composição, cores, clima) e crie algo original que não seja reconhecível como a marca. Diga isso ao usuário em uma frase.
- **Legibilidade**: o título precisa ser legível numa miniatura de 200px de largura (fonte ≥ 120px na arte de 1600px) e em tons de cinza (e-ink). Confira renderizando também a 200px e em escala de cinza.
- Mostre a capa no topo do `README.md` do curso (`<img src="capa.png" width="260">`) e envie a imagem ao usuário para aprovação junto do resumo final.
