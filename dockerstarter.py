import docker

client = docker.from_env()

def start_containers():

    #run Backend Container
    backend_container = client.containers.get('519bc459773330785938e61c3f9698ff9f16ab81d470065aa056f4ee90c57f95')
    backend_container.start()


    #run Nginx Container
    nginx_container = client.containers.get('4f336e0a8584b71d94e8af6f2470906042e3891306e4a2d147b1e46e96114a77')
    nginx_container.start()