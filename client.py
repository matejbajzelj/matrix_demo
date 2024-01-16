import socket
from tools.tools import decode_message, encode_message


def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Prepare message with a custom binary protocol
        data_to_sent = encode_message(1, f"Hello, Server!")
        s.sendall(data_to_sent)

        # Receive a response
        data = s.recv(1024)
        message_type, message_length, message = decode_message(data)
        print(f"Received message_type: {message_type}")
        print(f"Received message_length: {message_length}")
        print(f"Received message: {message}")

if __name__ == "__main__":
    start_client()
