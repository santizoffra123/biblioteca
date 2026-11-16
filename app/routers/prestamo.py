
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from app.schemas.prestamo import PrestamoVencidoResponse
from app.schemas.prestamo import PrestamoCreate, PrestamoResponse
from app.interfaces.prestamo import IPrestamoManager
from app.dependencies import get_prestamo_manager


router = APIRouter(prefix="/prestamos", tags=["Préstamos"])


@router.post("/", response_model=PrestamoResponse, status_code=status.HTTP_201_CREATED)
def crear_prestamo(
    datos: PrestamoCreate,
    manager: Annotated[IPrestamoManager, Depends(get_prestamo_manager)]
):
    return manager.crear(datos)


@router.get("/", response_model=list[PrestamoResponse])
def listar_prestamos(
    manager: Annotated[IPrestamoManager, Depends(get_prestamo_manager)],
    socio_id: int | None = None,
    ejemplar_id: int | None = None,
    estado: str | None = Query(default=None, pattern="^(vigente|vencido|devuelto)$")
):
    if socio_id is None and ejemplar_id is None and estado is None:
        return manager.listar()

    return manager.filtrar(
        socio_id=socio_id,
        ejemplar_id=ejemplar_id,
        estado=estado
    )
@router.get("/vencidos", response_model=list[PrestamoVencidoResponse])
def listar_prestamos_vencidos(
    manager: Annotated[IPrestamoManager, Depends(get_prestamo_manager)]
):
    return manager.listar_vencidos()

@router.get("/{prestamo_id}", response_model=PrestamoResponse)
def obtener_prestamo(
    prestamo_id: int,
    manager: Annotated[IPrestamoManager, Depends(get_prestamo_manager)]
):
    return manager.obtener_por_id(prestamo_id)


@router.post("/{prestamo_id}/devolver", response_model=PrestamoResponse)
def devolver_prestamo(
    prestamo_id: int,
    manager: Annotated[IPrestamoManager, Depends(get_prestamo_manager)]
):
    return manager.devolver(prestamo_id)
