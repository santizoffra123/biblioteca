from abc import ABC, abstractmethod

from app.schemas.genero import (
    GeneroCreate,
    GeneroUpdate,
    GeneroResponse
)


class IGeneroManager(ABC):

    @abstractmethod
    def crear(self, datos: GeneroCreate) -> GeneroResponse:
        pass

    @abstractmethod
    def obtener_por_id(self, genero_id: int) -> GeneroResponse:
        pass

    @abstractmethod
    def listar(self) -> list[GeneroResponse]:
        pass

    @abstractmethod
    def actualizar(
        self,
        genero_id: int,
        datos: GeneroUpdate
    ) -> GeneroResponse:
        pass

    @abstractmethod
    def eliminar(self, genero_id: int) -> None:
        pass