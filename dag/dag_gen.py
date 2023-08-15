import networkx as nx
from typing import Dict, Tuple
import sys
import json
import random
import util
import os

def generate_dag(num_nodes: int) -> nx.DiGraph:
    # Reserve last node as destination node
    dag = nx.random_tree(num_nodes-1, create_using=nx.DiGraph)
    # Add edge from the node whose outdegree is zero to the last node
    for node, out_degree in list(dag.out_degree()):
        if out_degree == 0:
            dag.add_edge(node, num_nodes-1)
    return dag

def get_dag_data(dag: nx.DiGraph, service_filename: str) -> Tuple:
    # Get service from a json file
    service = {}
    with open(service_filename, 'r') as fh:
        service = json.load(fh)
    service_name = sorted(list(service.keys()))
    # Generate random dag data
    # dag_service = [random.choice(service_name) for _ in range(num_nodes)]
    dag_service = service_name[:]
    dag_edge = [[] for _ in range(num_nodes)]
    for u, v in dag.edges():
        dag_edge[u].append(v)
    dag_edge_weight = [util.generate_random_weights(len(i)) for i in dag_edge]
    return service, dag_service, dag_edge, dag_edge_weight

def save_dag(dag_data: Tuple, node_name_prefix: str, filename: str) -> None:
    # Save dag data to a json file
    service, dag_service, dag_edge, dag_edge_weight = dag_data
    dag_json = {}
    for i in range(num_nodes):
        node_data = {}
        node_data['url'] = service[dag_service[i]]['url']
        node_data['exec_time'] = service[dag_service[i]]['exec_time']
        node_data['children'] = [{'name': f'{node_name_prefix}{node}', 'prob': weight} 
                                 for node, weight in zip(dag_edge[i], dag_edge_weight[i])]
        dag_json[f'{node_name_prefix}{i}'] = node_data
    with open(filename, 'w') as fh:
        json.dump(dag_json, fh, indent=2)

if __name__ == '__main__':
    num_nodes = int(sys.argv[1])
    dag = generate_dag(num_nodes)

    # Create folder and plot image
    folder_name = '.dag'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    util.plot_dag_with_plt(dag, 'dag_plt.png', folder_name)
    util.plot_dag_with_dot(dag, 'dag_dot.png', folder_name)
    
    # Save dag info to a json file
    dag_data = get_dag_data(dag, '../service/.service/service.json')
    save_dag(dag_data, 'node', f'{folder_name}/dag.json')