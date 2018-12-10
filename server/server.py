import traceback
import socket
from threading import Thread
from components import *

HOST = socket.gethostbyname(socket.gethostname())
TCP_PORT = 5002
BUFFER_SIZE = 1024
threads = []
rooms = {}

def handle_client(conn,addr):
  while True:
    try:
      data = ""
      current = conn.recv(BUFFER_SIZE)
      if current == b'':
        # client connection is lost
        print("exit", addr)
        break
      data = data + current.decode("utf-8")
      print("data: ",data)
      message = data.split(";")
      if message[0]=="discover":
        conn.sendall(str.encode("server;"+HOST))
      elif message[0]=="createRoom":
        r = Room(message[1],addr[0],message[2],conn)
        r.setCreatorConnection(conn)
        rooms[addr[0]] = r
      elif message[0] == "ready":
        creatorIP = message[1]
        playerType = message[2]
        if playerType == "creator":
          rooms[creatorIP].creatorReady = True
          if rooms[creatorIP].full:
            m = "readyNotification;"+rooms[creatorIP].creatorName
            rooms[creatorIP].participantConnection.sendall(str.encode(m))
        else:
          rooms[creatorIP].participantReady = True
          m = "readyNotification;"+rooms[creatorIP].participantName
          rooms[creatorIP].creatorConnection.sendall(str.encode(m))
        if rooms[creatorIP].participantReady and rooms[creatorIP].creatorReady:
          # TODO start game
          print("start game")
        else: 
          # TODO send ready notification to other
          pass
      elif message[0] == "listRooms":
        # TODO list only not full rooms
        print("listRooms",addr)
        message = "listRooms"
        for roomID,room in rooms.items():
          message = message +";"+ room.getListString()
        print("room list message: ",message)
        conn.sendall(str.encode(message))
      elif message[0] == "joinRoom":
        creatorIP = message[1]
        participantName = message[2]
        rooms[creatorIP].setParticipantInfo(participantName, addr[0], conn)
        rooms[creatorIP].full = True
        # TODO send join info back
        # conn.sendall(str.encode("joinInfo;"+HOST))
      elif message[0]=="status":
        print("Room Info: ")
        for roomID,room in rooms.items():
          print(room.getRoomLog())
      else:
        conn.sendall(str.encode("empty;message"))
    except Exception as e:
      traceback.print_exc()
    

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
    traceback.print_exc()

main()