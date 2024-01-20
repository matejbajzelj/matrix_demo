import random
from threading import Lock
from enum import Enum

# Create a list to store matches
all_matches = []
all_matches_lock = Lock()

class E_MATCH_STATUS(Enum):
    PENDING = 0,
    ACTIVE = 1,
    WON = 2,
    GIVE_UP = 3

# I added lock mechanisem, but I think in this simple demo program, would not need it, since
# it will be run by 2 clients, with high chance on runing on the same terminal, so 1 person has to write commands in 
# 2 clients and he can't do that fast to make problems. But in real case env, if you have multiple clients,
# lock would be prefered solution.
lock = Lock()

def start_match(client_a_id, client_b_id, word_to_guess, match_id):
    with lock:
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
            'status': E_MATCH_STATUS.PENDING,  # You can use 'ongoing', 'completed', 'canceled', etc.
            'client_a_tries': 0,
            'client_b_tries': 0
        }

        # Add the match to the list
        all_matches.append(match)

        return match

# Implement your own logic to generate unique IDs for clients
def generate_unique_match_id(min_auth_token_value, max_auth_token_value):
    # Generate a random ID for the client
    match_id = random.randint(min_auth_token_value, max_auth_token_value)        

    return match_id
    
def find_match_by_id(search_value, column_name:str = 'match_id'):
    with lock:
        isFound = False
        matchFound = None

        try:
            for match in all_matches:
                if int(match[column_name]) == int(search_value):
                    isFound = True
                    matchFound = match
                    break

            return isFound, matchFound
        except Exception as e:
            print(f"Error in find_match: {str(e)}")
            # Handle the error here if needed
            return False, matchFound    

def update_match_status(match_id, match_status:E_MATCH_STATUS):
    
    isFound, match = find_match_by_id(match_id)
    if isFound:
        with lock:
            match['status'] = match_status
            return True
    
    return False

def increase_match_tries(match_id):
    
    isFound, match = find_match_by_id(match_id)
    if isFound:
        with lock:
            match['client_b_tries'] += 1
            return match['client_b_tries']
    
    return -1

def remove_match(match_id):
    with lock:
        for match in all_matches:
            if int(match['match_id']) == int(match_id):
                all_matches.remove(match)
    
def is_client_in_match(client_id, match_status:E_MATCH_STATUS = E_MATCH_STATUS.ACTIVE):
    with lock:
        for match in all_matches:
            # Check if either of the clients in the match matches the specified client_id
            if (match['client_a'] == client_id or match['client_b'] == client_id) and match['status'] == match_status:
                return True
        return False

def get_all_matches():
    with all_matches_lock:
        return all_matches.copy()
