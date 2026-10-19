from fastapi import HTTPException, status

from ..schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioUpdate
from ..services.usuario_service import (
    UsuarioComGastosError,
    UsuarioEmailDuplicadoError,
    UsuarioNaoEncontradoError,
    UsuarioService,
)


class UsuarioController:
    def __init__(self, service: UsuarioService):
        self.service = service

    def create(self, data: UsuarioCreate) -> UsuarioResponse:
        try:
            usuario = self.service.create(data)
        except UsuarioEmailDuplicadoError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        return UsuarioResponse.model_validate(usuario)

    def get(self, usuario_id: int) -> UsuarioResponse:
        try:
            usuario = self.service.get(usuario_id)
        except UsuarioNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return UsuarioResponse.model_validate(usuario)

    def get_all(self) -> list[UsuarioResponse]:
        usuarios = self.service.get_all()
        return [UsuarioResponse.model_validate(usuario) for usuario in usuarios]

    def update(
        self,
        usuario_id: int,
        data: UsuarioUpdate,
    ) -> UsuarioResponse:
        try:
            usuario = self.service.update(usuario_id, data)
        except UsuarioNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        except UsuarioEmailDuplicadoError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        return UsuarioResponse.model_validate(usuario)

    def delete(self, usuario_id: int) -> None:
        try:
            self.service.delete(usuario_id)
        except UsuarioNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        except UsuarioComGastosError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
