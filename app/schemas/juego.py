from pydantic import BaseModel, ConfigDict, Field


class JuegoCreate(BaseModel):
    titulo: str = Field(min_length=1, max_length=150)
    descripcion: str | None = None
    anio_lanzamiento: int = Field(ge=1970, le=2100)
    clasificacion_edad: str = Field(pattern=r"^(E|E10\+|T|M|AO)$")
    desarrolladora_id: int = Field(gt=0)
    consolas_ids: list[int] = Field(min_length=1)
    generos_ids: list[int] = Field(min_length=1)


class JuegoUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1, max_length=150)
    descripcion: str | None = None
    anio_lanzamiento: int | None = Field(default=None, ge=1970, le=2100)
    clasificacion_edad: str | None = Field(default=None, pattern=r"^(E|E10\+|T|M|AO)$")
    desarrolladora_id: int | None = Field(default=None, gt=0)
    consolas_ids: list[int] | None = None
    generos_ids: list[int] | None = None


class JuegoResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    anio_lanzamiento: int
    clasificacion_edad: str
    desarrolladora_id: int

    consolas_ids: list[int]
    generos_ids: list[int]

    model_config = ConfigDict(from_attributes=True)
class JuegoFichaResponse(BaseModel):
    id: int
    titulo: str
    descripcion: str | None
    anio_lanzamiento: int
    clasificacion_edad: str
    desarrolladora: str
    consolas: list[str]
    generos: list[str]
    ejemplares_disponibles: int