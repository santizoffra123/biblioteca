
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.interfaces.socio import ISocioManager
from app.models.socio import Socio
from app.models.prestamo import Prestamo
from app.models.ejemplar import Ejemplar
from app.models.juego import Juego
from app.models.consola import Consola
from app.schemas.socio import SocioCreate, SocioUpdate, SocioResponse
from app.schemas.prestamo import PrestamoHistorialResponse
from app.exceptions import RecursoNoEncontrado, DatosInvalidos, Conflicto


class SocioManager(ISocioManager):

    def __init__(self, session: Session):
        self.session = session

    def crear(self, datos: SocioCreate) -> SocioResponse:
        try:
            socio = Socio(**datos.model_dump())

            self.session.add(socio)
            self.session.commit()
            self.session.refresh(socio)

            return SocioResponse.model_validate(socio)

        except IntegrityError:
            self.session.rollback()
            raise Conflicto("Ya existe un socio con ese email")

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, socio_id: int) -> SocioResponse:
        socio = self.session.get(Socio, socio_id)

        if socio is None:
            raise RecursoNoEncontrado("Socio no encontrado")

        return SocioResponse.model_validate(socio)

    def listar(self) -> list[SocioResponse]:
        socios = self.session.scalars(
            select(Socio).order_by(Socio.id)
        ).all()

        return [SocioResponse.model_validate(s) for s in socios]

    def filtrar(
        self,
        nombre: str | None = None,
        apellido: str | None = None,
        activo: bool | None = None
    ) -> list[SocioResponse]:

        consulta = select(Socio)

        if nombre:
            consulta = consulta.where(
                Socio.nombre.ilike(f"%{nombre}%")
            )

        if apellido:
            consulta = consulta.where(
                Socio.apellido.ilike(f"%{apellido}%")
            )

        if activo is not None:
            consulta = consulta.where(
                Socio.activo == activo
            )

        socios = self.session.scalars(
            consulta.order_by(Socio.id)
        ).all()

        return [SocioResponse.model_validate(s) for s in socios]

    def listar_prestamos(
        self,
        socio_id: int
    ) -> list[PrestamoHistorialResponse]:

        socio = self.session.get(Socio, socio_id)

        if socio is None:
            raise RecursoNoEncontrado("Socio no encontrado")

        consulta = (
            select(
                Prestamo,
                Juego.titulo,
                Consola.nombre
            )
            .join(Ejemplar, Prestamo.ejemplar_id == Ejemplar.id)
            .join(Juego, Ejemplar.juego_id == Juego.id)
            .join(Consola, Ejemplar.consola_id == Consola.id)
            .where(Prestamo.socio_id == socio_id)
            .order_by(Prestamo.fecha_prestamo.desc())
        )

        resultados = self.session.execute(consulta).all()

        ahora = datetime.now(timezone.utc)

        historial = []

        for prestamo, titulo, nombre_consola in resultados:

            if prestamo.fecha_devolucion_real is not None:
                estado = "devuelto"
            elif prestamo.fecha_vencimiento < ahora:
                estado = "vencido"
            else:
                estado = "vigente"

            historial.append(
                PrestamoHistorialResponse(
                    id=prestamo.id,
                    fecha_prestamo=prestamo.fecha_prestamo,
                    fecha_vencimiento=prestamo.fecha_vencimiento,
                    fecha_devolucion_real=prestamo.fecha_devolucion_real,
                    juego=titulo,
                    consola=nombre_consola,
                    estado=estado
                )
            )

        return historial

    def actualizar(self, socio_id: int, datos: SocioUpdate) -> SocioResponse:
        try:
            socio = self.session.get(Socio, socio_id)

            if socio is None:
                raise RecursoNoEncontrado("Socio no encontrado")

            cambios = datos.model_dump(exclude_unset=True)

            if not cambios:
                raise DatosInvalidos("No se enviaron campos para actualizar")

            for campo, valor in cambios.items():
                if campo in ("nombre", "apellido") and valor is None:
                    raise DatosInvalidos(f"{campo} no puede ser nulo")

                setattr(socio, campo, valor)

            self.session.commit()
            self.session.refresh(socio)

            return SocioResponse.model_validate(socio)

        except IntegrityError:
            self.session.rollback()
            raise Conflicto("Ya existe un socio con ese email")

        except Exception:
            self.session.rollback()
            raise

    def eliminar(self, socio_id: int) -> None:
        try:
            socio = self.session.get(Socio, socio_id)

            if socio is None:
                raise RecursoNoEncontrado("Socio no encontrado")

            self.session.delete(socio)
            self.session.commit()

        except IntegrityError:
            self.session.rollback()
            raise Conflicto(
                "No se puede eliminar un socio con préstamos registrados"
            )

        except Exception:
            self.session.rollback()
            raise
