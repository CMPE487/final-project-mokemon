import socket
from threading import Thread

HOST = socket.gethostbyname(socket.gethostname())
TCP_PORT = 5002
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response
threads = []

def handle_client(conn,addr):
  while True:
    data = ""
    current = conn.recv(BUFFER_SIZE)
    data = data + current.decode("utf-8")
    print("data: ",data)
    message = data.split(";")
    if message[0]=="discover":
      conn.sendall(str.encode("server;"+HOST))
    

def main():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.bind((HOST, TCP_PORT))
      s.listen(50)
      while True:
        conn, addr = s.accept()
        print(addr)
        t = Thread(target=handle_client,args=(conn, addr))
        t.daemon = True
        threads.append(t)
        t.start()
  except Exception as e:
    s.close()
    print(e)

main()