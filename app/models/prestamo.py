from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Prestamo(Base):
    __tablename__ = "prestamos"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    socio_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("socios.id", ondelete="RESTRICT"),
        nullable=False
    )

    ejemplar_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("ejemplares.id", ondelete="RESTRICT"),
        nullable=False
    )

    fecha_prestamo: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    fecha_vencimiento: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    fecha_devolucion_real: Mapped[DateTime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )