FROM apache/airflow:latest-python3.9

USER airflow

RUN pip install scikit-learn



