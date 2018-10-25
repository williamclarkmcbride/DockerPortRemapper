import docker
import os
import fileinput
import urllib3.exceptions

def get_container_id():
    
    print("Please enter or paste the name or id of the container you want to rebind: ")
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

is_docker_local = get_local_or_remote()
#print(is_docker_local)

container_id = get_container_id()
#print(container_id)

stop_docker_container_and_engine(container_id)

#test