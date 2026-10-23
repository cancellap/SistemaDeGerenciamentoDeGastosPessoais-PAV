from datetime import date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GastoCreate(BaseModel):
    descricao: str = Field(min_length=1)
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo descrição não pode ficar vazio.")
        return value


class GastoUpdate(BaseModel):
    descricao: str = Field(min_length=1)
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int

    @field_validator("descricao")
    @classmethod
    def validar_descricao(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo descrição não pode ficar vazio.")
        return value


class GastoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    descricao: str
    valor: Decimal
    data: date
    usuario_id: int
    categoria_id: int
