
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.interfaces.ejemplar import IEjemplarManager
from app.models.ejemplar import Ejemplar
from app.models.juego import juego_consola
from app.schemas.ejemplar import EjemplarCreate, EjemplarUpdate, EjemplarResponse
from app.exceptions import RecursoNoEncontrado, DatosInvalidos, Conflicto


class EjemplarManager(IEjemplarManager):

    def __init__(self, session: Session):
        self.session = session

    def crear(self, datos: EjemplarCreate) -> EjemplarResponse:
        try:
            combinacion = self.session.execute(
                select(juego_consola).where(
                    juego_consola.c.juego_id == datos.juego_id,
                    juego_consola.c.consola_id == datos.consola_id
                )
            ).first()

            if combinacion is None:
                raise DatosInvalidos(
                    "El juego no está asociado a esa consola"
                )

            ejemplar = Ejemplar(
                juego_id=datos.juego_id,
                consola_id=datos.consola_id,
                estado_conservacion=datos.estado_conservacion,
                disponible=True
            )

            self.session.add(ejemplar)
            self.session.commit()
            self.session.refresh(ejemplar)

            return EjemplarResponse.model_validate(ejemplar)

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, ejemplar_id: int) -> EjemplarResponse:
        ejemplar = self.session.get(Ejemplar, ejemplar_id)

        if ejemplar is None:
            raise RecursoNoEncontrado("Ejemplar no encontrado")

        return EjemplarResponse.model_validate(ejemplar)

    def listar(self) -> list[EjemplarResponse]:
        ejemplares = self.session.scalars(
            select(Ejemplar).order_by(Ejemplar.id)
        ).all()

        return [EjemplarResponse.model_validate(e) for e in ejemplares]

    def filtrar(
        self,
        juego_id: int | None = None,
        consola_id: int | None = None,
        estado_conservacion: str | None = None,
        disponible: bool | None = None
    ) -> list[EjemplarResponse]:

        consulta = select(Ejemplar)

        if juego_id is not None:
            consulta = consulta.where(
                Ejemplar.juego_id == juego_id
            )

        if consola_id is not None:
            consulta = consulta.where(
                Ejemplar.consola_id == consola_id
            )

        if estado_conservacion is not None:
            consulta = consulta.where(
                Ejemplar.estado_conservacion.ilike(
                    f"%{estado_conservacion}%"
                )
            )

        if disponible is not None:
            consulta = consulta.where(
                Ejemplar.disponible == disponible
            )

        ejemplares = self.session.scalars(
            consulta.order_by(Ejemplar.id)
        ).all()

        return [
            EjemplarResponse.model_validate(e)
            for e in ejemplares
        ]

    def actualizar(
        self,
        ejemplar_id: int,
        datos: EjemplarUpdate
    ) -> EjemplarResponse:
        try:
            ejemplar = self.session.get(Ejemplar, ejemplar_id)

            if ejemplar is None:
                raise RecursoNoEncontrado("Ejemplar no encontrado")

            cambios = datos.model_dump(exclude_unset=True)

            if not cambios:
                raise DatosInvalidos("No se enviaron campos para actualizar")

            for campo, valor in cambios.items():
                if valor is None:
                    raise DatosInvalidos(f"{campo} no puede ser nulo")
                setattr(ejemplar, campo, valor)

            self.session.commit()
            self.session.refresh(ejemplar)

            return EjemplarResponse.model_validate(ejemplar)

        except Exception:
            self.session.rollback()
            raise

    def eliminar(self, ejemplar_id: int) -> None:
        try:
            ejemplar = self.session.get(Ejemplar, ejemplar_id)

            if ejemplar is None:
                raise RecursoNoEncontrado("Ejemplar no encontrado")

            if not ejemplar.disponible:
                raise Conflicto("No se puede eliminar un ejemplar prestado")

            self.session.delete(ejemplar)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
    
    def listar_por_juego(self, juego_id: int) -> list[EjemplarResponse]:
        from app.models.juego import Juego

        juego = self.session.get(Juego, juego_id)

        if juego is None:
            raise RecursoNoEncontrado("Juego no encontrado")

        ejemplares = self.session.scalars(
            select(Ejemplar)
            .where(Ejemplar.juego_id == juego_id)
            .order_by(Ejemplar.id)
        ).all()

        return [
            EjemplarResponse.model_validate(e)
            for e in ejemplares
        ]

