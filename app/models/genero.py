from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Genero(Base):
    __tablename__ = "generos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    nombre: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        unique=True
    )

    descripcion: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )