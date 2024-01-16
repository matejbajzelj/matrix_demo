import struct

def encode_message(message_type, payload):
    # message_type is an integer (0-255), payload is in string
    binary_payload = payload.encode("utf-8")
    message_length = len(binary_payload)

    # Big-endian: 1 byte for type, 2 bytes for length. 
    # B 8bit-int = unsigned char since I need only positive values for message_type, 
    # H 16bit int - Assume for demo 0-65535 is enough big int.
    header = struct.pack('>BH', message_type, message_length) 
    return header + binary_payload

def decode_message(binary_data):
    
    # Assuming binary_data is a bytes object containing a full message
    # first 3 bytes are (1 message type, 2 payload length)
    message_type, message_length = struct.unpack('>BH', binary_data[:3])
    message = binary_data[3:3+message_length]
    return message_type, message_length, message