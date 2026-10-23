from fastapi import HTTPException, status

from ..schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)
from ..services.categoria_service import (
    CategoriaComGastosError,
    CategoriaNaoEncontradaError,
    CategoriaNomeDuplicadoError,
    CategoriaService,
)


class CategoriaController:
    def __init__(self, service: CategoriaService):
        self.service = service

    def create(self, data: CategoriaCreate) -> CategoriaResponse:
        try:
            categoria = self.service.create(data)
        except CategoriaNomeDuplicadoError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        return CategoriaResponse.model_validate(categoria)

    def get(self, categoria_id: int) -> CategoriaResponse:
        try:
            categoria = self.service.get(categoria_id)
        except CategoriaNaoEncontradaError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return CategoriaResponse.model_validate(categoria)

    def get_all(self) -> list[CategoriaResponse]:
        categorias = self.service.get_all()
        return [CategoriaResponse.model_validate(categoria) for categoria in categorias]

    def update(
        self,
        categoria_id: int,
        data: CategoriaUpdate,
    ) -> CategoriaResponse:
        try:
            categoria = self.service.update(categoria_id, data)
        except CategoriaNaoEncontradaError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        except CategoriaNomeDuplicadoError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        return CategoriaResponse.model_validate(categoria)

    def delete(self, categoria_id: int) -> None:
        try:
            self.service.delete(categoria_id)
        except CategoriaComGastosError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(error),
            ) from error
        except CategoriaNaoEncontradaError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
