from UseSupersetApi import UseSupersetApi
import json
import pprint
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.models import DAG
from datetime import datetime, timedelta
from airflow.operators.mysql_operator import MySqlOperator
from airflow.hooks.mysql_hook import MySqlHook
from airflow.utils.dates import days_ago
import logging
import os

superset_username = os.environ['SUPERSET_USERNAME']
superset_password = os.environ['SUPERSET_PASSWORD']

def insert_or_update_table(**kwargs):
    try:
        json_data = json.loads(kwargs["extra_json"])
        table_name = json_data['schedule_info']['output_table']
        sql = kwargs['sql']
        logging.info('trying the task')
        logging.info('connecting to source')
        src = MySqlHook(mysql_conn_id=kwargs['schema'])
        logging.info(f"Remotely received sql of {sql}")
        logging.info(f"Remotely received sql of {table_name}")
        logging.info('connecting to destination')
        dest = MySqlHook(mysql_conn_id='analytics')
        src_conn = src.get_conn()
        cursor = src_conn.cursor()
        cursor.execute(sql)
        dest.insert_rows(table=table_name, rows=cursor, replace=True)
    except Exception as e3:
        logging.error('Table update is failed, please refer the logs more details')
        logging.exception(e3)


def create_dag(dag_id, schedule, default_args, data):
    new_dag = DAG(dag_id, default_args=default_args, schedule_interval=schedule, catchup=False)
    logging.info(f"DAG is:{dag_id}")
    print(f"DAG is:{dag_id}")

    with new_dag:
        task_name = f"{dag_id}_task".upper()

        t1 = PythonOperator(
            task_id=task_name,
            python_callable=insert_or_update_table,
            op_kwargs=data,
            dag=new_dag
        )
    return new_dag


superset = UseSupersetApi(superset_username, superset_password)
saved_queries = superset.get(url_path='/savedqueryviewapi/api/read').text
saved_queries = json.loads(saved_queries)["result"]
for data in saved_queries:
    if 'extra_json' in data and 'schedule_info' in data['extra_json']:
        json_data = json.loads(data['extra_json'])
        if 'output_table' in json_data['schedule_info']:
            table_name = json_data['schedule_info']['output_table']
            dag_id = f"saved_queries_{table_name}".upper()

            default_args = {'owner': 'airflow',
                            'start_date': datetime(2018, 1, 1)
                            }

            schedule = timedelta(minutes=10)

            globals()[dag_id] = create_dag(
                dag_id,
                schedule,
                default_args,
                data
            )
