from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

# Configuración de base de datos de prueba
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Prueba para asignar rol a un usuario
def test_assign_role_to_user(setup_database):
    # Crear usuario y rol
    user_response = client.post("/users/create", json={"name": "test_user", "email": "test@example.com"})
    user_id = user_response.json()["id"]
    role_response = client.post("/roles/create", json={"name": "moderator", "description": "Moderator role"})
    role_id = role_response.json()["id"]

    # Asignar rol
    assign_response = client.post(f"/users/{user_id}/assign-role/{role_id}")
    assert assign_response.status_code == 200
    assert assign_response.json() == {"message": "Rol asignado exitosamente"}

# Prueba para eliminar rol de un usuario
def test_remove_role_from_user(setup_database):
    # Crear usuario y rol
    user_response = client.post("/users/create", json={"name": "test_user2", "email": "test2@example.com"})
    user_id = user_response.json()["id"]
    role_response = client.post("/roles/create", json={"name": "viewer", "description": "Viewer role"})
    role_id = role_response.json()["id"]

    # Asignar rol
    client.post(f"/users/{user_id}/assign-role/{role_id}")

    # Eliminar rol
    remove_response = client.delete(f"/users/{user_id}/remove-role/{role_id}")
    assert remove_response.status_code == 200
    assert remove_response.json() == {"message": "Rol eliminado del usuario"}
