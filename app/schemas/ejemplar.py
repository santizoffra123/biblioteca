from pydantic import BaseModel, ConfigDict, Field


class EjemplarCreate(BaseModel):
    juego_id: int = Field(gt=0)
    consola_id: int = Field(gt=0)
    estado_conservacion: str = Field(
        pattern=r"^(Excelente|Bueno|Regular|Malo)$"
    )


class EjemplarUpdate(BaseModel):
    estado_conservacion: str | None = Field(
        default=None,
        pattern=r"^(Excelente|Bueno|Regular|Malo)$"
    )


class EjemplarResponse(BaseModel):
    id: int
    juego_id: int
    consola_id: int
    estado_conservacion: str
    disponible: bool

    model_config = ConfigDict(from_attributes=True)