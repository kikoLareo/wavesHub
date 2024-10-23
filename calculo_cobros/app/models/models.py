# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from app.core.database import Base

# class PaymentRecord(Base):
#     __tablename__ = "payment_records"

#     id = Column(Integer, primary_key=True, index=True)
#     judge_id = Column(Integer, ForeignKey("judges.id"))
#     championship_id = Column(Integer, ForeignKey("championships.id"))
#     position = Column(String)
#     hours_worked = Column(Float)
#     hourly_rate = Column(Float)
#     bonus = Column(Float)
#     total = Column(Float)
#     details = Column(String)

#     judge = relationship("Judge", back_populates="payments")
#     championship = relationship("Championship", back_populates="payments")

# class Judge(Base):
#     __tablename__ = "judges"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     email = Column(String, unique=True, index=True)
#     position = Column(String)

#     payments = relationship("PaymentRecord", back_populates="judge")

# class Championship(Base):
#     __tablename__ = "championships"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     location = Column(String)
#     date = Column(String)

#     payments = relationship("PaymentRecord", back_populates="championship")

# class PositionRate(Base):
#     __tablename__ = "position_rates"

#     id = Column(Integer, primary_key=True, index=True)
#     position = Column(String, unique=True)
#     daily_rate = Column(Float)
