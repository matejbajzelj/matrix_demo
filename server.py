import socket
import threading
import random
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE

# Constants
correct_password = "mypass123"
min_auth_token_value = 1000000000
max_auth_token_value = 4294967295 # 4 bytes 32 bits

# Create a list to store verified client IDs
verified_clients = []

def allow_client_futher(message_type, auth_token, payload = ""):

    client_id = 0
    if auth_token >= min_auth_token_value and auth_token in verified_clients:        
        return True, client_id

    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and payload == correct_password:
        # Generate a random ID for the client
        client_id = random.randint(min_auth_token_value, max_auth_token_value)        

        # Assign the ID to the client
        verified_clients.append(client_id)
        return True, client_id
    
    return False, client_id


def disconnect_client(conn):
    # Password is incorrect, send an error message and close the connection
    error_message = "Incorrect password. Connection closed."
    error_message_data = encode_message(E_MESSAGE_TYPE.AUTHENTICATION_REJECTED, 0, error_message)
    conn.sendall(error_message_data)
    conn.close()


def listen_clients(conn, addr):
    try:
        print(f"Connected by {addr}")
        # Set message to connected client
        # Send a response

        while True:
            data = conn.recv(1024)
            if not data:
                break

            message_type, message_length, auth_token, payload = decode_message(data)
            allow, client_id = allow_client_futher(message_type, auth_token, payload)

            if allow == False:
                disconnect_client(conn)

            else:
                success_message = f"Message received from client: {payload}"
                print(success_message)

                success_message_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, success_message)
                conn.sendall(success_message_data)

                client_thread = threading.Thread(target=listen_clients, args=(conn, addr))
                client_thread.start()

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
            message_type, message_length, auth_token, payload = decode_message(data)

            allow, client_id = allow_client_futher(message_type, auth_token, payload)

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

                client_thread = threading.Thread(target=listen_clients, args=(conn, addr))
                client_thread.start()


if __name__ == "__main__":
    start_server()
