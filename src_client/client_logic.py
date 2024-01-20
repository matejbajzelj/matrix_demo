from src_common.tools import encode_message, decode_message, E_MESSAGE_TYPE
import socket

def client_receive(client_socket:socket.socket, data_from_server:str, client_id:int, is_game_started:bool, got_welcome_message:bool):
    
    message_type, message_length, auth_token, response = decode_message(data_from_server)

    if message_type == E_MESSAGE_TYPE.ASSIGNED_ID:
        client_id = auth_token
        print(f"{response}")
        
    elif message_type == E_MESSAGE_TYPE.NORMAL_COMMUNICATION:
        print(f"{response}")
        
    elif message_type == E_MESSAGE_TYPE.GAME_STARED:
        is_game_started = True        
        print(f"{response}")

    elif message_type == E_MESSAGE_TYPE.GAME_NOTIFICATION:
        print(f"{response}")
        
    elif message_type == E_MESSAGE_TYPE.GAME_WON or message_type == E_MESSAGE_TYPE.GAME_GIVE_UP:
        is_game_started = False
        print(f"{response}")
        
    elif message_type == E_MESSAGE_TYPE.WELCOME_MESSAGE:
        got_welcome_message = True
        print(f"{response}")
        # Prompt for the password
        password = input("Enter your password: ")

        # Prepare and send the password with the custom binary protocol
        password_data = encode_message(E_MESSAGE_TYPE.PASSWORD_SENT, client_id, password)
        client_socket.sendall(password_data)

    elif message_type == E_MESSAGE_TYPE.MATCH_INVITATION:
        print(f"Received match invitation: {response}")
        # Parse the match ID from the invitation message
        match_id_start = response.find("#") + 1
        match_id_end = response.find("#", match_id_start)
        match_id = response[match_id_start:match_id_end]
        
        # Display the invitation message and offer options to accept or decline
        print(f"Do you want to accept the match with id: {match_id}? (yes/no)")
        user_input = input("Command: ")
        
        if user_input.lower() == "yes":
            # Send an acceptance message to the server
            acceptance_message = encode_message(E_MESSAGE_TYPE.ACCEPT_MATCH, client_id, match_id)
            client_socket.sendall(acceptance_message)

        elif user_input.lower() == "no":
            # Send a decline message to the server (optional)
            decline_message = encode_message(E_MESSAGE_TYPE.DECLINE_MATCH, client_id, match_id)
            client_socket.sendall(decline_message)
    else:
         print(f"{response}")              
         
     # Add an input prompt for the user to enter a new command               
    return client_id, is_game_started, got_welcome_message
            
def client_sent(client_socket, message_for_server, client_id, is_game_started):
    message_type = E_MESSAGE_TYPE.NORMAL_COMMUNICATION
    
    if message_for_server == "get users":
        message_type = E_MESSAGE_TYPE.GET_USERS
        
    elif message_for_server.startswith("start match with"):
        message_type = E_MESSAGE_TYPE.START_MATCH
        
    elif message_for_server == "get matches":
        message_type = E_MESSAGE_TYPE.GET_MATCHES
        
    elif message_for_server == "show my id":
        print(f"Your id: {client_id}")
        return
    
    elif message_for_server == "help":
        message_type = E_MESSAGE_TYPE.HELP
        
    elif is_game_started == True:
        if message_for_server == "give up":
            message_type = E_MESSAGE_TYPE.GAME_GIVE_UP
        else:
            message_type = E_MESSAGE_TYPE.GAME_STARED

    elif message_for_server.startswith("hint:"):
        message_type = E_MESSAGE_TYPE.GAME_SENT_HINT
  
    else:
        print("No known command.")
        return

    data_to_send = encode_message(message_type, client_id, message_for_server)
    client_socket.send(data_to_send)
