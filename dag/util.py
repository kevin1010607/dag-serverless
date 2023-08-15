import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import random

def print_dag(dag: nx.DiGraph, filename: str) -> None:
    # Print dag with dot format to a dot file
    with open(filename, 'w') as fh:
        fh.write('digraph {\n')
        for u, v in dag.edges():
            fh.write(f'  {u} -> {v};\n')
        fh.write('}\n')

def plot_dag_with_plt(dag: nx.DiGraph, filename: str, folder_name: str = '.') -> None:
    # Use plt to plot the dag
    pos = nx.spring_layout(dag)
    nx.draw(dag, pos, with_labels=True, node_size=1000, 
        node_color='skyblue', font_size=10, font_color='black', font_weight='bold')
    plt.title("Random DAG Visualization")
    plt.savefig(f'{folder_name}/{filename}')
    # plt.show()

def plot_dag_with_dot(dag: nx.DiGraph, filename: str, folder_name: str = '.') -> None:
    # Use dot to plot the dag
    dot_filename = 'dag.dot'
    print_dag(dag, f'{folder_name}/{dot_filename}')
    cmd = f'dot -Tpng {folder_name}/{dot_filename} -o {folder_name}/{filename}'
    try:
        subprocess.check_output(cmd, shell=True, encoding='utf-8')
    except Exception as e:
        print(e)

def generate_random_weights(num_weights: int):
    # The sum of weight must be 1.0
    weights = [random.random() for _ in range(num_weights)]
    total = sum(weights)
    normalized_weights = [i / total for i in weights]
    return normalized_weights
