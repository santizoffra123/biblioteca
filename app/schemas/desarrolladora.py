from pydantic import BaseModel, ConfigDict, Field


class DesarrolladoraCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    pais: str | None = Field(default=None, max_length=80)


class DesarrolladoraUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    pais: str | None = Field(default=None, max_length=80)


class DesarrolladoraResponse(BaseModel):
    id: int
    nombre: str
    pais: str | None

    model_config = ConfigDict(from_attributes=True)