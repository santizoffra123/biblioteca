
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from app.models.ejemplar import Ejemplar
from app.schemas.juego import JuegoFichaResponse
from app.interfaces.juego import IJuegoManager
from app.models.juego import Juego
from app.models.desarrolladora import Desarrolladora
from app.models.consola import Consola
from app.models.genero import Genero
from app.models.ejemplar import Ejemplar
from app.schemas.juego import JuegoCreate, JuegoUpdate, JuegoResponse
from app.exceptions import RecursoNoEncontrado, DatosInvalidos, Conflicto


class JuegoManager(IJuegoManager):

    def __init__(self, session: Session):
        self.session = session

    def _respuesta(self, juego: Juego) -> JuegoResponse:
        return JuegoResponse(
            id=juego.id,
            titulo=juego.titulo,
            descripcion=juego.descripcion,
            anio_lanzamiento=juego.anio_lanzamiento,
            clasificacion_edad=juego.clasificacion_edad,
            desarrolladora_id=juego.desarrolladora_id,
            consolas_ids=[c.id for c in juego.consolas],
            generos_ids=[g.id for g in juego.generos]
        )

    def crear(self, datos: JuegoCreate) -> JuegoResponse:
        try:
            desarrolladora = self.session.get(
                Desarrolladora, datos.desarrolladora_id
            )

            if desarrolladora is None:
                raise RecursoNoEncontrado("Desarrolladora no encontrada")

            consolas = [
                self.session.get(Consola, id)
                for id in datos.consolas_ids
            ]

            generos = [
                self.session.get(Genero, id)
                for id in datos.generos_ids
            ]

            if any(c is None for c in consolas):
                raise RecursoNoEncontrado("Una o más consolas no existen")

            if any(g is None for g in generos):
                raise RecursoNoEncontrado("Uno o más géneros no existen")

            if consolas and datos.anio_lanzamiento < min(
                c.anio_lanzamiento for c in consolas
            ):
                raise DatosInvalidos(
                    "El año del juego no puede ser anterior al de sus consolas"
                )

            juego = Juego(
                titulo=datos.titulo,
                descripcion=datos.descripcion,
                anio_lanzamiento=datos.anio_lanzamiento,
                clasificacion_edad=datos.clasificacion_edad,
                desarrolladora_id=datos.desarrolladora_id,
                consolas=consolas,
                generos=generos
            )

            self.session.add(juego)
            self.session.commit()
            self.session.refresh(juego)

            return self._respuesta(juego)

        except Exception:
            self.session.rollback()
            raise

    def obtener_por_id(self, juego_id: int) -> JuegoResponse:
        juego = self.session.get(Juego, juego_id)

        if juego is None:
            raise RecursoNoEncontrado("Juego no encontrado")

        return self._respuesta(juego)

    def listar(self) -> list[JuegoResponse]:
        juegos = self.session.scalars(
            select(Juego).order_by(Juego.id)
        ).all()

        return [self._respuesta(j) for j in juegos]

    def filtrar(
        self,
        titulo: str | None = None,
        genero_id: int | None = None,
        consola_id: int | None = None,
        desarrolladora_id: int | None = None,
        anio_desde: int | None = None,
        anio_hasta: int | None = None,
        clasificacion_edad: str | None = None
    ) -> list[JuegoResponse]:

        consulta = select(Juego)

        if titulo:
            consulta = consulta.where(
                Juego.titulo.ilike(f"%{titulo}%")
            )

        if genero_id is not None:
            consulta = consulta.where(
                Juego.generos.any(Genero.id == genero_id)
            )

        if consola_id is not None:
            consulta = consulta.where(
                Juego.consolas.any(Consola.id == consola_id)
            )

        if desarrolladora_id is not None:
            consulta = consulta.where(
                Juego.desarrolladora_id == desarrolladora_id
            )

        if anio_desde is not None:
            consulta = consulta.where(
                Juego.anio_lanzamiento >= anio_desde
            )

        if anio_hasta is not None:
            consulta = consulta.where(
                Juego.anio_lanzamiento <= anio_hasta
            )

        if clasificacion_edad:
            consulta = consulta.where(
                Juego.clasificacion_edad == clasificacion_edad
            )

        juegos = self.session.scalars(
            consulta.order_by(Juego.id)
        ).all()

        return [self._respuesta(j) for j in juegos]

    def actualizar(self, juego_id: int, datos: JuegoUpdate) -> JuegoResponse:
        try:
            juego = self.session.get(Juego, juego_id)

            if juego is None:
                raise RecursoNoEncontrado("Juego no encontrado")

            cambios = datos.model_dump(exclude_unset=True)

            if not cambios:
                raise DatosInvalidos("No se enviaron campos para actualizar")

            if "desarrolladora_id" in cambios:
                desarrolladora = self.session.get(
                    Desarrolladora, cambios["desarrolladora_id"]
                )

                if desarrolladora is None:
                    raise RecursoNoEncontrado("Desarrolladora no encontrada")

                juego.desarrolladora_id = desarrolladora.id

            if "consolas_ids" in cambios:
                consolas = [
                    self.session.get(Consola, id)
                    for id in cambios["consolas_ids"]
                ]

                if any(c is None for c in consolas):
                    raise RecursoNoEncontrado("Una o más consolas no existen")

                juego.consolas = consolas

            if "generos_ids" in cambios:
                generos = [
                    self.session.get(Genero, id)
                    for id in cambios["generos_ids"]
                ]

                if any(g is None for g in generos):
                    raise RecursoNoEncontrado("Uno o más géneros no existen")

                juego.generos = generos

            for campo in (
                "titulo",
                "descripcion",
                "anio_lanzamiento",
                "clasificacion_edad"
            ):
                if campo in cambios:
                    if campo != "descripcion" and cambios[campo] is None:
                        raise DatosInvalidos(f"{campo} no puede ser nulo")

                    setattr(juego, campo, cambios[campo])

            if juego.consolas and juego.anio_lanzamiento < min(
                c.anio_lanzamiento for c in juego.consolas
            ):
                raise DatosInvalidos(
                    "El año del juego no puede ser anterior al de sus consolas"
                )

            self.session.commit()
            self.session.refresh(juego)

            return self._respuesta(juego)

        except Exception:
            self.session.rollback()
            raise

    def eliminar(self, juego_id: int) -> None:
        try:
            juego = self.session.get(Juego, juego_id)

            if juego is None:
                raise RecursoNoEncontrado("Juego no encontrado")

            ejemplares = self.session.scalar(
                select(Ejemplar.id).where(
                    Ejemplar.juego_id == juego_id
                ).limit(1)
            )

            if ejemplares is not None:
                raise Conflicto(
                    "No se puede eliminar un juego que tiene ejemplares"
                )

            self.session.delete(juego)
            self.session.commit()

        except Exception:
            self.session.rollback()
            raise
    
    def listar_por_desarrolladora(self, desarrolladora_id: int) -> list[JuegoResponse]:
        desarrolladora = self.session.get(Desarrolladora, desarrolladora_id)

        if desarrolladora is None:
            raise RecursoNoEncontrado("Desarrolladora no encontrada")

        juegos = self.session.scalars(
            select(Juego)
            .where(Juego.desarrolladora_id == desarrolladora_id)
            .order_by(Juego.id)
        ).all()

        return [self._respuesta(j) for j in juegos]

    def listar_consolas(self, juego_id: int) -> list[Consola]:
        juego = self.session.get(Juego, juego_id)

        if juego is None:
            raise RecursoNoEncontrado("Juego no encontrado")

        return juego.consolas

    def listar_por_consola(self, consola_id: int) -> list[JuegoResponse]:
        consola = self.session.get(Consola, consola_id)

        if consola is None:
            raise RecursoNoEncontrado("Consola no encontrada")

        juegos = self.session.scalars(
            select(Juego)
            .where(Juego.consolas.any(Consola.id == consola_id))
            .order_by(Juego.id)
        ).all()

        return [self._respuesta(j) for j in juegos]

    def listar_generos(self, juego_id: int) -> list[Genero]:
        juego = self.session.get(Juego, juego_id)

        if juego is None:
            raise RecursoNoEncontrado("Juego no encontrado")

        return juego.generos

    def listar_por_genero(self, genero_id: int) -> list[JuegoResponse]:
        genero = self.session.get(Genero, genero_id)

        if genero is None:
            raise RecursoNoEncontrado("Género no encontrado")

        juegos = self.session.scalars(
            select(Juego)
            .where(Juego.generos.any(Genero.id == genero_id))
            .order_by(Juego.id)
        ).all()

        return [self._respuesta(j) for j in juegos]

    def obtener_ficha_completa(self, juego_id: int) -> JuegoFichaResponse:
        juego = self.session.execute(
            select(Juego)
            .options(
                selectinload(Juego.desarrolladora),
                selectinload(Juego.consolas),
                selectinload(Juego.generos)
            )
            .where(Juego.id == juego_id)
        ).scalar_one_or_none()

        if juego is None:
            raise RecursoNoEncontrado("Juego no encontrado")

        disponibles = self.session.scalar(
            select(func.count(Ejemplar.id)).where(
                Ejemplar.juego_id == juego_id,
                Ejemplar.disponible.is_(True)
            )
        )

        return JuegoFichaResponse(
            id=juego.id,
            titulo=juego.titulo,
            descripcion=juego.descripcion,
            anio_lanzamiento=juego.anio_lanzamiento,
            clasificacion_edad=juego.clasificacion_edad,
            desarrolladora=juego.desarrolladora.nombre,
            consolas=[consola.nombre for consola in juego.consolas],
            generos=[genero.nombre for genero in juego.generos],
            ejemplares_disponibles=disponibles or 0
        )
