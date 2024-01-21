def get_starting_server_info(program_type:str, tcp_enabled:bool, tcp_port:int, tcp_host:str, unix_path:str):
    
    mode = 'TCP MODE' if tcp_enabled else 'UNIX MODE'
    
    message = []
    message.append(f"\n-----------------------{program_type} Starting Info--------------------------\n")
    message.append( f"{program_type} running in: {mode}\n")
    if tcp_enabled:
        message.append( f"TCP PORT:  {tcp_port}\n")
        message.append( f"TCP HOST:  {tcp_host}\n")        
    else:
        message.append( f"UNIX PATH:  {unix_path}\n")
    
    message.append(f"\nPossible ways to start the {program_type} in 2 different modes:\n")
    message.append(f"1. TCP MODE:  paython {program_type}.py true 65433 127.0.0.1\n")
    message.append(f"2. UNIX MODE: paython {program_type}.py false /tmp/my_unix_socket.sock\n")
    message.append(f"2. UNIX MODE: paython {program_type}.py false /tmp/my_unix_socket.sock\n")
    get_help_message
    message.append(f"-----------------------End {program_type} info----------------------")
    message_response = "".join(message)
    return message_response

def get_welcome_message(addr):
    message = []
    message.append("\n-----------------------Welcome message--------------------------\n")
    message.append( f"Initiating the communication. Client {addr} Send password\n")
    message.append( "For list of commands, use 'help' \n")
    message.append( "Password is 'pass123' ")
    message.append("\n-----------------------End Welcome message----------------------\n")
    message_response = "".join(message)
    return message_response


def get_server_notification(message_to_sent):
    message = []
    message.append("\n-----------------------Server Notification--------------------------\n")
    message.append( f"{message_to_sent}")
    message.append("\n-----------------------End Server Notification----------------------\n")
    message_response = "".join(message)
    return message_response

def get_help_message():
    message = []
    message.append("\n-----------------------Help message--------------------------\n")
    message.append( f"List of commands possible:\n")
    message.append( f"Password: pass123\n")
    message.append( f" 'get users' - Will return list of users connected\n")
    message.append( f" 'get matches' - will return list of matches (regardles of state)\n")
    message.append( f" 'show my id' - Will display to a client his ID\n")
    message.append( " 'start match with {id} {word_to_guess}' \n")
    message.append( f"During a match, client starting a match, can sent a hint with 'hint: it is growing in the forest' \n")
    message.append( f"During a match, client guessing, can give up with 'give up' input \n")
    message.append("\n-----------------------End Help message----------------------\n")
    message_response = "".join(message)
    return message_response