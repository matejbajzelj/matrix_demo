import struct
from enum import Enum
from src_common.constants import BINARY_ENCODE_FORMAT, STRING_ENCODE_FORMAT

class E_MESSAGE_TYPE(Enum):
    WELCOME_MESSAGE = 0
    AUTHENTICATION_REJECTED = 1
    PASSWORD_ACCEPETED = 2
    ASSIGNED_ID = 3
    NORMAL_COMMUNICATION = 4
    PASSWORD_SENT = 5    
    ERROR = 6
    GET_USERS = 7
    START_MATCH = 8
    MATCH_INVITATION = 9
    ACCEPT_MATCH = 10
    DECLINE_MATCH = 11
    GET_MATCHES = 12
    GAME_STARED = 13
    GAME_WON = 14
    GAME_NOTIFICATION = 15
    GAME_SENT_HINT = 16
    GAME_GIVE_UP = 17
    HELP = 18


# picked message type and size, picked message length and size of var to make my header.
# don't know at this time if I need message-type but starting somewhere.
# types could be "ping or heartbeat", "error", "auth", "game related message"...
# # Big-endian: 2 byte for type, 2 bytes for length, 4 byte for auth_token. 
def encode_message(message_type:E_MESSAGE_TYPE, auth_token:int, payload:str):
    # print(f"encode_message: {payload}")
    # message_type is an integer (0-255), payload is in string
    binary_payload = payload.encode(STRING_ENCODE_FORMAT)
    message_length = len(binary_payload)
    i_message_type = int(message_type.value)
    # B  8bit int - Assume for demo 0-255 is enough.
    # H 16bit int - Assume for demo 0-65535 is enough big int.
    # I 32bit - 4 bytes 4,294,967,295
    header = struct.pack(BINARY_ENCODE_FORMAT, i_message_type, message_length, auth_token) 
    # print(f"Send data: {header + binary_payload}")
    return header + binary_payload

def decode_message(binary_data):
    
    # Assuming binary_data is a bytes object containing a full message
    # first 7 bytes are (1bytes message type, 2bytes payload length, 4bytes auth token) header
    i_message_type, message_length, auth_token = struct.unpack(BINARY_ENCODE_FORMAT, binary_data[:7])
    b_message = binary_data[7:7+message_length]
    s_message = b_message.decode(STRING_ENCODE_FORMAT)
    
    message_type = E_MESSAGE_TYPE(i_message_type)

    # just to have printout in 1 place.
    # print(f"Received b_message: {b_message}")
    # print(f"{s_message}")
    # print(f"Received message_type: {message_type}")
    # print(f"Received message_length: {message_length}")
    # print(f"Received auth_token: {auth_token}")
    
    return message_type, message_length, auth_token, s_message