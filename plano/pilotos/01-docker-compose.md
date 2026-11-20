# Piloto 1: Docker Compose na prática

**Modo:** Criar · **Área:** tecnologia · **Testa:** ementa já aprovada, laboratórios executados, trilha (continua *Docker do zero*), imagens de processo × diagramas.

## Pedido (colar num chat novo com a skill)

```text
Quero criar um livro com o Syllabook.
Tema: Docker Compose. A ementa já está aprovada (abaixo); pode seguir para a escrita.
<colar a ementa>
```

## Ementa aprovada (2026-11-17)

```text
📘 Docker Compose na prática · iniciante · 14 capítulos · trilha devops (1º)
Para quem: quem já roda contêineres com docker run e quer subir um projeto com vários serviços
Ao terminar, você vai: descrever uma aplicação com API, banco e proxy num compose.yaml e subi-la, desenvolvê-la e configurá-la com um comando
Pré-requisitos: Docker do zero

1. Por que um arquivo para o projeto    → explicar o que o Compose substitui e reconstruir um docker run longo
2. Instalar e conferir o Compose        → verificar o plugin no Docker Desktop e no Linux
3. Primeiro compose.yaml                → subir, listar, ver logs e derrubar com up, ps, logs e down
4. Build pelo Compose                   → construir a imagem a partir de um Dockerfile e reconstruí-la
5. Variáveis, .env e configuração       → trocar valores por variáveis do .env sem editar o arquivo
6. Vários serviços e a rede do projeto  → fazer a API achar o banco pelo nome do serviço
7. Volumes no Compose                   → declarar volume nomeado e entender a diferença entre down e down -v
8. Ordem de início e saúde              → fazer a API esperar o banco com healthcheck e depends_on
9. Comandos do dia a dia                → executar com exec e run e reiniciar com restart policy
10. Desenvolvimento com watch           → ver mudanças do código refletidas sem reconstruir tudo
11. Perfis e arquivos sobrepostos       → separar ferramentas com profiles e configurar dev e produção com override
12. Segredos e dados sensíveis          → tirar a senha do compose.yaml e entregá-la com secrets
13. Recursos e escala                   → limitar CPU e memória e subir réplicas com scale
14. Projeto final: stack completa       → subir API, banco e proxy com dev e produção em um comando

Fica para livros futuros: Swarm, Kubernetes, segurança de imagens, build multiplataforma
Versão de referência: Docker Compose v5.6 com Docker Engine 29.9 (conferido em 2026-11-17)
```

Versão em YAML (cópia de `livros/docker-compose-na-pratica/ementa.yaml`, que será apagado):

```yaml
titulo: "Docker Compose na prática"
slug: docker-compose-na-pratica
trilha: devops
ordem_na_trilha: 1
nivel: iniciante
publico: "Quem já roda contêineres com docker run e quer subir um projeto com vários serviços"
objetivo: "Descrever uma aplicação com API, banco e proxy num compose.yaml e subi-la, desenvolvê-la e configurá-la com um comando"
pre_requisitos: [docker-do-zero]
versao_referencia: "Docker Compose v5.6 com Docker Engine 29.9 (conferido em 2026-11-17)"
fontes:
  - {titulo: "Docker Compose release notes (releases.sh)", url: "https://releases.sh/docker/docker-compose-releases.md", conferido_em: "2026-11-17"}
  - {titulo: "How Compose works", url: "https://docs.docker.com/compose/intro/compose-application-model/", conferido_em: "2026-11-17"}
  - {titulo: "Docker Compose Quickstart", url: "https://docs.docker.com/compose/gettingstarted/", conferido_em: "2026-11-17"}
  - {titulo: "Use Docker Compose (workshop)", url: "https://docs.docker.com/get-started/workshop/08_using_compose/", conferido_em: "2026-11-17"}
aprovada_em: "2026-11-17"
capitulos:
  - {n: 1, titulo: "Por que um arquivo para o projeto", objetivo: "Explicar o que o Compose substitui e reconstruir um docker run longo como um compose.yaml", topicos: [declarativo, servicos, compose-x-docker-run]}
  - {n: 2, titulo: "Instalar e conferir o Compose", objetivo: "Verificar o plugin docker compose no Docker Desktop e no Linux", topicos: [plugin-compose, versao, docker-compose-legado]}
  - {n: 3, titulo: "Primeiro compose.yaml", objetivo: "Subir, listar, ver os logs e derrubar um serviço com up, ps, logs e down", topicos: [services, image, ports, up-down]}
  - {n: 4, titulo: "Build pelo Compose", objetivo: "Fazer o Compose construir a imagem a partir de um Dockerfile e reconstruí-la", topicos: [build, rebuild]}
  - {n: 5, titulo: "Variáveis, .env e configuração", objetivo: "Trocar valores por variáveis do .env sem editar o arquivo", topicos: [interpolacao, env-file, valores-padrao]}
  - {n: 6, titulo: "Vários serviços e a rede do projeto", objetivo: "Fazer a API achar o banco pelo nome do serviço numa rede criada pelo Compose", topicos: [multiplos-servicos, redes, dns-por-servico]}
  - {n: 7, titulo: "Volumes no Compose", objetivo: "Declarar um volume nomeado para o banco e entender a diferença entre down e down -v", topicos: [volumes-nomeados, bind-mounts, down-v]}
  - {n: 8, titulo: "Ordem de início e saúde", objetivo: "Fazer a API esperar o banco ficar pronto com healthcheck e depends_on", topicos: [depends-on, healthcheck, service-healthy]}
  - {n: 9, titulo: "Comandos do dia a dia", objetivo: "Executar comandos num serviço com exec e run, e reiniciar serviços com restart policy", topicos: [exec, run, restart]}
  - {n: 10, titulo: "Desenvolvimento com watch", objetivo: "Ver as mudanças do código refletidas no contêiner sem reconstruir tudo", topicos: [develop-watch, sync, rebuild-watch]}
  - {n: 11, titulo: "Perfis e arquivos sobrepostos", objetivo: "Separar ferramentas opcionais com profiles e configurar desenvolvimento e produção com override", topicos: [profiles, compose-override, merge-de-arquivos]}
  - {n: 12, titulo: "Segredos e dados sensíveis", objetivo: "Tirar a senha do compose.yaml e entregá-la aos serviços com secrets", topicos: [secrets, env-sensivel, git-ignore]}
  - {n: 13, titulo: "Recursos e escala", objetivo: "Limitar CPU e memória de um serviço e subir várias réplicas com scale", topicos: [limites-recursos, scale, replicas]}
  - {n: 14, titulo: "Projeto final: stack completa", objetivo: "Subir API, banco e proxy com dev e produção em um comando, com healthcheck, volume e segredo", topicos: [projeto]}
cobre: [compose, compose-yaml, rede-compose, volumes-compose, healthcheck, perfis, segredos, watch]
fica_para_depois: [swarm, kubernetes, seguranca-de-imagens, build-multiplataforma]
```

## Comportamentos esperados

- Reconhece a ementa como aprovada e não reabre a discussão; monta o grafo de conceitos, grava o `book.yaml` e pergunta só as escolhas (imagens e leitura).
- Confere de novo a versão de referência na documentação oficial antes de escrever (a data da ementa pode estar velha).
- Todo comando e `compose.yaml` executados de verdade (sessão ou computador do aluno); saída real; o que não rodar fica marcado.
- Código sempre em bloco copiável, nunca como imagem; os arquivos do projeto final podem ser recriados só copiando os blocos.
- Diagramas SVG para estrutura (serviços, rede, volumes); ilustração só para processo (ex.: ordem de início com healthcheck), se o usuário escolheu ilustrações.
- Cada capítulo com a escada de prática, revisão cumulativa e fontes datadas.
- Referência cruzada a *Docker do zero* em vez de repetir o básico de contêineres.
- Fecha com Próximos caminhos (Swarm, Kubernetes...), pacote zip com Markdown + EPUB e, se houver GitHub, commit em `created-books/docker-compose-na-pratica/`.
- `audit.py` sem erros antes da entrega.
