from ..schemas.analise_schema import (
    AnomaliaResponse,
    CategoriaTotalResponse,
    MediaResponse,
    TotalResponse,
)
from ..services.analise_service import AnaliseService


class AnaliseController:
    def __init__(self, service: AnaliseService):
        self.service = service

    def get_total(self) -> TotalResponse:
        return TotalResponse.model_validate(self.service.get_total())

    def get_media(self) -> MediaResponse:
        return MediaResponse.model_validate(self.service.get_media())

    def get_por_categoria(self) -> list[CategoriaTotalResponse]:
        resultados = self.service.get_por_categoria()
        return [CategoriaTotalResponse.model_validate(item) for item in resultados]

    def get_anomalias(self) -> list[AnomaliaResponse]:
        resultados = self.service.get_anomalias()
        return [AnomaliaResponse.model_validate(item) for item in resultados]
