from pydantic import BaseModel, Field
from typing import Optional

class CalculationInput(BaseModel):
    judge_id: int = Field(..., gt=0)
    position: str
    hours: float = Field(..., gt=0)
    travel_distance_km: Optional[float] = 0.0
    full_meal_days: Optional[int] = 0
    half_meal_days: Optional[int] = 0
    lodging_days: Optional[int] = 0
    refresh_days: Optional[int] = 0
    operator_days: Optional[int] = 0

class CalculationOutput(BaseModel):
    fee_after_irpf: float
    total_expenses: float
    total_refresh_cost: float
    total_amount: float
    details: str
