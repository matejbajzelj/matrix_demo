
def get_users(connected_clients):
    user_info_list = []
    for client_info in connected_clients:
        client_id, _, client_addr = client_info
        user_info = f"Client ID: {client_id}, Address: {client_addr[0]}, Port: {client_addr[1]}"
        user_info_list.append(user_info)
    
    # Send the list of connected users back to the client
    user_info_response = "\n".join(user_info_list)
    return user_info_response