# Explorando Padrões de Projetos na Prática com Java

> 🗺️ **Nesta aula:** módulo sobre padrões de projeto do GoF: os conceitos, três padrões clássicos implementados em Java puro (Singleton, Strategy e Facade) e depois os mesmos padrões aplicados em uma API com Spring Boot.

## De onde paramos

Você já organiza a API em camadas e viu o Spring criar os beans. Agora vai reconhecer soluções clássicas para problemas recorrentes de projeto.

## Introdução

> 🗺️ **Nesta aula:** o que são padrões de projeto, o livro do GoF e as três categorias com os 23 padrões.

### De onde paramos

Você já sabe criar classes, usar interfaces e aplicar SOLID. Agora vai ver soluções prontas e nomeadas para problemas que aparecem em quase todo sistema.

### Padrões de projeto

**Padrões de projeto (design patterns) são soluções consolidadas para problemas recorrentes no desenvolvimento e na manutenção de software orientado a objetos.** Eles não são código pronto: são modelos de solução, com nome, problema, estrutura e consequências, que você adapta ao seu contexto.

> 💡 **Analogia:** são como receitas clássicas de cozinha. "Molho branco" não é um prato pronto, mas todo cozinheiro sabe o que é, quando usar e como adaptar. Dizer "use um Strategy aqui" comunica uma solução inteira em duas palavras.

A principal referência é o livro ***Design Patterns: Elements of Reusable Object-Oriented Software*** (1994), de **Erich Gamma, Richard Helm, Ralph Johnson e John Vlissides**, autores que ficaram conhecidos como ***Gang of Four*** **(GoF)**. O livro cataloga **23 padrões**, divididos em três categorias:

![Os 23 padrões do GoF por categoria; os marcados com ★ são vistos neste curso.](../img/gof-categorias.svg)

- **Criacionais**: abstraem *como* os objetos são criados. São eles: Abstract Factory, Builder, Factory Method, Prototype e Singleton.
- **Estruturais**: tratam de *como* classes e objetos se combinam em estruturas maiores. São eles: Adapter, Bridge, Composite, Decorator, Facade, Flyweight e Proxy.
- **Comportamentais**: cuidam da comunicação e da divisão de responsabilidades entre objetos. São eles: Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method e Visitor.

> 🛠️ **Correções:**
>
> - A lista de padrões comportamentais estava incompleta: faltavam Command, Interpreter, Mediator, Memento, State e Visitor. Agora estão os 11.
> - Faltava uma vírgula entre Facade e Flyweight.
> - O livro foi lançado em outubro de 1994. O copyright da edição é de 1995, por isso as duas datas aparecem por aí.

> ➡️ **Próximo passo:** **Singleton**, o primeiro padrão criacional, com suas variantes em Java.

### 🧠 Revisão rápida

**Quais são as três categorias do GoF?**

Criacionais, estruturais e comportamentais.

**Em qual categoria fica o Singleton? E o Strategy? E o Facade?**

Singleton: criacional. Strategy: comportamental. Facade: estrutural.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Padrão de projeto | Solução consolidada e nomeada para um problema recorrente. |
| GoF | Livro de 1994 com 23 padrões. |
| Criacionais | Como criar objetos (5). |
| Estruturais | Como combinar classes e objetos (7). |
| Comportamentais | Como os objetos interagem (11). |

## Singleton

> 🗺️ **Nesta aula:** o padrão Singleton, suas variações em Java (lazy, eager, lazy holder e enum) e como o Spring aplica a mesma ideia com os beans.

### De onde paramos

Você já sabe o que é um padrão de projeto e as três categorias do GoF. Agora vai ver o primeiro deles, que controla quantas instâncias de uma classe existem.

### «Padrão criacional»

**Objetivo:** garantir que uma classe tenha **uma única instância** e oferecer um ponto global de acesso a ela.

![O construtor é privado; todos obtêm a instância pelo método estático.](../img/singleton-uml.svg)

**Quando usar:** quando faz sentido existir um único objeto compartilhado, como configuração, cache, pool de conexões ou log.

> 💡 **Analogia:** um país tem um único presidente em exercício. Ninguém "cria" outro com `new`: todos falam com o mesmo, pelo cargo (o método `getInstancia()`).

### Variações em Java

#### Lazy (preguiçoso)

A instância só é criada no primeiro uso.

```java
public class SingletonLazy {
  private static SingletonLazy instancia;

  private SingletonLazy() { }

  public static SingletonLazy getInstancia() {
    if (instancia == null) {
      instancia = new SingletonLazy();
    }
    return instancia;
  }
}
```

> ⚠️ Esta versão **não é thread-safe**: duas threads podem passar pelo `if` ao mesmo tempo e criar duas instâncias.

#### Eager (apressado)

A instância é criada quando a classe é carregada. É thread-safe, porque a JVM garante a inicialização de campos estáticos uma única vez.

```java
public class SingletonEager {
  private static final SingletonEager
    INSTANCIA = new SingletonEager();

  private SingletonEager() { }

  public static SingletonEager getInstancia() {
    return INSTANCIA;
  }
}
```

#### Lazy Holder

Junta o melhor dos dois: é preguiçoso e thread-safe, sem `synchronized`. A classe interna só é carregada na primeira chamada de `getInstancia()`.

```java
public class SingletonLazyHolder {
  private SingletonLazyHolder() { }

  private static class Holder {
    static final SingletonLazyHolder
      INSTANCIA = new SingletonLazyHolder();
  }

  public static SingletonLazyHolder
      getInstancia() {
    return Holder.INSTANCIA;
  }
}
```

> 💡 **Alternativa:** um `enum` com um único valor (`enum Config { INSTANCIA; }`) também é um singleton thread-safe e resistente a serialização e reflexão. Joshua Bloch recomenda essa forma em *Effective Java*.

### Singleton no Spring

Os beans do Spring têm escopo **singleton por padrão**: o container cria **uma instância por contexto** e a injeta onde for pedida (`@Autowired` ou construtor). É o mesmo objetivo do padrão, mas quem controla a instância é o container. A classe não precisa de construtor privado nem de método estático.

> ⚠️ Singletons são compartilhados entre threads. Evite guardar estado mutável neles (ex.: um campo com o "usuário atual"), ou você terá condições de corrida.

> ➡️ **Próximo passo:** **Strategy**, um padrão comportamental para trocar algoritmos sem `if`.

### 🧠 Revisão rápida

**Quais são os dois ingredientes do Singleton clássico?**

Construtor privado e um método estático que devolve a instância única.

**Por que o lazy simples não é thread-safe?**

Duas threads podem passar pelo `if (instancia == null)` ao mesmo tempo e criar duas instâncias.

**Como o Spring garante uma instância só de um `@Service`?**

O container cria um bean singleton por contexto e injeta sempre o mesmo.

### 📌 Resumo

| Variação | Em uma frase |
| --- | --- |
| Lazy | Cria no primeiro uso; não é thread-safe. |
| Eager | Cria ao carregar a classe; thread-safe. |
| Lazy Holder | Preguiçoso e thread-safe, via classe interna. |
| Enum | Thread-safe e à prova de reflexão. |
| Spring | Beans são singleton por padrão. |

## Strategy

> 🗺️ **Nesta aula:** o padrão Strategy, um exemplo com comportamentos de um robô, as vantagens do padrão e como ele aparece no Spring.

### De onde paramos

Você já viu o Singleton e como o Spring controla as instâncias. Agora vai ver como trocar um comportamento inteiro sem mexer na classe que o usa.

### «Padrão comportamental»

**Objetivo:** definir uma família de algoritmos intercambiáveis para resolver o mesmo problema, encapsular cada um em sua própria classe e permitir **trocar o algoritmo em tempo de execução**, sem alterar quem o usa.

![O Robo depende só da interface; cada comportamento é uma estratégia concreta.](../img/strategy-uml.svg)

> 💡 **Analogia:** o aplicativo de mapas oferece rota de carro, a pé ou de ônibus. O destino é o mesmo; você troca a estratégia de cálculo com um toque, sem reinstalar o app.

### Exemplo: comportamentos de um robô

```java
// cada tipo fica em seu próprio arquivo .java
public interface Comportamento {
  void mover();
}

public class ComportamentoNormal
    implements Comportamento {
  public void mover() {
    System.out.println("Movendo normalmente");
  }
}

public class ComportamentoDefensivo
    implements Comportamento {
  public void mover() {
    System.out.println("Movendo defensivo");
  }
}

public class ComportamentoAgressivo
    implements Comportamento {
  public void mover() {
    System.out.println("Movendo agressivo");
  }
}

public class Robo {
  private Comportamento comportamento =
    new ComportamentoNormal();

  public void setComportamento(
      Comportamento c) {
    this.comportamento = c;
  }

  public void mover() {
    // delega para a estratégia atual
    comportamento.mover();
  }
}
```

Uso:

```java
Robo robo = new Robo();
robo.mover(); // normal
robo.setComportamento(
  new ComportamentoDefensivo());
robo.mover(); // defensivo
// estratégia via lambda
robo.setComportamento(
  () -> System.out.println("Parado."));
robo.mover();
```

### Por que usar

- **Elimina ifs e switches** que escolhem o algoritmo: cada variação vive em sua própria classe.
- Segue o princípio **aberto/fechado**: para criar um comportamento novo, você adiciona uma classe, sem mexer no `Robo`.
- Facilita testes: dá para injetar uma estratégia falsa.

> 💡 **Em Java moderno:** se a interface tem um único método, ela é funcional, e a estratégia pode ser um lambda. O `Comparator` passado para `list.sort(...)` é um Strategy do dia a dia.

### Strategy no Spring

Declare uma interface (ex.: `ClienteService`) e uma ou mais implementações anotadas com `@Service`. Quem usa depende só da interface, e o Spring injeta a implementação. Com várias implementações, escolha com `@Qualifier` ou injete todas numa `Map<String, ClienteService>`.

> ➡️ **Próximo passo:** **Facade**, que esconde vários subsistemas atrás de um método simples.

### 🧠 Revisão rápida

**Qual problema o Strategy resolve?**

Trocar o algoritmo em tempo de execução sem encher a classe de `if`/`switch`.

**Por que uma estratégia pode ser um lambda?**

Porque a interface tem um único método abstrato (é funcional).

**Cite um Strategy da biblioteca padrão do Java.**

O `Comparator` usado em `list.sort(...)`.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Strategy | Família de algoritmos atrás de uma interface. |
| Contexto | A classe (Robo) que delega à estratégia atual. |
| Troca | `setComportamento(...)` em tempo de execução. |
| Aberto/fechado | Novo comportamento = nova classe. |
| Spring | Interface de serviço + implementações `@Service`. |

## Facade

> 🗺️ **Nesta aula:** o padrão Facade, um exemplo de migração de cliente que esconde três subsistemas atrás de um método e como ele aparece nos services do Spring.

### De onde paramos

Você já viu como Strategy troca um comportamento por dentro. Agora vai ver como esconder várias integrações atrás de uma interface simples.

### «Padrão estrutural»

**Objetivo:** oferecer uma **interface simples** que reduza a complexidade das integrações com um conjunto de subsistemas. O cliente conversa só com a fachada, que sabe quais subsistemas chamar e em que ordem.

![O cliente faz uma chamada; a Facade coordena CRM, consulta de CEP e e-mail.](../img/facade-uml.svg)

> 💡 **Analogia:** o botão "ligar" do home theater. Por trás, ele liga a TV, o receiver e o projetor, ajusta a entrada e o volume. Você aperta um botão só.

### Exemplo: migrar um cliente

Sem a fachada, quem quisesse cadastrar um cliente teria de conhecer a API de CEP, o CRM e o serviço de e-mail. Com ela, basta uma chamada:

```java
// Subsistemas (cada um com sua API)
class CepApi {
    String recuperarCidade(String cep) {
        return "Araraquara";
    }
    String recuperarEstado(String cep) {
        return "SP";
    }
}

class CrmService {
    void gravarCliente(String nome, String cep,
            String cidade, String estado) {
        System.out.printf(
            "Cliente %s salvo: %s - %s/%s%n",
            nome, cep, cidade, estado);
    }
}

// Facade
public class Facade {
    private final CepApi cepApi = new CepApi();
    private final CrmService crm =
        new CrmService();

    public void migrarCliente(String nome,
                              String cep) {
        String cidade =
            cepApi.recuperarCidade(cep);
        String estado =
            cepApi.recuperarEstado(cep);
        crm.gravarCliente(
            nome, cep, cidade, estado);
    }
}

// Cliente
new Facade().migrarCliente("Ana", "14801-788");
```

### Por que usar

- **Desacopla** o cliente dos subsistemas: se a API de CEP mudar, só a Facade é alterada.
- Deixa o código cliente curto e legível.
- Não esconde nada à força: quem precisar pode continuar acessando os subsistemas diretamente.

> 💡 **No dia a dia com Spring:** uma classe `@Service` que orquestra vários repositórios e clientes HTTP, expondo métodos como `inserir(cliente)`, é na prática uma Facade.

> ➡️ **Próximo passo:** **Praticando os padrões de projeto com o Spring**, onde Singleton, Strategy e Facade aparecem num projeto real.

### 🧠 Revisão rápida

**O Facade impede o acesso direto aos subsistemas?**

Não. Ele só oferece um caminho mais simples; quem precisar ainda pode usá-los diretamente.

**Se a API de CEP mudar, quem precisa ser alterado?**

Só a Facade; os clientes continuam chamando `migrarCliente`.

### 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Facade | Interface simples na frente de subsistemas complexos. |
| Benefício | Desacopla o cliente dos detalhes. |
| Spring | Um `@Service` orquestrador é uma Facade. |

## Praticando os padrões de projeto com o Spring

> 🗺️ **Nesta aula:** onde Singleton, Strategy e Facade aparecem num projeto Spring Boot, a arquitetura da API de clientes com ViaCEP e o código do cliente Feign e do serviço.

### De onde paramos

Você já viu Singleton, Strategy e Facade isoladamente. Agora vai reconhecê-los num projeto Spring Boot com API, JPA e OpenFeign.

### Os padrões dentro do Spring

- ***Singleton***: os beans (`@Component`, `@Service`, `@Repository`, `@Bean`) são **singletons por padrão**. O container cria uma instância e a injeta com `@Autowired` ou pelo construtor.
- ***Strategy***: definimos a interface `ClienteService` e a implementação `ClienteServiceImpl` (`@Service`). O controller depende só da interface, então a implementação pode ser trocada sem tocar nele. Os repositórios (`@Repository`, interfaces do Spring Data) seguem a mesma ideia.
- ***Facade***: a API REST esconde atrás de métodos simples (`inserir`, `atualizar`, `buscarPorId`...) a integração com o **Spring Data JPA** (banco **H2** em memória) e com a API pública **ViaCEP**, consumida via **OpenFeign**.

> 🛠️ **Correção:** `@Autowired` não *cria* singletons. Ele só injeta o bean. O que define a instância única é o **escopo** do bean, que é `singleton` por padrão.

> 💡 **Analogia:** é um restaurante com cozinha que pode trocar de cozinheiro. O cliente pede um prato pelo nome do cardápio (a interface `ClienteService`); a cozinha pode trocar quem prepara sem que o pedido mude.

### Arquitetura do projeto

![O controller depende da interface ClienteService; a implementação orquestra os repositórios JPA e o cliente Feign do ViaCEP.](../img/spring-padroes.svg)

#### Cliente Feign para o ViaCEP

```java
@FeignClient(name = "viacep",
  url = "https://viacep.com.br/ws")
public interface ViaCepService {

  @GetMapping("/{cep}/json/")
  Endereco consultarCep(
    @PathVariable("cep") String cep);
}
```

Para ativar, anote a classe principal com `@EnableFeignClients` e inclua a dependência `spring-cloud-starter-openfeign`.

> 💡 **Feign em uma frase:** você só escreve a interface com as anotações HTTP; o Feign cria, em tempo de execução, a classe que faz a chamada e converte o JSON em objeto.

#### Lógica do serviço (Facade)

```java
@Service
public class ClienteServiceImpl
    implements ClienteService {

  private final ClienteRepository clientes;
  private final EnderecoRepository enderecos;
  private final ViaCepService viaCep;

  // injeção por construtor
  // (dispensa @Autowired)
  public ClienteServiceImpl(
      ClienteRepository c,
      EnderecoRepository e,
      ViaCepService v) {
    this.clientes = c;
    this.enderecos = e;
    this.viaCep = v;
  }

  @Override
  public void inserir(Cliente cliente) {
    String cep =
      cliente.getEndereco().getCep();
    // reaproveita o endereço salvo;
    // se não existir, consulta o ViaCEP
    Endereco endereco = enderecos
      .findById(cep)
      .orElseGet(() -> enderecos.save(
        viaCep.consultarCep(cep)));
    cliente.setEndereco(endereco);
    clientes.save(cliente);
  }
}
```

### Ferramentas úteis

ViaCEP, a API pública e gratuita de consulta de CEP:

🔗 [ViaCEP - Webservice CEP e IBGE gratuito](https://viacep.com.br/)

jsonschema2pojo, que gera as classes Java a partir de um JSON de exemplo (útil para montar a classe `Endereco`):

🔗 [https://www.jsonschema2pojo.org/](https://www.jsonschema2pojo.org/)

### Projeto

> ➡️ **Próximo passo:** **Desafios**, para praticar os conceitos do curso em exercícios próprios.

### 🧠 Revisão rápida

**Onde está o Strategy neste projeto?**

Na interface `ClienteService` com a implementação `ClienteServiceImpl`, trocável sem mexer no controller.

**Por que o serviço consulta o banco antes do ViaCEP?**

Para reaproveitar endereços já salvos e evitar chamadas externas repetidas.

**O que é preciso para usar o OpenFeign?**

A dependência `spring-cloud-starter-openfeign` e `@EnableFeignClients` na classe principal.

### 📌 Resumo

| Padrão | No projeto |
| --- | --- |
| Singleton | Todo bean do Spring, por padrão. |
| Strategy | `ClienteService`  • `ClienteServiceImpl`. |
| Facade | O service esconde JPA + ViaCEP atrás de `inserir`. |
| OpenFeign | Interface que vira cliente HTTP. |

## Repositórios

> "Alguém está sentado à sombra hoje porque alguém plantou uma árvore há muito tempo." (Warren Buffett)

> "Falar é fácil. Mostre-me o código." (Linus Torvalds)

> 🛠️ **Correções:** "sobra" → "sombra", "Mostre me" → "Mostre-me" e "TOrvalds" → "Torvalds".

> ➡️ **Próximo passo:** **Desafio animal**, na seção 7, para praticar decisões encadeadas com o que você aprendeu.

## 🧠 Revisão rápida

**Qual padrão garante uma única instância de uma classe?**

Singleton. No Spring, todo bean é singleton por padrão.

**Qual padrão troca o algoritmo em tempo de execução?**

Strategy: uma interface com implementações intercambiáveis.

## 📌 Resumo

| Padrão | Em uma frase |
| --- | --- |
| Padrões GoF | soluções conhecidas para problemas comuns: criacionais, estruturais e comportamentais |
| Singleton | garante uma única instância (no Spring, todo bean é singleton por padrão) |
| Strategy | troca o algoritmo em tempo de execução por meio de uma interface |
| Facade | uma interface simples na frente de subsistemas complexos |
| No Spring | `@Bean`/`@Component` (Singleton), interfaces de serviço (Strategy), serviços que orquestram outros (Facade) |

## 🧭 Mapa da seção

![Mapa mental para revisar Spring](../img/dio-mapa-spring.svg)
