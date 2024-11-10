from BD.routers import users_role
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
import logging
from app.logging_config import setup_logging
from app.calculo_cobros.app.routes.routes import router as calculo_router
from BD.routers import roles


def generate_transaction_id():
    return str(uuid.uuid4())


# Configurar logging
setup_logging()
logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Crear las tablas en la base de datos (opcional, solo en entornos de desarrollo)
Base.metadata.create_all(bind=engine)

# Crear la aplicación de FastAPI
app = FastAPI()

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permitir solicitudes desde React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Incluir las rutas con prefijos
app.include_router(calculo_router, prefix="/api/calculo_cobros")
app.include_router(roles.router, prefix="/api/roles")
app.include_router(users_role.router, prefix="/api/user_roles")
