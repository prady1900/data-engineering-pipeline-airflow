from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import json
import pandas as pd
import os


from sqlalchemy import create_engine, insert,Table, Column, Integer, String, MetaData

meta = MetaData()
engine = create_engine('postgresql+psycopg2://admin:admin@postgres_host/admin')

default_args = {
    'owner':'prady1900',
    'depends_on_past':False,
    'start_date': datetime(2023,1,1),
    'retries':2,
    'retry_delay': timedelta(minutes=2),
    'email_on_retry': False,
    'email_on_failure': False

}

def create_DB(task_instance):
    incident_db = Table(
    'incident_table',meta,
    Column('id',Integer, primary_key=True),
    Column('number',Integer),
    Column('impact',Integer),
    Column('severity',Integer),
    Column('priority',Integer),
    Column('category',String),
    Column('calendar_stc',Integer),
    Column('assignment_group',String)
)
    meta.create_all(engine)
    task_instance.xcom_push(key='table_ob')
    os.environ['TABLE_NAME'] = incident_db

def insert_data_postg(task_instance):
    pg_hook = PostgresHook.get_hook('postgres_connect')
    df_inc = pd.read_csv('./data/incidents.csv')
    df_inc.to_sql('incident_new',pg_hook.get_sqlalchemy_engine(),if_exists='append', chunksize=500, index=False)

    


with DAG(
    'db_dg',
    default_args= default_args,
    schedule_interval=None,
    catchup=False

) as dag:
    
    create_post_DB = PostgresOperator(
        task_id = 'create_post_DB',
        postgres_conn_id='postgres_connect',
        sql="""
    create table if not exists incident_new(
    id serial ,
    impact integer,
    number varchar(50),
    severity integer,
    priority integer,
    assignment_group varchar(40),
    resolve_time integer,
    category varchar(50),
    primary key(id)
)
"""
    )

    # insert data using hooks
    insert_using_python_data = PythonOperator(
        task_id='insert_using_python_data',
        python_callable=insert_data_postg
    )

    #trigger ML Model Creation
    triggerMlModel = TriggerDagRunOperator(
        task_id='triggerMlModel',
        trigger_dag_id='target',
        wait_for_completion=False
    )


    
    create_post_DB>>insert_using_python_data >> triggerMlModel