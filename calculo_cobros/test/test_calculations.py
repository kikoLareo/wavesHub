import pytest
from app.services.calculations import SurfFeeCalculator


# Configuraciones iniciales para las pruebas
@pytest.fixture
def calculator():
    position_rates = {
        "director_competicion": 150,
        "delegado": 120,
        "juez": 100
    }
    expenses = {
        "kilometraje": 0.30,
        "manutencion_completa": 50,
        "media_manutencion": 25,
        "alojamiento": 80,
        "refresh": 10,
        "operator": 15
    }
    irpf_rate = 0.15
    return SurfFeeCalculator(position_rates, expenses, irpf_rate)

# Pruebas unitarias para el cálculo de tarifas
def test_calculate_hourly_rate(calculator):
    assert calculator.calculate_hourly_rate(150) == 18.75

def test_calculate_fee_director(calculator):
    fee = calculator.calculate_fee(hours=8, position="director_competicion")
    assert fee == pytest.approx(127.5, 0.1)


def test_calculate_fee_invalid_position(calculator):
    with pytest.raises(ValueError):
        calculator.calculate_fee(hours=8, position="invalid_position")

def test_calculate_fee_negative_hours(calculator):
    with pytest.raises(ValueError):
        calculator.calculate_fee(hours=-5, position="director_competicion")

def test_calculate_expenses(calculator):
    expenses = calculator.calculate_expenses(
        travel_distance_km=150,
        full_meal_days=2,
        half_meal_days=1,
        lodging_days=3
    )
    assert expenses == pytest.approx(410.0, 0.1)


def test_calculate_refresh_cost(calculator):
    cost = calculator.calculate_refresh_cost(refresh_days=2, operator_days=1)
    assert cost == 35
