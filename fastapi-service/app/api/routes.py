from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy import func
import httpx
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO

from app.models.models import WeatherData
from app.db.database import get_db
from app.models import models
from app.api import schemas

router = APIRouter()

OPENWEATHER_API_KEY = "fb085c2dc735b55fe30a4f099834db37"


# Alle Wetterdaten abrufen/ optinal mit Stadt/Zeitfilter
@router.get("/weather", response_model=List[schemas.WeatherOut])
def get_weather(
    city: Optional[str] = None,
    date: Optional[datetime] = Query(None, description="Format: YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    query = db.query(models.WeatherData)

    if city:
        query = query.filter(models.WeatherData.city == city)

    if date:
        query = query.filter(
            models.WeatherData.timestamp >= date,
            models.WeatherData.timestamp < date + timedelta(days=1),
        )

    return query.all()


# Neue Wetterdaten speichern
@router.post("/weather", response_model=schemas.WeatherOut)
def create_weather_entry(data: schemas.WeatherIn, db: Session = Depends(get_db)):
    new_entry = WeatherData(
        city=data.city,
        temperature=data.temperature,
        timestamp=data.timestamp
        or datetime.utcnow(),  # fallback auf "jetzt", falls leer
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


# Eintrag löschen
@router.delete("/weather/{id}")
def delete_weather(id: int, db: Session = Depends(get_db)):
    entry = db.query(models.WeatherData).filter(models.WeatherData.id == id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Wetterdaten nicht gefunden.")
    db.delete(entry)
    db.commit()
    return {"message": f"Wetterdaten mit ID {id} wurden gelöscht."}


# get live weather from openweather api
@router.post("/weather/live/{city}", response_model=schemas.WeatherOut)
async def fetch_and_store_weather(city: str, db: Session = Depends(get_db)):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Stadt nicht gefunden")

    data = await response.json()
    new_entry = models.WeatherData(
        city=city, temperature=data["main"]["temp"], humidity=data["main"]["humidity"]
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


# ------------- frontend --------------


# get all dates in dataset for frontend
@router.get("/weather/dates", response_model=List[str])
def get_available_dates(db: Session = Depends(get_db)):
    dates = (
        db.query(func.date(models.WeatherData.timestamp))
        .distinct()
        .order_by(func.date(models.WeatherData.timestamp))
        .all()
    )
    return [str(d[0]) for d in dates]


# for range date
@router.get("/weather/range", response_model=List[schemas.WeatherOut])
def get_weather_range(
    from_date: datetime = Query(..., description="Startdatum (YYYY-MM-DD)"),
    to_date: datetime = Query(..., description="Enddatum (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.WeatherData)
        .filter(
            models.WeatherData.timestamp >= from_date,
            models.WeatherData.timestamp < to_date + timedelta(days=1),
        )
        .order_by(models.WeatherData.timestamp.asc())
        .all()
    )


# download option
@router.get("/weather/download_excel")
def download_weather_excel(
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    db: Session = Depends(get_db),
):
    data = (
        db.query(models.WeatherData)
        .filter(
            models.WeatherData.timestamp >= from_date,
            models.WeatherData.timestamp < to_date + timedelta(days=1),
        )
        .order_by(models.WeatherData.timestamp.asc(), models.WeatherData.city.asc())
    )

    if not data:
        raise HTTPException(status_code=404, detail="Keine Daten vorhanden.")

    sorted_data = sorted(
        data,
        key=lambda d: (
            d.timestamp.replace(microsecond=0),  # runde auf Sekunde
            d.city.lower(),  # alphabetisch nach Stadt
        ),
    )

    # Umwandeln in DataFrame
    df = pd.DataFrame(
        [
            {
                "Zeitpunkt": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "Stadt": entry.city,
                "Temperatur (°C)": round(entry.temperature, 2),
            }
            for entry in sorted_data
        ]
    )

    # Excel-Datei in Memory schreiben
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Wetterdaten")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=wetterdaten.xlsx"},
    )


# Vorschau Daten


@router.get("/weather/preview")
def preview_weather_data(
    from_date: datetime = Query(...),
    to_date: datetime = Query(...),
    db: Session = Depends(get_db),
):
    data = (
        db.query(models.WeatherData)
        .filter(
            models.WeatherData.timestamp >= from_date,
            models.WeatherData.timestamp < to_date + timedelta(days=1),
        )
        .order_by(models.WeatherData.timestamp.asc(), models.WeatherData.city.asc())
        .all()
    )

    preview_count = 5
    if len(data) <= 10:
        preview = data
    else:
        preview = data[:preview_count] + data[-preview_count:]

    return [
        {
            "timestamp": entry.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "city": entry.city,
            "temperature": round(entry.temperature, 2),
        }
        for entry in preview
    ]
