import socket
import threading
from tools.tools import decode_message, encode_message

# Define the correct password
correct_password = "mypass123"

def listen_clients(conn, addr):
    try:
        print(f"Connected by {addr}")
        # Set message to connected client
        # Send a response

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
            
            welcome_message = f"Initiating the communication. Client {addr} Send password"
            response = encode_message(0, welcome_message)
            conn.sendall(response)

             # Receive the password from the client
            data = conn.recv(1024)
            message_type, message_length, received_password = decode_message(data)            
            print("**** password: ****")
            print(received_password)
            if received_password == correct_password:
                 # Password is correct, send a success message and keep the connection alive
                success_message = "Password accepted. Connection established."
                success_message_data = encode_message(200, success_message)
                conn.sendall(success_message_data)

                client_thread = threading.Thread(target=listen_clients, args=(conn, addr))
                client_thread.start()

            else:
                # Password is incorrect, send an error message and close the connection
                error_message = "Incorrect password. Connection closed."
                error_message_data = encode_message(401, error_message)
                conn.sendall(error_message_data)
                conn.close()

if __name__ == "__main__":
    start_server()
