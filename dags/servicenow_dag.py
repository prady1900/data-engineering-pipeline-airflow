from airflow import DAG
from datetime import datetime, timedelta
from airflow.decorators import task
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
import os
import json
import pandas as pd

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData


def transform_data(task_instance):
    # list_col = ['number','assignment_group.value','urgency', 'severity','priority','category','impact']
    data = task_instance.xcom_pull(task_ids="extract_incident_data")
    dataFrame = pd.json_normalize(data['result'])
    dataFrame = dataFrame[['number','impact','severity','priority','category','calendar_stc','assignment_group.value']]
    dataFrame = dataFrame.rename(columns={'calendar_stc':'resolve_time','assignment_group.value':'assignment_group'})
    if os.path.exists('./data/incidents.csv'):
        os.remove('./data/incidents.csv')
        dataFrame.to_csv('./data/incidents.csv', index=False)
    else:
        dataFrame.to_csv('./data/incidents.csv', index=False)
    
    


default_args = {
    'owner':'prady1900',
    'depends_on_past':False,
    'start_date': datetime(2023,1,1),
    'retries':'2',
    'retry_delay': timedelta(minutes=2),
    'email_on_retry': False,
    'email_on_failure': False

}

with DAG(
    'snow_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    
    is_snow_api_ready = HttpSensor(
        task_id='is_snow_api_ready',
        http_conn_id='snow_api_id',
        endpoint='api/now/table/incident'
    )

    extract_incident_data = SimpleHttpOperator(
        task_id='extract_incident_data',
        http_conn_id='snow_api_id',
        endpoint='api/now/table/incident??sysparm_query=state=6^ORstate=7&sysparm_limit=1000',
        method='GET',
        log_response = True,
        response_filter = lambda r: json.loads(r.text)
    )

    transform_inc_data = PythonOperator(
        task_id = 'transform_inc_data',
        python_callable=transform_data
    )

    triggerDbDag = TriggerDagRunOperator(
        task_id='triggerDbDag',
        trigger_dag_id='target',
        wait_for_completion=False
    )
    

    is_snow_api_ready >> extract_incident_data >> transform_inc_data >>triggerDbDag
