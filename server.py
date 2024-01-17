import socket
import threading
from src_common.tools import LISTEN_PORT, decode_message, encode_message, E_MESSAGE_TYPE, correct_password, min_auth_token_value, max_auth_token_value 
from src_server.client_lib import remove_client
from src_server.commands import get_users, get_matches
from src_server.match import remove_match
from src_server.server_logic import get_server_notification, server_action_accepted_match, server_action_game_started, server_action_start_match, allow_client_futher, get_welcome_message

# Create a list to store verified client IDs
connected_clients = []
active_matches = []

def disconnect_client(conn, auth_token=0):
    # Password is incorrect, send an error message and close the connection
    error_message = get_server_notification("Incorrect password. Connection closed.")
    remove_client(auth_token, connected_clients)
    error_message_data = encode_message(E_MESSAGE_TYPE.AUTHENTICATION_REJECTED, 0, error_message)
    conn.sendall(error_message_data)
    conn.close()


def listen_clients(conn, addr):
    try:
        print(f"THREAD: Connected by {addr}")
        # Set message to connected client
        # Send a response

        skip_last_response = False
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message_type, message_length, auth_token, message_from_client = decode_message(data)
            
            allow, client_id = allow_client_futher(conn, addr, message_type, auth_token, connected_clients, message_from_client)
            
            if allow == False:
                disconnect_client(conn)
            else:
                if message_type == E_MESSAGE_TYPE.PASSWORD_SENT:
                    # Password is correct, send a success message and keep the connection alive
                    skip_last_response = True
                    success_message = get_server_notification(f"Password accepted. Connection established. Your Id {client_id}")
                    success_message_data = encode_message(E_MESSAGE_TYPE.ASSIGNED_ID, client_id, success_message)
                    conn.sendall(success_message_data)
                
                elif message_type == E_MESSAGE_TYPE.GET_USERS:
                    
                    message_to_sent = get_users(connected_clients)

                elif message_type == E_MESSAGE_TYPE.GET_MATCHES:
               
                    message_to_sent = get_matches(active_matches)

                elif message_type == E_MESSAGE_TYPE.START_MATCH:
                    skip_last_response = True
                    server_action_start_match(conn, client_id, message_from_client, auth_token, active_matches, connected_clients)
                
                elif message_type == E_MESSAGE_TYPE.ACCEPT_MATCH:
                    skip_last_response = True
                    server_action_accepted_match(message_from_client, active_matches, connected_clients)

                elif message_type == E_MESSAGE_TYPE.DECLINE_MATCH:
                    
                    accepted_match_id = message_from_client
                    remove_match(accepted_match_id, active_matches)
               
                elif message_type == E_MESSAGE_TYPE.GAME_STARED:
                    skip_last_response = True
                    server_action_game_started(message_from_client, auth_token, active_matches, connected_clients)

                if skip_last_response == False :                    
                    success_message_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, message_to_sent)
                    conn.sendall(success_message_data)
                else:
                    skip_last_response = False

    except Exception as e:
        print(f"Error handling client {addr}: {str(e)}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed")


def start_server(host='127.0.0.1', port=LISTEN_PORT):
    # with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Set SO_REUSEADDR option to allow reusing the same port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        while True:
            conn, addr = s.accept()
            
            welcome_message = get_welcome_message(addr)
            response = encode_message(E_MESSAGE_TYPE.WELCOME_MESSAGE, 0, welcome_message)
            conn.sendall(response)
            
            client_thread = threading.Thread(target=listen_clients, args=(conn, addr))
            client_thread.start()
           
if __name__ == "__main__":
    start_server()
