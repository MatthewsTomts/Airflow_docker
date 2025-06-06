from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

def greet(year, ti):
    first_name = ti.xcom_pull(task_ids='get_name', key='first_name')
    last_name = ti.xcom_pull(task_ids='get_name', key='last_name')
    age = ti.xcom_pull(task_ids='get_age', key='age')
    print(f'Hello World!! My name is {first_name} {last_name} and I\'m {age} years old, I was born at {year}')

def get_name(ti):
    ti.xcom_push(key='first_name', value='Violet')
    ti.xcom_push(key='last_name', value='Vohor')

def get_age(ti):
    ti.xcom_push(key='age', value=32)

with DAG(
    dag_id='dag_with_python_operator',
    default_args=default_args,
    description='This is my first dag with python operators',
    start_date=datetime(2021, 7, 29),
    schedule='@daily'
) as dag:
    task1 = PythonOperator(
        task_id='greet',
        python_callable=greet,
        op_kwargs={'year':1993}
    )

    task2 = PythonOperator(
        task_id='get_name',
        python_callable=get_name
    )

    task3 = PythonOperator(
        task_id = 'get_age',
        python_callable=get_age
    )

    [task2, task3] >> task1
