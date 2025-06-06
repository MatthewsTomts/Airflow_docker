from airflow.decorators import dag
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    dag_id='dag_with_cron_expression_v4',
    default_args=default_args,
    start_date=datetime(2025,5,2),
    schedule='30 3 * * Thu,Mon',
    catchup=True
)
def dag_with_cron_expression():
    task1 = BashOperator(
        task_id='task1',
        bash_command='echo dag with cron expression!!'
    )

    task1

dag_with_cron_expression()
