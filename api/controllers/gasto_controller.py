from fastapi import HTTPException, status

from ..schemas.gasto_schema import GastoCreate, GastoResponse, GastoUpdate
from ..services.gasto_service import (
    CategoriaGastoNaoEncontradaError,
    GastoNaoEncontradoError,
    GastoService,
    UsuarioGastoNaoEncontradoError,
    ValorGastoInvalidoError,
)


class GastoController:
    def __init__(self, service: GastoService):
        self.service = service

    def create(self, data: GastoCreate) -> GastoResponse:
        try:
            gasto = self.service.create(data)
        except (ValorGastoInvalidoError, CategoriaGastoNaoEncontradaError,
                UsuarioGastoNaoEncontradoError) as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                if isinstance(error, ValorGastoInvalidoError)
                else status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return GastoResponse.model_validate(gasto)

    def get(self, gasto_id: int) -> GastoResponse:
        try:
            gasto = self.service.get(gasto_id)
        except GastoNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return GastoResponse.model_validate(gasto)

    def get_all(self) -> list[GastoResponse]:
        gastos = self.service.get_all()
        return [GastoResponse.model_validate(gasto) for gasto in gastos]

    def update(self, gasto_id: int, data: GastoUpdate) -> GastoResponse:
        try:
            gasto = self.service.update(gasto_id, data)
        except GastoNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        except (ValorGastoInvalidoError, CategoriaGastoNaoEncontradaError,
                UsuarioGastoNaoEncontradoError) as error:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                if isinstance(error, ValorGastoInvalidoError)
                else status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
        return GastoResponse.model_validate(gasto)

    def delete(self, gasto_id: int) -> None:
        try:
            self.service.delete(gasto_id)
        except GastoNaoEncontradoError as error:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(error),
            ) from error
