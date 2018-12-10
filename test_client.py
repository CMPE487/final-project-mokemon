import socket
HOST = socket.gethostbyname(socket.gethostname())
PORT = 5002
try:
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
      m = input("Enter: ")
      s.sendall(str.encode(m))
except:
  print("some problem")
