from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..controllers.analise_controller import AnaliseController
from ..repositories.gasto_repository import GastoRepository
from ..schemas.analise_schema import (
    AnomaliaResponse,
    CategoriaTotalResponse,
    MediaResponse,
    TotalResponse,
)
from ..services.analise_service import AnaliseService


router = APIRouter(prefix="/analises/gastos", tags=["Análises"])


def get_controller(db: Session = Depends(get_db)) -> AnaliseController:
    return AnaliseController(AnaliseService(GastoRepository(db)))


@router.get("/total", response_model=TotalResponse)
def get_total(
    controller: AnaliseController = Depends(get_controller),
) -> TotalResponse:
    return controller.get_total()


@router.get("/media", response_model=MediaResponse)
def get_media(
    controller: AnaliseController = Depends(get_controller),
) -> MediaResponse:
    return controller.get_media()


@router.get("/por-categoria", response_model=list[CategoriaTotalResponse])
def get_por_categoria(
    controller: AnaliseController = Depends(get_controller),
) -> list[CategoriaTotalResponse]:
    return controller.get_por_categoria()


@router.get("/anomalias", response_model=list[AnomaliaResponse])
def get_anomalias(
    controller: AnaliseController = Depends(get_controller),
) -> list[AnomaliaResponse]:
    return controller.get_anomalias()
