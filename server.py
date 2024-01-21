import socket
import sys
import os
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO
from src_common.constants import TCP_ENABLED, TCP_PORT, TCP_HOST, UNIX_PATH, FLASK_PORT
from src_common.tools import decode_message, encode_message, E_MESSAGE_TYPE
from src_common.messages import get_server_notification, get_welcome_message, get_starting_server_info, get_help_message
from src_server.client_lib import remove_client
from src_server.commands import get_users_command_output, get_matches_command_output
from src_server.match_lib import get_all_matches, generate_mock_matches
from src_server.socket_io_manager import socketio
from src_server.server_logic import (server_action_sent_hint, 
                                     server_action_accepted_match, 
                                     server_action_game_started,
                                     server_action_start_match,
                                     allow_client_further,
                                     server_action_declined_match,
                                     server_action_game_give_up)


website_app = Flask(__name__)
socketio.init_app(website_app)

@website_app.route('/')
def display_active_matches():
    # Here, you can fetch the active_matches array from src_server.match_lib
    # You can also format the data or manipulate it as needed
    # Then, pass the data to a template and render it
    active_matches = get_all_matches()  # Fetch active_matches using the appropriate function
    
    # if len(active_matches) == 0:
    #    active_matches = generate_mock_matches()
        
    return render_template('active_matches.html', active_matches=active_matches)

def disconnect_client(conn, auth_token=0):
    # Password is incorrect, send an error message and close the connection
    error_message = get_server_notification("Incorrect password. Connection closed.")
    remove_client(auth_token)
    error_message_data = encode_message(E_MESSAGE_TYPE.AUTHENTICATION_REJECTED, 0, error_message)
    conn.sendall(error_message_data)
    # conn.close() I close it in try-finally at this time. 
    

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
            
            allow, client_id = allow_client_further(conn, addr, message_type, auth_token, message_from_client)
            
            if allow == False:
                disconnect_client(conn)
                break
            else:
                if message_type == E_MESSAGE_TYPE.PASSWORD_SENT:
                    # Password is correct, send a success message and keep the connection alive
                    skip_last_response = True
                    success_message = get_server_notification(f"Password accepted. Connection established. Your Id {client_id}")
                    success_message_data = encode_message(E_MESSAGE_TYPE.ASSIGNED_ID, client_id, success_message)
                    conn.sendall(success_message_data)
                
                elif message_type == E_MESSAGE_TYPE.GET_USERS:
                    
                    message_to_sent = get_users_command_output()

                elif message_type == E_MESSAGE_TYPE.GET_MATCHES:
            
                    message_to_sent = get_matches_command_output()

                elif message_type == E_MESSAGE_TYPE.START_MATCH:
                    skip_last_response = True
                    server_action_start_match(conn, client_id, message_from_client)
                
                elif message_type == E_MESSAGE_TYPE.ACCEPT_MATCH:
                    skip_last_response = True
                    server_action_accepted_match(message_from_client)

                elif message_type == E_MESSAGE_TYPE.DECLINE_MATCH:
                    
                    accepted_match_id = message_from_client
                    server_action_declined_match(accepted_match_id)
            
                elif message_type == E_MESSAGE_TYPE.GAME_STARED:
                    skip_last_response = True
                    server_action_game_started(message_from_client, auth_token)
                    
                elif message_type == E_MESSAGE_TYPE.GAME_GIVE_UP:
                    skip_last_response = True
                    server_action_game_give_up(auth_token)
                
                elif message_type == E_MESSAGE_TYPE.GAME_SENT_HINT:
                    server_action_sent_hint(message_from_client, auth_token)
                    
                elif message_type == E_MESSAGE_TYPE.HELP:
                    message_to_sent = get_help_message()                    

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
        
    if tcp_enabled and len(sys.argv) > 2:
        tcp_port = int(sys.argv[2])
    
    elif tcp_enabled == False and len(sys.argv) > 2:
        unix_path = sys.argv[2]
        
    if tcp_enabled and len(sys.argv) > 3:
        tcp_host = sys.argv[3]
    
    message = get_starting_server_info("server", tcp_enabled, tcp_port, tcp_host, unix_path)
    print (message)    
              
    # Create threads for both the server and Flask
    server_thread = threading.Thread(target=start_server, args=(tcp_enabled, tcp_port, tcp_host, unix_path))
    flask_thread = threading.Thread(target=socketio.run, args=(website_app,), kwargs={'host': tcp_host, 'port': FLASK_PORT})

    # flask_thread = threading.Thread(target=socketio.run(website_app), kwargs={'host': tcp_host, 'port': FLASK_PORT})
    # flask_thread = threading.Thread(target=website_app.run, kwargs={'host': tcp_host, 'port': FLASK_PORT})
    flask_thread.daemon = True  # Terminate the Flask thread when the main thread exits
    server_thread.daemon = True
    
    # clear website (if someone has opened html).
    # Start the server thread first
    server_thread.start()

    # Start the Flask thread
    flask_thread.start()  
            
    # Wait for both threads to finish before exiting
    server_thread.join()
    flask_thread.join()
    
    # just to clear the table (if anyone leave website opened and restartes the server)  
    socketio.emit('refresh_matches')
