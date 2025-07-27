from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WeatherIn(BaseModel):
    city: str
    temperature: float
    timestamp: Optional[datetime] = None  # optional, damit er auch leer sein darf

class WeatherOut(WeatherIn):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True