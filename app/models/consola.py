
from sqlalchemy import BigInteger, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Consola(Base):

    __tablename__ = "consolas"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    fabricante: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    anio_lanzamiento: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
