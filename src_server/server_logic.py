from src_common.constants import MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE, PASSWORD
from src_common.tools import E_MESSAGE_TYPE, encode_message
from src_server.client_lib import find_client, generate_unique_id, add_client
from src_common.messages import get_server_notification
from src_server.match_lib import (remove_match,
                                  is_client_in_match,
                                  find_match_by_id,
                                  find_match_by_custom_id,
                                  generate_unique_match_id,
                                  start_match,
                                  update_match_status,
                                  increase_match_tries,
                                  E_MATCH_STATUS)


def allow_client_further(conn, addr, message_type, auth_token, message_from_client = ""):
    
    if auth_token >= MIN_AUTH_TOKEN_VALUE and find_client(auth_token):
        return True, auth_token

    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and message_from_client == PASSWORD:
        # Generate a random ID for the client
        client_id =  generate_unique_id(MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE)   
        add_client(conn, addr, client_id)
        return True, client_id
    
    return False, 0


def server_action_start_match(client_a_conn, client_a_id, message_from_client):
    
    # TODO - add reuse logic if client is in pending match. So use that match.
    active_match_exist = is_client_in_match(client_a_id)
    pending_match_exist = is_client_in_match(client_a_id, E_MATCH_STATUS.PENDING)
    
    if active_match_exist:
        # Client is already in a match, send an error response
        error_message = get_server_notification("You are already in a active match.")
        error_response_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, error_message)
        client_a_conn.sendall(error_response_data)
    elif pending_match_exist:
        # Client is already in a match, send an error response
        error_message = get_server_notification("You are already in a pending match.")
        error_response_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, error_message)
        client_a_conn.sendall(error_response_data)
    else:
        parts = message_from_client.split()
        client_b_id = int(parts[3])
        word_to_guess = " ".join(parts[4:])
     
        found_client_b, client_b = find_client(client_b_id)
        
        if word_to_guess == "":
            # Opponent not found, send an error response
            client_a_message = get_server_notification("No word provided for the game. Please start a match with all parameters.")
            client_a_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, client_a_message)
            client_a_conn.sendall(client_a_data)
            
        elif client_a_id == client_b_id:
            # Opponent not found, send an error response
            client_a_message = get_server_notification("You cannot start a match with your self.")
            client_a_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, client_a_message)
            client_a_conn.sendall(client_a_data)
        
        elif found_client_b:
            # Start the match and send a success response
            match_id = generate_unique_match_id(MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE)
            match = start_match(client_a_id, client_b_id, word_to_guess, match_id)
            client_a_message = get_server_notification(f"Match started with ID {match_id}. Your word to guess: {word_to_guess}")
            client_a_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, client_a_message)
            client_a_conn.sendall(client_a_data)
            
            # sent invite to an opponent
            client_b_conn = client_b[1]
            client_b_message = get_server_notification(f"Invitation to match #{match['match_id']}# with guess a word. Accept or Decline?")
            client_b_data = encode_message(E_MESSAGE_TYPE.MATCH_INVITATION, client_b_id, client_b_message)
            client_b_conn.sendall(client_b_data)

        else:
            # Opponent not found, send an error response
            client_a_message = get_server_notification(f"Client B with id {client_b_id} not found.")
            client_a_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, client_a_message)
            client_a_conn.sendall(client_a_data)
                        

def server_action_accepted_match(s_accepted_match_id:str):
    accepted_match_id = int(s_accepted_match_id)
    isMatchFound, matchFound = find_match_by_id(accepted_match_id)
    update_match_status(accepted_match_id, E_MATCH_STATUS.ACTIVE)
    
    client_a_id = matchFound["client_a_id"]
    client_b_id = matchFound["client_b_id"]

    is_client_a_found, client_a = find_client(client_a_id)
    client_a_conn = client_a[1]
    
    is_client_b_found, client_b = find_client(client_b_id)
    client_b_conn = client_b[1]
    
    message_to_send_to_a = get_server_notification(f"Match with id {accepted_match_id} started. You will be notified about progress")    
    client_a_message = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_b_id, message_to_send_to_a)
    client_a_conn.sendall(client_a_message)
    
    message_to_send_to_b = get_server_notification(f"Match with id {accepted_match_id} started. Try to guess a word.")    
    client_b_message = encode_message(E_MESSAGE_TYPE.GAME_STARED, client_b_id, message_to_send_to_b)
    client_b_conn.sendall(client_b_message)
 
    
def server_action_declined_match(accepted_match_id):
        
    isMatchFound, matchFound = find_match_by_id(accepted_match_id)
    remove_match(accepted_match_id)
    
    client_a_id = matchFound["client_a_id"]
    client_b_id = matchFound["client_b_id"]

    is_client_a_found, client_a = find_client(client_a_id)
    client_a_conn = client_a[1]
    
    is_client_b_found, client_b = find_client(client_b_id)
    client_b_conn = client_b[1]
    
    message_to_send_to_a = get_server_notification(f"Match with id {accepted_match_id} was declined")
    client_a_message = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_a_id, message_to_send_to_a)
    client_a_conn.sendall(client_a_message)
    
    message_to_send_to_b = get_server_notification(f"Match with id {accepted_match_id} was declined by client_b: {client_b_id}")
    client_b_message = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_b_id, message_to_send_to_b)
    client_b_conn.sendall(client_b_message)
    
    
def server_action_game_started(guess_word, client_b_id):
    isMatchFound, matchFound = find_match_by_custom_id(int(client_b_id), 'client_b_id', E_MATCH_STATUS.ACTIVE)    
    client_a_id = matchFound['client_a_id']    
    match_id = matchFound['match_id']
    
    client_b_found, client_b = find_client(client_b_id)
    client_b_conn = client_b[1]

    client_a_found, client_a = find_client(client_a_id)           
    client_a_conn = client_a[1]
                        
    if (matchFound['word_to_guess'] == guess_word):
        
        update_match_status(match_id, E_MATCH_STATUS.WON)
        client_b_message = encode_message(E_MESSAGE_TYPE.GAME_WON, client_b_id, "You found a word. You WON!")
        client_b_conn.sendall(client_b_message)

        client_a_message = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, client_a_id, "Word was found. Client B Won")
        client_a_conn.sendall(client_a_message)
    else:
        client_b_match_tries = increase_match_tries(match_id)
        client_b_message = encode_message(E_MESSAGE_TYPE.GAME_STARED, client_b_id, f"Wrong word. You had {client_b_match_tries} tries")
        client_b_conn.sendall(client_b_message)

        client_a_message = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, client_a_id, f"Wrong word. Client B had {client_b_match_tries} tries")
        client_a_conn.sendall(client_a_message)
        
        
def server_action_game_give_up(client_b_id):
    isMatchFound, matchFound = find_match_by_custom_id(client_b_id, 'client_b_id', E_MATCH_STATUS.ACTIVE )
    client_a_id = matchFound['client_a_id']
    match_id = matchFound['match_id']
    
    client_b_found, client_b = find_client(client_b_id)
    client_b_conn = client_b[1]

    client_a_found, client_a = find_client(client_a_id)
    client_a_conn = client_a[1]
    
    message_type = E_MESSAGE_TYPE.GAME_GIVE_UP
    message_for_client_a, message_for_client_b = '',''
    message_for_client_b = get_server_notification("Game was Stopped. You gave up, You lose.")
    message_for_client_a = get_server_notification(f"Game was Stopped. Client B: {client_b_id} Gave up.")
        
    if matchFound['status'] == E_MATCH_STATUS.ACTIVE:    
        update_match_status(match_id, E_MATCH_STATUS.GIVE_UP)
        
    client_b_message = encode_message(message_type, client_b_id, message_for_client_b)
    client_b_conn.sendall(client_b_message)

    client_a_message = encode_message(message_type, client_a_id, message_for_client_a)
    client_a_conn.sendall(client_a_message)
    
    
def server_action_sent_hint(message_from_client_a, client_a_id):
    
    isMatchFound, foundMatch = find_match_by_custom_id(client_a_id, 'client_a_id', E_MATCH_STATUS.ACTIVE)
    client_b_id = foundMatch['client_b_id']
    
    client_b_found, client_b = find_client(client_b_id)
    client_b_conn = client_b[1]
    
    sent_hint = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, client_b_id, message_from_client_a)
    client_b_conn.sendall(sent_hint)
    
    print(f"{message_from_client_a}")