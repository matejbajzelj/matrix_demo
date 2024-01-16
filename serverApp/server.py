import socket
import struct

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

                # Unpack received data
                message_length = struct.unpack('I', data[:4])[0]
                message = data[4:4 + message_length].decode('utf-8')
                print(f"Received message: {message}")

                # Send a response
                response = f"Received your message: {message}".encode('utf-8')
                response_length = struct.pack('I', len(response))
                conn.sendall(response_length + response)

if __name__ == "__main__":
    start_server()
