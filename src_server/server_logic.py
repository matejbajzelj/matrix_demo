from src_common.tools import E_MESSAGE_TYPE, encode_message, min_auth_token_value, max_auth_token_value, correct_password
from src_server.client_lib import find_client, generate_unique_id, add_client
from src_server.match import is_client_in_match, find_match, find_match_by_invited_id, generate_unique_match_id, start_match

def get_welcome_message(addr):
    message = []
    message.append("\n-----------------------Welcome message--------------------------\n")
    message.append( f"Initiating the communication. Client {addr} Send password")
    message.append("\n-----------------------End Welcome message----------------------\n")
    message_response = "".join(message)
    return message_response

def get_server_notification(message_to_sent):
    message = []
    message.append("\n-----------------------Server Warning--------------------------\n")
    message.append( f"{message_to_sent}")
    message.append("\n-----------------------End Server Warning----------------------\n")
    message_response = "".join(message)
    return message_response

def allow_client_futher(conn, addr, message_type, auth_token, connected_clients, message_from_client = ""):

    if auth_token >= min_auth_token_value and find_client(auth_token, connected_clients):
        return True, auth_token

    if message_type == E_MESSAGE_TYPE.PASSWORD_SENT and message_from_client == correct_password:
        # Generate a random ID for the client
        client_id =  generate_unique_id(min_auth_token_value, max_auth_token_value)   
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
            match_id = generate_unique_match_id(min_auth_token_value, max_auth_token_value)
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
    
    isMatchFound, matchFound = find_match(accepted_match_id, active_matches)
    matchFound["state"] = "active" # set status

    started_client_id = matchFound["client_a_id"]
    invited_client_id = matchFound["client_b_id"]

    # sent to client messate_Type
    # startedIsFound, started_client = find_client(started_client_id, connected_clients)           
    # invitation_data = encode_message(E_MESSAGE_TYPE.GAME_STARED, started_client_id, accepted_match_id)
    # staring_person_conn.sendall(invitation_data)

    invitedIsFound, invited_client = find_client(invited_client_id, connected_clients)
    invited_person_conm = invited_client[1]
    invitation_data = encode_message(E_MESSAGE_TYPE.GAME_STARED, invited_client_id, accepted_match_id)
    invited_person_conm.sendall(invitation_data)
        
def server_action_game_started(guess_word, auth_token, active_matches, connected_clients):
    isMatchFound, matchFound = find_match_by_invited_id(auth_token, active_matches)
    started_client_id = matchFound['client_a_id']

    invitedIsFound, invited_client = find_client(auth_token, connected_clients)
    invited_person_conm = invited_client[1]

    startedIsFound, started_client = find_client(started_client_id, connected_clients)           
    staring_person_conn = started_client[1]
                        
    if (matchFound['word_to_guess'] == guess_word):
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
    