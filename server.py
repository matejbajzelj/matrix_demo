import socket
import sys
import os
import threading
from src_common.constants import TCP_ENABLED, TCP_PORT, TCP_HOST, UNIX_PATH
from src_common.tools import decode_message, encode_message, E_MESSAGE_TYPE
from src_common.messages import get_server_notification, get_welcome_message, get_starting_server_info
from src_server.client_lib import remove_client
from src_server.commands import get_users, get_matches
from src_server.match import remove_match
from src_server.server_logic import server_action_accepted_match, server_action_game_started, server_action_start_match, allow_client_futher

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

            message_to_sent = ""
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


def start_server(tcp_enabled:bool, tcp_port:int, tcp_host:str, unix_path:str):
    
    if tcp_enabled:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((tcp_host, tcp_port))
        server_socket.listen()
        # print(f"TCP socket server is listening on {host}:{tcp_port}")
    else:
        # Delete the existing socket file if it exists
        if os.path.exists(unix_path):
            os.remove(unix_path)
    
        server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(unix_path)
        server_socket.listen()
        print(f"Unix socket server is listening on {unix_path}")

    while True:
        client_socket, addr = server_socket.accept()
        
        # welcome message
        welcome_message = get_welcome_message(addr)
        response = encode_message(E_MESSAGE_TYPE.WELCOME_MESSAGE, 0, welcome_message)
        client_socket.sendall(response)
            
        client_thread = threading.Thread(target=listen_clients, args=(client_socket, addr))
        client_thread.start()
           
if __name__ == "__main__":
    
    # USE TCP:  paython server.py true 65433 127.0.0.1
    # USE UNIX: paython server.py false /tmp/my_unix_socket.sock
    tcp_enabled = TCP_ENABLED
    tcp_port = TCP_PORT
    tcp_host = TCP_HOST
    unix_path = UNIX_PATH
    
    if len(sys.argv) > 1:
        tcp_enabled = sys.argv[1].lower() == 'true'
    else:
        tcp_enabled = False         
        
    if tcp_enabled and len(sys.argv) > 2:
        tcp_port = int(sys.argv[2])
    
    elif tcp_enabled == False and len(sys.argv) > 2:
        unix_path = sys.argv[2]
        
    if tcp_enabled and len(sys.argv) > 3:
        tcp_host = sys.argv[3]
        
    message = get_starting_server_info("Server", tcp_enabled, tcp_port, tcp_host, unix_path)
    print (message)
    start_server(tcp_enabled, tcp_port, tcp_host, unix_path)
