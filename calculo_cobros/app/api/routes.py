from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import CalculationInput, CalculationOutput
from app.services.calculations import calculate_payment
from app.api.deps import get_db

router = APIRouter()

@router.post("/calculate", response_model=CalculationOutput)
async def calculate(data: CalculationInput, db: Session = Depends(get_db)):
    result = calculate_payment(data, db)
    return result
