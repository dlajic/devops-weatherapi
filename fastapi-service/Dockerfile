FROM python:3.11-slim

# Install PostgreSQL client tools (incl. pg_isready)
RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

# Arbeitsverzeichnis im container setzen
WORKDIR /fastapi-service

# requirements installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# gesamten Code in den Container kopieren
COPY . .
EXPOSE 8000

# starte start.sh
RUN chmod +x start.sh

# App starten
CMD ["./start.sh"]
