from pydantic import BaseModel


class TotalResponse(BaseModel):
    total: float


class MediaResponse(BaseModel):
    media: float


class CategoriaTotalResponse(BaseModel):
    categoria: str
    total: float


class AnomaliaResponse(BaseModel):
    descricao: str
    valor: float
    media: float
