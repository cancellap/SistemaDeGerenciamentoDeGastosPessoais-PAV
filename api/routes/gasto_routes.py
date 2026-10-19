from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..controllers.gasto_controller import GastoController
from ..repositories.categoria_repository import CategoriaRepository
from ..repositories.gasto_repository import GastoRepository
from ..repositories.usuario_repository import UsuarioRepository
from ..schemas.gasto_schema import GastoCreate, GastoResponse, GastoUpdate
from ..services.gasto_service import GastoService


router = APIRouter(prefix="/gastos", tags=["Gastos"])


def get_controller(db: Session = Depends(get_db)) -> GastoController:
    service = GastoService(
        GastoRepository(db),
        UsuarioRepository(db),
        CategoriaRepository(db),
    )
    return GastoController(service)


@router.post("", response_model=GastoResponse, status_code=status.HTTP_201_CREATED)
def create_gasto(data: GastoCreate, controller: GastoController = Depends(get_controller)) -> GastoResponse:
    return controller.create(data)


@router.get("", response_model=list[GastoResponse])
def get_gastos(controller: GastoController = Depends(get_controller)) -> list[GastoResponse]:
    return controller.get_all()


@router.get("/{gasto_id}", response_model=GastoResponse)
def get_gasto(gasto_id: int, controller: GastoController = Depends(get_controller)) -> GastoResponse:
    return controller.get(gasto_id)


@router.put("/{gasto_id}", response_model=GastoResponse)
def update_gasto(gasto_id: int, data: GastoUpdate, controller: GastoController = Depends(get_controller)) -> GastoResponse:
    return controller.update(gasto_id, data)


@router.delete("/{gasto_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_gasto(gasto_id: int, controller: GastoController = Depends(get_controller)) -> Response:
    controller.delete(gasto_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
