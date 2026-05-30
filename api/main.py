"""API de exemplo desenvolvida durante a aula de Construção de APIs para IA."""

from dotenv import load_dotenv
from fastapi import Depends, FastAPI

from routers.llm_router import router as llm_router
from routers.operacoes_router import router as operacoes_router
from utils import common_api_token


load_dotenv()


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


app.include_router(router=llm_router, tags=["IA"])
app.include_router(router=operacoes_router, tags=["Operações matemáticas"])


# ---------------------------------------------------------------------------
# Execução local
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000)
