FROM apache/airflow:1.10.12-python3.6

ADD ./dags /opt/airflow/dags


RUN pip install --upgrade --user pip
RUN pip install --user bs4

RUN airflow db upgrade

# ENTRYPOINT [ "bash" , "/opt/airflow/scripts/airflow-entrypoint.sh"]
