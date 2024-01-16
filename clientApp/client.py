import socket
import struct

def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Prepare message with a custom binary protocol
        message = "Hello, Server!".encode('utf-8')
        message_length = struct.pack('I', len(message))
        s.sendall(message_length + message)

        # Receive a response
        data = s.recv(1024)
        response_length = struct.unpack('I', data[:4])[0]
        response = data[4:4 + response_length].decode('utf-8')
        print(f"Received response: {response}")

if __name__ == "__main__":
    start_client()
