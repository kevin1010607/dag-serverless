from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import datetime
import os
import json
import random
import requests
import subprocess

# Get dag information from a json file
DAG_FILENAME = '<DAG_FILENAME>'
dag_data= {}
with open(DAG_FILENAME, 'r') as fh:
    dag_data = json.load(fh)
# Define dag args
dag_id = 'knative'
default_args = {
    'owner': 'airflow', 
    'start_date': datetime(2023, 7, 18), 
}
schedule = None

# Define server info
DOMAIN = 'http://127.0.0.1:8000'

def init_dag():
    url = f'{DOMAIN}/init'
    dag = {'dag_id': dag_id, 'dag_data': dag_data}
    # response = requests.post(url, json=dag, timeout=5)
    # return response.json()
    return dag

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

# Define the dag
with DAG(dag_id, default_args=default_args, schedule=schedule) as dag:
    tasks = {}
    indegree = {name: 0 for name in dag_data}
    # Define the nodes
    for name, data in dag_data.items():
        # Update indegree
        for child in data['children']:
            indegree[child['name']] += 1
        # Create task
        task = BranchPythonOperator(
            task_id=name, 
            python_callable=request_service,
            op_kwargs={'url': data['url'], 'children': data['children']}, 
            trigger_rule='one_success', 
            provide_context=True, 
            dag=dag, 
        )
        tasks[name] = task
    # Define the edges
    for name, data in dag_data.items():
        children_tasks = [tasks[child['name']] for child in data['children']]
        tasks[name] >> children_tasks
    # Add a master root to all source nodes
    master_root = PythonOperator(
        task_id='master_root', 
        python_callable=init_dag, 
        provide_context=True, 
        dag=dag, 
    )
    master_root >> [tasks[name] for name in dag_data if indegree[name] == 0]