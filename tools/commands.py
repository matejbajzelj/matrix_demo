
def get_users(connected_clients):
    if not connected_clients:
        return "No users. List is empty."

    user_info_list = []
    for client_info in connected_clients:
        client_id, _, client_addr = client_info
        user_info = f"Client ID: {client_id}, Address: {client_addr[0]}, Port: {client_addr[1]}"
        user_info_list.append(user_info)
    
    # Send the list of connected users back to the client
    user_info_response = "\n".join(user_info_list)
    return user_info_response


def get_matches(active_matches):
    if not active_matches:
        return "No matches started. List is empty."

    match_info_list = []
    for match in active_matches:
        match_id = match['match_id']
        client_a_id = match['client_a_id']
        client_b_id = match['client_b_id']
        match_state = match['state']
        client_a_tries = match['client_a_tries']
        client_b_tries = match['client_b_tries']

        # Create a string with match information
        match_info_str = f"Match ID: {match_id}, Client A: {client_a_id}, Client B: {client_b_id}, State: {match_state}, A tries: {client_a_tries}, B tries: {client_b_tries}"
        match_info_list.append(match_info_str)

    # Concatenate match information strings
    matches_output = "\n".join(match_info_list)
    return matches_output    