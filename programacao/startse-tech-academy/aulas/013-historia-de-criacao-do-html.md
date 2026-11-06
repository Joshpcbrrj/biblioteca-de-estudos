# História de criação do HTML

> 🗺️ **Nesta aula:** o que é HTML, a pilha TCP/IP por onde ele viaja, a história da linguagem até o HTML5 e as partes de um elemento HTML.

## De onde paramos

O módulo II terminou com algoritmos e lógica. O HTML é diferente: não descreve passos, descreve **conteúdo**. É a primeira das três camadas do front-end que você vai dominar.

## O que é HTML?

**HTML (*HyperText Markup Language*) é a linguagem de marcação que define a estrutura e o significado do conteúdo de uma página web.** Ela diz ao navegador "isto é um título", "isto é um parágrafo", "isto é um link", "isto é uma imagem".

- HTML **não é linguagem de programação**: não tem variáveis, decisões nem laços. Ela *marca* o conteúdo com **tags**.
- Cada tag tem um propósito, e o navegador a interpreta para exibir o conteúdo.
- O HTML trabalha em conjunto com o **CSS** (aparência) e o **JavaScript** (comportamento). São as três camadas do front-end.

> 💡 "Hipertexto" é texto com **links** para outros textos. Essa ideia de ligar documentos é o coração da Web.

> 💡 **Analogia:** uma página web é como uma casa. O HTML é a estrutura (paredes, portas, cômodos), o CSS é o acabamento (pintura, móveis, iluminação) e o JavaScript é a parte elétrica (interruptores e campainha, que reagem quando alguém mexe).

## O modelo TCP/IP

O HTML viaja pela internet sobre a pilha de protocolos **TCP/IP**.

![Aplicação, transporte, internet e acesso à rede.](../img/tcpip-camadas.svg)

| Camada | Faz | Exemplos |
| --- | --- | --- |
| Aplicação | o que o programa quer dizer | HTTP, HTTPS, DNS, SMTP |
| Transporte | entrega entre programas (portas) | TCP, UDP |
| Internet | endereço e rota entre redes | IP |
| Acesso à rede | envio dentro da rede local | Ethernet, Wi-Fi |

### Linha do tempo

- **Anos 1960**: a ARPA financia a ARPANET, uma rede de **comutação de pacotes**. Entre os nomes centrais estão J.C.R. Licklider, Robert Taylor, Leonard Kleinrock e Lawrence Roberts.
- **1970**: a ARPANET passa a usar o **NCP** (*Network Control Protocol*), que funcionava bem dentro de uma única rede, mas não interligava redes diferentes.
- **1974**: Vint Cerf e Bob Kahn publicam o desenho do **TCP**, pensado para interligar redes diferentes (*inter-net*).
- **1978**: o protocolo é dividido em dois: o **TCP**, que garante a entrega confiável e ordenada, e o **IP**, que endereça e roteia os pacotes.
- **1º de janeiro de 1983**: a ARPANET troca o NCP pelo TCP/IP. É o "nascimento" da internet como rede de redes.
- O **IPv4** (32 bits) domina até hoje. O **IPv6** (128 bits, padronizado em 1998) resolve a falta de endereços.

## Linha do tempo do HTML

| Ano | Marco |
| --- | --- |
| 1980 | Tim Berners-Lee cria o **ENQUIRE**, um programa pessoal de notas ligadas entre si |
| 1989 | Berners-Lee propõe ao CERN um sistema de hipertexto distribuído: a **World Wide Web** |
| 1990–1991 | primeiro navegador, primeiro servidor e o primeiro documento HTML, com cerca de 18 tags, baseado no **SGML** |
| 1995 | **HTML 2.0** (RFC 1866), a primeira especificação oficial, com formulários e imagens |
| 1997 | **HTML 3.2** (tabelas) e **HTML 4.0** (CSS, scripts, frames, acessibilidade) |
| 1999 | **HTML 4.01** |
| 2000 | **XHTML 1.0**: o HTML reescrito com as regras rígidas do XML |
| 2004 | navegadores criam o **WHATWG** e começam o que viraria o HTML5 |
| 2014 | **HTML5** vira recomendação oficial do W3C: tags semânticas, `<video>`, `<audio>`, `<canvas>`, novos campos de formulário |
| 2019 | W3C e WHATWG acordam um padrão único: o **HTML Living Standard**, atualizado continuamente |

> ⚠️ Não houve um "HTML 1.0" oficial: o primeiro padrão foi o HTML 2.0. E **não existe "HTML6"**: desde 2019, o HTML é um padrão vivo, sem números de versão.

## Componentes de um elemento HTML

![Tag de abertura (com atributo e valor), conteúdo e tag de fechamento formam o elemento.](../img/html-anatomia.svg)

- **Tag**: o nome entre `<` e `>`, como `<p>` ou `<a>`.
- **Atributo**: informação extra na tag de abertura, como `href`, `src`, `alt`, `id` ou `class`.
- **Valor**: o que o atributo recebe, sempre entre aspas.
- **Conteúdo**: o que fica entre a abertura e o fechamento. Pode conter outros elementos (aninhamento).
- **Elementos vazios**: não têm conteúdo nem fechamento, como `<img>`, `<br>`, `<hr>`, `<meta>`, `<link>` e `<input>`.

```html
<!-- elemento com atributo e conteúdo -->
<a href="sobre.html">Sobre nós</a>

<!-- elemento vazio -->
<img src="logo.png" alt="Logo da loja">

<!-- aninhamento: feche na ordem inversa -->
<p>Texto com <strong>destaque</strong>.</p>
```

## 🧠 Revisão rápida

**Por que se diz que HTML não é linguagem de programação?**

Porque não tem variáveis, decisões nem laços: só marca o conteúdo com tags.

**Em qual camada do TCP/IP fica o HTTP?**

Na camada de aplicação.

**Em `<img src="a.png" alt="Gato">`, o que é `alt` e o que é `"Gato"`?**

`alt` é o atributo; `"Gato"` é o valor dele.

> ➡️ **Próximo passo:** antes de escrever, saiba onde consultar e como escrever bem: **Principais fontes de documentação sobre HTML e boas práticas de como escrever**.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| HTML | marca a estrutura e o significado do conteúdo |
| HTML × CSS × JS | estrutura, aparência, comportamento |
| TCP/IP | aplicação, transporte, internet, acesso à rede |
| HTML5 / Living Standard | o padrão atual, atualizado continuamente |
| Elemento | abertura com atributos, conteúdo e fechamento |
| Elemento vazio | sem conteúdo nem fechamento (`img`, `br`) |
