import threading

# Define the connected_clients list and a lock for thread safety
connected_clients = []
lock = threading.Lock()

# Function to add a client to the connected_clients list
def add_client(client_id):
    with lock:
        connected_clients.append(client_id)

# Function to get a copy of the connected_clients list
def get_users():
    with lock:
        return connected_clients.copy()

# Simulate adding clients to the list
add_client(1)
add_client(2)

# Get a copy of the list and print it
user_list = get_users()
print("Original connected_clients:", connected_clients)
print("User list returned by get_users:", user_list)

# Modify the user list copy
user_list.append(3)
print("Modified user list:", user_list)

# Print the original connected_clients again
print("Original connected_clients after modification:", connected_clients)
