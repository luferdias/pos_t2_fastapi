from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

API_TOKEN = "123"


def common_api_token(api_token: str):
    if api_token != API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return {"api_token": api_token}


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


@app.get("/teste", summary="Hello World")
def hello_world():
    return {"mensagem": "Hello World"}


# http://127.0.0.1:8000/soma/3/2
# Passando o número 1 e 2 na URL
@app.post("/soma/v1/{numero1}/{numero2}", summary="Soma", tags=["Operações matemáticas"], deprecated=True)
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post("/soma/v2", summary="Soma Formato2", tags=["Operações matemáticas"])
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}

# Passando o número 1 e 2 no corpo da requisição
class Numeros(BaseModel):
    numero1: int = Field(..., description="O primeiro número a ser somado")
    numero2: int = Field(..., description="O segundo número a ser somado")

class Resultado(BaseModel):
    resultado: int = Field(..., description="O resultado da soma dos dois números")
    




# 'http://127.0.0.1:8000/soma_formato3' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "numero1": 3,
#   "numero2": 2
# }'

@app.post(
    "/soma/v3",
    response_model=Resultado,
    summary="Soma de dois números utilizando um modelo de dados",
    tags=["Operações matemáticas"],
)
def soma_formato3(numeros: Numeros):
    if numeros.numero1 < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O número 1 deve ser um inteiro positivo",
        )

    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}


class TipoOperacao(str, Enum):
    soma = "soma"
    subtracao = "subtracao"
    multiplicacao = "multiplicacao"
    divisao = "divisao"


@app.post("/operacao_matematica", tags=["Operações matemáticas"])
def operacao_matematica(numeros: Numeros, operacao: TipoOperacao):
    if operacao == TipoOperacao.soma:
        resultado = numeros.numero1 + numeros.numero2
    elif operacao == TipoOperacao.subtracao:
        resultado = numeros.numero1 - numeros.numero2
    elif operacao == TipoOperacao.multiplicacao:
        resultado = numeros.numero1 * numeros.numero2
    elif operacao == TipoOperacao.divisao:
        resultado = numeros.numero1 / numeros.numero2
    return {"resultado": resultado}


@app.post(
    path="/soma_formato3",
    tags=["Operações matemáticas"],
)
def soma_formato3_dep(numeros: Numeros):
    return {"resultado": numeros.numero1 + numeros.numero2}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000)