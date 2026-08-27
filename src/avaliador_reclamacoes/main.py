"""Ponto de entrada da aplicação."""

import os

from dotenv import load_dotenv

from avaliador_reclamacoes.openai_service import (
  OpenAIServiceError,
  gerar_resposta,
)


def main() -> int:
  """Recebe uma reclamação e apresenta a resposta."""

  load_dotenv()

  api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
  model = (os.getenv("OPENAI_MODEL") or "gpt-5.6-luna").strip()
  reasoning_effort = (os.getenv("OPENAI_REASONING_EFFORT") or "minimal").strip()

  if not api_key:
    print("Configuração ausente: defina OPENAI_API_KEY.")
    return 1

  reclamacao = input("Digite sua reclamação: ").strip()

  if not reclamacao:
    print("A reclamação não pode estar vazia.")
    return 1

  try:
    resposta = gerar_resposta(
      reclamacao=reclamacao,
      api_key=api_key,
      model=model,
      reasoning_effort=reasoning_effort,
    )
  except OpenAIServiceError as error:
    print(f"Erro: {error}")
    return 1

  print("\nResposta:")
  print(resposta)
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
