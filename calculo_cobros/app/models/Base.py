from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

# Definir `Base` correctamente
class Base(DeclarativeBase):
    pass
# Ejemplos de Modelos utilizando `Base`
class Judge(Base):
    __tablename__ = "judges"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    position = Column(String)
    payments = relationship("PaymentRecord", back_populates="judge")

class PaymentRecord(Base):
    __tablename__ = "payment_records"
    id = Column(Integer, primary_key=True, index=True)
    judge_id = Column(Integer, ForeignKey("judges.id"))
    position = Column(String)
    hours_worked = Column(Float)
    total = Column(Float)
    details = Column(String)
    judge = relationship("Judge", back_populates="payments")
