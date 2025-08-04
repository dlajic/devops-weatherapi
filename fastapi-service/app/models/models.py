from sqlalchemy import Column, Integer, String, DateTime, Float
from app.db.database import Base
from datetime import datetime


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(String(255))


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String, index=True)
    temperature = Column(Float)
    humidity = Column(Integer)
    timestamp = Column(DateTime, default=datetime.utcnow)
