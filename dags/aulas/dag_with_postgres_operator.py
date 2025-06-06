from airflow.decorators import dag
from datetime import datetime, timedelta
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator 

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

@dag(
    default_args=default_args,
    dag_id='dag_with_postgres_operator',
    start_date=datetime(2025,5,2),
    schedule='@daily'
)
def dag_with_postgres_operator():
    task1 = SQLExecuteQueryOperator(
        task_id='create_postgres_table',
        conn_id='postgresql',
        sql= """
            CREATE TABLE IF NOT EXISTS dag_runs (
                dt date,
                dag_id character varying,
                primary key (dt, dag_id)
            )
        """
    )

    task2 = SQLExecuteQueryOperator(
        task_id='insert_into_table',
        conn_id='postgresql',
        sql="""
            insert into dag_runs (dt, dag_id) values ('{{ ds }}', '{{ dag.dag_id }}')
        """
    )

    task3 = SQLExecuteQueryOperator(
        task_id='delete_into_table',
        conn_id='postgresql',
        sql="""
            delete from dag_runs where dt = '{{ ds }}' and dag_id = '{{ dag.dag_id }}'
        """
    )

    task1 >> task3 >> task2

dag_with_postgres_operator()
