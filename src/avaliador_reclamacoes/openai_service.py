"""Integração com a API da OpenAI."""

from openai import (
  APIConnectionError,
  APIError,
  APIStatusError,
  AuthenticationError,
  OpenAI,
  RateLimitError,
)

from avaliador_reclamacoes.reasoning import criar_configuracao_reasoning

INSTRUCTIONS = """
Você recebe uma reclamação de um cliente.
Responda em português do Brasil, com clareza e respeito.
Não invente políticas, direitos ou soluções específicas da empresa.
Quando faltarem informações, explique quais dados são necessários.
""".strip()


class OpenAIServiceError(Exception):
  """Erro controlado durante a comunicação com a OpenAI."""


def gerar_resposta(
  reclamacao: str,
  api_key: str,
  model: str,
  reasoning_effort: str,
) -> str:
  """Envia a reclamação e retorna uma resposta textual válida."""

  try:
    reasoning = criar_configuracao_reasoning(reasoning_effort)
  except ValueError as error:
    raise OpenAIServiceError(str(error)) from error

  client = OpenAI(api_key=api_key)

  try:
    response = client.responses.create(
      model=model,
      instructions=INSTRUCTIONS,
      input=reclamacao,
      reasoning=reasoning,
    )
  except AuthenticationError as error:
    raise OpenAIServiceError(
      "Falha de autenticação. Verifique se a chave da API está correta."
    ) from error
  except RateLimitError as error:
    raise OpenAIServiceError(
      "O limite ou a cota disponível para a API foi excedido."
    ) from error
  except APIConnectionError as error:
    raise OpenAIServiceError(
      "Não foi possível conectar à OpenAI. Verifique sua conexão."
    ) from error
  except APIStatusError as error:
    raise OpenAIServiceError(
      "A OpenAI não conseguiu processar a solicitação. "
      f"Código HTTP: {error.status_code}."
    ) from error
  except APIError as error:
    raise OpenAIServiceError(
      "Ocorreu um erro inesperado na comunicação com a OpenAI."
    ) from error

  if response.status != "completed":
    raise OpenAIServiceError(
      "A resposta da OpenAI não foi concluída. "
      f"Status recebido: {response.status}."
    )

  resposta = (response.output_text or "").strip()

  if not resposta:
    raise OpenAIServiceError(
      "A OpenAI concluiu a solicitação, mas não retornou texto."
    )

  return resposta
