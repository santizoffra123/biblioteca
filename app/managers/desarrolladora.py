from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.interfaces.desarrolladora import IDesarrolladoraManager
from app.models.desarrolladora import Desarrolladora
from app.schemas.desarrolladora import (
    DesarrolladoraCreate,
    DesarrolladoraUpdate,
    DesarrolladoraResponse
)
from app.exceptions import RecursoNoEncontrado, Conflicto, DatosInvalidos


class DesarrolladoraManager(IDesarrolladoraManager):

    def __init__(self, session: Session):
        self.session = session

    def crear(self, datos: DesarrolladoraCreate) -> DesarrolladoraResponse:
        desarrolladora = Desarrolladora(
            nombre=datos.nombre,
            pais=datos.pais
        )

        try:
            self.session.add(desarrolladora)
            self.session.commit()
            self.session.refresh(desarrolladora)
            return DesarrolladoraResponse.model_validate(desarrolladora)
        except IntegrityError:
            self.session.rollback()
            raise Conflicto("No se pudo crear la desarrolladora")
        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, desarrolladora_id: int) -> DesarrolladoraResponse:
        desarrolladora = self.session.get(Desarrolladora, desarrolladora_id)

        if not desarrolladora:
            raise RecursoNoEncontrado("Desarrolladora no encontrada")

        return DesarrolladoraResponse.model_validate(desarrolladora)

    def listar(self) -> list[DesarrolladoraResponse]:
        consulta = select(Desarrolladora).order_by(Desarrolladora.id)
        desarrolladoras = self.session.scalars(consulta).all()

        return [
            DesarrolladoraResponse.model_validate(d)
            for d in desarrolladoras
        ]

    def actualizar(
        self,
        desarrolladora_id: int,
        datos: DesarrolladoraUpdate
    ) -> DesarrolladoraResponse:
        desarrolladora = self.session.get(Desarrolladora, desarrolladora_id)

        if not desarrolladora:
            raise RecursoNoEncontrado("Desarrolladora no encontrada")

        cambios = datos.model_dump(exclude_unset=True)

        if "nombre" in cambios and cambios["nombre"] is None:
            raise DatosInvalidos("El nombre no puede ser nulo")

        try:
            for campo, valor in cambios.items():
                setattr(desarrolladora, campo, valor)

            self.session.commit()
            self.session.refresh(desarrolladora)

            return DesarrolladoraResponse.model_validate(desarrolladora)
        except IntegrityError:
            self.session.rollback()
            raise Conflicto("No se pudo actualizar la desarrolladora")
        except Exception:
            self.session.rollback()
            raise

    def eliminar(self, desarrolladora_id: int) -> None:
        desarrolladora = self.session.get(Desarrolladora, desarrolladora_id)

        if not desarrolladora:
            raise RecursoNoEncontrado("Desarrolladora no encontrada")

        try:
            self.session.delete(desarrolladora)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            raise Conflicto(
                "No se puede eliminar una desarrolladora que tiene juegos asociados"
            )
        except Exception:
            self.session.rollback()
            raise