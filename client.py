import socket
import select
import sys
from src_client.client_logic import client_receive, client_sent
from src_common.messages import get_server_notification, get_welcome_message, get_starting_server_info
from src_common.constants import TCP_ENABLED, TCP_PORT, TCP_HOST, UNIX_PATH

def start_client(tcp_enabled:bool, tcp_port:int, tcp_host:str, unix_path:str):
    if tcp_enabled:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((tcp_host, tcp_port))
    else:
        client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client_socket.connect(unix_path)
        
    client_socket.setblocking(0)  # Set socket to non-blocking mode

    inputs = [client_socket, sys.stdin]
    outputs = []
    client_id = 0
    is_game_started = False
    got_welcome_message = False

    try:
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            for s in readable:
                if s is client_socket:
                    # Data is available to read from the server
                    data_from_server = s.recv(1024)
                    if not data_from_server:
                        print("Server closed the connection.")
                        return

                    # handle data you get from the server
                    client_id_response, is_game_started_response, welcome_mess_resp = client_receive(client_socket, data_from_server, client_id, is_game_started, got_welcome_message)
                    client_id = client_id_response
                    is_game_started = is_game_started_response
                    got_welcome_message = welcome_mess_resp
                    
                elif s is sys.stdin:
                    # User entered a message
                    message_for_server = input("")
                    if message_for_server == 'exit':
                        client_socket.close()
                        return

                    # handle data before sending to server
                    client_sent(client_socket, message_for_server, client_id, is_game_started)
            
            for s in exceptional:
                print(f"Error with {s}")
                s.close()
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)

    except KeyboardInterrupt:
        print("Client terminated.")
    finally:
        client_socket.close()

if __name__ == "__main__":
    # USE TCP:  paython client.py true 65433 127.0.0.1
    # USE UNIX: paython client.py false /tmp/my_unix_socket.sock
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
    
    message = get_starting_server_info("Client", tcp_enabled, tcp_port, tcp_host, unix_path)
    print (message)
    start_client(tcp_enabled, tcp_port, tcp_host, unix_path)
