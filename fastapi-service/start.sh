#!/bin/bash
set -e

echo "Waiting for PostgreSQL to become available...."
until pg_isready -h db -p 5432 -U weather; do
  sleep 1
done

echo "PostgreSQL is available, proceeding..."
python -m app.create_db
uvicorn app.main:app --host 0.0.0.0 --port 8000