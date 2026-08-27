"""Configurações de raciocínio da OpenAI."""

from typing import cast

from openai.types.shared import ReasoningEffort
from openai.types.shared_params import Reasoning

REASONING_EFFORTS_VALIDOS = {
  "none",
  "minimal",
  "low",
  "medium",
  "high",
  "xhigh",
  "max",
}


def criar_configuracao_reasoning(reasoning_effort: str) -> Reasoning:
  """Valida o esforço e cria a configuração tipada do SDK."""

  if reasoning_effort not in REASONING_EFFORTS_VALIDOS:
    valores = ", ".join(sorted(REASONING_EFFORTS_VALIDOS))

    raise ValueError(
      "OPENAI_REASONING_EFFORT inválido. "
      f"Valores reconhecidos: {valores}."
    )

  effort = cast(ReasoningEffort, reasoning_effort)

  return { "effort": effort }
