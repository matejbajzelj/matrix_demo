import random

def start_match(client_a_id, client_b_id, word_to_guess, match_id, active_matches,):
    # Generate a unique match ID (you can implement your logic)
    # Create a new match entry
    match = {
        'match_id': match_id,
        'client_a_id': client_a_id,
        'client_b_id': client_b_id,
        'word_to_guess': word_to_guess,
        'state': 'ongoing'  # You can use 'ongoing', 'completed', 'canceled', etc.
    }

    # Add the match to the list
    active_matches.append(match)

    return match

# Implement your own logic to generate unique IDs for clients
def generate_unique_match_id(min_auth_token_value, max_auth_token_value):
    # Generate a random ID for the client
    match_id = random.randint(min_auth_token_value, max_auth_token_value)        

    return match_id


def is_client_in_match(client_id, active_matches):
    for match in active_matches:
        # Check if either of the clients in the match matches the specified client_id
        if match['client_a'] == client_id or match['client_b'] == client_id:
            return True
    return False


def handle_start_match_request(client_id, opponent_id, word_to_guess):
    # Check if the specified opponent_id exists in the list of connected clients
    # and is available for a match (not already in a match)
    if find_client(opponent_id) and not is_client_in_match(opponent_id):
        # Create a match between client_id and opponent_id with the specified word to guess
        match = create_match(client_id, opponent_id, word_to_guess)
        # Inform both clients about the match
        inform_clients_about_match(client_id, opponent_id, match['match_id'], word_to_guess)
    else:
        # Inform the client that the match request is invalid (opponent not available)
        send_invalid_match_request_response(client_id)
