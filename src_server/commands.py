
def get_users(connected_clients):
    user_info_list = []
    user_info_list.append("\n--------------------------User List----------------------------\n")
    
    if not connected_clients:
        user_info_list.append("No users. List is empty.")
    else:        
        for client_info in connected_clients:
            client_id, _, client_addr = client_info
            user_info = f"Client ID: {client_id}, Address: {client_addr[0]}, Port: {client_addr[1]}"
            user_info_list.append(user_info)
    
    user_info_list.append("\n-----------------------End User List----------------------------\n")
    # Send the list of connected users back to the client
    user_info_response = "\n".join(user_info_list)
    return user_info_response


def get_matches(active_matches):
    match_info_list = []
    match_info_list.append("\n--------------------------Match List----------------------------\n")
    
    if not active_matches:
        match_info_list.append("No matches started. List is empty.")
    else:    
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

    match_info_list.append("\n-----------------------End Match List----------------------------\n")
    # Concatenate match information strings
    matches_output = "\n".join(match_info_list)
    return matches_output    