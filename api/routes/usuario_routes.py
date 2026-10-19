from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..controllers.usuario_controller import UsuarioController
from ..repositories.usuario_repository import UsuarioRepository
from ..schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from ..services.usuario_service import UsuarioService


router = APIRouter(prefix="/usuarios", tags=["Usuários"])


def get_controller(db: Session = Depends(get_db)) -> UsuarioController:
    return UsuarioController(UsuarioService(UsuarioRepository(db)))


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def create_usuario(data: UsuarioCreate, controller: UsuarioController = Depends(get_controller)) -> UsuarioResponse:
    return controller.create(data)


@router.get("", response_model=list[UsuarioResponse])
def get_usuarios(controller: UsuarioController = Depends(get_controller)) -> list[UsuarioResponse]:
    return controller.get_all()


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int, controller: UsuarioController = Depends(get_controller)) -> UsuarioResponse:
    return controller.get(usuario_id)


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(usuario_id: int, data: UsuarioUpdate, controller: UsuarioController = Depends(get_controller)) -> UsuarioResponse:
    return controller.update(usuario_id, data)


@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(usuario_id: int, controller: UsuarioController = Depends(get_controller)) -> Response:
    controller.delete(usuario_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
