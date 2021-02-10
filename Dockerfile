FROM apache/airflow

RUN pip install bs4
RUN airflow db upgrade

ADD ./dags /opt/airflow/dags
