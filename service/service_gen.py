import os
import sys
import json
import random
import subprocess

def generate_service(num_services: int, folder_name: str, service_name_prefix: str, filename: str):
    service_json = {}
    for i in range(num_services):
        service_name = f'{service_name_prefix}{i}'
        url = f'http://{service_name_prefix}{i}.default.127.0.0.1.sslip.io:8080'
        exec_time = random.random()
        service_json[service_name] = {
            'url': url, 
            'exec_time': exec_time
        }
        # Create the corresponding yaml file
        cmd1 = f'cp {folder_name}/service.yaml.template {folder_name}/{service_name}.yaml'
        cmd2 = f'sed -i "" "s#<SERVICE_NAME>#\'{service_name}\'#g" {folder_name}/{service_name}.yaml'
        cmd3 = f'sed -i "" "s#<EXEC_TIME>#\'{exec_time}\'#g" {folder_name}/{service_name}.yaml'
        try:
            subprocess.check_output(cmd1, shell=True, encoding='utf-8')
            subprocess.check_output(cmd2, shell=True, encoding='utf-8')
            subprocess.check_output(cmd3, shell=True, encoding='utf-8')
        except Exception as e:
            print(e)
    # Save service info to a json files
    with open(f"{folder_name}/{filename}", 'w') as fh:
        json.dump(service_json, fh, indent=2)

if __name__ == '__main__':
    num_services = int(sys.argv[1])
    docker_username = sys.argv[2]

    # Create folder and copy a service yaml template
    folder_name = '.service'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    cmd1 = f'cp service.yaml.template .service/'
    cmd2 = f'sed -i "" "s#<DOCKER_USERNAME>#{docker_username}#g" .service/service.yaml.template'
    try:
        subprocess.check_output(cmd1, shell=True, encoding='utf-8')
        subprocess.check_output(cmd2, shell=True, encoding='utf-8')
    except Exception as e:
        print(e)
    
    # Start to generate service info
    generate_service(num_services, folder_name, 'service', 'service.json')