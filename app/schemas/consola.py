
from pydantic import BaseModel, ConfigDict, Field


class ConsolaBase(BaseModel):

    nombre: str = Field(
        min_length=1,
        max_length=100
    )

    fabricante: str = Field(
        min_length=1,
        max_length=100
    )

    anio_lanzamiento: int = Field(
        ge=1970,
        le=2100
    )


class ConsolaCreate(ConsolaBase):
    pass


class ConsolaUpdate(BaseModel):

    nombre: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    fabricante: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )

    anio_lanzamiento: int | None = Field(
        default=None,
        ge=1970,
        le=2100
    )


class ConsolaResponse(ConsolaBase):

    id: int

    model_config = ConfigDict(from_attributes=True)
