from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Desarrolladora(Base):
    __tablename__ = "desarrolladoras"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )
    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    pais: Mapped[str | None] = mapped_column(
        String(80),
        nullable=True
    )