from config import *
from sys import stdin
from socket import *
from threading import Thread

def send_discover_message(to, pck):
	try:
		sock = socket(AF_INET, SOCK_STREAM)
		sock.connect(to)
		sock.send(bytes(pck, "utf8"))
		resp = sock.recv(disc_pck_size)
		data = resp.decode("utf8")
		print("data is: ", data)
		## "server" ; host_ip
		tag, server_ip = data.split(";")
		if tag == "server":
			global server_sock
			server_sock = sock
		else:
			server_sock = None
	except Exception as e:
		print("server is not: ", to, " and ", e)

def connect_to_server():
  arr = host.split(".")
  arr.pop()
  ip = ".".join(arr)
  threads = []
  for i in range(201, 202):
    req_ip = ip + "." + str(i)
    if req_ip==host:
      continue
    discover_pck = "discover;" + host + ";" + username
    thread = Thread(target=send_discover_message, args=((req_ip, port), discover_pck))
    threads.append(thread)
    thread.start()
  for thread in threads:
  	thread.join()

while(True):
	print("connecting to server..")
	connect_to_server()
	if(server_sock is None):
		print("Server not found")
		choice = input("would you like to try again")
		if choice == "yes":
			continue
		else:
			exit()
	else:
		print("connected successfully")
		break

while(True):
	server_sock.send(b"dnm pack")







