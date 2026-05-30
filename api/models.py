from enum import Enum
from pydantic import BaseModel, Field


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


class Historia(BaseModel):
    tema: str = Field(..., description="O tema da história a ser gerada")


class HistoriaGerada(BaseModel):
    historia: str = Field(..., description="A história gerada pelo modelo")
