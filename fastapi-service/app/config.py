# app/config.py
import os

# mir fallback, über docker wird env gesetzt, falls lokal gestartet lege neu an
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://weather:weather123@db:5432/weatherdb"
)
