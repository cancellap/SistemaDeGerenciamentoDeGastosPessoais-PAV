from fastapi import FastAPI

from .routes.analise_routes import router as analise_router
from .routes.categoria_routes import router as categoria_router
from .routes.gasto_routes import router as gasto_router
from .routes.usuario_routes import router as usuario_router


app = FastAPI(title="Análise de Gastos Pessoais")
app.include_router(analise_router)
app.include_router(categoria_router)
app.include_router(usuario_router)
app.include_router(gasto_router)
