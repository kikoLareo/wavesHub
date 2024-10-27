from fastapi import FastAPI
from app.routes import roles, user_roles

app = FastAPI()

# Registrar rutas
app.include_router(roles.router)
app.include_router(user_roles.router)
