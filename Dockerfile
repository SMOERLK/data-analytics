FROM apache/airflow:1.10.12-python3.6

ADD ./dags /opt/airflow/dags

CMD ['airflow', 'db' , 'upgrade']
