from pydantic import BaseModel, ConfigDict, Field, field_validator


class CategoriaCreate(BaseModel):
    nome: str = Field(min_length=1)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo nome não pode ficar vazio.")
        return value


class CategoriaUpdate(BaseModel):
    nome: str = Field(min_length=1)

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("O campo nome não pode ficar vazio.")
        return value


class CategoriaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
