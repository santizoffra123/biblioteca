
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.socio import SocioCreate, SocioUpdate, SocioResponse
from app.schemas.prestamo import PrestamoHistorialResponse
from app.interfaces.socio import ISocioManager
from app.dependencies import get_socio_manager


router = APIRouter(prefix="/socios", tags=["Socios"])


@router.post("/", response_model=SocioResponse, status_code=status.HTTP_201_CREATED)
def crear_socio(
    datos: SocioCreate,
    manager: Annotated[ISocioManager, Depends(get_socio_manager)]
):
    return manager.crear(datos)


@router.get("/", response_model=list[SocioResponse])
def listar_socios(
    manager: Annotated[ISocioManager, Depends(get_socio_manager)],
    nombre: str | None = None,
    apellido: str | None = None,
    activo: bool | None = None
):
    filtros = {
        "nombre": nombre,
        "apellido": apellido,
        "activo": activo
    }

    if all(valor is None for valor in filtros.values()):
        return manager.listar()

    return manager.filtrar(**filtros)


@router.get("/{socio_id}/prestamos", response_model=list[PrestamoHistorialResponse])
def listar_prestamos_socio(
    socio_id: int,
    manager: Annotated[ISocioManager, Depends(get_socio_manager)]
):
    return manager.listar_prestamos(socio_id)


@router.get("/{socio_id}", response_model=SocioResponse)
def obtener_socio(
    socio_id: int,
    manager: Annotated[ISocioManager, Depends(get_socio_manager)]
):
    return manager.obtener_por_id(socio_id)


@router.put("/{socio_id}", response_model=SocioResponse)
def actualizar_socio(
    socio_id: int,
    datos: SocioUpdate,
    manager: Annotated[ISocioManager, Depends(get_socio_manager)]
):
    return manager.actualizar(socio_id, datos)


@router.delete("/{socio_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_socio(
    socio_id: int,
    manager: Annotated[ISocioManager, Depends(get_socio_manager)]
):
    manager.eliminar(socio_id)
