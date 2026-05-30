import logging
import os

from fastapi import HTTPException, status
from groq import Groq

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

API_TOKEN = "123"


def get_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger("fastapi")


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("fastapi")

# ---------------------------------------------------------------------------
# Dependências
# ---------------------------------------------------------------------------


def common_api_token(api_token: str) -> dict:
    logger = get_logger()
    logger.info(f"Token recebido: {api_token} ")

    if api_token != API_TOKEN:
        logger.warning("Tentativa de acesso com token inválido: %s", api_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return {"api_token": api_token}


def execute_prompt(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )
    return chat_completion.choices[0].message.content
