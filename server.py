import socket
import threading
from tools.tools import decode_message, encode_message

def listen_clients(conn, addr):
    try:
        print(f"Connected by {addr}")

        while True:
            data = conn.recv(1024)
            if not data:
                break

            # Unpack received data
            message_type, message_length, message = decode_message(data)
            print(f"Received message from {addr}: {message}")
            print(f"Received message_type: {message_type}")
            print(f"Received message_length: {message_length}")

            # Send a response
            response = encode_message(1, f"Received your message: {message}")
            conn.sendall(response)
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
            client_thread = threading.Thread(target=listen_clients, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()
