import sys
sys.path.append("/opt/shared-code")

from app.fetch_weather_daily import main as run  # <- jetzt klappt der Import

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def run_sync():
    import asyncio
    asyncio.run(run())

with DAG(
    dag_id="fetch_weather_daily",
    start_date=datetime(2025, 1, 1),
    schedule_interval="0 12 * * *",
    catchup=False,
) as dag:
    task = PythonOperator(
        task_id="run_weather_fetch",
        python_callable=run_sync,
    )
