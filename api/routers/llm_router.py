from fastapi import APIRouter

from models import Historia, HistoriaGerada
from utils import execute_prompt

router = APIRouter()


@router.post("/gerar_historia/v1", response_model=HistoriaGerada)
def gerar_historia(historia: Historia):
    prompt = f"Escreva uma história sobre o tema: {historia.tema}."

    historia_gerada = execute_prompt(prompt)

    return {"historia": historia_gerada}
