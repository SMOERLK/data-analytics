FROM apache/airflow:1.10.12-python3.6

RUN pip install --upgrade --user pip

RUN pip install --user bs4

ADD ./dags /opt/airflow/dags

ADD ./scripts /opt/airflow/scripts

RUN chmod 777  /opt/airflow/logs

ENTRYPOINT [ "bash" , "/opt/airflow/scripts/airflow-entrypoint.sh"]