"""Ponto de entrada da aplicação."""

import os

from dotenv import load_dotenv
from openai import OpenAI

def main() -> int:
  """Valida a configuração necessária para iniciar a aplicação."""

  load_dotenv()  # Carrega variáveis de ambiente do arquivo .env

  api_key = os.getenv("OPENAI_API_KEY")

  if not api_key:
    print("Configuração ausente: defina a variável OPENAI_API_KEY.")
    return 1

  OpenAI(api_key=api_key)

  print("Ambiente preparado: configuração da OpenAI encontrada.")
  print("Nenhuma chamada à API foi realizada.")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
