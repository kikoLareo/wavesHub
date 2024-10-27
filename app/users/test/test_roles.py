from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Configuración de una base de datos en memoria para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
Base.metadata.create_all(bind=engine)

# Dependencia para la base de datos de prueba
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# Fixture de Pytest para inicializar la base de datos antes de cada prueba
@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Prueba de creación de rol
def test_create_role(setup_database):
    response = client.post("/roles/create", json={"name": "admin", "description": "Admin role"})
    assert response.status_code == 200
    assert response.json()["name"] == "admin"

# Prueba de actualización de rol
def test_update_role(setup_database):
    # Crear rol inicial
    create_response = client.post("/roles/create", json={"name": "user", "description": "User role"})
    role_id = create_response.json()["id"]

    # Actualizar rol
    response = client.put(f"/roles/update/{role_id}", json={"description": "Updated User role"})
    assert response.status_code == 200
    assert response.json()["description"] == "Updated User role"

# Prueba de eliminación de rol
def test_delete_role(setup_database):
    # Crear rol inicial
    create_response = client.post("/roles/create", json={"name": "editor", "description": "Editor role"})
    role_id = create_response.json()["id"]

    # Eliminar rol
    response = client.delete(f"/roles/delete/{role_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Rol eliminado exitosamente"}
