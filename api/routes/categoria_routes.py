from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..controllers.categoria_controller import CategoriaController
from ..repositories.categoria_repository import CategoriaRepository
from ..schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)
from ..services.categoria_service import CategoriaService


router = APIRouter(prefix="/categorias", tags=["Categorias"])


def get_controller(db: Session = Depends(get_db)) -> CategoriaController:
    repository = CategoriaRepository(db)
    service = CategoriaService(repository)
    return CategoriaController(service)


@router.post(
    "",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_categoria(
    data: CategoriaCreate,
    controller: CategoriaController = Depends(get_controller),
) -> CategoriaResponse:
    return controller.create(data)


@router.get("", response_model=list[CategoriaResponse])
def get_categorias(
    controller: CategoriaController = Depends(get_controller),
) -> list[CategoriaResponse]:
    return controller.get_all()


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def get_categoria(
    categoria_id: int,
    controller: CategoriaController = Depends(get_controller),
) -> CategoriaResponse:
    return controller.get(categoria_id)


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def update_categoria(
    categoria_id: int,
    data: CategoriaUpdate,
    controller: CategoriaController = Depends(get_controller),
) -> CategoriaResponse:
    return controller.update(categoria_id, data)


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_categoria(
    categoria_id: int,
    controller: CategoriaController = Depends(get_controller),
) -> Response:
    controller.delete(categoria_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
