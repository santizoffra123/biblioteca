
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_ejemplar_manager
from app.interfaces.ejemplar import IEjemplarManager
from app.schemas.ejemplar import (
    EjemplarCreate,
    EjemplarUpdate,
    EjemplarResponse
)


router = APIRouter(
    prefix="/ejemplares",
    tags=["Ejemplares"]
)


@router.post(
    "/",
    response_model=EjemplarResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_ejemplar(
    datos: EjemplarCreate,
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)]
):
    return manager.crear(datos)


@router.get(
    "/",
    response_model=list[EjemplarResponse]
)
def listar_ejemplares(
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)],
    juego_id: int | None = None,
    consola_id: int | None = None,
    estado_conservacion: str | None = None,
    disponible: bool | None = None
):
    filtros = {
        "juego_id": juego_id,
        "consola_id": consola_id,
        "estado_conservacion": estado_conservacion,
        "disponible": disponible
    }

    if all(valor is None for valor in filtros.values()):
        return manager.listar()

    return manager.filtrar(**filtros)


@router.get(
    "/juego/{juego_id}",
    response_model=list[EjemplarResponse]
)
def listar_ejemplares_por_juego(
    juego_id: int,
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)]
):
    return manager.listar_por_juego(juego_id)


@router.get(
    "/{ejemplar_id}",
    response_model=EjemplarResponse
)
def obtener_ejemplar(
    ejemplar_id: int,
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)]
):
    return manager.obtener_por_id(ejemplar_id)


@router.put(
    "/{ejemplar_id}",
    response_model=EjemplarResponse
)
def actualizar_ejemplar(
    ejemplar_id: int,
    datos: EjemplarUpdate,
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)]
):
    return manager.actualizar(ejemplar_id, datos)


@router.delete(
    "/{ejemplar_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_ejemplar(
    ejemplar_id: int,
    manager: Annotated[IEjemplarManager, Depends(get_ejemplar_manager)]
):
    manager.eliminar(ejemplar_id)
