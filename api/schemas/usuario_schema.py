from pydantic import BaseModel, ConfigDict, Field


class UsuarioCreate(BaseModel):
    nome: str = Field(min_length=1)
    email: str = Field(min_length=1)


class UsuarioUpdate(BaseModel):
    nome: str = Field(min_length=1)
    email: str = Field(min_length=1)


class UsuarioResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
