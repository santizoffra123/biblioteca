from sqlalchemy import (
    BigInteger,
    String,
    Boolean,
    ForeignKeyConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Ejemplar(Base):
    __tablename__ = "ejemplares"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    juego_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    consola_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    estado_conservacion: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    disponible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    __table_args__ = (
        ForeignKeyConstraint(
            ["juego_id", "consola_id"],
            ["juego_consola.juego_id", "juego_consola.consola_id"],
            ondelete="RESTRICT"
        ),
    )