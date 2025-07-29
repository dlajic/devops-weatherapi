# DevOps Weather API – Version 1.0

## Overview

This is the first stable version of the **DevOps Weather API** – a containerized application built with FastAPI (backend) and a static HTML/CSS/JS frontend.

The backend fetches and stores weather data in a PostgreSQL database, and exposes endpoints to query it. The project is fully containerized using **Docker** and runs locally via **Docker Compose**.

---

## Current Features (v1.0)

- **FastAPI backend** with async PostgreSQL access
- **Modular architecture** for data models, routes & DB handling
- **Script-based weather data fetcher**
- **PostgreSQL database container** (auto-created on startup)
- **Daily weather data fetch manually triggerable**
- **Simple static frontend** to visualize the data
- **Dockerized backend + DB** (via `docker-compose`)

---

## Roadmap (Next Milestones)

### v1.1
- Containerize the **frontend**
- Integrate a **daily automated scheduler** for weather fetching (e.g. `cron` or `Airflow` inside Docker)
- Improve error handling and logging

### v1.2+
- Move deployment to **cloud environment** (Render, Railway, etc.)
- CI/CD pipeline setup via **GitLab**
- Add basic monitoring & health checks

### v2.x (Advanced)
- Switch to **managed cloud services** (e.g. PostgreSQL on Railway)
- Integrate **Airflow** or **Dagster** for orchestration
- Deploy via **Kubernetes** (optional advanced deployment)

---

## How to Run (Development)

```bash
# Build and start the containers
docker compose up --build

# Stop all containers
docker compose down
```

Then open your browser at: http://localhost:8000

## Project Structure

devops-weatherapi/
│
├── fastapi-service/ # Backend API (FastAPI)
│ ├── app/ # Main application code
│ ├── Dockerfile # Backend Docker build
│ └── start.sh # Startup script
│
├── frontend/ # Static frontend (to be containerized)
│ └── index.html
│
├── docker-compose.yml # Compose config for backend + PostgreSQL
└── README.md


## Tech Stack

- **Python 3.11** + **FastAPI**
- **PostgreSQL 15**
- **Docker** + **Docker Compose**
- **HTML/CSS/JavaScript** (Frontend)