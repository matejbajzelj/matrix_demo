import socket
from tools.tools import decode_message, encode_message


def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Receive the welcome message from the server
        data = s.recv(1024)
        message_type, message_length, message = decode_message(data)
      
        # Prompt for the password
        password = input("Enter your password: ")

        # Prepare and send the password with the custom binary protocol
        password_data = encode_message(1, password)
        s.sendall(password_data)

        data = s.recv(1024)
        message_type, message_length, response = decode_message(data)

        if message_type == 200:
     
            while True:
                # Prompt for user input
                message = input("Enter a message to send to the server (or 'exit' to quit): ")

                if message == 'exit':
                    break  # Exit the loop and close the client

                # Prepare and send the message with the custom binary protocol
                data_to_send = encode_message(1, message)
                s.sendall(data_to_send)

                # Receive a response
                data = s.recv(1024)
                message_type, message_length, response = decode_message(data)
                
        else:
              # It's an error message (incorrect password)
            print(f"response from server: {response}")
            print("Connection closed.")

if __name__ == "__main__":
    start_client()
