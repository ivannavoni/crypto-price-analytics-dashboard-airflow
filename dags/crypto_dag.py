from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.append('/opt/airflow/scripts')
from etl import run_etl

default_args = {
    "owner": "Ivan",
    "depends_on_past": False,
    "start_date": datetime(2025, 2, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

dag = DAG(
    "crypto_etl_pipeline",
    default_args=default_args,
    description="ETL pipeline for crypto prices",
    schedule_interval="0 */6 * * *",  # Every 6 hours
    catchup=True
)

etl_task = PythonOperator(
    task_id="extract_data_and_load_to_SQL",
    python_callable=run_etl,
    dag=dag
)