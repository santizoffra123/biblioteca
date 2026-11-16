from abc import ABC, abstractmethod

from app.schemas.prestamo import (
    PrestamoCreate,
    PrestamoResponse,
    PrestamoVencidoResponse
)


class IPrestamoManager(ABC):

    @abstractmethod
    def crear(self, datos: PrestamoCreate) -> PrestamoResponse:
        pass

    @abstractmethod
    def obtener_por_id(self, prestamo_id: int) -> PrestamoResponse:
        pass

    @abstractmethod
    def listar(self) -> list[PrestamoResponse]:
        pass

    @abstractmethod
    def filtrar(
        self,
        socio_id: int | None = None,
        ejemplar_id: int | None = None,
        estado: str | None = None
    ) -> list[PrestamoResponse]:
        pass

    @abstractmethod
    def listar_vencidos(self) -> list[PrestamoVencidoResponse]:
        pass

    @abstractmethod
    def devolver(self, prestamo_id: int) -> PrestamoResponse:
        pass