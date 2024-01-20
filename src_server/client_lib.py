import random
from threading import Lock

# I added lock mechanisem, but I think in this simple demo program, would not need it, since
# it will be run by 2 clients, with high chance on runing on the same terminal, so 1 person has to write commands in 
# 2 clients and he can't do that fast to make problems. But in real case env, if you have multiple clients,
# lock would be prefered solution.
connected_clients = []
connected_clients_lock = Lock()

# When a new client connects, add them to the list with a unique ID
# So since this is he only place that adds clients to the array and this
# is called concurrently - we need to think if we need a lock or not.
def add_client(conn, addr, client_id):
    with connected_clients_lock:
        connected_clients.append((client_id, conn, addr))
        print(f"Client {client_id} connected from {addr}")


# When a client disconnects, remove them from the list
def remove_client(client_id):
    with connected_clients_lock:
        for client in connected_clients:
            if client[0] == client_id:
                connected_clients.remove(client)
                print(f"Client {client_id} disconnected")


def find_client(client_id):
    with connected_clients_lock:
        isFound = False
        clientFound = None
        
        for client in connected_clients:
            if client[0] == client_id:
                print(f"Client {client_id} found")
                isFound = True
                clientFound = client
                break
        
        return isFound, clientFound

def get_all_users():    
    with connected_clients_lock:
        return connected_clients.copy()    

# Implement your own logic to generate unique IDs for clients
def generate_unique_id(min_auth_token_value, max_auth_token_value):
    # Generate a random ID for the client
    client_id = random.randint(min_auth_token_value, max_auth_token_value)        

    return client_id
