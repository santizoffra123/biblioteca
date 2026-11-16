from sqlalchemy import (
    BigInteger,
    String,
    Integer,
    Text,
    ForeignKey,
    Table,
    Column
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.consola import Consola
from app.models.genero import Genero
from app.models.desarrolladora import Desarrolladora


juego_consola = Table(
    "juego_consola",
    Base.metadata,
    Column("juego_id", BigInteger, ForeignKey("juegos.id", ondelete="CASCADE"), primary_key=True),
    Column("consola_id", BigInteger, ForeignKey("consolas.id", ondelete="RESTRICT"), primary_key=True)
)

juego_genero = Table(
    "juego_genero",
    Base.metadata,
    Column("juego_id", BigInteger, ForeignKey("juegos.id", ondelete="CASCADE"), primary_key=True),
    Column("genero_id", BigInteger, ForeignKey("generos.id", ondelete="RESTRICT"), primary_key=True)
)


class Juego(Base):
    __tablename__ = "juegos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    descripcion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    anio_lanzamiento: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    clasificacion_edad: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    desarrolladora_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("desarrolladoras.id", ondelete="RESTRICT"),
        nullable=False
    )

    desarrolladora: Mapped[Desarrolladora] = relationship()

    consolas: Mapped[list[Consola]] = relationship(
        secondary=juego_consola
    )

    generos: Mapped[list[Genero]] = relationship(
        secondary=juego_genero
    )