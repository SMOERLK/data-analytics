FROM apache/airflow:1.10.12-python3.6

RUN pip install --upgrade pip

RUN pip install bs4

ADD ./dags /opt/airflow/dags
