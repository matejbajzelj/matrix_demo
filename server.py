import socket
import threading
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE
from tools.client_lib import find_client, generate_unique_id, add_client, remove_client
from tools.commands import get_users

# Constants
correct_password = "mypass123"
min_auth_token_value = 1000000000
max_auth_token_value = 4294967295 # 4 bytes 32 bits

# Create a list to store verified client IDs
connected_clients = []
matches = []

def allow_client_futher(conn, addr, message_type, auth_token, payload = ""):

    print("allow_client_futher 1")
    client_id = 0
    if auth_token >= min_auth_token_value and find_client(auth_token, connected_clients):
        return True, client_id

    print("allow_client_futher 2")
    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and payload == correct_password:
        # Generate a random ID for the client
        client_id =  generate_unique_id(min_auth_token_value, max_auth_token_value)   
        add_client(conn, addr, client_id, connected_clients)
        return True, client_id
    
    print("allow_client_futher 3")
    return False, client_id


def disconnect_client(conn, auth_token=0):
    # Password is incorrect, send an error message and close the connection
    error_message = "Incorrect password. Connection closed."
    remove_client(auth_token, connected_clients)
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
                    print("51")
                    message_to_sent = get_users(connected_clients)

                print(f"message before sending: {message_to_sent}")
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
                
                else:
                    success_message = f"Message received from client: {payload}"
                    print(success_message)

                    success_message_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, success_message)
                    conn.sendall(success_message_data)

                client_thread = threading.Thread(target=listen_clients, args=(conn, addr, client_id))
                client_thread.start()


if __name__ == "__main__":
    start_server()
