from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.calculations import calculate_payment
from app.schemas.schemas import CalculationInput, CalculationOutput
import uuid

router = APIRouter()

def generate_transaction_id():
    return str(uuid.uuid4())

@router.post("/calculate", response_model=CalculationOutput)
async def calculate(data: CalculationInput, db: Session = Depends(get_db)):
    # Generar un `transaction_id` único para esta solicitud
    transaction_id = generate_transaction_id()
    
    # Pasar `transaction_id` a la función `calculate_payment`
    result = calculate_payment(data, db, transaction_id)
    
    return result
