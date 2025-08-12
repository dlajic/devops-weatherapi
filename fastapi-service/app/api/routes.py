from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import httpx
import pytz
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO

from app.models.models import WeatherData
from app.db.database import get_db
from app.models import models
from app.api import schemas

router = APIRouter()

OPENWEATHER_API_KEY = "fb085c2dc735b55fe30a4f099834db37"

# UTC -> Europe/Berlin (für Ausgabe)
def to_berlin_time(ts: datetime) -> datetime:
    if ts.tzinfo is None:  # naive UTC
        ts = ts.replace(tzinfo=pytz.UTC)
    return ts.astimezone(pytz.timezone("Europe/Berlin"))


# -------------------------------------
# API: Wetterdaten
# -------------------------------------

# Alle Wetterdaten abrufen (optional Filter) – Ausgabezeit in Berlin
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

    data = query.all()
    # Zeit vor Rückgabe nach Europe/Berlin konvertieren
    for w in data:
        if w.timestamp is not None:
            w.timestamp = to_berlin_time(w.timestamp)
    return data


# Neuen Messpunkt speichern (Speicherung in UTC)
@router.post("/weather", response_model=schemas.WeatherOut)
def create_weather_entry(data: schemas.WeatherIn, db: Session = Depends(get_db)):
    new_entry = WeatherData(
        city=data.city,
        temperature=data.temperature,
        humidity=getattr(data, "humidity", None),
        timestamp=data.timestamp or datetime.utcnow(),  # UTC speichern
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    # Ausgabezeit auf Berlin drehen (nur Response)
    if new_entry.timestamp is not None:
        new_entry.timestamp = to_berlin_time(new_entry.timestamp)
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


# Live-Wetter holen & speichern (UTC speichern)
@router.post("/weather/live/{city}", response_model=schemas.WeatherOut)
async def fetch_and_store_weather(city: str, db: Session = Depends(get_db)):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Stadt nicht gefunden")

    data = response.json()
    new_entry = models.WeatherData(
        city=city,
        temperature=data["main"]["temp"],
        humidity=data["main"]["humidity"],
        timestamp=datetime.utcnow(),  # UTC
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    # Ausgabezeit auf Berlin drehen
    new_entry.timestamp = to_berlin_time(new_entry.timestamp)
    return new_entry


# -------------------------------------
# Endpunkte fürs Frontend
# -------------------------------------

# Verfügbare Tage – nach Berlin-Zeit gruppieren (statt UTC)
@router.get("/weather/dates", response_model=List[str])
def get_available_dates(db: Session = Depends(get_db)):
    # Alle Timestamps holen und lokal auf Tag mappen
    raw = db.query(models.WeatherData.timestamp).all()
    berlin_dates = sorted({to_berlin_time(t[0]).date() for t in raw})
    return [str(d) for d in berlin_dates]


# Bereichsabfrage – Ausgabezeit in Berlin
@router.get("/weather/range", response_model=List[schemas.WeatherOut])
def get_weather_range(
    from_date: datetime = Query(..., description="Startdatum (YYYY-MM-DD)"),
    to_date: datetime = Query(..., description="Enddatum (YYYY-MM-DD)"),
    db: Session = Depends(get_db),
):
    data = (
        db.query(models.WeatherData)
        .filter(
            models.WeatherData.timestamp >= from_date,
            models.WeatherData.timestamp < to_date + timedelta(days=1),
        )
        .order_by(models.WeatherData.timestamp.asc())
        .all()
    )
    for w in data:
        if w.timestamp is not None:
            w.timestamp = to_berlin_time(w.timestamp)
    return data


# Excel-Download – Zeitspalte in Berlin
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
        .all()
    )

    if not data:
        raise HTTPException(status_code=404, detail="Keine Daten vorhanden.")

    sorted_data = sorted(
        data,
        key=lambda d: (
            to_berlin_time(d.timestamp).replace(microsecond=0) if d.timestamp else datetime.min,
            d.city.lower(),
        ),
    )

    df = pd.DataFrame(
        [
            {
                "Zeitpunkt": to_berlin_time(entry.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
                "Stadt": entry.city,
                "Temperatur (°C)": round(entry.temperature, 2),
            }
            for entry in sorted_data
        ]
    )

    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Wetterdaten")
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=wetterdaten.xlsx"},
    )


# Vorschau – Zeiten in Berlin
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
            "timestamp": to_berlin_time(entry.timestamp).strftime("%Y-%m-%d %H:%M:%S"),
            "city": entry.city,
            "temperature": round(entry.temperature, 2),
        }
        for entry in preview
    ]
