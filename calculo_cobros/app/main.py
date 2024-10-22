from fastapi import FastAPI
from app.api.routes import router
from app.models import models
from app.core.database import engine

# Crear las tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="WavesHub - Cálculo de Cobros")

app.include_router(router, prefix="/api")
