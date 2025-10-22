from sqlalchemy import Column, Integer, String, Date, Float, DateTime, func, Index
from database.database import Base

class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String(100), index=True)
    vehicle_model = Column(String(100), index=True)
    units_sold = Column(Integer, nullable=False)
    booking_count = Column(Integer, nullable=True)
    delivery_time = Column(Float, nullable=True)
    dealer_rating = Column(Float, nullable=True)
    date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

Index('ix_sales_region_model_date', Sales.region, Sales.vehicle_model, Sales.date)
