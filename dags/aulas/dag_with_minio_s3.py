from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor 

default_args= {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

with DAG(
    default_args=default_args,
    start_date=datetime(2025,5,2),
    schedule='@daily',
    dag_id='dag_with_minio_s3'
) as dag:
    task1 = S3KeySensor(
        task_id='sensor_minio_s3',
        bucket_key='s3://airflow/data.csv',
        aws_conn_id='minioS3',
        mode='poke',
        poke_interval=5,
        timeout=30
    )
