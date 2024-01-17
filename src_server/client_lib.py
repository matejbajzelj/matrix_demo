import random

# When a new client connects, add them to the list with a unique ID
def add_client(conn, addr, client_id, connected_clients):
    # Generate a unique ID for the client (you can implement your own logic)
    connected_clients.append((client_id, conn, addr))
    print(f"Client {client_id} connected from {addr}")


# When a client disconnects, remove them from the list
def remove_client(client_id, connected_clients):
    for client in connected_clients:
        if client[0] == client_id:
            connected_clients.remove(client)
            print(f"Client {client_id} disconnected")


def find_client(client_id, connected_clients):
    isFound = False
    clientFound = None
    
    for client in connected_clients:
        if client[0] == client_id:
            print(f"Client {client_id} found")
            isFound = True
            clientFound = client
            break
    
    return isFound, clientFound


# Implement your own logic to generate unique IDs for clients
def generate_unique_id(min_auth_token_value, max_auth_token_value):
    # Generate a random ID for the client
    client_id = random.randint(min_auth_token_value, max_auth_token_value)        

    return client_id
