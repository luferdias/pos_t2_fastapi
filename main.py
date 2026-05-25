from fastapi import FastAPI, status
from pydantic import BaseModel

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
)

@app.get("/teste")
def hello_world():
    return {"mensagem": "Hello World"}


# http://127.0.0.1:8000/soma/3/2
# Passando o número 1 e 2 na URL
@app.post("/soma/{numero1}/{numero2}", tags=["Operações matemáticas"])
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post("/soma_formato2", tags=["Operações matemáticas"])
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}

# Passando o número 1 e 2 no corpo da requisição
class Numeros(BaseModel):
    numero1: int
    numero2: int

class Resultado(BaseModel):
    resultado: int

# 'http://127.0.0.1:8000/soma_formato3' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "numero1": 3,
#   "numero2": 2
# }'

@app.post("/soma_formato3", response_model=Resultado, tags=["Operações matemáticas"])
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}

@app.post(
    path="/soma/{numero1}/{numero2}",
    summary="Soma dois números inteiros",
    description="Recebe dois números inteiros e retorna a soma",
    tags=["Operações matemáticas"]
)
def soma_get(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}

@app.post(
    path="/soma_formato3",
    response_model=Numeros,
    status_code=status.HTTP_200_OK,
    tags=["Operações matemáticas"]
)
def soma_post_final(numeros: Numeros):
    return numeros