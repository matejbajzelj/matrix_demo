from src_common.constants import MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE, PASSWORD
from src_common.tools import E_MESSAGE_TYPE, encode_message
from src_server.client_lib import find_client, generate_unique_id, add_client
from src_server.match import is_client_in_match, find_match_by_id, generate_unique_match_id, start_match
from src_common.messages import get_server_notification

def allow_client_futher(conn, addr, message_type, auth_token, connected_clients, message_from_client = ""):

    if auth_token >= MIN_AUTH_TOKEN_VALUE and find_client(auth_token, connected_clients):
        return True, auth_token

    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and message_from_client == PASSWORD:
        # Generate a random ID for the client
        client_id =  generate_unique_id(MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE)   
        add_client(conn, addr, client_id, connected_clients)
        return True, client_id
    
    return False, 0

def server_action_start_match(conn, client_id, message_from_client, auth_token, active_matches, connected_clients):
    if is_client_in_match(client_id, active_matches):
        # Client is already in a match, send an error response
        error_message = "You are already in a match."
        error_response_data = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_id, error_message)
        conn.sendall(error_response_data)
    else:
        parts = message_from_client.split()
        opponent_id = int(parts[3])
        word_to_guess = " ".join(parts[4:])
     
        isFound, opponentExist = find_client(opponent_id, connected_clients)
        
        if isFound:
            # Start the match and send a success response
            match_id = generate_unique_match_id(MIN_AUTH_TOKEN_VALUE, MAX_AUTH_TOKEN_VALUE)
            match = start_match(auth_token, opponent_id, word_to_guess, match_id, active_matches)
            message_to_sent = f"Match started with ID {match_id}. Your word to guess: {word_to_guess}"

            # sent invite to an opponent
            opponent_conn = opponentExist[1]
            invitation_message = f"Invitation to match #{match['match_id']}# with guess a word. Accept or Decline?"
            invitation_data = encode_message(E_MESSAGE_TYPE.MATCH_INVITATION, opponent_id, invitation_message)
            opponent_conn.sendall(invitation_data)
     
        else:
            # Opponent not found, send an error response
            message_to_sent = "Opponent not found."
            invitation_data = encode_message(E_MESSAGE_TYPE.MATCH_INVITATION, opponent_id, message_to_sent)
            opponent_conn.sendall(message_to_sent)
                        

def server_action_accepted_match(accepted_match_id, active_matches, connected_clients):
    
    isMatchFound, matchFound = find_match_by_id(accepted_match_id, 'match_id', active_matches)
    matchFound["state"] = "active" # set status

    client_a_id = matchFound["client_a_id"]
    client_b_id = matchFound["client_b_id"]

    # sent to client messate_Type
    # startedIsFound, started_client = find_client(started_client_id, connected_clients)           
    # invitation_data = encode_message(E_MESSAGE_TYPE.GAME_STARED, started_client_id, accepted_match_id)
    # staring_person_conn.sendall(invitation_data)

    is_client_a_found, client_a = find_client(client_a_id, connected_clients)
    client_a_conn = client_a[1]
    
    is_client_b_found, client_b = find_client(client_b_id, connected_clients)
    client_b_conn = client_b[1]
    
    message_to_send_to_a = get_server_notification(f"Match with id {accepted_match_id} started. You will be notified about progress")    
    client_a_message = encode_message(E_MESSAGE_TYPE.NORMAL_COMMUNICATION, client_b_id, message_to_send_to_a)
    client_a_conn.sendall(client_a_message)
    
    message_to_send_to_b = get_server_notification(f"Match with id {accepted_match_id} started. Try to guess a word.")    
    client_b_message = encode_message(E_MESSAGE_TYPE.GAME_STARED, client_b_id, message_to_send_to_b)
    client_b_conn.sendall(client_b_message)
        
def server_action_game_started(guess_word, auth_token, active_matches, connected_clients):
    isMatchFound, matchFound = find_match_by_id(auth_token, 'client_b_id', active_matches)
    
    started_client_id = matchFound['client_a_id']

    invitedIsFound, invited_client = find_client(auth_token, connected_clients)
    invited_person_conm = invited_client[1]

    startedIsFound, started_client = find_client(started_client_id, connected_clients)           
    staring_person_conn = started_client[1]
                        
    if (matchFound['word_to_guess'] == guess_word):
                
        matchFound["state"] = "won" # set status        
        invitation_data = encode_message(E_MESSAGE_TYPE.GAME_WON, auth_token, "You found a word. You WON!")
        invited_person_conm.sendall(invitation_data)

        staring_person_data = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, started_client_id, "Word was found. Client B Won")
        staring_person_conn.sendall(staring_person_data)
    else:
        matchFound['client_b_tries'] += 1
        invitation_data = encode_message(E_MESSAGE_TYPE.GAME_STARED, auth_token, f"Wrong word. You had {matchFound['client_b_tries']} tries")
        invited_person_conm.sendall(invitation_data)

        staring_person_data = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, started_client_id, f"Wrong word. Client B had {matchFound['client_b_tries']} tries")
        staring_person_conn.sendall(staring_person_data)
    
    
def server_action_sent_hint(message_from_client_a, auth_token, active_matches, connected_clients):
    
    isMatchFound, foundMatch = find_match_by_id(auth_token, 'client_a_id', active_matches)
    client_b_id = foundMatch['client_b_id']
    
    isClientBFound, client_b = find_client(client_b_id, connected_clients)
    client_b_conn = client_b[1]
    
    sent_hint = encode_message(E_MESSAGE_TYPE.GAME_NOTIFICATION, client_b_id, message_from_client_a)
    client_b_conn.sendall(sent_hint)
    
    print(f"{message_from_client_a}")