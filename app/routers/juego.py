
from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import get_juego_manager
from app.interfaces.juego import IJuegoManager
from app.schemas.juego import JuegoCreate, JuegoFichaResponse, JuegoUpdate, JuegoResponse


router = APIRouter(
    prefix="/juegos",
    tags=["Juegos"]
)


@router.post("/", response_model=JuegoResponse, status_code=201)
def crear_juego(
    datos: JuegoCreate,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.crear(datos)


@router.get("/", response_model=list[JuegoResponse])
def listar_juegos(
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)],
    titulo: str | None = None,
    genero_id: int | None = None,
    consola_id: int | None = None,
    desarrolladora_id: int | None = None,
    anio_desde: int | None = None,
    anio_hasta: int | None = None,
    clasificacion_edad: str | None = None
):
    filtros = {
        "titulo": titulo,
        "genero_id": genero_id,
        "consola_id": consola_id,
        "desarrolladora_id": desarrolladora_id,
        "anio_desde": anio_desde,
        "anio_hasta": anio_hasta,
        "clasificacion_edad": clasificacion_edad
    }

    if all(valor is None for valor in filtros.values()):
        return manager.listar()

    return manager.filtrar(**filtros)


@router.get("/desarrolladora/{desarrolladora_id}", response_model=list[JuegoResponse])
def listar_juegos_por_desarrolladora(
    desarrolladora_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.listar_por_desarrolladora(desarrolladora_id)


@router.get("/consola/{consola_id}", response_model=list[JuegoResponse])
def listar_juegos_por_consola(
    consola_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.listar_por_consola(consola_id)


@router.get("/genero/{genero_id}", response_model=list[JuegoResponse])
def listar_juegos_por_genero(
    genero_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.listar_por_genero(genero_id)


@router.get("/{juego_id}/consolas")
def listar_consolas_de_juego(
    juego_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.listar_consolas(juego_id)


@router.get("/{juego_id}/generos")
def listar_generos_de_juego(
    juego_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.listar_generos(juego_id)

@router.get("/ficha/{juego_id}", response_model=JuegoFichaResponse)
def obtener_ficha_completa(
    juego_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.obtener_ficha_completa(juego_id)
@router.get("/{juego_id}", response_model=JuegoResponse)
def obtener_juego(
    juego_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.obtener_por_id(juego_id)


@router.put("/{juego_id}", response_model=JuegoResponse)
def actualizar_juego(
    juego_id: int,
    datos: JuegoUpdate,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    return manager.actualizar(juego_id, datos)


@router.delete("/{juego_id}", status_code=204)
def eliminar_juego(
    juego_id: int,
    manager: Annotated[IJuegoManager, Depends(get_juego_manager)]
):
    manager.eliminar(juego_id)
