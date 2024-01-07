from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import joblib
import os
import json
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
import pandas as pd


def load_data():
    pg_hook = PostgresHook.get_hook('postgres_connect')
    df = pg_hook.get_pandas_df(sql='select impact,severity,priority,category,resolve_time from incident_new')
    #df = pd.DataFrame(json.load(df.to_json(index=False)))
    df.dropna(inplace=True)
    my_feat = df[['impact','severity','priority','category','resolve_time']]
    df_new = pd.get_dummies(my_feat,columns=['category'])
    tg_value = df['resolve_time']

    x_train, x_test, y_train, y_test = train_test_split(
        df_new, tg_value, random_state=106, test_size=0.2, shuffle= True
    )
    print('Model... start training');
    model_svr = LinearRegression()
    model_svr.fit(x_train,y_train)
    print('Model Finished Training');
    if(os.path.exists('./ml_model_file/res_time_predictor.pkl')):
        os.remove('./ml_model_file/res_time_predictor.pkl')
        joblib.dump(model_svr, './ml_model_file/res_time_predictor.pkl')
    else:
        joblib.dump(model_svr, './ml_model_file/res_time_predictor.pkl')


default_args = {
    'owner':'prady1900',
    'depends_on_past':False,
    'start_date': datetime(2023,1,1),
    'retries':'2',
    'retry_delay': timedelta(minutes=2),
    'email_on_retry': False,
    'email_on_failure': False

}
with DAG (
    'ml_dag',
    default_args=default_args,
    schedule_interval=None,
    catchup=False
)as ml_dag:
    start_task = EmptyOperator(
        task_id='start_task',
    )

    load_data_from_idea = PythonOperator(
        task_id = 'load_data_from_idea',
        python_callable=load_data
    )

    start_task>>load_data_from_idea


