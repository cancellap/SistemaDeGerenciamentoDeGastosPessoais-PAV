from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class GastoCreate(BaseModel):
    descricao: str = Field(min_length=1)
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int


class GastoUpdate(BaseModel):
    descricao: str = Field(min_length=1)
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int


class GastoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int
