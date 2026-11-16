
from abc import ABC, abstractmethod
from app.schemas.juego import JuegoFichaResponse

class IJuegoManager(ABC):

    @abstractmethod
    def listar(self):
        pass

    @abstractmethod
    def obtener_por_id(self, juego_id: int):
        pass

    @abstractmethod
    def crear(self, datos):
        pass

    @abstractmethod
    def actualizar(self, juego_id: int, datos):
        pass

    @abstractmethod
    def eliminar(self, juego_id: int):
        pass

    @abstractmethod
    def filtrar(
        self,
        titulo=None,
        genero_id=None,
        consola_id=None,
        desarrolladora_id=None,
        anio_desde=None,
        anio_hasta=None,
        clasificacion_edad=None
    ):
        pass

    @abstractmethod
    def listar_por_desarrolladora(self, desarrolladora_id: int):
        pass

    @abstractmethod
    def listar_consolas(self, juego_id: int):
        pass

    @abstractmethod
    def listar_por_consola(self, consola_id: int):
        pass

    @abstractmethod
    def listar_generos(self, juego_id: int):
        pass

    @abstractmethod
    def listar_por_genero(self, genero_id: int):
        pass
    @abstractmethod
    def obtener_ficha_completa(self, juego_id: int) -> JuegoFichaResponse:
        pass