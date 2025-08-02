# DevOps Weather API – Version 1.0

## Overview

This is the first stable version of the **DevOps Weather API** – a containerized application built with FastAPI (backend) and a static HTML/CSS/JS frontend.

The backend fetches and stores weather data in a PostgreSQL database, and exposes endpoints to query it. The project is fully containerized using **Docker** and runs locally via **Docker Compose**.

---

## 🔄 Current Features (**v1.1**)

- **FastAPI backend** with async PostgreSQL access
- **Modular architecture** for data models, routes & DB handling
- **Script-based weather data fetcher** via Airflow
- **PostgreSQL database container** (auto-created on startup)
- **Daily weather data fetch via Apache Airflow** (scheduled DAG)
- **Simple static frontend** to visualize and download the data
- **Fully containerized setup** (backend, frontend, DB, Airflow)
- **Orchestrated with `docker-compose`**
- **Internal network communication** between services
- **ENV-based config** for DB access & API keys

---

## Roadmap (Next Milestones)

### **v1.2**
- Set up **CI pipeline** via GitLab (.gitlab-ci.yml)
- Add **unit tests** for API & fetcher logic (pytest)
- Push images to **GitLab Container Registry**
- Prepare deployment to **cloud environment** (e.g. EC2, Railway)

### **v1.3**
- Add basic **monitoring & health checks** (e.g. Uptime Kuma, Prometheus)
- Externalize API Key handling (via `.env` or secret manager)
- Auto-deploy via GitLab CI → SSH or Docker Remote

### **v2.x (Advanced Goals)**
- Switch to **managed PostgreSQL** (e.g. Railway)
- Move DAGs to **Dagster** (or enhanced Airflow setup)
- Optional: Deploy to **Kubernetes**
- Add ML component: **temperature trend forecasting**
- API public docs (e.g. via Swagger + custom frontend)

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

```
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
```

## Tech Stack

- **Python 3.11** + **FastAPI**
- **PostgreSQL 15**
- **Docker** + **Docker Compose**
- **HTML/CSS/JavaScript** (Frontend)

## Version History

### v1.0
- FastAPI backend & PostgreSQL DB setup
- Manual weather fetcher logic
- Static frontend + local rendering
- Dockerized backend & DB

### v1.1 *(current)*
- Frontend containerized (Node + http-server)
- Airflow DAG for daily weather fetch added
- Docker-compose for full stack (frontend, backend, Airflow, DB)
- Internal networking + volume config cleaned up