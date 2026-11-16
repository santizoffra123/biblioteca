
from abc import ABC, abstractmethod


class IEjemplarManager(ABC):

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def obtener_por_id(self, ejemplar_id: int):
        pass

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def filtrar(
        self,
        juego_id=None,
        consola_id=None,
        estado_conservacion=None,
        disponible=None
    ):
        pass

    @abstractmethod
    def listar_por_juego(self, juego_id: int):
        pass

    @abstractmethod
    def actualizar(self, ejemplar_id: int, datos):
        pass

    @abstractmethod
    def eliminar(self, ejemplar_id: int):
        pass
