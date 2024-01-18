# Constants
BINARY_ENCODE_FORMAT = '>BHI' # 1bytes, 2bytes, 4 bytes
STRING_ENCODE_FORMAT = 'utf-8'
PASSWORD = "pass123"
MIN_AUTH_TOKEN_VALUE = 1000000000
MAX_AUTH_TOKEN_VALUE = 4294967295 # 4 bytes 32 bits
TCP_PORT = 65433
TCP_ENABLED = True  # Set to True for TCP, False for Unix socket
TCP_HOST = '127.0.0.1'  # Host for TCP
UNIX_PATH = "/tmp/my_unix_socket.sock"  # Path for Unix socket