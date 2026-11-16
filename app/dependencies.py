from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal

from app.interfaces.desarrolladora import IDesarrolladoraManager
from app.managers.desarrolladora import DesarrolladoraManager

from app.interfaces.consola import IConsolaManager
from app.managers.consola import ConsolaManager

from app.interfaces.genero import IGeneroManager
from app.managers.genero import GeneroManager

from app.interfaces.juego import IJuegoManager
from app.managers.juego import JuegoManager

from app.interfaces.ejemplar import IEjemplarManager
from app.managers.ejemplar import EjemplarManager

from app.interfaces.socio import ISocioManager
from app.managers.socio import SocioManager

from app.interfaces.prestamo import IPrestamoManager
from app.managers.prestamo import PrestamoManager


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_desarrolladora_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IDesarrolladoraManager:
    return DesarrolladoraManager(db)


def get_consola_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IConsolaManager:
    return ConsolaManager(db)


def get_genero_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IGeneroManager:
    return GeneroManager(db)


def get_juego_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IJuegoManager:
    return JuegoManager(db)


def get_ejemplar_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IEjemplarManager:
    return EjemplarManager(db)


def get_socio_manager(
    db: Annotated[Session, Depends(get_db)]
) -> ISocioManager:
    return SocioManager(db)


def get_prestamo_manager(
    db: Annotated[Session, Depends(get_db)]
) -> IPrestamoManager:
    return PrestamoManager(db)