import csv
import logging
from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tempfile import NamedTemporaryFile

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

def postgres_to_s3(ds_nodash):
    hook = PostgresHook(postgres_conn_id='postgresql')
    conn = hook.get_conn()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM public.orders WHERE date <= '{ds_nodash}'")

    with NamedTemporaryFile(mode='w', suffix=f'{ds_nodash}') as f:
    #with open(f"dags/get_orders_{ds_nodash}.txt", "w") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

        f.flush()
        cursor.close()
        conn.close()

        logging.info(f"Saved orders data in text file get_orders_{ds_nodash}.txt")

        s3_hook = S3Hook(aws_conn_id='minioS3')
        s3_hook.load_file(
            filename=f.name,
            key=f"orders/orders_{ds_nodash}.txt",
            bucket_name="airflow",
            replace=True
        )

        logging.info(f"Orders files {f.name} has been pushed to S3!!")


with DAG (
    default_args=default_args,
    start_date=datetime(2025,5,2),
    schedule='@daily',
    dag_id='dag_with_postgres_hooks'
) as dag:
    task1 = PythonOperator(
        task_id='Postgres_to_S3',
        python_callable=postgres_to_s3
    ) 
