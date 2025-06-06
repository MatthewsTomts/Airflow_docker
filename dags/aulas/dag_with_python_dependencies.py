from airflow.decorators import dag, task
from datetime import datetime, timedelta

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    default_args=default_args,
    dag_id='dag_with_python_dependencies',
    start_date=datetime(2025,5,2),
    schedule='@daily'
)
def dag_with_scikit():
    @task(
        task_id='get_sklearn'
    )
    def get_sklearn():
        import sklearn
        print(f'scikit-learn version: {sklearn.__version__}')

    @task(
        task_id='get_matplotlib'
    )
    def get_matplotlib():
        import matplotlib 
        print(f'matplotlib version: {matplotlib.__version__}')

    get_sklearn()
    get_matplotlib()

dag_with_scikit()
