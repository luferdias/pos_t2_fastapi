from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/teste")
def hello_world():
    return {"mensagem": "Hello World"}


# http://127.0.0.1:8000/soma/3/2
# Passando o número 1 e 2 na URL
@app.post("/soma/{numero1}/{numero2}")
def soma(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}


# http://127.0.0.1:8000/soma_formato2?numero1=3&numero2=2
@app.post("/soma_formato2")
def soma_formato2(numero1: int, numero2: int):
    total = numero1 + numero2
    return {"resultado": total}

# Passando o número 1 e 2 no corpo da requisição
class Numeros(BaseModel):
    numero1: int
    numero2: int

# 'http://127.0.0.1:8000/soma_formato3' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "numero1": 3,
#   "numero2": 2
# }'

@app.post("/soma_formato3")
def soma_formato3(numeros: Numeros):
    total = numeros.numero1 + numeros.numero2
    return {"resultado": total}