# Plano de estudo e implementação — avaliador de reclamações

## 1. Objetivo do projeto

Construir aos poucos, em Python, um sistema que receba reclamações de clientes pelo terminal, utilize a API da OpenAI e evolua de uma chamada simples para um agente de avaliação com conversa, RAG, fluxo transacional e relatório de execução.

Resultado final esperado:

1. receber a reclamação do cliente;
2. interpretar e responder adequadamente;
3. manter o histórico quando houver mais de um turno;
4. consultar políticas de uma empresa fictícia por RAG;
5. avaliar a reclamação dentro de um fluxo controlado;
6. exibir um relatório condensado da execução.

## 2. Princípios do desenvolvimento

- Implementar um conceito por vez.
- Começar sem frameworks de agentes.
- Manter a mensagem do cliente separada das instruções da aplicação.
- Fazer o Python controlar regras, estado e transições importantes.
- Tratar a saída da LLM como uma resposta que precisa ser validada.
- Criar exemplos de teste antes de sofisticar o prompt.
- Só adicionar RAG quando a versão sem RAG estiver funcionando e puder ser comparada.

## 3. Arquitetura inicial

```text
Cliente digita a reclamação
          ↓
Terminal captura o texto
          ↓
Harness Python adiciona as instruções
          ↓
SDK da OpenAI chama a Responses API
          ↓
Harness extrai e valida a resposta
          ↓
Terminal exibe a resposta ao cliente
```

No começo, tudo pode estar em um único arquivo. A separação em módulos deve acontecer quando as responsabilidades começarem a crescer.

## 4. Roteiro de implementação e estudo

### Fase 0 — Preparação do ambiente

Implementar:

- ambiente virtual Python;
- SDK oficial da OpenAI;
- chave da API carregada por variável de ambiente;
- arquivo de configuração sem segredos versionados;
- comando simples para iniciar o programa.

Estudar:

- ambiente virtual e dependências;
- variáveis de ambiente;
- diferença entre o produto ChatGPT e a API da OpenAI;
- estrutura básica de uma requisição e de uma resposta.

Critério de conclusão: o projeto inicia e consegue acessar a configuração sem expor a chave da API.

### Fase 1 — Uma mensagem e uma resposta

Implementar:

- ler uma reclamação com `input()`;
- enviar instruções fixas e a mensagem do cliente para a Responses API;
- obter o texto consolidado da resposta;
- imprimir a resposta no terminal;
- tratar erros básicos de autenticação, conexão e resposta incompleta.

Não adicionar ainda:

- histórico;
- RAG;
- banco de dados;
- ferramentas;
- classes ou abstrações desnecessárias;
- fluxo com múltiplas chamadas à LLM.

Estudar:

- cliente do SDK;
- `model`, `instructions`, `input` e `output_text`;
- diferença entre instrução da aplicação e conteúdo do usuário;
- tratamento de exceções.

Critério de conclusão: cada execução recebe uma reclamação, faz uma chamada e mostra uma resposta compreensível.

### Fase 2 — Prompt engineering

Definir o contrato do avaliador:

- papel do sistema;
- tarefa exata;
- tom de voz;
- limites e proibições;
- comportamento quando faltarem informações;
- formato esperado da resposta;
- situações que exigem encaminhamento humano.

Criar um pequeno conjunto fixo de reclamações para avaliação, incluindo:

- reclamação clara e completa;
- reclamação vaga;
- cliente irritado;
- pedido fora do escopo;
- tentativa de fazer o modelo ignorar suas instruções;
- reclamação que exige política ainda não disponível.

Estudar:

- hierarquia e separação de instruções;
- zero-shot e few-shot prompting;
- exemplos positivos e negativos;
- critérios de qualidade;
- versionamento de prompts;
- avaliações repetíveis.

Critério de conclusão: uma versão do prompt apresenta resultados aceitáveis no conjunto de testes e não inventa políticas da empresa.

### Fase 3 — Saída estruturada

Fazer o modelo produzir dados internos previsíveis, além do texto destinado ao cliente. Exemplo conceitual:

```text
categoria
severidade
resumo
dados_faltantes
necessita_escalonamento
justificativa_interna
resposta_ao_cliente
```

Implementar validação do formato e comportamento seguro quando a saída for inválida.

Estudar:

- JSON e schemas;
- Structured Outputs;
- validação com tipos Python;
- diferença entre informação interna e mensagem pública.

Critério de conclusão: o sistema sempre obtém uma estrutura válida ou encerra de maneira controlada.

### Fase 4 — Histórico de conversa

Transformar a execução única em um loop de conversa:

- receber várias mensagens;
- relacionar cada resposta ao turno anterior;
- definir um comando para encerrar;
- manter ou reconstruir o contexto;
- limitar o crescimento da conversa.

Comparar duas estratégias:

1. usar o identificador da resposta anterior ou um objeto de conversa;
2. armazenar e reenviar o histórico administrado pelo próprio programa.

Manter separados:

- histórico da conversa;
- estado oficial da reclamação.

Critério de conclusão: o cliente consegue complementar informações sem o sistema perder o contexto relevante.

### Fase 5 — Empresa fictícia e base de conhecimento

Criar uma empresa totalmente fictícia para que o RAG trabalhe com dados externos ao prompt e controlados pelo projeto.

Sugestão: **Loja Aurora**, um comércio eletrônico fictício de eletrônicos e acessórios.

Corpus inicial:

- apresentação da empresa;
- catálogo resumido de produtos;
- política de troca e devolução;
- política de reembolso;
- prazos e regras de entrega;
- garantia por categoria de produto;
- níveis de severidade;
- prazos de atendimento (SLA);
- critérios de encaminhamento humano;
- perguntas frequentes.

Possível organização futura:

```text
knowledge_base/
├── empresa.md
├── trocas_e_devolucoes.md
├── reembolsos.md
├── entregas.md
├── garantias.md
├── severidade_e_escalonamento.md
├── sla.md
└── produtos.json
```

Todos os nomes, clientes, pedidos, produtos e regras devem ser sintéticos. Para aprender RAG, não é necessário começar buscando conteúdo na internet: arquivos locais externos ao prompt já formam uma base adequada, previsível e fácil de testar.

Critério de conclusão: existe um corpus coerente, sem contradições conhecidas, com respostas de referência para perguntas de teste.

### Fase 6 — RAG

Implementar o fluxo:

```text
Reclamação ou pergunta
          ↓
Preparação da consulta
          ↓
Busca de trechos relevantes
          ↓
Seleção do contexto
          ↓
LLM recebe pergunta + contexto recuperado
          ↓
Resposta fundamentada nas políticas
```

Estudar:

- documentos, chunks e metadados;
- embeddings;
- busca vetorial e busca por palavras;
- top-k e relevância;
- contexto recuperado;
- citações e rastreabilidade;
- diferença entre RAG, histórico e treinamento;
- avaliação de recuperação e de resposta.

Testar pelo menos:

- pergunta cuja resposta está claramente no corpus;
- pergunta que exige combinar dois documentos;
- pergunta sem resposta no corpus;
- recuperação de trecho irrelevante;
- documentos com regras semelhantes;
- tentativa de instrução maliciosa dentro de um documento.

Critério de conclusão: o sistema usa apenas as políticas recuperadas, informa quando não há base suficiente e permite identificar a origem da resposta.

### Fase 7 — Fluxo transacional da reclamação

Definir estados explícitos, por exemplo:

```text
NOVA
  ↓
COLETANDO_DADOS
  ↓
AGUARDANDO_CONFIRMACAO
  ↓
PRONTA_PARA_AVALIACAO
  ↓
AVALIADA
  ↓
ENCERRADA ou ESCALADA
```

O modelo pode interpretar, extrair dados e recomendar o próximo passo. O Python deve:

- manter o estado oficial;
- validar campos obrigatórios;
- autorizar transições;
- impedir transições inválidas;
- evitar ações duplicadas;
- registrar as decisões.

Critério de conclusão: a mesma entrada leva a transições válidas e auditáveis, inclusive em casos de erro ou interrupção.

### Fase 8 — Persistência, segurança e robustez

Adicionar conforme a necessidade:

- persistência das reclamações;
- logs estruturados;
- identificador de protocolo;
- timeout e tentativas controladas;
- proteção de dados pessoais;
- moderação e encaminhamento humano;
- limites de tamanho e número de turnos;
- testes automatizados;
- prevenção de efeitos duplicados.

Critério de conclusão: uma falha não corrompe o estado nem faz o sistema repetir uma ação importante.

### Fase 9 — Métricas e relatório final

Instrumentar o harness e, somente no final do fluxo, imprimir um relatório condensado.

Dados mínimos:

- quantidade de chamadas à LLM;
- total de tokens de entrada;
- total de tokens de saída;
- total geral de tokens;
- latência acumulada das chamadas à API;
- latência de recuperação do RAG;
- latência total do processamento;
- estado final da reclamação;
- resultado da avaliação;
- quantidade de turnos;
- erros ou tentativas adicionais, quando existirem.

A Responses API informa o uso por resposta nos campos `input_tokens`, `output_tokens` e `total_tokens`. O harness deverá acumular esses valores quando houver várias chamadas.

A latência deverá ser medida pelo Python com um relógio monotônico. Definições sugeridas:

- **Latência da API:** tempo imediatamente antes e depois de cada chamada à OpenAI.
- **Latência do RAG:** tempo gasto na preparação, busca e seleção dos documentos.
- **Latência total:** tempo entre o recebimento da mensagem já digitada e a conclusão de todo o processamento. O tempo que o usuário passa digitando não entra nessa métrica.

Exemplo conceitual do relatório:

```text
===== RELATÓRIO DA EXECUÇÃO =====
Protocolo: REC-0001
Estado final: AVALIADA
Turnos: 3
Chamadas à LLM: 4
Tokens de entrada: 2.450
Tokens de saída: 630
Tokens totais: 3.080
Latência da API: 5,82 s
Latência do RAG: 0,18 s
Latência total: 6,14 s
Resultado: reclamação procedente e encaminhada para reembolso
================================
```

Critério de conclusão: os totais representam toda a execução, e não apenas a última chamada.

## 5. Ordem resumida

```text
Ambiente
  → chamada única
  → prompt engineering e testes
  → saída estruturada
  → histórico
  → empresa fictícia
  → RAG
  → fluxo transacional
  → persistência e segurança
  → métricas e relatório final
```

## 6. Definição de projeto concluído

O projeto estará concluído quando:

- receber reclamações pelo terminal;
- conversar para coletar dados faltantes;
- consultar a base da empresa fictícia;
- responder sem inventar políticas;
- produzir uma avaliação estruturada;
- executar somente transições permitidas;
- preservar um histórico auditável;
- lidar de forma controlada com falhas;
- imprimir o relatório final com tokens e latências acumuladas;
- passar pelo conjunto definido de casos de teste.

## 7. Referência oficial inicial

- [Responses API — criação de uma resposta](https://developers.openai.com/api/reference/cli/resources/responses/methods/create): entrada, instruções, continuidade de conversa, saída e campos de uso de tokens.

Antes da implementação, confirmar novamente na documentação oficial da OpenAI os nomes dos modelos, parâmetros e recursos disponíveis, pois a plataforma pode evoluir.
