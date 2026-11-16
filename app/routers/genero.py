from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.schemas.genero import (
    GeneroCreate,
    GeneroUpdate,
    GeneroResponse
)

from app.interfaces.genero import IGeneroManager
from app.dependencies import get_genero_manager


router = APIRouter(
    prefix="/generos",
    tags=["Géneros"]
)


@router.post(
    "/",
    response_model=GeneroResponse,
    status_code=status.HTTP_201_CREATED
)
def crear_genero(
    datos: GeneroCreate,
    manager: Annotated[IGeneroManager, Depends(get_genero_manager)]
):
    return manager.crear(datos)


@router.get("/", response_model=list[GeneroResponse])
def listar_generos(
    manager: Annotated[IGeneroManager, Depends(get_genero_manager)]
):
    return manager.listar()


@router.get("/{genero_id}", response_model=GeneroResponse)
def obtener_genero(
    genero_id: int,
    manager: Annotated[IGeneroManager, Depends(get_genero_manager)]
):
    return manager.obtener_por_id(genero_id)


@router.put("/{genero_id}", response_model=GeneroResponse)
def actualizar_genero(
    genero_id: int,
    datos: GeneroUpdate,
    manager: Annotated[IGeneroManager, Depends(get_genero_manager)]
):
    return manager.actualizar(genero_id, datos)


@router.delete(
    "/{genero_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def eliminar_genero(
    genero_id: int,
    manager: Annotated[IGeneroManager, Depends(get_genero_manager)]
):
    manager.eliminar(genero_id)