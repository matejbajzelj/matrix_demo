import socket
import threading
import random
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE

# Constants
correct_password = "mypass123"
min_auth_token_value = 1000000000
max_auth_token_value = 4294967295 # 4 bytes 32 bits

# Create a list to store verified client IDs
connected_clients = []

# When a new client connects, add them to the list with a unique ID
def add_client(conn, addr):
    # Generate a unique ID for the client (you can implement your own logic)
    client_id = generate_unique_id(conn, addr)
    connected_clients.append((client_id, conn, addr))
    print(f"Client {client_id} connected from {addr}")


# When a client disconnects, remove them from the list
def remove_client(client_id):
    for client in connected_clients:
        if client[0] == client_id:
            connected_clients.remove(client)
            print(f"Client {client_id} disconnected")


def find_client(client_id):
    found = False
    
    for client in connected_clients:
        if client[0] == client_id:
            print(f"Client {client_id} found")            
            found = True
            break
    
    return found


# Implement your own logic to generate unique IDs for clients
def generate_unique_id(conn, addr):
    # Generate a random ID for the client
    client_id = random.randint(min_auth_token_value, max_auth_token_value)        

    # Assign the ID to the client
    connected_clients.append((client_id, conn, addr))
    return client_id


def allow_client_futher(conn, addr, message_type, auth_token, payload = ""):

    client_id = 0
    if auth_token >= min_auth_token_value and find_client(auth_token):
        return True, client_id

    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and payload == correct_password:
        # Generate a random ID for the client
        client_id = generate_unique_id(conn, addr)   
        return True, client_id
    
    return False, client_id


def get_users():
    user_info_list = []
    for client_info in connected_clients:
        client_id, _, client_addr = client_info
        user_info = f"Client ID: {client_id}, Address: {client_addr[0]}, Port: {client_addr[1]}"
        user_info_list.append(user_info)
    
    # Send the list of connected users back to the client
    user_info_response = "\n".join(user_info_list)
    return user_info_response

def disconnect_client(conn, auth_token):
    # Password is incorrect, send an error message and close the connection
    error_message = "Incorrect password. Connection closed."
    remove_client(auth_token)
    error_message_data = encode_message(E_MESSAGE_TYPE.AUTHENTICATION_REJECTED, 0, error_message)
    conn.sendall(error_message_data)
    conn.close()


def listen_clients(conn, addr, client_id):
    try:
        print(f"THREAD: Connected by {addr}, clientid: {client_id}")
        # Set message to connected client
        # Send a response

        while True:
            data = conn.recv(1024)
            if not data:
                break

            print("10")
            message_type, message_length, auth_token, payload = decode_message(data)
            print("20")
            allow, client_id = allow_client_futher(conn, addr, message_type, auth_token, payload)
            message_to_sent = f"Message received from client: {payload}"
            print(message_to_sent)

            print("30")
            if allow == False:
                print("40")
                disconnect_client(conn)
                print("50")

            else:
                
                print("41")

                if message_type == E_MESSAGE_TYPE.GET_USERS:
                    message_to_sent = get_users()

                success_message_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, message_to_sent)
                conn.sendall(success_message_data)

    except Exception as e:
        print(f"Error handling client {addr}: {str(e)}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed")


def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            
            welcome_message = f"Initiating the communication. Client {addr} Send password"
            response = encode_message(E_MESSAGE_TYPE.WELCOME_MESSAGE, 0, welcome_message)
            conn.sendall(response)

             # Receive the password from the client
            data = conn.recv(1024)
            print("1")
            message_type, message_length, auth_token, payload = decode_message(data)
            print("2")
            allow, client_id = allow_client_futher(conn, addr, message_type, auth_token, payload)
            print("3")
            if allow == False:
                disconnect_client(conn)

            else:
                if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and allow == True:
            
                    print(f"Server generated ID {client_id} for listening on {host}:{port}")
                    # Password is correct, send a success message and keep the connection alive
                    success_message = "Password accepted. Connection established. ID sent"                
                    success_message_data = encode_message(E_MESSAGE_TYPE.ASSIGNED_ID, client_id, success_message)
                    conn.sendall(success_message_data)


                success_message = f"Message received from client: {payload}"
                print(success_message)

                success_message_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, success_message)
                conn.sendall(success_message_data)

                client_thread = threading.Thread(target=listen_clients, args=(conn, addr, client_id))
                client_thread.start()


if __name__ == "__main__":
    start_server()
