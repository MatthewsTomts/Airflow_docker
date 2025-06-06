import os
import shutil
import pandas as pd
from airflow import DAG
from math import ceil as math_ceil
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from pyspark.sql.types import IntegerType, DateType 
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.standard.operators.python import PythonOperator
from pyspark.sql.functions import col, regexp_replace, try_to_timestamp 

default_args = {
    'owner': 'me',
    'retries': 5,
    'retry_delay': timedelta(minutes=1)
}

def transform_spark():
    spark = (
        SparkSession.builder
        .master('local')
        .appName('Projeto_postgres')
        .getOrCreate()
    )
    
    df = spark.read.csv('./data/sample_with_errors_100.csv', header=True, inferSchema=True)

    df = df.withColumn('JoinDate', try_to_timestamp('JoinDate')).filter(col('JoinDate').isNotNull())
    df = df.drop('Name').dropna(subset=['Email', 'JoinDate'])

    sum = 0
    df_filtered = df.filter(col('Age').rlike('^\d+$'))
    for row in df_filtered.collect():
        sum += int(row[1])

    avg = math_ceil(sum / len(df_filtered.collect()))

    df = df.withColumn('Age', regexp_replace('Age', '.*\D.*', avg))
    df = df.fillna({'Age': avg})
    df = df.withColumn('ID', regexp_replace('ID', 'ID_', ''))

    df = df.withColumn('ID', col('ID').cast(IntegerType()))
    df = df.withColumn('Age', col('Age').cast(IntegerType()))
    df = df.withColumn('JoinDate', col('JoinDate').cast(DateType()))

    df.printSchema()

    df.write.mode("overwrite").parquet("./data/projeto_postgres")

def insert_minio():
    dir = './data/projeto_postgres/' 
    files = os.listdir(dir)
    part_files = [f for f in files if f.startswith("part-")]

    for i in range(0, len(part_files)):
        file_path = os.path.join(dir, part_files[i])
        new_file_path = os.path.join(dir, f'projeto_postgres_{i+1}.parquet')

        shutil.move(file_path, new_file_path)

        minio_hook = S3Hook(aws_conn_id="minioS3")
        minio_hook.load_file(
            filename=new_file_path,
            key=f'projeto_postgres/projeto_postgres_{i+1}.parquet',
            bucket_name='airflow',
            replace=True
        )

def insert_postgres():
    dir = './data/projeto_postgres/' 
    files = os.listdir(dir)
    part_files = [f for f in files if f.endswith("parquet")]

    print(part_files)

    for file in part_files:
        df = pd.read_parquet(dir + file)
        postgres_hook = PostgresHook(postgres_conn_id="postgresql")

        engine = postgres_hook.get_sqlalchemy_engine()

        print(engine)

        df.to_sql(
            name='projeto_postgres',
            con=engine, 
            index=False,
            schema='public'
        )

        print(df)
        

with DAG(
    default_args=default_args,
    start_date=datetime(2022,5,30),
    schedule='@daily',
    dag_id='Projeto_postgres'
) as dag:
    task1 = PythonOperator(
        task_id='transformSpark',
        python_callable=transform_spark
    )

    task2 = PythonOperator(
        task_id='insertMinio',
        python_callable=insert_minio
    )

    task3 = PythonOperator(
        task_id='insertPostgres',
        python_callable=insert_postgres
    )

    task1 >> task2 >> task3

