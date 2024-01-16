import socket
from tools.tools import decode_message, encode_message

def start_server(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print(f"Server listening on {host}:{port}")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                # Unpack received dataI pick
                message_type, message_length, message = decode_message(data)
                print(f"Received message: {message}")
                print(f"Received message_type: {message_type}")
                print(f"Received message_length: {message_length}")

                # Send a response
                response = encode_message(1, f"Received your message: {message}")
                conn.sendall(response)

if __name__ == "__main__":
    start_server()
