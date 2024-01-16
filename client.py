import socket
from tools.tools import decode_message, encode_message, E_MESSAGE_TYPE



def start_client(host='127.0.0.1', port=65432):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        client_id = 0

        # Receive the welcome message from the server
        data = s.recv(1024)
        message_type, message_length, auth_token, response = decode_message(data)
      
        # Prompt for the password
        password = input("Enter your password: ")

        # Prepare and send the password with the custom binary protocol
        password_data = encode_message(E_MESSAGE_TYPE.PASSWORD_SENT, client_id, password)
        s.sendall(password_data)

        data = s.recv(1024)
        message_type, message_length, auth_token, response = decode_message(data)
        
        if message_type == E_MESSAGE_TYPE.ASSIGNED_ID:

            # store client id:
            client_id = auth_token
            print(f"Client id stored: {client_id}")

        if message_type == E_MESSAGE_TYPE.NORMAL_COMMUNICATION or message_type == E_MESSAGE_TYPE.ASSIGNED_ID:
     
            while True:
                # Prompt for user input
                message = input("Enter a message to send to the server (or 'exit' to quit):")

                message_type = E_MESSAGE_TYPE.NORMAL_COMMUNICATION
                if message == 'exit':
                    break  # Exit the loop and close the client
                elif message == "get users":
                    message_type = E_MESSAGE_TYPE.GET_USERS
                elif message.startswith("start match with"):                    
                    message_type = E_MESSAGE_TYPE.START_MATCH


                # Prepare and send the message with the custom binary protocol
                data_to_send = encode_message(message_type, client_id, message)
                s.sendall(data_to_send)

                # Receive a response
                data = s.recv(1024)
                message_type, message_length, auth_token, response = decode_message(data)
                
        else:
              # It's an error message (incorrect password)
            print(f"response from server: {response}")
            print("Connection closed.")
            s.close()

if __name__ == "__main__":
    start_client()