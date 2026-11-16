from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, EmailStr


class SocioCreate(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    apellido: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=30)


class SocioUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=100)
    apellido: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    telefono: str | None = Field(default=None, max_length=30)
    activo: bool | None = None


class SocioResponse(BaseModel):
    id: int
    nombre: str
    apellido: str
    email: str | None
    telefono: str | None
    fecha_registro: datetime
    activo: bool

    model_config = ConfigDict(from_attributes=True)