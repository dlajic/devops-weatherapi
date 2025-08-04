from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class WeatherIn(BaseModel):
    city: str
    temperature: float
    timestamp: Optional[datetime] = None  # optional, damit er auch leer sein darf


class WeatherOut(WeatherIn):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)
