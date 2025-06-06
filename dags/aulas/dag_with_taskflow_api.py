from airflow.decorators import dag, task
from datetime import timedelta, datetime

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay':timedelta(minutes=1)
}

@dag(
    dag_id='dag_with_taskflow_api',
    default_args=default_args,
    start_date=datetime(2021,7,2),
    schedule='@daily'
)
def hello_world_etl():
    @task(multiple_outputs=True)
    def get_name():
        return {
            'first_name': 'Violett',
            'last_name': 'Vohor'
        }

    @task()
    def get_age():
        return 32

    @task()
    def greet(first_name, last_name, age):
        print(f'Hello world, my name is {first_name} {last_name} and I\'m {age} years old!!')


    name_dict = get_name()
    age = get_age()
    greet(name_dict['first_name'], name_dict['last_name'], age)

greet_dag = hello_world_etl()
