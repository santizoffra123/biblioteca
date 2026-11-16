
from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.consola import (
    ConsolaCreate,
    ConsolaUpdate,
    ConsolaResponse
)

from app.interfaces.consola import IConsolaManager
from app.dependencies import get_consola_manager


router = APIRouter(
    prefix="/consolas",
    tags=["Consolas"]
)


@router.post(
    "/",
    response_model=ConsolaResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_consola(
    datos: ConsolaCreate,
    manager: Annotated[
        IConsolaManager,
        Depends(get_consola_manager)
    ]
):
    return manager.crear(datos)


@router.get(
    "/",
    response_model=list[ConsolaResponse]
)
def listar_consolas(
    manager: Annotated[
        IConsolaManager,
        Depends(get_consola_manager)
    ]
):
    return manager.listar()


@router.get(
    "/{consola_id}",
    response_model=ConsolaResponse
)
def obtener_consola(
    consola_id: int,
    manager: Annotated[
        IConsolaManager,
        Depends(get_consola_manager)
    ]
):
    return manager.obtener_por_id(consola_id)


@router.put(
    "/{consola_id}",
    response_model=ConsolaResponse
)
def actualizar_consola(
    consola_id: int,
    datos: ConsolaUpdate,
    manager: Annotated[
        IConsolaManager,
        Depends(get_consola_manager)
    ]
):
    return manager.actualizar(consola_id, datos)


@router.delete(
    "/{consola_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_consola(
    consola_id: int,
    manager: Annotated[
        IConsolaManager,
        Depends(get_consola_manager)
    ]
):
    manager.eliminar(consola_id)
