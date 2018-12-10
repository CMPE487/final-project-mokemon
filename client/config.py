from socket import *

host = gethostbyname(gethostname())
port = 5002
username = "dummy"
DISCOVER_TIMEOUT = 1
BUFFER_SIZE = 1024
server_sock = None
currentState = None