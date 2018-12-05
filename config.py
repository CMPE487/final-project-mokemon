from socket import *

host = gethostbyname(gethostname())
port = 5002
username = "dummy"
disc_pck_size = 1024
server_conn = None