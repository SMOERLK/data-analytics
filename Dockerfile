FROM apache/airflow

RUN pip install --upgrade --user pip

RUN pip install --user bs4

# ADD ./scripts /opt/airflow/scripts

# ENTRYPOINT [ "bash" , "/opt/airflow/scripts/airflow-entrypoint.sh"]
