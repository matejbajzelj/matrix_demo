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

def find_match(match_id, matches):
    isFound = False
    matchFound = None

    try:
        print(f"find_match 1 match_id: {match_id}")
        print(f"find_match 1 match count: {len(matches)}")
        for match in matches:
            print("find_match 2")
            print(f"find_match 2: ID {match['match_id']}")

            array_match_id = match['match_id'] 
            print(f"find_match 2: array_match_id {array_match_id}")
            print(f"find_match 2: array_match_id==match_id {int(array_match_id)==int(match_id)}")

            if int(match['match_id']) == int(match_id):
                print("find_match 3 Found")
                isFound = True
                matchFound = match
                break

        print("find_match 4")
        return isFound, matchFound
    except Exception as e:
        print(f"Error in find_match: {str(e)}")
        # Handle the error here if needed
        return False, matchFound

def find_match_by_invited_id(client_b_id, matches):
    isFound = False
    matchFound = None

    try:
        print(f"find_match_by_invited_id 1 client_b_id: {client_b_id}")
        print(f"find_match_by_invited_id 1 match count: {len(matches)}")
        for match in matches:
            print("find_match_by_invited_id 2")
            print(f"find_match_by_invited_id 2: client_b_id {match['client_b_id']}")

            if int(match['client_b_id']) == int(client_b_id):
                print("find_match_by_invited_id 3 Found client_b_id")
                isFound = True
                matchFound = match
                break

        print("find_match_by_invited_id 4")
        return isFound, matchFound
    except Exception as e:
        print(f"Error in find_match_by_invited_id: {str(e)}")
        # Handle the error here if needed
        return False, matchFound        


def remove_match(match_id, active_matches):
    print(f"remove_match 1 match_id: {match_id}")
    print(f"remove_match 1 match len: {len(active_matches)}")
    for match in active_matches:
        print("remove_match 2")
        if int(match['match_id']) == int(match_id):
            print("remove_match Found match_id")
            active_matches.remove(match)
            print(f"remove_match {match_id} removed")


def is_client_in_match(client_id, active_matches):
    for match in active_matches:
        # Check if either of the clients in the match matches the specified client_id
        if match['client_a'] == client_id or match['client_b'] == client_id:
            return True
    return False

