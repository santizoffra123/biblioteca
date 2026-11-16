
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import BibliotecaException

from app.routers import (
    desarrolladora,
    consola,
    genero,
    juego,
    ejemplar,
    socio,
    prestamo
)


app = FastAPI(
    title="Biblioteca Retro",
    description="API REST para gestionar una biblioteca comunitaria de videojuegos retro",
    version="1.0.0"
)


@app.exception_handler(BibliotecaException)
async def manejar_excepciones(
    request: Request,
    exc: BibliotecaException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.mensaje}
    )


app.include_router(desarrolladora.router)
app.include_router(consola.router)
app.include_router(genero.router)
app.include_router(juego.router)
app.include_router(ejemplar.router)
app.include_router(socio.router)
app.include_router(prestamo.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a Biblioteca Retro",
        "estado": "Funcionando correctamente",
        "documentacion": "/docs"
    }
