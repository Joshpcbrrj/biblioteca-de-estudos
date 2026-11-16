# Criando API REST documentada com Spring Web e Swagger

> 🗺️ **Nesta aula:** o que é REST e o modelo de maturidade de Richardson, como criar endpoints com `@RestController`, documentar a API com Swagger e tratar erros em um só lugar com exception handlers.

## De onde paramos

Você já sabe criar componentes Spring. Agora vai expor esses componentes como endpoints HTTP, com o padrão REST.

## Introdução ao REST e RESTful

> 🗺️ **Nesta aula:** o que é REST, a diferença entre REST e RESTful, as seis restrições de Fielding e os quatro níveis do modelo de maturidade de Richardson.

### De onde paramos

Você já sabe criar uma aplicação Spring Boot. Agora vai aprender o estilo de API que vai expor os dados dela pela web.

### O que é REST?

**REST** (*Representational State Transfer*) é um **estilo de arquitetura** para sistemas distribuídos, descrito por **Roy Fielding** em sua tese de doutorado em **2000**. Na prática, quase sempre é aplicado sobre **HTTP**, e uma "API REST" é uma API que segue esse estilo.

- A API é organizada em **recursos** (usuários, pedidos, produtos), cada um identificado por uma **URI** (ex.: `/usuarios/7`).
- Os recursos são manipulados com os **métodos HTTP**: GET (ler), POST (criar), PUT/PATCH (alterar) e DELETE (remover).
- O cliente recebe **representações** do recurso — normalmente em **JSON**, às vezes XML.
- O servidor usa os **códigos de status** HTTP para indicar o resultado (200, 201, 404…).

> 💡 **Analogia:** numa biblioteca, cada livro tem um endereço na estante (a URI) e há poucas ações possíveis — consultar, emprestar, devolver, descartar (os verbos). Você não precisa de um balcão diferente para cada livro: o mesmo conjunto de ações vale para todos.

#### REST x RESTful

Os termos costumam ser usados como sinônimos. Uma distinção comum é:

- **REST:** o estilo de arquitetura em si.
- **RESTful:** uma API que **aplica** esse estilo. Alguns autores reservam "RESTful" para APIs que seguem **todas** as restrições, inclusive **HATEOAS** (links entre recursos); na prática, a maioria das APIs chamadas de REST não chega a esse ponto.

#### Restrições do REST (segundo Fielding)

1. **Cliente-servidor:** interface e armazenamento de dados ficam separados, e cada lado evolui de forma independente.
2. **Sem estado (*stateless*):** cada requisição traz tudo o que é necessário para ser entendida; o servidor não guarda contexto da sessão entre uma chamada e outra.
3. **Cache:** as respostas informam se podem ser armazenadas em cache, reduzindo carga e latência.
4. **Interface uniforme:**
  - recursos identificados por URIs;
  - manipulação por meio de **representações** (JSON, XML);
  - mensagens **autodescritivas** (método, cabeçalhos e status dizem o que está acontecendo);
  - **HATEOAS** — *Hypermedia as the Engine of Application State*: as respostas trazem links que guiam o cliente para as próximas ações.
5. **Sistema em camadas:** o cliente não sabe se fala direto com o servidor ou com intermediários (proxy, balanceador, cache).
6. **Código sob demanda (opcional):** o servidor pode enviar código executável ao cliente (ex.: JavaScript).

### Modelo de maturidade de Richardson

Leonard Richardson propôs uma escala para medir o quanto uma API adota os princípios do REST.

![Do nível 0 (RPC sobre HTTP) ao nível 3 (HATEOAS).](../img/rest-richardson.svg)

#### Nível 0 — o HTTP é só um transporte

Um **único endpoint** e um único verbo (geralmente POST); a operação desejada vai dentro do corpo, como uma chamada de procedimento remoto (RPC/SOAP).

| Verbo | URL | Corpo |
| --- | --- | --- |
| POST | `/api` | `{ "acao": "buscarUsuario", "id": 1 }` |
| POST | `/api` | `{ "acao": "salvarUsuario", ... }` |
| POST | `/api` | `{ "acao": "excluirUsuario", "id": 1 }` |

#### Nível 1 — recursos

Cada recurso ganha sua própria URI, mas o verbo ainda não tem significado: as ações aparecem no nome da URL e tudo continua via POST.

| Verbo | URL | Operação |
| --- | --- | --- |
| POST | `/usuarios/1/buscar` | Pesquisar usuário |
| POST | `/usuarios/salvar` | Salvar |
| POST | `/usuarios/1/alterar` | Alterar |
| POST | `/usuarios/1/excluir` | Excluir |

#### Nível 2 — verbos e códigos de status

A URI identifica o **recurso** e o **verbo HTTP** diz a **ação**. As respostas usam os códigos de status corretos (`201 Created`, `204 No Content`, `404 Not Found`…). É o nível da maioria das APIs do mercado.

| Verbo | URL | Operação | Resposta típica |
| --- | --- | --- | --- |
| GET | `/usuarios/1` | Pesquisar | `200 OK` |
| POST | `/usuarios` | Criar | `201 Created`  • `Location` |
| PUT | `/usuarios/1` | Alterar | `200 OK` ou `204` |
| DELETE | `/usuarios/1` | Excluir | `204 No Content` |

> 💡 Uma dúvida comum: o GET não deve ter corpo. Se uma busca precisa de muitos filtros, use **parâmetros de consulta** (`GET /usuarios?nome=ana&ativo=true`) ou, em casos complexos, um `POST /usuarios/busca` — sabendo que isso foge um pouco do nível 2.

#### Nível 3 — HATEOAS

A resposta traz **links** para as ações e recursos relacionados. O cliente só precisa conhecer o ponto de entrada da API; o resto ele descobre navegando pelos links.

```json
{
  "nome": "Ana Souza",
  "email": "ana@exemplo.com",
  "_links": {
    "self":
      { "href": "/usuarios/1234" },
    "pedidos":
      { "href": "/usuarios/1234/pedidos" },
    "alterar":
      { "href": "/usuarios/1234",
        "method": "PUT" },
    "excluir":
      { "href": "/usuarios/1234",
        "method": "DELETE" }
  }
}
```

No Spring, o projeto **Spring HATEOAS** ajuda a montar esses links.

> 🛠️ **Ajustes:**
>
> - REST foi descrito como "padrão que utiliza o protocolo HTTP"; ele é um **estilo de arquitetura** (Fielding, 2000), normalmente aplicado sobre HTTP.
> - A lista de "princípios" misturava restrições reais com itens que não são restrições do REST (como "usar o protocolo HTTP" e "interoperabilidade"). Troquei pelas **seis restrições** de Fielding.
> - Os exemplos do modelo de Richardson estavam deslocados: a tabela do nível 1 já usava GET/PUT/DELETE (isso é **nível 2**) e a do nível 0 tinha várias URLs. Refiz os exemplos de cada nível.
> - A imagem foi substituída por um diagrama, e o JSON do nível 3 foi traduzido.

> ➡️ **Próximo passo:** **REST Controller**, para transformar métodos Java em endpoints HTTP.

### 🧠 Revisão rápida

**Quem descreveu o REST e quando?**

Roy Fielding, na tese de doutorado de 2000.

**Uma API com um único endpoint `POST /api` está em qual nível de Richardson?**

Nível 0.

**O que caracteriza o nível 2?**

URIs por recurso + verbos HTTP com significado + códigos de status corretos.

**O que é HATEOAS?**

Respostas com links que mostram ao cliente as próximas ações possíveis (nível 3).

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| REST | Estilo de arquitetura com recursos, URIs e verbos HTTP. |
| Stateless | Cada requisição é completa por si só. |
| Richardson | Níveis 0 (RPC) a 3 (HATEOAS). |
| Nível 2 | Onde está a maioria das APIs. |
| HATEOAS | Links nas respostas guiam o cliente. |

## REST Controller

> 🗺️ **Nesta aula:** o caminho de uma requisição até o controller, as anotações de mapeamento e de parâmetros e um controller REST completo com `ResponseEntity`.

### De onde paramos

Você já sabe o que é REST e quais são os verbos e códigos de status. Agora vai escrever a classe que expõe esses endpoints no Spring.

**REST controllers** são as classes que expõem os **endpoints** da aplicação: recebem as requisições HTTP, chamam a camada de serviço e devolvem a resposta — normalmente em **JSON**.

![O DispatcherServlet encaminha a requisição ao controller certo, que delega ao service.](../img/rest-fluxo.svg)

> 💡 **Analogia:** o controller é a recepção de um hotel. Ele recebe o hóspede (requisição), entende o pedido e chama o setor certo (service) — mas não arruma o quarto nem cozinha. Por isso a regra de negócio fica no service.

### Anotações mais usadas

| Anotação | Para que serve |
| --- | --- |
| `@RestController` | Marca a classe como controller REST. É `@Controller`  • `@ResponseBody`: o retorno dos métodos vira o corpo da resposta (JSON). |
| `@RequestMapping("/usuarios")` | Define o **caminho base** (prefixo) da classe ou de um método. Também aceita o método HTTP (`method = RequestMethod.GET`), mas hoje se usam os atalhos abaixo. |
| `@GetMapping` | Mapeia o método para requisições **GET**. |
| `@PostMapping` | Mapeia para **POST**. |
| `@PutMapping` / `@PatchMapping` | Mapeia para **PUT** / **PATCH**. |
| `@DeleteMapping` | Mapeia para **DELETE**. |
| `@PathVariable` | Lê um trecho do **caminho**: em `@GetMapping("/{id}")`, o valor de `{id}`. |
| `@RequestParam` | Lê um **parâmetro de consulta** (`?nome=ana`). Pode ter `required = false` e `defaultValue`. |
| `@RequestBody` | Converte o **corpo** da requisição (JSON) num objeto Java. |
| `@ResponseStatus` | Define o código de status padrão da resposta (ex.: `HttpStatus.CREATED`). |

### Exemplo completo

```java
@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

  private final UsuarioService service;

  public UsuarioController(
      UsuarioService service) {
    this.service = service;
  }

  // GET /usuarios?nome=ana
  @GetMapping
  public List<Usuario> listar(
    @RequestParam(required = false)
    String nome) {
    return service.listar(nome);
  }

  // GET /usuarios/7
  @GetMapping("/{id}")
  public Usuario buscar(
      @PathVariable Long id) {
    return service.buscar(id);
  }

  // 201 Created + cabeçalho Location
  @PostMapping
  public ResponseEntity<Usuario> criar(
      @RequestBody Usuario usuario) {
    Usuario salvo = service.salvar(usuario);
    URI location = URI.create(
      "/usuarios/" + salvo.getId());
    return ResponseEntity
      .created(location).body(salvo);
  }

  @PutMapping("/{id}")
  public Usuario atualizar(
      @PathVariable Long id,
      @RequestBody Usuario usuario) {
    return service.atualizar(id, usuario);
  }

  // 204 No Content
  @DeleteMapping("/{id}")
  @ResponseStatus(HttpStatus.NO_CONTENT)
  public void excluir(@PathVariable Long id) {
    service.excluir(id);
  }
}
```

> 💡 Use `ResponseEntity` quando precisar controlar o status, os cabeçalhos e o corpo da resposta ao mesmo tempo — como no `201 Created` com o cabeçalho `Location`.

> ⚠️ **@PathVariable × @RequestParam:** o primeiro lê o caminho (`/usuarios/7`) e identifica **qual** recurso; o segundo lê a query (`?nome=ana`) e serve para **filtrar**, ordenar ou paginar.

> 🛠️ **Ajustes:** o `@RequestMapping` foi descrito como a anotação que "indica qual verbo deve ser usado"; seu uso principal é definir o **caminho base**, e os verbos ficam com `@GetMapping`, `@PostMapping` etc. Corrigido o erro de digitação "Itilizada", as anotações viraram uma tabela e acrescentei `@PatchMapping`, `@ResponseStatus`, `ResponseEntity`, um exemplo completo de controller e um diagrama do fluxo da requisição.

> ➡️ **Próximo passo:** **Swagger**, para documentar e testar esses endpoints no navegador.

### 🧠 Revisão rápida

**O que `@RestController` acrescenta a `@Controller`?**

O `@ResponseBody`: o retorno dos métodos vira o corpo da resposta (JSON).

**Qual anotação converte o JSON recebido num objeto Java?**

`@RequestBody`.

**Como devolver `201 Created` com o cabeçalho `Location`?**

`ResponseEntity.created(uri).body(objeto)`.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `@RestController` | Classe que devolve dados (JSON). |
| `@GetMapping` etc. | Liga um método a um verbo e caminho. |
| `@PathVariable` | Lê um trecho do caminho. |
| `@RequestParam` | Lê um parâmetro de consulta. |
| `@RequestBody` | Converte o corpo JSON em objeto. |
| `ResponseEntity` | Controla status, cabeçalhos e corpo. |

## Swagger

> 🗺️ **Nesta aula:** o que são o Swagger e a especificação OpenAPI, suas ferramentas e como gerar a documentação interativa num projeto Spring Boot com springdoc.

### De onde paramos

Você já cria controllers REST com endpoints. Agora vai gerar a documentação da API automaticamente e testá-la no navegador.

### Página do Swagger

🔗 [https://swagger.io/](https://swagger.io/)

#### O que é

**Swagger** é um conjunto de ferramentas open source para **projetar, documentar, testar e consumir APIs REST**. Ele nasceu em **2010–2011**, criado por **Tony Tam** na empresa **Wordnik**, e em **2015** foi adquirido pela **SmartBear**.

Também em 2015 a **especificação** do Swagger foi doada à **OpenAPI Initiative** (Linux Foundation) e passou a se chamar **OpenAPI Specification** — a versão 3.0 saiu em 2017. Hoje:

- **OpenAPI** = a especificação (o formato YAML/JSON que descreve a API);
- **Swagger** = as ferramentas da SmartBear que trabalham com essa especificação.

![Num projeto Spring Boot, o springdoc gera a especificação e o Swagger UI a exibe.](../img/swagger-fluxo.svg)

> 💡 **Analogia:** a especificação OpenAPI é o cardápio do restaurante (o que existe, ingredientes, preço); o Swagger UI é o garçom que mostra o cardápio e deixa você provar cada prato ali mesmo.

#### Vantagens

- **Documentação sempre atualizada:** gerada a partir do código (ou o código gerado a partir dela).
- **Interatividade:** dá para testar cada endpoint direto na página, sem Postman.
- **Padronização:** um formato único para descrever APIs, que facilita o trabalho entre times.
- **Geração de código:** clientes e servidores em várias linguagens a partir da especificação.

#### Principais ferramentas

- **Swagger Editor:** editor web para escrever especificações OpenAPI, com validação e pré-visualização em tempo real.
- **Swagger UI:** página web que mostra a documentação da API a partir da especificação e permite testar os endpoints.
- **Swagger Codegen** (e o projeto comunitário **OpenAPI Generator**): geram clientes e *stubs* de servidor em diversas linguagens.
- **SwaggerHub:** plataforma na nuvem para hospedar, versionar e colaborar em especificações.

### Swagger num projeto Spring Boot

A biblioteca recomendada hoje é o **springdoc-openapi**. Basta adicionar a dependência:

```xml
<dependency>
  <groupId>org.springdoc</groupId>
  <artifactId>
    springdoc-openapi-starter-webmvc-ui
  </artifactId>
  <version>2.6.0</version>
</dependency>
```

Ao subir a aplicação:

- `http://localhost:8080/v3/api-docs` → especificação OpenAPI em JSON;
- `http://localhost:8080/swagger-ui.html` → Swagger UI.

As anotações são opcionais e enriquecem a documentação:

```java
@Tag(name = "Usuários")
@RestController
@RequestMapping("/usuarios")
public class UsuarioController {

  @Operation(
    summary = "Busca um usuário pelo id")
  @ApiResponse(responseCode = "404",
    description = "Usuário não encontrado")
  @GetMapping("/{id}")
  public Usuario buscar(
      @PathVariable Long id) { ... }
}
```

> ⚠️ O antigo **Springfox** (`springfox-swagger2` / `springfox-swagger-ui`) está **abandonado** e não funciona no Spring Boot 3 — e era a origem de muitos erros de dependência (como o do Spring Boot 2.6 com o *path matcher*). Em projetos novos, use o **springdoc-openapi**.

> 🛠️ **Ajustes:**
>
> - O Swagger foi criado na **Wordnik** (por Tony Tam), não "pela Reverb Technologies em 2010"; a SmartBear o adquiriu em 2015. Acrescentei a diferença entre **OpenAPI** (especificação) e **Swagger** (ferramentas).
> - "O Swagger gera a documentação com base nas anotações dos controladores" — quem faz isso em projetos Spring é uma biblioteca de integração (springdoc ou, antigamente, Springfox); o Swagger UI só exibe a especificação.
> - Incluí a configuração com springdoc, os endereços padrão e um diagrama do fluxo.

> ➡️ **Próximo passo:** **Exception handlers**, para devolver erros padronizados nas respostas da API.

### 🧠 Revisão rápida

**Qual a diferença entre OpenAPI e Swagger?**

OpenAPI é a especificação (o formato); Swagger é o conjunto de ferramentas que trabalha com ela.

**Qual biblioteca usar no Spring Boot 3?**

`springdoc-openapi`. O Springfox está abandonado.

**Em que endereço fica o Swagger UI por padrão?**

`/swagger-ui.html`; a especificação JSON fica em `/v3/api-docs`.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| OpenAPI | Especificação que descreve a API em YAML/JSON. |
| Swagger UI | Página para ler e testar a API. |
| springdoc | Gera a especificação a partir do código Spring. |
| `@Operation` / `@Tag` | Enriquecem a documentação. |

## Exception handlers

> 🗺️ **Nesta aula:** como transformar exceções em respostas HTTP padronizadas com `@RestControllerAdvice` e `@ExceptionHandler`, e o formato `ProblemDetail`.

### De onde paramos

Você já documenta a API com Swagger e sabe devolver respostas com status. Agora vai tratar os erros de forma centralizada, para que nenhum endpoint devolva um erro improvisado.

Erros acontecem: dados inválidos enviados pelo cliente, registro inexistente, falha no banco ou num serviço externo. Numa API, o importante é que o cliente receba uma **resposta clara e padronizada** — com o **código de status** certo e uma mensagem útil —, sem expor detalhes internos como *stack traces*.

### O que são exception handlers

**Exception handlers** são métodos que **capturam exceções** lançadas pela aplicação e as transformam em **respostas HTTP**. No Spring, eles costumam ficar numa classe anotada com `@RestControllerAdvice` (ou `@ControllerAdvice`), que vale para **todos** os controllers.

![A exceção lançada no service é capturada pelo advice e vira uma resposta 404 em JSON.](../img/exc-advice.svg)

> 💡 **Analogia:** é o SAC de uma empresa. Qualquer setor que tiver um problema encaminha para o mesmo atendimento, que responde ao cliente de forma educada e padronizada — em vez de cada setor improvisar a sua resposta.

### Como funciona

1. Um controller ou service lança uma exceção (ex.: `UsuarioNaoEncontradoException`).
2. O Spring procura um método `@ExceptionHandler` compatível com o tipo da exceção — primeiro no próprio controller, depois nas classes `@ControllerAdvice`.
3. Se encontrar, executa esse método e devolve a resposta que ele montar.
4. Se não encontrar, o Spring Boot devolve uma resposta de erro padrão (normalmente `500 Internal Server Error`).

### Como criar

```java
// exceção do domínio
public class UsuarioNaoEncontradoException
    extends RuntimeException {
  public UsuarioNaoEncontradoException(
      Long id) {
    super("Usuário " + id
      + " não encontrado");
  }
}

// tratamento centralizado
@RestControllerAdvice
public class GlobalExceptionHandler {

  @ExceptionHandler(
    UsuarioNaoEncontradoException.class)
  public ResponseEntity<Map<String, Object>>
      naoEncontrado(
      UsuarioNaoEncontradoException ex) {
    return ResponseEntity
      .status(HttpStatus.NOT_FOUND)
      .body(Map.of("status", 404,
        "erro", ex.getMessage()));
  }

  @ExceptionHandler(
    IllegalArgumentException.class)
  public ResponseEntity<Map<String, Object>>
      requisicaoInvalida(
      IllegalArgumentException ex) {
    return ResponseEntity.badRequest()
      .body(Map.of("status", 400,
        "erro", ex.getMessage()));
  }

  // rede de segurança para o resto
  @ExceptionHandler(Exception.class)
  public ResponseEntity<Map<String, Object>>
      erroInesperado(Exception ex) {
    // registre o erro completo no log,
    // mas não envie detalhes ao cliente
    return ResponseEntity
      .status(HttpStatus
        .INTERNAL_SERVER_ERROR)
      .body(Map.of("status", 500,
        "erro", "Erro interno."));
  }
}
```

> 💡 A partir do Spring 6 / Spring Boot 3 existe o tipo `ProblemDetail`, que segue a RFC 9457 (*Problem Details for HTTP APIs*) e padroniza o formato do erro: `type`, `title`, `status`, `detail`, `instance`.

### Vantagens

- **Centralização:** um só lugar para o tratamento de erros, sem `try/catch` repetido em cada endpoint.
- **Respostas consistentes:** mesmo formato e códigos de status corretos em toda a API.
- **Segurança:** evita vazar *stack traces*, nomes de tabelas e outros detalhes internos.
- **Observabilidade:** facilita registrar e monitorar os erros num ponto único.

> 🛠️ **Ajustes:** o texto explicava o conceito, mas não tinha nenhum código; acrescentei um exemplo completo com `@RestControllerAdvice`, a ordem em que o Spring procura o handler, o tipo `ProblemDetail` e um diagrama do fluxo no lugar da imagem.

> ➡️ **Próximo passo:** **Projeto REST API**, que junta controllers, Swagger e tratamento de erros numa API completa.

### 🧠 Revisão rápida

**O que faz uma classe `@RestControllerAdvice`?**

Reúne os `@ExceptionHandler` que valem para todos os controllers.

**Por que não devolver o stack trace ao cliente?**

Ele expõe detalhes internos (classes, tabelas, versões) que ajudam atacantes e não ajudam o usuário.

**Se nenhum handler tratar a exceção, o que o cliente recebe?**

A resposta de erro padrão do Spring Boot, normalmente 500.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| `@ExceptionHandler` | Método que trata um tipo de exceção. |
| `@RestControllerAdvice` | Classe com handlers globais. |
| Status correto | 400, 404, 500… conforme o erro. |
| `ProblemDetail` | Formato padrão de erro (RFC 9457). |

## Projeto REST API

> 🗺️ **Nesta aula:** o projeto que junta REST, documentação com Swagger e tratamento de exceções em uma API Spring Boot.

### De onde paramos

Você já viu controllers, Swagger e handlers de exceção separadamente. Agora vai juntá-los numa API só.

#### Spring Web REST API — o que o projeto cobre

- Criar um projeto web com Spring Boot.
- Configurar os controllers e os endpoints.
- Documentar a API com Swagger/OpenAPI.
- Tratar exceções com handlers centralizados.
- E outros pontos do dia a dia de uma API.

#### Vídeo que me ajudou a resolver o problema das dependências do Swagger

🔗 [Resolvendo problemas no Swagger - Java Spring Boot](https://www.youtube.com/watch?v=pMXnR1T47e0)

#### Issue que me ajudou a achar o vídeo

> 💡 Esse tipo de erro costuma vir do **Springfox**, que deixou de ser mantido e quebra em versões novas do Spring Boot. Em projetos novos, troque pelo **springdoc-openapi** (veja a página *Swagger*).

### 📦 Meu projeto de API com Spring, documentada no Swagger

> ➡️ **Próximo passo:** **Adicionando segurança a uma API REST com Spring**, para proteger os endpoints com login e permissões.

### 🧠 Revisão rápida

**Qual anotação devolve os erros de todos os controllers de forma padronizada?**

`@RestControllerAdvice`, com métodos `@ExceptionHandler`.

**Por que preferir o springdoc-openapi ao Springfox?**

O Springfox está abandonado e costuma quebrar em versões novas do Spring Boot.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Projeto | API REST com controllers, Swagger e handlers de erro. |
| Dependências | Confira as versões do Springfox: prefira o springdoc-openapi. |

> ➡️ **Próximo passo:** **Validação de dados com Bean Validation**, para barrar dados inválidos na entrada da API.

## 🧠 Revisão rápida

**Qual a diferença entre `@Controller` e `@RestController`?**

`@RestController` devolve os dados diretamente (JSON), em vez de uma view.

**Qual anotação trata as exceções de todos os controllers em um só lugar?**

`@RestControllerAdvice`.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| REST | estilo de API com recursos identificados por URL e manipulados por métodos HTTP |
| Richardson | níveis 0 a 3: um endpoint, recursos, verbos HTTP e links (HATEOAS) |
| `@RestController` | classe cujos métodos devolvem dados (JSON) |
| Mapeamentos | `@GetMapping`, `@PostMapping`, `@PutMapping`, `@DeleteMapping` |
| Parâmetros | `@PathVariable`, `@RequestParam`, `@RequestBody` |
| `ResponseEntity` | controla o status e o corpo da resposta |
| Swagger / OpenAPI | documentação interativa gerada a partir do código |
| `@RestControllerAdvice` | trata as exceções de todos os controllers num só lugar |
