from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PrestamoCreate(BaseModel):
    socio_id: int = Field(gt=0)
    ejemplar_id: int = Field(gt=0)
    fecha_vencimiento: datetime


class PrestamoResponse(BaseModel):
    id: int
    socio_id: int
    ejemplar_id: int
    fecha_prestamo: datetime
    fecha_vencimiento: datetime
    fecha_devolucion_real: datetime | None

    model_config = ConfigDict(from_attributes=True)


class PrestamoHistorialResponse(BaseModel):
    id: int
    fecha_prestamo: datetime
    fecha_vencimiento: datetime
    fecha_devolucion_real: datetime | None
    juego: str
    consola: str
    estado: str


class PrestamoVencidoResponse(BaseModel):
    id: int
    socio_id: int
    nombre_socio: str
    apellido_socio: str
    email_socio: str | None
    titulo_juego: str
    nombre_consola: str
    fecha_prestamo: datetime
    fecha_vencimiento: datetime