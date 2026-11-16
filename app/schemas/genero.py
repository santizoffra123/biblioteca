from pydantic import BaseModel, ConfigDict, Field


class GeneroBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=80)
    descripcion: str | None = Field(default=None, max_length=200)


class GeneroCreate(GeneroBase):
    pass


class GeneroUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=80)
    descripcion: str | None = Field(default=None, max_length=200)


class GeneroResponse(GeneroBase):
    id: int

    model_config = ConfigDict(from_attributes=True)