from sqlalchemy.orm import Session
from app.models.models import PaymentRecord
from app.schemas.schemas import CalculationInput, CalculationOutput
import logging
from fastapi import HTTPException


# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - [ID: %(thread)d] - %(message)s'
)
logger = logging.getLogger(__name__)

class SurfFeeCalculator:
    def __init__(self, position_rates, expenses, irpf_rate):
        self.position_rates = position_rates
        self.expenses = expenses
        self.irpf_rate = irpf_rate
        logger.info(f"Inicializando SurfFeeCalculator con IRPF: {irpf_rate}")

    def calculate_hourly_rate(self, daily_rate):
        hourly_rate = daily_rate / 8
        logger.info(f"Tarifa por hora calculada: {hourly_rate:.2f}")
        return hourly_rate

    def calculate_fee(self, hours, position):
        if position not in self.position_rates:
            logger.error(f"Puesto {position} no válido.")
            raise ValueError(f"Puesto {position} no válido.")
        if hours < 0:
            logger.error(f"Número de horas no puede ser negativo: {hours}")
            raise ValueError(f"Número de horas no puede ser negativo: {hours}")

        daily_rate = self.position_rates[position]
        hourly_rate = self.calculate_hourly_rate(daily_rate)
        fee_before_irpf = hourly_rate * hours
        fee_after_irpf = fee_before_irpf * (1 - self.irpf_rate)
        logger.info(f"Tarifa calculada para {position}: {fee_after_irpf:.2f} € después de IRPF")
        return fee_after_irpf

    def calculate_expenses(self, travel_distance_km, full_meal_days, half_meal_days, lodging_days):
        travel_cost = travel_distance_km * self.expenses['kilometraje']
        meal_cost = (full_meal_days * self.expenses['manutencion_completa']) + (half_meal_days * self.expenses['media_manutencion'])
        lodging_cost = lodging_days * self.expenses['alojamiento']

        total_expenses = travel_cost + meal_cost + lodging_cost
        logger.info(f"Gastos adicionales calculados: {total_expenses:.2f} €")
        return total_expenses

    def calculate_refresh_cost(self, refresh_days, operator_days):
        refresh_cost = refresh_days * self.expenses['refresh']
        operator_cost = operator_days * self.expenses['operator']
        total_refresh_cost = refresh_cost + operator_cost
        logger.info(f"Costos del sistema Refresh calculados: {total_refresh_cost:.2f} €")
        return total_refresh_cost

def calculate_payment(data: CalculationInput, db: Session) -> CalculationOutput:
    # Configurar tarifas y gastos
    position_rates = {
        'director_competicion': 150.0,
        'delegado': 120.0,
        'juez': 100.0,
        'tabulator': 80.0,
        # Añade más posiciones si es necesario
    }

    expenses = {
        'kilometraje': 0.19,  # Por km
        'manutencion_completa': 37.4,  # Por día
        'media_manutencion': 18.7,  # Por día
        'alojamiento': 65.97,  # Por día
        'refresh': 60.0,  # Por día
        'operator': 80.0,  # Por día
    }

    irpf_rate = 0.15  # Tasa de IRPF del 15%

    calculator = SurfFeeCalculator(position_rates, expenses, irpf_rate)

    try:
        # Calcular tarifa después de IRPF
        fee_after_irpf = calculator.calculate_fee(data.hours, data.position)

        # Calcular gastos adicionales
        total_expenses = calculator.calculate_expenses(
            data.travel_distance_km,
            data.full_meal_days,
            data.half_meal_days,
            data.lodging_days
        )

        # Calcular costos del sistema Refresh
        total_refresh_cost = calculator.calculate_refresh_cost(
            data.refresh_days,
            data.operator_days
        )

        # Calcular el monto total
        total_amount = fee_after_irpf + total_expenses + total_refresh_cost

        # Detalles del cálculo
        details = (
            f"Tarifa después de IRPF: {fee_after_irpf:.2f} €, "
            f"Gastos adicionales: {total_expenses:.2f} €, "
            f"Costos de Refresh: {total_refresh_cost:.2f} €, "
            f"Total: {total_amount:.2f} €"
        )

        # Guardar en la base de datos
        payment_record = PaymentRecord(
            judge_id=data.judge_id,
            position=data.position,
            hours_worked=data.hours,
            hourly_rate=fee_after_irpf / data.hours if data.hours > 0 else 0,
            bonus=total_expenses + total_refresh_cost,
            total=total_amount,
            details=details
        )

        db.add(payment_record)
        db.commit()
        db.refresh(payment_record)

        return CalculationOutput(
            fee_after_irpf=fee_after_irpf,
            total_expenses=total_expenses,
            total_refresh_cost=total_refresh_cost,
            total_amount=total_amount,
            details=details
        )
    
    except ValueError as e:
        # Captura errores específicos, como posición no válida
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        # Captura cualquier otro error que pueda ocurrir
        db.rollback()  # Revertir la transacción si hay un error
        raise HTTPException(status_code=500, detail="Error interno del servidor")
