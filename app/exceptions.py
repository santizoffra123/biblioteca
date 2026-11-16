class BibliotecaException(Exception):
    def __init__(self, mensaje: str, status_code: int):
        self.mensaje = mensaje
        self.status_code = status_code


class RecursoNoEncontrado(BibliotecaException):
    def __init__(self, mensaje: str):
        super().__init__(mensaje, 404)


class Conflicto(BibliotecaException):
    def __init__(self, mensaje: str):
        super().__init__(mensaje, 409)


class DatosInvalidos(BibliotecaException):
    def __init__(self, mensaje: str):
        super().__init__(mensaje, 422)