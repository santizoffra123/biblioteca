from datetime import datetime, timezone
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.interfaces.prestamo import IPrestamoManager
from app.models.prestamo import Prestamo
from app.models.socio import Socio
from app.models.ejemplar import Ejemplar
from app.schemas.prestamo import PrestamoCreate, PrestamoResponse
from app.exceptions import RecursoNoEncontrado, DatosInvalidos, Conflicto
from app.models.juego import Juego
from app.models.consola import Consola
from app.schemas.prestamo import PrestamoVencidoResponse

class PrestamoManager(IPrestamoManager):

    def __init__(self, session: Session):
        self.session = session

    
    def crear(self, datos: PrestamoCreate) -> PrestamoResponse:
        try:
            socio = self.session.scalar(
                select(Socio)
                .where(Socio.id == datos.socio_id)
                .with_for_update()
            )

            if socio is None:
                raise RecursoNoEncontrado("Socio no encontrado")

            ejemplar = self.session.scalar(
                select(Ejemplar)
                .where(Ejemplar.id == datos.ejemplar_id)
                .with_for_update()
            )

            if ejemplar is None:
                raise RecursoNoEncontrado("Ejemplar no encontrado")

            ahora = datetime.now(timezone.utc)

            if datos.fecha_vencimiento.tzinfo is None:
                raise DatosInvalidos("La fecha de vencimiento debe incluir zona horaria")

            if datos.fecha_vencimiento <= ahora:
                raise DatosInvalidos("La fecha de vencimiento debe ser futura")

            if not socio.activo:
                raise Conflicto("El socio está inactivo")

            if not ejemplar.disponible:
                raise Conflicto("El ejemplar no está disponible")

            prestamos_activos = self.session.scalar(
                select(func.count(Prestamo.id)).where(
                    Prestamo.socio_id == socio.id,
                    Prestamo.fecha_devolucion_real.is_(None)
                )
            )

            if prestamos_activos >= 3:
                raise Conflicto("El socio ya tiene tres préstamos activos")

            prestamos_vencidos = self.session.scalar(
                select(func.count(Prestamo.id)).where(
                    Prestamo.socio_id == socio.id,
                    Prestamo.fecha_devolucion_real.is_(None),
                    Prestamo.fecha_vencimiento < ahora
                )
            )

            if prestamos_vencidos:
                raise Conflicto("El socio tiene préstamos vencidos")

            prestamo = Prestamo(
                socio_id=socio.id,
                ejemplar_id=ejemplar.id,
                fecha_vencimiento=datos.fecha_vencimiento
            )

            ejemplar.disponible = False

            self.session.add(prestamo)
            self.session.commit()
            self.session.refresh(prestamo)

            return PrestamoResponse.model_validate(prestamo)

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, prestamo_id: int) -> PrestamoResponse:
        prestamo = self.session.get(Prestamo, prestamo_id)

        if prestamo is None:
            raise RecursoNoEncontrado("Préstamo no encontrado")

        return PrestamoResponse.model_validate(prestamo)

    def listar(self) -> list[PrestamoResponse]:
        prestamos = self.session.scalars(
            select(Prestamo).order_by(Prestamo.id)
        ).all()

        return [PrestamoResponse.model_validate(p) for p in prestamos]

    def filtrar(
        self,
        socio_id: int | None = None,
        ejemplar_id: int | None = None,
        estado: str | None = None
    ) -> list[PrestamoResponse]:

        consulta = select(Prestamo)
        ahora = datetime.now(timezone.utc)

        if socio_id is not None:
            consulta = consulta.where(Prestamo.socio_id == socio_id)

        if ejemplar_id is not None:
            consulta = consulta.where(Prestamo.ejemplar_id == ejemplar_id)

        if estado == "vigente":
            consulta = consulta.where(
                Prestamo.fecha_devolucion_real.is_(None),
                Prestamo.fecha_vencimiento >= ahora
            )

        elif estado == "vencido":
            consulta = consulta.where(
                Prestamo.fecha_devolucion_real.is_(None),
                Prestamo.fecha_vencimiento < ahora
            )

        elif estado == "devuelto":
            consulta = consulta.where(
                Prestamo.fecha_devolucion_real.is_not(None)
            )

        elif estado is not None:
            raise DatosInvalidos(
                "Estado inválido. Use vigente, vencido o devuelto"
            )

        prestamos = self.session.scalars(
            consulta.order_by(Prestamo.id)
        ).all()

        return [PrestamoResponse.model_validate(p) for p in prestamos]

    def devolver(self, prestamo_id: int) -> PrestamoResponse:
        try:
            prestamo = self.session.scalar(
                select(Prestamo)
                .where(Prestamo.id == prestamo_id)
                .with_for_update()
            )

            if prestamo is None:
                raise RecursoNoEncontrado("Préstamo no encontrado")

            if prestamo.fecha_devolucion_real is not None:
                raise Conflicto("Este préstamo ya fue devuelto")

            ejemplar = self.session.scalar(
                select(Ejemplar)
                .where(Ejemplar.id == prestamo.ejemplar_id)
                .with_for_update()
            )

            prestamo.fecha_devolucion_real = datetime.now(timezone.utc)
            ejemplar.disponible = True

            self.session.commit()
            self.session.refresh(prestamo)

            return PrestamoResponse.model_validate(prestamo)

        except Exception:
            self.session.rollback()
            raise
    def listar_vencidos(self) -> list[PrestamoVencidoResponse]:
        ahora = datetime.now(timezone.utc)

        resultados = self.session.execute(
            select(
                Prestamo.id,
                Prestamo.socio_id,
                Socio.nombre.label("nombre_socio"),
                Socio.apellido.label("apellido_socio"),
                Socio.email.label("email_socio"),
                Juego.titulo.label("titulo_juego"),
                Consola.nombre.label("nombre_consola"),
                Prestamo.fecha_prestamo,
                Prestamo.fecha_vencimiento
            )
            .join(Socio, Prestamo.socio_id == Socio.id)
            .join(Ejemplar, Prestamo.ejemplar_id == Ejemplar.id)
            .join(Juego, Ejemplar.juego_id == Juego.id)
            .join(Consola, Ejemplar.consola_id == Consola.id)
            .where(
                Prestamo.fecha_devolucion_real.is_(None),
                Prestamo.fecha_vencimiento < ahora
            )
            .order_by(Prestamo.fecha_vencimiento)
        ).mappings().all()

        return [
            PrestamoVencidoResponse(**dict(resultado))
            for resultado in resultados
        ]
