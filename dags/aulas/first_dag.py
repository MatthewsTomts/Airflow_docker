from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    dag_id='first_dag',
    default_args=default_args,
    description='The first airflow dag that I wrote!!',
    start_date=datetime(2021, 7, 29, 2),
    schedule='@daily'
) as dag:
    task1 = BashOperator(
        task_id='first_task',
        bash_command='echo hello world, this is my 1° task!'
    ) 

    task2 = BashOperator(
        task_id='second_task',
        bash_command="echo I am the second task, and I run after the first"
    )

    task3 = BashOperator(
        task_id='third_task',
        bash_command='echo I am task three and I run with task two after task one'
    )

    # task Dependency method 1
    #task1.set_downstream(task2)
    #task1.set_downstream(task3)

    # task dependency method 2
    #task1 >> task2
    #task1 >> task3

    # task dependency method 3
    task1 >> [task2, task3]



