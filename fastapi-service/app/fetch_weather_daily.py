import asyncio
import httpx
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.models import models
from datetime import datetime

API_KEY = "fb085c2dc735b55fe30a4f099834db37"

# Alle Landeshauptstädte
STÄDTE = [
    "Berlin", "Potsdam", "Schwerin", "Dresden", "Erfurt", "Magdeburg",
    "Hannover", "Kiel", "Hamburg", "Bremen", "Düsseldorf", "Mainz",
    "Wiesbaden", "Stuttgart", "München", "Saarbrücken",
]


async def fetch_city_weather(city: str, db: Session):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code == 200:
        data = response.json()  # <<< HIER: KEIN await
        entry = models.WeatherData(
            city=city,
            temperature=data["main"]["temp"],
            humidity=data["main"]["humidity"],
            timestamp=datetime.utcnow(),
        )
        db.add(entry)
        db.commit()
        db.refresh(entry)
        print(f"Gespeichert: {city} – {entry.temperature}°C")


async def main():
    db = SessionLocal()
    tasks = [fetch_city_weather(city, db) for city in STÄDTE]
    await asyncio.gather(*tasks)
    db.close()


if __name__ == "__main__":
    asyncio.run(main())
