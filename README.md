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

Edite `.env` e substitua o valor de exemplo pela sua chave da API. O arquivo
`.env` é local e está ignorado pelo Git.

Inicie a aplicação carregando a configuração local:

```bash
uv run --env-file .env avaliador-reclamacoes
```

Também é possível fornecer a variável diretamente pelo ambiente e executar:

```bash
export OPENAI_API_KEY="sua_chave"
uv run avaliador-reclamacoes
```

Nesta fase, o programa apenas valida a configuração e inicializa o cliente do
SDK. Nenhuma chamada à API é realizada.

## Arquivos gerenciados pelo uv

- `pyproject.toml`: declara o projeto e suas dependências diretas.
- `uv.lock`: registra as versões exatas resolvidas e deve ser versionado.
- `.venv/`: contém o ambiente virtual local e não deve ser versionado.
- `.python-version`: define a versão padrão do Python do projeto.

