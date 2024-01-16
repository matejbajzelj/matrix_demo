import socket
import select
import sys
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE

LISTEN_PORT = 65432

def start_client(host='127.0.0.1', port=LISTEN_PORT):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.setblocking(0)  # Set socket to non-blocking mode

    inputs = [client_socket, sys.stdin]
    outputs = []
    client_id = 0

    # Prompt for the password
    password = input("Enter your password: ")

    # Prepare and send the password with the custom binary protocol
    password_data = encode_message(E_MESSAGE_TYPE.PASSWORD_SENT, client_id, password)
    client_socket.sendall(password_data)

    try:
        while True:
            readable, writable, exceptional = select.select(inputs, outputs, inputs)

            for s in readable:
                if s is client_socket:
                    # Data is available to read from the server
                    data = s.recv(1024)
                    if not data:
                        print("Server closed the connection.")
                        return

                    message_type, message_length, auth_token, response = decode_message(data)

                    if message_type == E_MESSAGE_TYPE.ASSIGNED_ID:
                        client_id = auth_token
                        print(f"Client id stored: {client_id}")
                    elif message_type == E_MESSAGE_TYPE.NORMAL_COMMUNICATION:
                        print(f"{response}")
                    elif message_type == E_MESSAGE_TYPE.MATCH_INVITATION:
                        print(f"Received match invitation: {response}")
                         # Parse the match ID from the invitation message
                        match_id_start = response.find("#") + 1
                        match_id_end = response.find("#", match_id_start)
                        match_id = response[match_id_start:match_id_end]
                        
                         # Display the invitation message and offer options to accept or decline
                        print(f"Do you want to accept the match with id: {match_id}? (yes/no)")
                        user_input = input()
                        
                        if user_input.lower() == "yes":
                            # Send an acceptance message to the server
                            acceptance_message = encode_message(E_MESSAGE_TYPE.ACCEPT_MATCH, client_id, match_id)
                            client_socket.sendall(acceptance_message)

                        elif user_input.lower() == "no":
                            # Send a decline message to the server (optional)
                            decline_message = encode_message(E_MESSAGE_TYPE.DECLINE_MATCH, client_id, match_id)
                            client_socket.sendall(decline_message)

                elif s is sys.stdin:
                    # User entered a message
                    message = input("Enter a message to send to the server (or 'exit' to quit): ")
                    if message == 'exit':
                        return

                    message_type = E_MESSAGE_TYPE.NORMAL_COMMUNICATION
                    if message == "get users":
                        message_type = E_MESSAGE_TYPE.GET_USERS
                    elif message.startswith("start match with"):
                        message_type = E_MESSAGE_TYPE.START_MATCH
                    elif message == "get matches":
                        message_type = E_MESSAGE_TYPE.GET_MATCHES

                    data_to_send = encode_message(message_type, client_id, message)
                    client_socket.send(data_to_send)

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
