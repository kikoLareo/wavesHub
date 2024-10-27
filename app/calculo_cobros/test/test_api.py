from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_calculate_endpoint_success():
    response = client.post("/api/calculate", json={
        "judge_id": 1,
        "championship_id": 1,
        "position": "director_competicion",
        "hours": 8,
        "travel_distance_km": 150,
        "full_meal_days": 2,
        "half_meal_days": 1,
        "lodging_days": 3,
        "refresh_days": 1,
        "operator_days": 2
    })
    assert response.status_code == 200
    result = response.json()
    assert "total_amount" in result
    assert result["total_amount"] > 0


def test_calculate_endpoint_invalid_position():
    response = client.post("/api/calculate", json={
        "judge_id": 1,
        "championship_id": 1,
        "position": "invalid_position",
        "hours": 8,
        "travel_distance_km": 150,
        "full_meal_days": 2,
        "half_meal_days": 1,
        "lodging_days": 3,
        "refresh_days": 1,
        "operator_days": 2
    })
    assert response.status_code == 400
    assert response.json()["detail"] == "Puesto invalid_position no válido."

def test_calculate_endpoint_missing_fields():
    response = client.post("/api/calculate", json={
        "position": "director_competicion"
        # Faltan campos como 'hours'
    })
    assert response.status_code == 422  # Error de validación
