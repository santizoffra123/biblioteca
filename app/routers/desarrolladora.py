from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.dependencies import get_desarrolladora_manager
from app.interfaces.desarrolladora import IDesarrolladoraManager
from app.schemas.desarrolladora import (
    DesarrolladoraCreate,
    DesarrolladoraUpdate,
    DesarrolladoraResponse
)


router = APIRouter(
    prefix="/desarrolladoras",
    tags=["Desarrolladoras"]
)


@router.post(
    "/",
    response_model=DesarrolladoraResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_desarrolladora(
    datos: DesarrolladoraCreate,
    manager: Annotated[
        IDesarrolladoraManager,
        Depends(get_desarrolladora_manager)
    ]
):
    return manager.crear(datos)


@router.get("/", response_model=list[DesarrolladoraResponse])
def listar_desarrolladoras(
    manager: Annotated[
        IDesarrolladoraManager,
        Depends(get_desarrolladora_manager)
    ]
):
    return manager.listar()


@router.get("/{desarrolladora_id}", response_model=DesarrolladoraResponse)
def obtener_desarrolladora(
    desarrolladora_id: int,
    manager: Annotated[
        IDesarrolladoraManager,
        Depends(get_desarrolladora_manager)
    ]
):
    return manager.obtener_por_id(desarrolladora_id)


@router.put("/{desarrolladora_id}", response_model=DesarrolladoraResponse)
def actualizar_desarrolladora(
    desarrolladora_id: int,
    datos: DesarrolladoraUpdate,
    manager: Annotated[
        IDesarrolladoraManager,
        Depends(get_desarrolladora_manager)
    ]
):
    return manager.actualizar(desarrolladora_id, datos)


@router.delete(
    "/{desarrolladora_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_desarrolladora(
    desarrolladora_id: int,
    manager: Annotated[
        IDesarrolladoraManager,
        Depends(get_desarrolladora_manager)
    ]
):
    manager.eliminar(desarrolladora_id)