import struct
from enum import Enum

my_binary_encode_format = '>HHI' # 2bytes, 2bytes, 4 bytes
my_string_encode_format = 'utf-8'

class E_MESSAGE_TYPE(Enum):
    AUTHENTICATION_REJECTED = 401
    PASSWORD_ACCEPETED = 201
    ASSIGNED_ID = 3
    NORMAL_COMMUNICATION = 1
    PASSWORD_SENT = 4
    WELCOME_MESSAGE = 0
    ERROR = 500
    GET_USERS = 5

# picked message type and size, picked message length and size of var to make my header.
# don't know at this time if I need message-type but starting somewhere.
# types could be "ping or heartbeat", "error", "auth", "game related message"...

def encode_message(message_type:E_MESSAGE_TYPE, auth_token:int, payload:str):
    # print(f"encode_message: {payload}")
    # message_type is an integer (0-255), payload is in string
    binary_payload = payload.encode(my_string_encode_format)
    message_length = len(binary_payload)
    i_message_type = int(message_type.value)
    # Big-endian: 2 byte for type, 2 bytes for length, 4 byte for auth_token. 
    # H 16bit int - Assume for demo 0-65535 is enough big int.
    # I 32bit - 4 bytes 4,294,967,295
    header = struct.pack('>HHI', i_message_type, message_length, auth_token) 
    print(f"Send data: {header + binary_payload}")
    return header + binary_payload

def decode_message(binary_data):
    
    # Assuming binary_data is a bytes object containing a full message
    # first 8 bytes are (2 message type, 2 payload length, 4 bytes auth token) header
    i_message_type, message_length, auth_token = struct.unpack(my_binary_encode_format, binary_data[:8])
    b_message = binary_data[8:8+message_length]
    s_message = b_message.decode(my_string_encode_format)
    
    message_type = E_MESSAGE_TYPE(i_message_type)

    # just to have printout in 1 place.
    # print(f"Received b_message: {b_message}")
    print(f"Received s_message: {s_message}")
    print(f"Received message_type: {message_type}")
    # print(f"Received message_length: {message_length}")
    # print(f"Received auth_token: {auth_token}")
    
    return message_type, message_length, auth_token, s_message