from fastapi import APIRouter, HTTPException, status

from models import Numeros, Resultado, TipoOperacao

router = APIRouter()
# ---------------------------------------------------------------------------
# Rotas
# ---------------------------------------------------------------------------


@router.post(
    "/soma/v1/{numero1}/{numero2}",
    summary="Soma",
        deprecated=True,
)
def soma_v1(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}


@router.post(
    "/soma/v2",
    summary="Soma Formato2",
    )
def soma_v2(numero1: int, numero2: int):
    return {"resultado": numero1 + numero2}


@router.post(
    "/soma/v3",
    response_model=Resultado,
    summary="Soma de dois números utilizando um modelo de dados",
    
)
def soma_v3(numeros: Numeros):
    if numeros.numero1 < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O número 1 deve ser um inteiro positivo",
        )
    return {"resultado": numeros.numero1 + numeros.numero2}


@router.post(
    "/operacao_matematica/v1",
    
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
