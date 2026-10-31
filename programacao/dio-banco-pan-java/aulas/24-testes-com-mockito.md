# Testes com Mockito

> 🗺️ **Nesta aula:** por que usar objetos falsos (mocks) nos testes, como escrever um teste com Mockito, os recursos principais e como usar mocks em testes do Spring.

## Por que "mockar"

Um **teste unitário** testa uma classe **isolada**. Mas um `TransferenciaService` depende de repositório, banco de dados, serviço de notificação... Subir tudo isso deixaria o teste lento e frágil.

**Um mock é um objeto falso que imita uma dependência:** você define o que ele responde e, depois, confere como ele foi usado. **Mockito** é a biblioteca padrão para isso em Java e já vem no `spring-boot-starter-test`.

## A classe que vamos testar

```java
@Service
public class TransferenciaService {
  private final ContaRepository contas;
  private final NotificacaoService notificacao;

  public TransferenciaService(ContaRepository contas, NotificacaoService notificacao) {
    this.contas = contas;
    this.notificacao = notificacao;
  }

  public void transferir(Long origemId, Long destinoId, BigDecimal valor) {
    Conta origem = contas.findById(origemId)
        .orElseThrow(() -> new ContaNaoEncontradaException(origemId));
    Conta destino = contas.findById(destinoId)
        .orElseThrow(() -> new ContaNaoEncontradaException(destinoId));

    if (origem.getSaldo().compareTo(valor) < 0) throw new SaldoInsuficienteException();

    origem.debitar(valor);
    destino.creditar(valor);
    contas.save(origem);
    contas.save(destino);
    notificacao.enviar(origem.getClienteId(), "Transferência de R$ " + valor);
  }
}
```

Repare que as dependências chegam **pelo construtor**. É isso que permite trocar as reais por mocks no teste.

## O teste

```java
@ExtendWith(MockitoExtension.class)  // ativa o Mockito no JUnit 5
class TransferenciaServiceTest {

  @Mock ContaRepository contas;  // dublês falsos
  @Mock NotificacaoService notificacao;

  @InjectMocks TransferenciaService service;  // classe real, com os mocks injetados

  @Test
  void deveTransferirQuandoHaSaldo() {
    // Arrange (Given): prepara o cenário
    Conta origem = new Conta(1L, new BigDecimal("500.00"));
    Conta destino = new Conta(2L, new BigDecimal("100.00"));
    when(contas.findById(1L)).thenReturn(Optional.of(origem));
    when(contas.findById(2L)).thenReturn(Optional.of(destino));

    // Act (When): executa
    service.transferir(1L, 2L, new BigDecimal("200.00"));

    // Assert (Then): confere o resultado...
    assertEquals(new BigDecimal("300.00"), origem.getSaldo());
    assertEquals(new BigDecimal("300.00"), destino.getSaldo());
    // ...e as interações com os mocks
    verify(contas, times(2)).save(any(Conta.class));
    verify(notificacao).enviar(eq(origem.getClienteId()), anyString());
  }

  @Test
  void deveFalharSemSaldoENaoSalvarNada() {
    Conta origem = new Conta(1L, new BigDecimal("50.00"));
    Conta destino = new Conta(2L, BigDecimal.ZERO);
    when(contas.findById(1L)).thenReturn(Optional.of(origem));
    when(contas.findById(2L)).thenReturn(Optional.of(destino));

    assertThrows(SaldoInsuficienteException.class,
        () -> service.transferir(1L, 2L, new BigDecimal("200.00")));

    verify(contas, never()).save(any());
    verifyNoInteractions(notificacao);
  }
}
```

## Principais recursos

| Recurso | Para quê |
| --- | --- |
| `when(x).thenReturn(v)` | define o retorno |
| `when(x).thenThrow(e)` / `doThrow(e).when(mock).metodoVoid()` | simula um erro |
| `verify(mock).metodo(...)` | confere se foi chamado |
| `times(n)`, `never()`, `atLeastOnce()` | quantas vezes |
| `any()`, `eq(v)`, `anyString()`, `argThat(...)` | *matchers* de argumentos |
| `ArgumentCaptor` | captura o argumento enviado para inspecionar |
| `@Spy` | objeto real em que só alguns métodos são falsos |

```java
ArgumentCaptor<String> msg = ArgumentCaptor.forClass(String.class);
verify(notificacao).enviar(anyLong(), msg.capture());
assertTrue(msg.getValue().contains("200.00"));
```

> ⚠️ Se um argumento usa *matcher*, **todos** precisam usar: `verify(n).enviar(1L, anyString())` dá erro; o certo é `verify(n).enviar(eq(1L), anyString())`. E o `MockitoExtension` acusa `UnnecessaryStubbingException` se você configurar um `when` que o teste nunca usa.

## Mocks em testes Spring

```java
@WebMvcTest(TransferenciaController.class)  // sobe só a camada web
class TransferenciaControllerTest {
    @Autowired MockMvc mvc;
    @MockitoBean TransferenciaService service;  // Spring Boot 3.4+ (antes: @MockBean)

    @Test
    void deveRetornar400ComValorNegativo() throws Exception {
        mvc.perform(post("/transferencias")
                .contentType(MediaType.APPLICATION_JSON)
                .content("""
                    {"origemId":1,"destinoId":2,"valor":-10}
                    """))
           .andExpect(status().isBadRequest());
    }
}
```

## Boas práticas

- Mocke **dependências externas** (repositórios, clientes HTTP, filas), e não objetos simples de dados (entidades, DTOs, `BigDecimal`).
- Um teste deve verificar **um comportamento**, com um nome que o descreva (`deveFalharSemSaldo...`).
- Mocks demais costumam indicar uma classe com responsabilidades demais (veja SOLID).

> ✨ **Página nova:** a página de JUnit testava classes sem dependências. Em projetos Spring, quase todo teste de service precisa de Mockito, que só era citado de passagem.

## 📌 Resumo

| Item | Em uma frase |
| --- | --- |
| Mock | objeto falso que substitui uma dependência (banco, API) no teste |
| `@Mock` / `@InjectMocks` | cria o mock / injeta os mocks na classe testada |
| `when(...).thenReturn(...)` | define o que o mock devolve |
| `verify(...)` | confere se o método do mock foi chamado, e quantas vezes |
| `@MockitoBean` | substitui um bean por um mock em testes do Spring |
| Boa prática | mocke só o que está fora da unidade testada |
