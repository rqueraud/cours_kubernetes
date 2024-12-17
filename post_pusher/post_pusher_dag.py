from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Définir le DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

with DAG(
    'post_pusher_dag',
    default_args=default_args,
    description='Run post_pusher regularly',
    schedule_interval='*/1 * * * *',  # Exécution toutes les minutes
    start_date=datetime(2024, 12, 15),
    catchup=False,
) as dag:

    # Tâche pour exécuter post_pusher
    run_post_pusher = BashOperator(
        task_id='run_post_pusher',
        bash_command='kubectl exec -n app deployment/post-pusher -- ./run_post_pusher.sh'
    )
