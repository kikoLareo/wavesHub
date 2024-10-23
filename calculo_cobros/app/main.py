from fastapi import FastAPI, Request
from app.api.routes import router
from app.models.Base import Base
from app.core.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.utils.helpers import generate_transaction_id  # Importar la función que generamos
import logging
from app.core.logging_config import setup_logging

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

setup_logging()

app = FastAPI(title="WavesHub - Cálculo de Cobros")


# Configuración del Logger
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Middleware para generar el ID de transacción
@app.middleware("http")
async def add_transaction_id(request: Request, call_next):
    transaction_id = generate_transaction_id()  # Generar un ID único
    request.state.transaction_id = transaction_id  # Guardarlo en el estado de la request

    # Registrar el inicio de la solicitud con el ID
    logger.info("Iniciando solicitud", extra={"transaction_id": transaction_id})
    
    # Pasar el ID a la respuesta y a los logs
    response = await call_next(request)
    response.headers["X-Transaction-ID"] = transaction_id  # Añadir el ID a la respuesta para seguimiento
    return response

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")
