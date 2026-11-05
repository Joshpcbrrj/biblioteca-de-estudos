# Exercícios I

> 🗺️ **Nesta lista:** cinco perguntas sobre quem organiza a internet, equipamentos, cabos, TCP × UDP e o protocolo IP. Responda com suas palavras antes de abrir.

## De onde paramos

Você viu equipamentos, cabos, os modelos em camadas e os endereços IP. Hora de conferir.

## Questão 1

Qual é a responsabilidade da ICANN?

<details>
<summary>Ver resposta</summary>

A **ICANN** (Internet Corporation for Assigned Names and Numbers) coordena os **identificadores únicos** da internet: distribui os grandes blocos de endereços IP aos registros regionais (que repassam a provedores e empresas) e administra o sistema de nomes de domínio no topo, credenciando quem opera os domínios de topo (.com, .org...) e coordenando a zona raiz do DNS.

</details>

> ⚠️ **Ajuste:** a resposta original dizia que a ICANN "gerencia os servidores DNS". Ela coordena o sistema, mas os servidores são operados por várias organizações: os servidores raiz por 12 entidades diferentes, os de cada TLD pelos seus registros (o .br pelo NIC.br) e os demais pelos donos dos domínios.

## Questão 2

Qual é o papel do switch em uma rede e por que ele substituiu o hub?

<details>
<summary>Ver resposta</summary>

O switch faz a **comutação de quadros** na rede local: lê o endereço MAC de destino e entrega o quadro só na porta certa. Substituiu o hub porque permite envio **unicast** e várias conversas simultâneas, enquanto o hub repete tudo para todas as portas e gera colisões.

</details>

## Questão 3

O cabo coaxial transporta bits através de qual meio?

<details>
<summary>Ver resposta</summary>

Sinais elétricos em condutores de **cobre** (o fio central e a malha de blindagem).

</details>

## Questão 4

Os protocolos TCP e UDP estão na camada 4 do modelo OSI. Qual a diferença entre eles?

<details>
<summary>Ver resposta</summary>

O **TCP** abre uma conexão, confirma o recebimento de cada parte, reenvia o que se perde e entrega na ordem. O **UDP** só envia, sem conexão nem confirmação: é mais rápido e usado quando um pouco de perda é aceitável (vídeo ao vivo, jogos, voz).

</details>

## Questão 5

O que é o protocolo IP?

<details>
<summary>Ver resposta</summary>

É o **Internet Protocol**, da camada de rede. Ele dá um endereço a cada dispositivo e permite que os roteadores encaminhem os pacotes, salto a salto, até o destino. Não garante entrega: isso fica a cargo do TCP, na camada de cima.

</details>

> ➡️ **Próximo passo:** dividir redes com máscara de sub-rede.

## 📌 Resumo

| Questão | O que pratica |
| --- | --- |
| 1 | Organização da internet (ICANN) |
| 2 | Switch × hub |
| 3 | Meios de transmissão |
| 4 | TCP × UDP |
| 5 | Protocolo IP |
