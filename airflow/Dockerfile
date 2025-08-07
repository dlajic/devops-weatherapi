FROM apache/airflow:2.8.1-python3.11

COPY airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY airflow/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

COPY airflow/dags/weather_dag.py /opt/airflow/dags/weather_dag.py

# WICHTIG: App-Code aus FastAPI reinpacken!
COPY fastapi-service/app /opt/shared-code/app
ENV PYTHONPATH=/opt/shared-code
