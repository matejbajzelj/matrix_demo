import random

def start_match(client_a_id, client_b_id, word_to_guess, match_id, active_matches,):
    print(f"start_match 1 client_a_id: {client_a_id}")
    print(f"start_match 1 client_b_id: {client_b_id}")
    print(f"start_match 1 word_to_guess: {word_to_guess}")
    print(f"start_match 1 match_id: {match_id}")
    # Generate a unique match ID (you can implement your logic)
    # Create a new match entry
    match = {
        'match_id': match_id,
        'client_a_id': client_a_id,
        'client_b_id': client_b_id,
        'word_to_guess': word_to_guess,
        'state': 'pending',  # You can use 'ongoing', 'completed', 'canceled', etc.
        'client_a_tries': 0,
        'client_b_tries': 0
    }

    # Add the match to the list
    active_matches.append(match)

    return match

# Implement your own logic to generate unique IDs for clients
def generate_unique_match_id(min_auth_token_value, max_auth_token_value):
    # Generate a random ID for the client
    match_id = random.randint(min_auth_token_value, max_auth_token_value)        

    return match_id

    
def find_match_by_id(search_value, column_name, matches):
    isFound = False
    matchFound = None

    try:
        for match in matches:
            if int(match[column_name]) == int(search_value):
                isFound = True
                matchFound = match
                break

        return isFound, matchFound
    except Exception as e:
        print(f"Error in find_match: {str(e)}")
        # Handle the error here if needed
        return False, matchFound    

def remove_match(match_id, active_matches):
    for match in active_matches:
        if int(match['match_id']) == int(match_id):
            active_matches.remove(match)
    
def is_client_in_match(client_id, active_matches):
    for match in active_matches:
        # Check if either of the clients in the match matches the specified client_id
        if match['client_a'] == client_id or match['client_b'] == client_id:
            return True
    return False

