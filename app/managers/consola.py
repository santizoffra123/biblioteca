
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.interfaces.consola import IConsolaManager
from app.models.consola import Consola
from app.schemas.consola import (
    ConsolaCreate,
    ConsolaUpdate,
    ConsolaResponse
)
from app.exceptions import RecursoNoEncontrado


class ConsolaManager(IConsolaManager):

    def __init__(self, session: Session):
        self.session = session

    def crear(self, datos: ConsolaCreate) -> ConsolaResponse:
        try:
            consola = Consola(
              nombre=datos.nombre,
             fabricante=datos.fabricante,
             anio_lanzamiento=datos.anio_lanzamiento
            )

            self.session.add(consola)
            self.session.commit()
            self.session.refresh(consola)

            return ConsolaResponse.model_validate(consola)

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, consola_id: int) -> ConsolaResponse:
        consola = self.session.get(Consola, consola_id)

        if consola is None:
            raise RecursoNoEncontrado("Consola no encontrada")

        return ConsolaResponse.model_validate(consola)

    def listar(self) -> list[ConsolaResponse]:
        consulta = select(Consola)
        consolas = self.session.scalars(consulta).all()

        return [
            ConsolaResponse.model_validate(c)
            for c in consolas
        ]

    def actualizar(
        self,
        consola_id: int,
        datos: ConsolaUpdate
    ) -> ConsolaResponse:

        consola = self.session.get(Consola, consola_id)

        if consola is None:
            raise RecursoNoEncontrado("Consola no encontrada")

        cambios = datos.model_dump(exclude_unset=True)

        for campo, valor in cambios.items():
            if valor is None:
                raise ValueError(f"{campo} no puede ser nulo")

            setattr(consola, campo, valor)

        self.session.commit()
        self.session.refresh(consola)

        return ConsolaResponse.model_validate(consola)

    def eliminar(self, consola_id: int) -> None:
        consola = self.session.get(Consola, consola_id)

        if consola is None:
            raise RecursoNoEncontrado("Consola no encontrada")

        self.session.delete(consola)
        self.session.commit()
