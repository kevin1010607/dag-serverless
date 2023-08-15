from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import datetime
import os
import json
import random
import subprocess

# Get dag information from a json file
DAG_FILENAME = '<DAG_FILENAME>'
dag_data= {}
with open(DAG_FILENAME, 'r') as fh:
    dag_data = json.load(fh)

def next_task(children, number):
    cumulative_prob = 0
    for child in children:
        cumulative_prob += child['prob']
        if cumulative_prob >= number:
            return child['name']
    return None

def request_service(**kwargs):
    url, children = kwargs['url'], kwargs['children']
    # cmd = f"curl -o /dev/null -s -w '%{{time_total}}s\n' {url}"
    cmd = f"curl {url}"
    try:
        result = float(subprocess.check_output(cmd, shell=True, encoding='utf-8'))
    except Exception as e:
        print(e)
        result = random.random()
    return next_task(children, result)

# Define dag args
dag_id = 'knative'
default_args = {
    'owner': 'airflow', 
    'start_date': datetime(2023, 7, 18), 
}
schedule = None

# Define the dag
with DAG(dag_id, default_args=default_args, schedule=schedule) as dag:
    tasks = {}
    # Define the nodes
    for name, data in dag_data.items():
        task = BranchPythonOperator(
            task_id=name, 
            python_callable=request_service,
            op_kwargs={'url': data['url'], 'children': data['children']}, 
            trigger_rule='one_success', 
            provide_context=True, 
            dag=dag, 
        )
        tasks[name] = task
    # Define the edge
    for name, data in dag_data.items():
        children_tasks = [tasks[child['name']] for child in data['children']]
        tasks[name] >> children_tasks