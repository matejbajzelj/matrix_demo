import socket
import select
import sys
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE

def start_client(host='127.0.0.1', port=65433):
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
                        print(f"Received message from server: {response}")
                    elif message_type == E_MESSAGE_TYPE.MATCH_INVITATION:
                        print(f"Received match invitation: {response}")

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
