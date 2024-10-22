from sqlalchemy import Column, Integer, Float, String
from app.core.database import Base

class PaymentRecord(Base):
    __tablename__ = "payment_records"

    id = Column(Integer, primary_key=True, index=True)
    judge_id = Column(Integer, index=True)
    position = Column(String)
    hours_worked = Column(Float)
    hourly_rate = Column(Float)
    bonus = Column(Float, default=0.0)
    total = Column(Float)
    details = Column(String)
