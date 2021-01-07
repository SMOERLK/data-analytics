FROM apache/airflow

RUN pip install bs4

ADD ./dags /opt/airflow/dags
