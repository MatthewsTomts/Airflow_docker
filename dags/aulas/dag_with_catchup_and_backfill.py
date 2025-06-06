from airflow.decorators import dag
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    dag_id = 'dag_with_catchup_backfill_v1',
    default_args=default_args,
    start_date=datetime(2025,5,2),
    schedule='@daily',
    catchup=True
)
def catchup():
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo This is a simple bash command'
    )

    task1

catchup()
