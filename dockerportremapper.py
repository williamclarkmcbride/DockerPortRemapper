import docker
import os
import json
import urllib3.exceptions

def get_container_id():
    
    print("Please enter or paste the name or id of the container you want to rebind:")
    container_id = input()
    try:
        docker_client = docker.from_env()
        docker_container = docker_client.containers.get(container_id)
    except urllib3.exceptions.HTTPError:
        print("That does not appear to be a valid container name or id")
        quit()
    container_id = docker_container.id

    return container_id

def get_local_or_remote():

    print("Is the Docker host local or is it on a remote server? Enter the number that matches\n1 local\n2 remote")
    user_entry = input()

    if user_entry == "1":
        is_docker_local = True
    elif user_entry == "2":
        is_docker_local = False
        print("Rebinding ports for a remote Docker engine has not been implemented yet")
        quit()
    else:
        print("Invalid entry, please enter a valid option")
        is_docker_local = get_local_or_remote()
    
    return is_docker_local

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

def get_tcp_or_udp():

    print("Is the port binding for TCP or UDP?\n1 TCP\n2 UDP")
    response = input()
    if response == "1":
        tcp = True
    elif response == "2":
        tcp = False
    else:
        print("Invalid selection")
        tcp = get_tcp_or_udp()
    
    return tcp

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

    message = "Completed Successfully"

    return message

def get_container_port_number():

    print("Enter the container port that you want to remap to a new port on the host:")
    container_port_number = input()

    return container_port_number

def get_host_port_number ():

    print("Enter the host port that you want to remap the container port to:")
    host_port_number = input()

    return host_port_number

def main():

    #is_docker_local = get_local_or_remote()

    container_id = get_container_id()

    container_port_number = get_container_port_number()

    host_port_number = get_host_port_number()

    tcp = get_tcp_or_udp()

    stop_docker_container_and_engine(container_id)

    message = get_hostconfig_json(container_id, container_port_number, host_port_number, tcp)

    print(message)

    start_docker_container_and_engine(container_id)

main()