from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.interfaces.genero import IGeneroManager
from app.models.genero import Genero
from app.schemas.genero import (
    GeneroCreate,
    GeneroUpdate,
    GeneroResponse
)
from app.exceptions import (
    RecursoNoEncontrado,
    Conflicto,
    DatosInvalidos
)


class GeneroManager(IGeneroManager):

    def __init__(self, session: Session):
        self.session = session

    def crear(self, datos: GeneroCreate) -> GeneroResponse:
        try:
            genero = Genero(
                nombre=datos.nombre,
                descripcion=datos.descripcion
            )

            self.session.add(genero)
            self.session.commit()
            self.session.refresh(genero)

            return GeneroResponse.model_validate(genero)

        except IntegrityError:
            self.session.rollback()
            raise Conflicto("Ya existe un género con ese nombre")

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, genero_id: int) -> GeneroResponse:
        genero = self.session.get(Genero, genero_id)

        if genero is None:
            raise RecursoNoEncontrado("Género no encontrado")

        return GeneroResponse.model_validate(genero)

    def listar(self) -> list[GeneroResponse]:
        consulta = select(Genero).order_by(Genero.id)
        generos = self.session.scalars(consulta).all()

        return [
            GeneroResponse.model_validate(genero)
            for genero in generos
        ]

    def actualizar(
        self,
        genero_id: int,
        datos: GeneroUpdate
    ) -> GeneroResponse:

        try:
            genero = self.session.get(Genero, genero_id)

            if genero is None:
                raise RecursoNoEncontrado("Género no encontrado")

            cambios = datos.model_dump(exclude_unset=True)

            if not cambios:
                raise DatosInvalidos("No se enviaron campos para actualizar")

            for campo, valor in cambios.items():
                if campo == "nombre" and valor is None:
                    raise DatosInvalidos("El nombre no puede ser nulo")

                setattr(genero, campo, valor)

            self.session.commit()
            self.session.refresh(genero)

            return GeneroResponse.model_validate(genero)

        except IntegrityError:
            self.session.rollback()
            raise Conflicto("Ya existe un género con ese nombre")

        except Exception:
            self.session.rollback()
            raise

    def eliminar(self, genero_id: int) -> None:
        try:
            genero = self.session.get(Genero, genero_id)

            if genero is None:
                raise RecursoNoEncontrado("Género no encontrado")

            self.session.delete(genero)
            self.session.commit()

        except IntegrityError:
            self.session.rollback()
            raise Conflicto("No se puede eliminar: el género tiene juegos asociados")

        except Exception:
            self.session.rollback()
            raise