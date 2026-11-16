from abc import ABC, abstractmethod

from app.schemas.desarrolladora import (
    DesarrolladoraCreate,
    DesarrolladoraUpdate,
    DesarrolladoraResponse
)


class IDesarrolladoraManager(ABC):

    @abstractmethod
    def crear(self, datos: DesarrolladoraCreate) -> DesarrolladoraResponse:
        pass

    @abstractmethod
    def obtener_por_id(self, desarrolladora_id: int) -> DesarrolladoraResponse:
        pass

    @abstractmethod
    def listar(self) -> list[DesarrolladoraResponse]:
        pass

    @abstractmethod
    def actualizar(
        self,
        desarrolladora_id: int,
        datos: DesarrolladoraUpdate
    ) -> DesarrolladoraResponse:
        pass

    @abstractmethod
    def eliminar(self, desarrolladora_id: int) -> None:
        pass