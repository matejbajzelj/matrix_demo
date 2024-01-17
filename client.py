import socket
import select
import sys
from src_client.client_logic import client_receive, client_sent
from src_common.tools import encode_message, E_MESSAGE_TYPE, LISTEN_PORT

def start_client(host='127.0.0.1', port=LISTEN_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
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
    start_client()
