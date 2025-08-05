#!/bin/bash

# WICHTIG: Datenbank-Init
airflow db migrate

# Admin-User erstellen (nur wenn noch nicht existiert)
airflow users create --username admin --firstname airflow --lastname admin --role Admin --password admin --email admin@example.com || true

# Starte Webserver oder Scheduler
exec airflow "$@"
