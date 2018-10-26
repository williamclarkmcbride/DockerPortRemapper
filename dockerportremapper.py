import docker
import os
import json
import urllib3.exceptions
import sys

def get_container_id(container_id):
    
    try:
        docker_client = docker.from_env()
        docker_container = docker_client.containers.get(container_id)
    except urllib3.exceptions.HTTPError:
        print("That does not appear to be a valid container name or id")
        quit()
    container_id = docker_container.id

    return container_id

def stop_docker_container_and_engine(container_id):
    
    docker_client = docker.from_env()
    docker_container = docker_client.containers.get(container_id)
    docker_container.stop()
    os.system("sudo systemctl stop docker.service")
    
    status = "Container and Docker Engine stopped successfully"

    #need to write error handling in here

    return status

def start_docker_container_and_engine(container_id):

    os.system("sudo systemctl start docker.service")
    docker_client = docker.from_env()
    docker_container = docker_client.containers.get(container_id)
    docker_container.start()

    status = "Container and Docker Engine started successfully"

    return status

def get_hostconfig_json(container_id, container_port_number, host_port_number, tcp = True):

    if tcp:
        container_port_binding = container_port_number + "/tcp"
    else:
        container_port_binding = container_port_number + "/udp"
    
    hostconfig_path = "/var/lib/docker/containers/" + container_id + "/hostconfig.json"
    hostconfig_file = open(hostconfig_path, "r+")
    hostconfig_json_data = json.load(hostconfig_file)
    hostconfig_json_data['PortBindings'][container_port_binding][0]['HostPort'] = host_port_number

    os.remove(hostconfig_path)
    new_hostconfig_file = open(hostconfig_path, "w")
    json.dump(hostconfig_json_data, new_hostconfig_file)

    status = "Ports remapped successfully"

    return status

def main(container_id, host_port_number, container_port_number, tcp):

    #is_docker_local = get_local_or_remote()

    #container_id = get_container_id()

    #container_port_number = get_container_port_number()

    #host_port_number = get_host_port_number()

    #tcp = get_tcp_or_udp()

    container_id = get_container_id(container_id)
    status = stop_docker_container_and_engine(container_id)
    print(status)
    status= get_hostconfig_json(container_id, container_port_number, host_port_number, tcp)
    print(status)
    status = start_docker_container_and_engine(container_id)
    print (status)

script_input_container_id = sys.argv[1]
script_input_host_port_number = sys.argv[2]
script_input_container_port_number = sys.argv[3]
script_input_tcp = sys.argv[4]

main(script_input_container_id, script_input_host_port_number, script_input_container_port_number, script_input_tcp)