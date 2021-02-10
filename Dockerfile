FROM apache/airflow

RUN pip install --upgrade --user pip

RUN pip install --user bs4
RUN airflow db upgrade

# ENTRYPOINT [ "bash" , "/opt/airflow/scripts/airflow-entrypoint.sh"]
