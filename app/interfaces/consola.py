
from abc import ABC, abstractmethod

from app.schemas.consola import (
    ConsolaCreate,
    ConsolaUpdate,
    ConsolaResponse
)


class IConsolaManager(ABC):

    @abstractmethod
    def crear(self, datos: ConsolaCreate) -> ConsolaResponse:
        pass

    @abstractmethod
    def obtener_por_id(self, consola_id: int) -> ConsolaResponse:
        pass

    @abstractmethod
    def listar(self) -> list[ConsolaResponse]:
        pass

    @abstractmethod
    def actualizar(
        self,
        consola_id: int,
        datos: ConsolaUpdate
    ) -> ConsolaResponse:
        pass

    @abstractmethod
    def eliminar(self, consola_id: int) -> None:
        pass
