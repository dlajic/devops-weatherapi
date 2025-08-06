FROM apache/airflow:2.8.1-python3.11

# 1. Install requirements
COPY ../airflow/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# 2. Set entrypoint
COPY ../airflow/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# 3. DAGs + Shared Code
COPY ../airflow/dags /opt/airflow/dags
COPY ../fastapi-service/app /opt/shared-code/app

# 4. PYTHONPATH für DAG-Imports
ENV PYTHONPATH=/opt/shared-code

