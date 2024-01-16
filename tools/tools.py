import struct
my_binary_encode_format = '>HH'
my_string_encode_format = 'utf-8'

# picked message type and size, picked message length and size of var to make my header.
# don't know at this time if I need message-type but starting somewhere.
# types could be "ping or heartbeat", "error", "auth", "game related message"...

def encode_message(message_type, payload):
    # message_type is an integer (0-255), payload is in string
    binary_payload = payload.encode(my_string_encode_format)
    message_length = len(binary_payload)

    # Big-endian: 1 byte for type, 2 bytes for length. 
    # B 8bit-int = unsigned char since I need only positive values for message_type, 
    # H 16bit int - Assume for demo 0-65535 is enough big int.
    header = struct.pack(my_binary_encode_format, message_type, message_length) 
    return header + binary_payload

def decode_message(binary_data):
    
    # Assuming binary_data is a bytes object containing a full message
    # first 3 bytes are (1 message type, 2 payload length)
    message_type, message_length = struct.unpack(my_binary_encode_format, binary_data[:4])
    b_message = binary_data[4:4+message_length]
    s_message = b_message.decode(my_string_encode_format)

    # just to have printout in 1 place.
    print(f"Received b_message: {b_message}")
    print(f"Received s_message: {s_message}")
    print(f"Received message_type: {message_type}")
    print(f"Received message_length: {message_length}")
    
    return message_type, message_length, s_message