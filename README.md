# 🌦 DevOps Weather API – Full CI/CD Data Pipeline

## Overview

**DevOps Weather API** is a fully containerized **DevOps showcase project** that demonstrates the complete lifecycle of a weather-based data platform from **data ingestion** to **automated cloud deployment**.

The project implements modern DevOps practices in a production-like architecture:

- **Daily weather data ingestion** via scheduled workflows (Apache Airflow)
- **Persistent storage** in a PostgreSQL database
- **API exposure** through a FastAPI backend service
- **Data visualization** via a static frontend
- **Containerized infrastructure** with Docker & Docker Compose
- **CI/CD pipeline** with GitLab for automated deployment to AWS EC2
- **Infrastructure-as-Code** principles for reproducible deployments

**🌍 Live Demo:** [https://devops-weatherapi.dev](https://devops-weatherapi.dev)  
*The application is permanently online, hosted on a cloud instance, and fetches fresh weather data daily via automated pipelines.*

---

## 🚀 Features

- **FastAPI Backend**
  - Asynchronous endpoints
  - PostgreSQL integration
  - Automatic loading of new data
- **Frontend (HTML/CSS/JavaScript)**
  - Displays current weather data
  - Data download option
- **Apache Airflow**
  - Scheduled DAG for daily data ingestion
  - Easily extendable for complex workflows
- **PostgreSQL**
  - Persistent weather data storage
  - Automatic schema initialization
- **Dockerized Setup**
  - Separate containers for backend, frontend, DB, and Airflow
  - Unified internal network configuration
- **GitLab CI/CD**
  - Automatic deployment on push to `main`
  - SSH-based rollout using `docker compose up -d --build`
- **Security**
  - Key-based SSH authentication
  - Restricted access to admin services

---

## Project Structure

```
devops-weatherapi/
│
├── fastapi-service/              # Backend API (FastAPI)
│   ├── app/                      # Application logic: routes, DB models, fetchers
│   ├── Dockerfile                # Backend Docker image
│   └── requirements.txt          # Python dependencies
│
├── frontend/                     # Static frontend (HTML/CSS/JS)
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── Dockerfile                # Frontend container (Node + http-server)
│
├── airflow/                      # Airflow scheduler (DAG for weather fetch)
│   ├── dags/                     # Contains Airflow DAG definition
│   ├── Dockerfile                # Airflow image with dependencies
│   ├── entrypoint.sh             # Entrypoint for init
│   └── requirements.txt
│
├── docker-compose.yml            # Orchestration of all services
├── .env                          # Environment variables (DB URL, API keys etc.)
└── README.md
```

---

## 🛠 Tech Stack

- **Python 3.11** – Backend & automation scripts  
- **FastAPI** – API framework  
- **PostgreSQL 15** – Relational database  
- **Apache Airflow** – Workflow orchestration  
- **Docker & Docker Compose** – Containerization & service orchestration  
- **Node.js + http-server** – Frontend delivery  
- **HTML/CSS/JavaScript** – Static UI  

---

## Local Development

If you want to run the project locally instead of using the live instance:

```bash
# Build and start the containers
docker compose up --build

# Stop all containers
docker compose down
```
Once running, access:

Backend API: http://localhost:8000
Frontend: http://localhost:3000