
from abc import ABC, abstractmethod

from app.schemas.socio import SocioCreate, SocioUpdate, SocioResponse
from app.schemas.prestamo import PrestamoHistorialResponse


class ISocioManager(ABC):

    @abstractmethod
    def crear(self, datos: SocioCreate) -> SocioResponse:
        pass

    @abstractmethod
    def obtener_por_id(self, socio_id: int) -> SocioResponse:
        pass

    @abstractmethod
    def listar(self) -> list[SocioResponse]:
        pass

    @abstractmethod
    def filtrar(
        self,
        nombre=None,
        apellido=None,
        activo=None
    ) -> list[SocioResponse]:
        pass

    @abstractmethod
    def listar_prestamos(self, socio_id: int) -> list[PrestamoHistorialResponse]:
        pass

    @abstractmethod
    def actualizar(self, socio_id: int, datos: SocioUpdate) -> SocioResponse:
        pass

    @abstractmethod
    def eliminar(self, socio_id: int) -> None:
        pass
