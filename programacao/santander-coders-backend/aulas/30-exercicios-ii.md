# Exercícios II

> 🗺️ **Nesta lista:** cinco perguntas sobre classes de IP, resolução DNS, tracert, SSO e segmentação de rede, mais um cálculo de sub-rede de bônus.

## De onde paramos

Esta lista fecha o módulo de redes, cobrindo a segunda metade: sub-redes, DNS, comandos e segurança.

## Questão 1

A tabela de classes de endereço IP é dividida em cinco classes. Qual a importância dela para a organização das redes?

<details>
<summary>Ver resposta</summary>

Ela determina, pelo primeiro octeto, quantas **redes** e quantos **hosts por rede** cada classe comporta (A: poucas redes enormes; C: muitas redes pequenas) e reserva faixas para usos especiais (D para multicast, E experimental). Hoje o CIDR substituiu as classes por máscaras de qualquer tamanho, mas a ideia de dividir rede e host continua a mesma.

</details>

## Questão 2

Como funciona o fluxo de uma resolução DNS?

<details>
<summary>Ver resposta</summary>

O navegador pergunta ao **resolvedor**. O resolvedor consulta um **servidor raiz**, que indica os servidores do **TLD** (.com, .br...); o servidor TLD indica o **autoritativo** do domínio; o autoritativo responde o IP. O resolvedor devolve o IP ao navegador e guarda em cache.

</details>

## Questão 3

Você precisa descobrir o caminho que um pacote percorreu até o destino. Qual comando ajuda?

<details>
<summary>Ver resposta</summary>

`tracert` no Windows (ou `traceroute` no Linux e no macOS). Ele lista cada roteador do caminho e a latência de cada salto.

</details>

## Questão 4

Qual a importância de usar SSO (Single Sign-On)?

<details>
<summary>Ver resposta</summary>

Com um único login, o usuário acessa vários sistemas: o provedor de identidade emite um **token** que os sistemas aceitam no lugar da senha. Isso reduz o número de senhas (e o risco de reutilizá-las), centraliza o controle de acesso e permite bloquear tudo de uma vez quando alguém sai da empresa.

</details>

## Questão 5

Por que é importante separar a rede Wi-Fi corporativa entre funcionários e visitantes?

<details>
<summary>Ver resposta</summary>

Para **isolar** a rede interna, onde estão os sistemas e dados da empresa. Um aparelho de visitante pode estar infectado ou ser usado num ataque; na rede de visitantes ele só chega à internet, nunca aos servidores internos. Isso se faz com redes (SSIDs) e VLANs separadas e regras de firewall entre elas.

</details>

## Bônus

Quantos hosts úteis cabem em 10.0.0.0/22? Qual o último host?

<details>
<summary>Ver resposta</summary>

/22 deixa 32 − 22 = 10 bits de host: 2¹⁰ − 2 = **1.022 hosts**. A rede vai de 10.0.0.0 a 10.0.3.255 (broadcast), então o último host é **10.0.3.254**.

</details>

> ➡️ **Próximo passo:** começar a programar em Java.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 | Classes de IP |
| 2 | Resolução DNS |
| 3 | Comandos de diagnóstico |
| 4 | SSO |
| 5 | Segmentação e segurança |
| Bônus | Cálculo de sub-rede |
