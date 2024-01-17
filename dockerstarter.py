from python_on_whales import docker as d
import docker as docker

def are_containers_running():
    container1 = 'blocker'
    container2 = 'nginx'

    client = docker.from_env()
    running_containers = client.containers.list()
    running_container_names = [container.name for container in running_containers]
    
    if container1 in running_container_names:
        container1_running = True
    else:
        container1_running = False

    if container2 in running_container_names:
        container2_running = True
    else:
        container2_running = False
    
    return container1_running,container2_running

def compose_start():
    container_running = are_containers_running()

    if container_running[0] == False and container_running[1] == False:
        d.compose.up(detach=True, log_prefix=False)
        print("Containers started succesfully")
    elif container_running[0] == True and container_running[1] == False:
        print("Blocker Container already running")
        print("Nginx Container not running")
    elif container_running[1] == True and container_running[0] == False:
        print("Nginx Container already running")
        print("Blocker Container not running")
    else:
        print("Nginx Container already running")
        print("Blocker Container already running")


def compose_stop():
    d.compose.down()

compose_start()