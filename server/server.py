import traceback
import socket
from threading import Thread
from components import *
from monsters import *

HOST = socket.gethostbyname(socket.gethostname())
TCP_PORT = 5000
BUFFER_SIZE = 1024
threads = []
rooms = {}
battles = {}
mainScreenUsers = []

def sendRoomNotification(r):
  message = "listRooms;"+r.getListString()
  for wConn in mainScreenUsers:
    wConn.sendall(str.encode(message))

def sendAllRoomNotification(conn):
  print("sendall room")
  print(rooms)
  message = "listRooms"
  for roomID,room in rooms.items():
    if not room.full:
      message = message +";"+ room.getListString()
  conn.sendall(str.encode(message))

def handle_client(conn,addr):
  while True:
    try:
      data = ""
      current = conn.recv(BUFFER_SIZE)
      if current == b'':
        # TODO do necessary actions
        # client connection is lost
        print("exit", addr)
        break
      data = data + current.decode("utf-8")
      print("data: ",data)
      message = data.split(";")
      if message[0]=="discover":
        # discover message
        conn.sendall(str.encode("server;"+HOST))
      elif message[0]=="createRoom":
        # create room message
        mainScreenUsers.remove(conn)
        r = Room(message[1],addr[0],message[2],conn)
        r.setCreatorConnection(conn)
        rooms[addr[0]] = r
        # send notification to users in main screen
        sendRoomNotification(r)
      elif message[0] == "mainscreen":
        # in mainscreen message
        mainScreenUsers.append(conn)
        sendAllRoomNotification(conn)
      elif message[0] == "ready":
        # ready message - unready if already ready
        creatorIP = message[1]
        playerType = message[2]
        if playerType == "creator":
          if rooms[creatorIP].creatorReady:
            rooms[creatorIP].creatorReady = False
          else:
            rooms[creatorIP].creatorReady = True
          if rooms[creatorIP].full:
            m = "readyNotification;"+rooms[creatorIP].creatorName
            rooms[creatorIP].participantConnection.sendall(str.encode(m))
        else:
          if rooms[creatorIP].participantReady:
            rooms[creatorIP].participantReady = False
          else:
            rooms[creatorIP].participantReady = True
          m = "readyNotification;"+rooms[creatorIP].participantName
          rooms[creatorIP].creatorConnection.sendall(str.encode(m))
        if rooms[creatorIP].participantReady and rooms[creatorIP].creatorReady:
          # start game
          print("start game: " + rooms[creatorIP].creatorName + 
            " and " + rooms[creatorIP].participantName)
          # init battle
          r = rooms[creatorIP]
          battles[creatorIP] = Battle(r.title)
          battles[creatorIP].setPlayer1(r.creatorName,r.creatorIP,r.creatorConnection)
          battles[creatorIP].setPlayer2(r.participantName,r.participantIP,r.participantConnection)
          # TODO team select
          battles[creatorIP]._players[0].setTeam([Mika()])
          battles[creatorIP]._players[1].setTeam([Mika()])
          # send init battle message
          messages = []
          for i in range(2):
            messages.append("initBattle;" + creatorIP + ";"+str(i)+";" +
              battles[creatorIP]._players[i].getCurrentMonsterInfo() + ";" +
              battles[creatorIP]._players[i].getCurrentMonsterActionList() + ";" +
              battles[creatorIP]._players[1-i].getCurrentMonsterInfo())
          # creator - player[0]
          rooms[creatorIP].creatorConnection.sendall(str.encode(messages[0]))
          # participant - player[1]
          rooms[creatorIP].participantConnection.sendall(str.encode(messages[1]))
          # delete room
          rooms.pop(creatorIP, None)
      elif message[0] == "battle":
        battleKey = message[1]
        side = message[2]
        actionId = message[3]
        battles[battleKey].setAction(side,actionId)
        if battles[battleKey].turnReady():
          log = battles[battleKey].turnUpdate()
          print("turn ready")
          print(log)
          # send update message
          for i in range(2):
            message = "turnUpdate;" + \
              battles[creatorIP]._players[i].getCurrentMonsterInfo() + ";" + \
              battles[creatorIP]._players[1-i].getCurrentMonsterInfo()+ ";" + log
            battles[creatorIP].sendToPlayer(i,message)
      elif message[0] == "listRooms":
        # list only not full rooms
        print("listRooms",addr)
        message = "listRooms"
        for roomID,room in rooms.items():
          if not room.full:
            message = message +";"+ room.getListString()
        print("room list message: ",message)
        conn.sendall(str.encode(message))
      elif message[0] == "joinRoom":
        # participant join room message
        creatorIP = message[1]
        participantName = message[2]
        rooms[creatorIP].setParticipantInfo(participantName, addr[0], conn)
        rooms[creatorIP].full = True
        # send join info to creator
        m = "joinInfo;"+rooms[creatorIP].participantName
        rooms[creatorIP].creatorConnection.sendall(str.encode(m))
        mainScreenUsers.remove(conn)
        # send clients in mainscreen to remove this room
        message = "removeRoom;"+creatorIP
        for wConn in mainScreenUsers:
          wConn.sendall(str.encode(message))
      elif message[0] == "leaveRoom":
        playerType = message[1]
        creatorIP = message[2]
        if playerType=="creator":
          rooms[creatorIP].creatorConnection.sendall(b"leaveRoom")
          if rooms[creatorIP].full:
            rooms[creatorIP].participantConnection.sendall(b"leaveRoom")
          rooms.pop(creatorIP, None)
        else:
          # send room available
          pConn = rooms[creatorIP].participantConnection
          rooms[creatorIP].participantLeft()
          sendRoomNotification(rooms[creatorIP])
          pConn.sendall(b"leaveRoom")
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
      s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    print("Socket is closed!")
    s.close()
    traceback.print_exc()

main()