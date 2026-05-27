"""API de exemplo desenvolvida durante a aula de Construção de APIs para IA."""

import logging
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------

API_TOKEN = "123"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("fastapi")


# ---------------------------------------------------------------------------
# Modelos
# ---------------------------------------------------------------------------

class Numeros(BaseModel):
    numero1: int = Field(..., description="O primeiro número a ser somado")
    numero2: int = Field(..., description="O segundo número a ser somado")


class Resultado(BaseModel):
    resultado: int = Field(..., description="O resultado da operação")


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


# ---------------------------------------------------------------------------
# Dependências
# ---------------------------------------------------------------------------

def common_api_token(api_token: str) -> dict:
    if api_token != API_TOKEN:
        logger.warning("Tentativa de acesso com token inválido: %s", api_token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return {"api_token": api_token}


# ---------------------------------------------------------------------------
# Aplicação
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Aula",
    summary="API desenvolvida durante a aula de Construção de APIs para IA",
    version="0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Rogério Rodrigues Carvalho",
        "url": "http://github.com/rogerior/",
        "email": "rogerior@ufg.br",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    dependencies=[Depends(common_api_token)],
)


# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------

@app.get("/teste", summary="Hello World")
def hello_world():
    return {"mensagem": "Hello World"}


@app.post(
    "/soma/v1/{numero1}/{numero2}",
    summary="Soma",
    tags=["Operações matemáticas"],
    deprecated=True,
)
def soma_v1(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}


@app.post(
    "/soma/v2",
    summary="Soma Formato2",
    tags=["Operações matemáticas"],
)
def soma_v2(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}


@app.post(
    "/soma/v3",
    response_model=Resultado,
    summary="Soma de dois números utilizando um modelo de dados",
    tags=["Operações matemáticas"],
)
def soma_v3(numeros: Numeros):
    if numeros.numero1 < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O número 1 deve ser um inteiro positivo",
        )
    return {"resultado": numeros.numero1 + numeros.numero2}


@app.post(
    "/soma_formato3",
    tags=["Operações matemáticas"],
)
def soma_formato3(numeros: Numeros):
    return {"resultado": numeros.numero1 + numeros.numero2}


@app.post(
    "/operacao_matematica",
    tags=["Operações matemáticas"],
)
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):
    if operacao is TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2
    elif operacao is TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2
    elif operacao is TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2
    else:
        if numeros.numero2 == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Divisão por zero não é permitida",
            )
        resultado = numeros.numero1 / numeros.numero2
    return {"resultado": resultado}


# ---------------------------------------------------------------------------
# Execução local
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)
