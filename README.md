# Avaliador de reclamações

Projeto de estudo em Python que evoluirá de uma chamada simples à API da OpenAI
para um avaliador de reclamações com conversa, RAG, fluxo transacional e relatório
de execução.

## Preparação do ambiente

O projeto usa Python 3.12 e o `uv` para gerenciar o ambiente virtual, as
dependências e o arquivo de lock.

Crie o ambiente e instale as dependências:

```bash
uv sync
```

Crie a configuração local a partir do exemplo:

```bash
cp .env.example .env
```

Edite `.env`, informe sua chave da API, escolha o modelo da OpenAI e defina o
nível de esforço de raciocínio. O arquivo deve conter as três variáveis abaixo:

```dotenv
OPENAI_API_KEY="sua_chave"
OPENAI_MODEL="nome_do_modelo"
OPENAI_REASONING_EFFORT="medium"
```

O arquivo `.env` é local e está ignorado pelo Git.

Inicie a aplicação carregando a configuração local:

```bash
uv run --env-file .env avaliador-reclamacoes
```

Também é possível fornecer a variável diretamente pelo ambiente e executar:

```bash
export OPENAI_API_KEY="sua_chave"
export OPENAI_MODEL="nome_do_modelo"
export OPENAI_REASONING_EFFORT="medium"
uv run avaliador-reclamacoes
```

O esforço de raciocínio é enviado em `reasoning.effort`. Os valores aceitos
dependem do modelo escolhido; altere `OPENAI_REASONING_EFFORT` para comparar o
comportamento entre execuções.

Cada execução recebe uma reclamação, realiza uma chamada à Responses API e
exibe o texto retornado. A chamada pode gerar cobrança na conta associada à
chave da API.

Erros de autenticação, limite, conexão, status da API e respostas incompletas
são encerrados de maneira controlada, sem apresentar uma resposta inválida como
sucesso.

## Arquivos gerenciados pelo uv

- `pyproject.toml`: declara o projeto e suas dependências diretas.
- `uv.lock`: registra as versões exatas resolvidas e deve ser versionado.
- `.venv/`: contém o ambiente virtual local e não deve ser versionado.
- `.python-version`: define a versão padrão do Python do projeto.
